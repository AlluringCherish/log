import math
import os
import re
from collections import defaultdict, deque
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

from Benchmarks.re2_ob import Case


ToolCall = Dict[str, Any]
ToolObservation = Dict[str, Any]


class ServiceGraphToolRuntime:
    """Deterministic KG tool runtime for one RCA case."""

    TOOL_NAMES = {
        "check_node_existence",
        "get_node_attributes",
        "get_all_instances_of_entity_type",
        "get_edge_attributes",
        "get_node_neighborhood",
        "get_all_simple_paths",
    }

    METRIC_SUFFIXES = (
        ("latency-90", "latency"),
        ("latency-50", "latency"),
        ("diskio", "diskio"),
        ("socket", "socket"),
        ("cpu", "cpu"),
        ("mem", "mem"),
    )

    SERVICE_ALIASES = {
        "frontendservice": "frontend",
        "frontend-external": "frontend",
        "redis-cart": "redis",
    }

    def __init__(self, case: Case) -> None:
        self.case = case
        self.case_context = case.agent_context()
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edge_attrs: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self.out_edges: Dict[str, List[str]] = defaultdict(list)
        self.in_edges: Dict[str, List[str]] = defaultdict(list)

        self._load_topology(self.case_context.get("service_dependency_graph", {}))
        self._attach_metric_summaries()
        self._attach_log_summaries()
        self._attach_trace_summaries()

    def execute_tool_calls(self, tool_calls: Any) -> List[ToolObservation]:
        if isinstance(tool_calls, dict):
            tool_calls = [tool_calls]
        if not isinstance(tool_calls, list):
            return [
                {
                    "tool_call": tool_calls,
                    "status": False,
                    "observation": "Error: tool_calls must be a list of tool call objects.",
                }
            ]

        observations: List[ToolObservation] = []
        for index, raw_call in enumerate(tool_calls, start=1):
            call = self._normalize_tool_call(raw_call)
            name = call.get("name", "")
            args = call.get("args", {})
            result: ToolObservation = {
                "tool_call": call,
                "status": False,
                "observation": "",
            }
            try:
                if name not in self.TOOL_NAMES:
                    raise ValueError(f"Unknown tool `{name}`. Available tools: {', '.join(sorted(self.TOOL_NAMES))}.")
                result["observation"] = self._dispatch(name, args)
                result["status"] = True
            except Exception as exc:
                result["observation"] = f"Tool call {index} failed: {exc}"
            observations.append(result)
        return observations

    def check_node_existence(self, node: str) -> str:
        resolved = self._resolve_node(node)
        exists = resolved in self.nodes
        if exists and resolved != node:
            return f"Node `{node}` resolves to `{resolved}` and exists in the knowledge graph."
        return f"Node `{node}` exists in the knowledge graph: {exists}."

    def get_node_attributes(self, node: str) -> str:
        resolved = self._resolve_node(node)
        if resolved not in self.nodes:
            return f"Node `{node}` not found in the knowledge graph."
        attributes = self.nodes[resolved]
        return f"The attributes of node `{resolved}` are:\n{self._format_attributes(attributes)}."

    def get_all_instances_of_entity_type(self, entity_type: str) -> str:
        if not entity_type:
            return "Error: `type` is required."
        wanted = entity_type.lower()
        matches = [
            node
            for node, attrs in sorted(self.nodes.items())
            if str(attrs.get("type", "")).lower() == wanted
        ]
        if not matches:
            available = sorted({str(attrs.get("type", "")) for attrs in self.nodes.values()})
            return f"No nodes of entity type `{entity_type}` are present. Available entity types: {', '.join(available)}."
        return f"The nodes of entity type `{entity_type}` are: {', '.join(matches)}."

    def get_edge_attributes(self, node1: str, node2: str) -> str:
        source = self._resolve_node(node1)
        target = self._resolve_node(node2)
        missing = [node for node in (node1, node2) if self._resolve_node(node) not in self.nodes]
        if missing:
            return f"Node(s) not found in the knowledge graph: {', '.join(missing)}."

        attrs = self.edge_attrs.get((source, target))
        reverse_attrs = self.edge_attrs.get((target, source))
        if attrs is None:
            if reverse_attrs is not None:
                return f"No edge found from `{source}` to `{target}`. Reverse edge `{target}` -> `{source}` exists."
            return f"No edge found between `{source}` and `{target}`."

        return (
            f"The attributes of edge `{source} --({attrs.get('label', 'control_flow')})--> {target}` are:\n"
            f"{self._format_attributes(attrs)}."
        )

    def get_node_neighborhood(self, node: str, r: int = 3) -> str:
        resolved = self._resolve_node(node)
        if resolved not in self.nodes:
            return f"Node `{node}` not found in the knowledge graph."

        depth_limit = max(0, int(r))
        visited = {resolved: 0}
        queue: deque[str] = deque([resolved])
        edge_set = set()

        while queue:
            current = queue.popleft()
            depth = visited[current]
            if depth >= depth_limit:
                continue
            neighbors = self.out_edges.get(current, []) + self.in_edges.get(current, [])
            for neighbor in neighbors:
                if (current, neighbor) in self.edge_attrs:
                    edge_set.add((current, neighbor))
                if (neighbor, current) in self.edge_attrs:
                    edge_set.add((neighbor, current))
                if neighbor not in visited:
                    visited[neighbor] = depth + 1
                    queue.append(neighbor)

        nodes_str = ", ".join(sorted(visited))
        edges_str = self._format_edges(sorted(edge_set))
        return f"r-hop neighborhood of `{resolved}` up to depth {depth_limit}:\nNodes: {nodes_str}.\nEdges:\n{edges_str}."

    def get_all_simple_paths(self, source: str, target: str) -> str:
        src = self._resolve_node(source)
        dst = self._resolve_node(target)
        if src not in self.nodes and dst not in self.nodes:
            return f"Both the source and target nodes ({source}, {target}) are not found in the graph."
        if src not in self.nodes:
            return f"The source node `{source}` is not found in the graph."
        if dst not in self.nodes:
            return f"The target node `{target}` is not found in the graph."

        paths: List[List[str]] = []
        self._dfs_paths(src, dst, [src], paths, cutoff=6)
        if not paths:
            return f"All simple paths from {src} to {dst}:\nNone"
        formatted = []
        for path in paths[:25]:
            pieces = [path[0]]
            for left, right in zip(path, path[1:]):
                label = self.edge_attrs.get((left, right), {}).get("label", "control_flow")
                pieces.append(f"--({label})--> {right}")
            formatted.append("- " + " ".join(pieces))
        suffix = "\n**Note**: only the first 25 paths are shown." if len(paths) > 25 else ""
        return f"All simple paths from {src} to {dst}:\n" + "\n".join(formatted) + suffix

    def _dispatch(self, name: str, args: Dict[str, Any]) -> str:
        if name == "check_node_existence":
            return self.check_node_existence(str(args.get("node", "")))
        if name == "get_node_attributes":
            return self.get_node_attributes(str(args.get("node", "")))
        if name == "get_all_instances_of_entity_type":
            entity_type = args.get("type", args.get("entity_type", ""))
            return self.get_all_instances_of_entity_type(str(entity_type))
        if name == "get_edge_attributes":
            node1 = args.get("node1", args.get("source", ""))
            node2 = args.get("node2", args.get("target", ""))
            return self.get_edge_attributes(str(node1), str(node2))
        if name == "get_node_neighborhood":
            return self.get_node_neighborhood(str(args.get("node", "")), int(args.get("r", 3)))
        if name == "get_all_simple_paths":
            return self.get_all_simple_paths(str(args.get("source", "")), str(args.get("target", "")))
        raise ValueError(f"Unknown tool `{name}`.")

    def _load_topology(self, graph: Any) -> None:
        if not isinstance(graph, dict):
            graph = {}
        for node in graph.get("nodes", []):
            if isinstance(node, str):
                self.nodes[node] = {"type": "Service"}
            elif isinstance(node, dict) and node.get("id"):
                attrs = {k: v for k, v in node.items() if k != "id"}
                attrs.setdefault("type", "Service")
                self.nodes[str(node["id"])] = attrs

        for edge in graph.get("edges", []):
            if not isinstance(edge, dict):
                continue
            source = edge.get("source", edge.get("caller"))
            target = edge.get("target", edge.get("callee"))
            if not source or not target:
                continue
            source = str(source)
            target = str(target)
            self.nodes.setdefault(source, {"type": "Service"})
            self.nodes.setdefault(target, {"type": "Service"})
            self.edge_attrs[(source, target)] = {
                "label": str(edge.get("label", "control_flow")),
            }
            self.out_edges[source].append(target)
            self.in_edges[target].append(source)

    def _attach_metric_summaries(self) -> None:
        path = self.case.metric_path
        if not path or not os.path.exists(path):
            return
        try:
            df = pd.read_csv(path)
        except Exception as exc:
            self._add_global_note(f"Metric summary failed: {exc}")
            return
        if "time" not in df.columns:
            self._add_global_note("Metric summary skipped: no `time` column.")
            return

        time_values = pd.to_numeric(df["time"], errors="coerce")
        pre = df[time_values < self.case.inject_time]
        post = df[time_values >= self.case.inject_time]
        if pre.empty or post.empty:
            self._add_global_note("Metric summary skipped: pre/post inject windows are empty.")
            return

        per_service: Dict[str, List[Tuple[float, str]]] = defaultdict(list)
        for column in df.columns:
            parsed = self._parse_metric_column(column)
            if parsed is None:
                continue
            service, metric = parsed
            service = self._normalize_service(service)
            if service not in self.nodes:
                continue
            pre_values = pd.to_numeric(pre[column], errors="coerce").dropna()
            post_values = pd.to_numeric(post[column], errors="coerce").dropna()
            if pre_values.empty or post_values.empty:
                continue

            pre_mean = float(pre_values.mean())
            post_mean = float(post_values.mean())
            delta = post_mean - pre_mean
            pooled_std = math.sqrt(float(pre_values.std(ddof=0)) ** 2 + float(post_values.std(ddof=0)) ** 2) / math.sqrt(2)
            z_score = delta / pooled_std if pooled_std > 0 and math.isfinite(pooled_std) else 0.0
            norm_delta = abs(delta) / (abs(pre_mean) + 1e-9)
            score = max(abs(z_score), norm_delta)
            direction = "up" if delta >= 0 else "down"
            peak_idx = post_values.abs().idxmax()
            peak_time = df.loc[peak_idx, "time"] if peak_idx in df.index else "unknown"
            peak_value = df.loc[peak_idx, column] if peak_idx in df.index else "unknown"

            summary = (
                f"{service}_{metric} ({column}) | direction={direction}, "
                f"pre_mean={self._fmt(pre_mean)}, post_mean={self._fmt(post_mean)}, "
                f"delta={self._fmt(delta)}, z_like={self._fmt(z_score)}, "
                f"peak_t={peak_time}, peak_value={self._fmt(peak_value)}"
            )
            per_service[service].append((score, summary))

        for service, summaries in per_service.items():
            top = [summary for _, summary in sorted(summaries, key=lambda item: item[0], reverse=True)[:8]]
            if top:
                self.nodes[service]["metric_alerts"] = top

    def _attach_log_summaries(self) -> None:
        path = self.case.logs_path
        if not path or not os.path.exists(path):
            return
        try:
            df = pd.read_csv(path)
        except Exception as exc:
            self._add_global_note(f"Log summary failed: {exc}")
            return
        if "container_name" not in df.columns:
            self._add_global_note("Log summary skipped: no `container_name` column.")
            return

        filtered = df
        if "timestamp" in df.columns:
            seconds = pd.to_numeric(df["timestamp"], errors="coerce") / 1_000_000_000
            post = df[seconds >= self.case.inject_time]
            if not post.empty:
                filtered = post

        template_col = "log_template" if "log_template" in filtered.columns else "message"
        if template_col not in filtered.columns:
            return
        work = filtered.copy()
        work["_service"] = work["container_name"].map(self._normalize_service)
        work = work[work["_service"].isin(self.nodes)]
        if work.empty:
            return

        if "level" not in work.columns:
            work["level"] = "unknown"
        work["_template"] = work[template_col].fillna("").astype(str).str.slice(0, 300)
        grouped = (
            work.groupby(["_service", "level", "_template"], dropna=False)
            .size()
            .reset_index(name="count")
        )
        grouped["_severity"] = grouped["level"].astype(str).str.lower().map(
            lambda level: 2 if "error" in level else 1 if "warn" in level else 0
        )
        grouped = grouped.sort_values(["_service", "_severity", "count"], ascending=[True, False, False])

        for service, group in grouped.groupby("_service"):
            alerts = []
            for _, row in group.head(8).iterrows():
                alerts.append(
                    f"level={row['level']}, count={int(row['count'])}, template=`{row['_template']}`"
                )
            if alerts:
                self.nodes[service]["log_alerts"] = alerts

    def _attach_trace_summaries(self) -> None:
        path = self.case.traces_path
        if not path or not os.path.exists(path):
            return
        needed = ["traceID", "spanID", "parentSpanID", "serviceName", "operationName", "duration", "statusCode", "startTimeMillis"]
        try:
            df = pd.read_csv(path, usecols=lambda col: col in needed)
        except Exception as exc:
            self._add_global_note(f"Trace summary failed: {exc}")
            return
        if not {"traceID", "spanID", "parentSpanID", "serviceName"}.issubset(df.columns):
            self._add_global_note("Trace summary skipped: required span columns are missing.")
            return

        filtered = df
        if "startTimeMillis" in df.columns:
            seconds = pd.to_numeric(df["startTimeMillis"], errors="coerce") / 1000
            post = df[seconds >= self.case.inject_time]
            if not post.empty:
                filtered = post

        spans = filtered.dropna(subset=["traceID", "spanID", "serviceName"]).copy()
        spans["_service"] = spans["serviceName"].map(self._normalize_service)
        parents = spans[["traceID", "spanID", "_service"]].rename(
            columns={"spanID": "parentSpanID", "_service": "_parent_service"}
        )
        merged = spans.merge(parents, on=["traceID", "parentSpanID"], how="inner")
        if merged.empty:
            return

        merged["_duration"] = pd.to_numeric(merged.get("duration"), errors="coerce")
        merged["_status"] = pd.to_numeric(merged.get("statusCode"), errors="coerce").fillna(0)
        grouped = merged.groupby(["_parent_service", "_service"], dropna=False)

        for (source, target), group in grouped:
            if not source or not target or source == target:
                continue
            if (source, target) not in self.edge_attrs:
                continue
            durations = group["_duration"].dropna()
            if durations.empty:
                avg_duration = p90_duration = max_duration = 0.0
            else:
                avg_duration = float(durations.mean())
                p90_duration = float(durations.quantile(0.9))
                max_duration = float(durations.max())
            error_count = int((group["_status"] != 0).sum())
            operations = []
            if "operationName" in group.columns:
                operations = [
                    f"{op} ({count})"
                    for op, count in group["operationName"].fillna("unknown").astype(str).value_counts().head(3).items()
                ]
            summary = (
                f"count={len(group)}, error_count={error_count}, "
                f"avg_duration={self._fmt(avg_duration)}, p90_duration={self._fmt(p90_duration)}, "
                f"max_duration={self._fmt(max_duration)}, top_operations={'; '.join(operations) or 'unknown'}"
            )
            alerts = self.edge_attrs[(source, target)].setdefault("trace_alerts", [])
            alerts.append(summary)

    def _parse_metric_column(self, column: str) -> Optional[Tuple[str, str]]:
        if column == "time" or "_" not in column:
            return None
        service, suffix = column.split("_", 1)
        for raw_suffix, metric in self.METRIC_SUFFIXES:
            if suffix == raw_suffix:
                return service, metric
        return None

    def _normalize_service(self, value: Any) -> str:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return ""
        raw = str(value).strip()
        if raw in self.SERVICE_ALIASES:
            return self.SERVICE_ALIASES[raw]
        if raw in self.nodes:
            return raw
        lowered = raw.lower()
        if lowered in self.SERVICE_ALIASES:
            return self.SERVICE_ALIASES[lowered]
        for node in sorted(self.nodes, key=len, reverse=True):
            if lowered.startswith(node.lower()):
                return node
        stripped = re.sub(r"[-_]\d+$", "", lowered)
        stripped = re.sub(r"2[-_]\d+$", "", stripped)
        if stripped in self.nodes:
            return stripped
        return raw

    def _resolve_node(self, node: str) -> str:
        if node in self.nodes:
            return node
        normalized = self._normalize_service(node)
        if normalized in self.nodes:
            return normalized
        return node

    def _normalize_tool_call(self, raw_call: Any) -> ToolCall:
        if not isinstance(raw_call, dict):
            return {"name": "", "args": {}, "reasoning": f"Invalid tool call object: {raw_call!r}"}
        name = raw_call.get("name") or raw_call.get("tool_name") or raw_call.get("tool") or ""
        args = raw_call.get("args", raw_call.get("parameters", {}))
        if not isinstance(args, dict):
            args = {}
        args = dict(args)
        reasoning = raw_call.get("reasoning") or args.pop("reasoning", "")
        return {
            "name": str(name),
            "args": args,
            "reasoning": str(reasoning),
        }

    def _dfs_paths(self, current: str, target: str, path: List[str], paths: List[List[str]], cutoff: int) -> None:
        if current == target:
            paths.append(list(path))
            return
        if len(path) > cutoff:
            return
        for neighbor in self.out_edges.get(current, []):
            if neighbor in path:
                continue
            path.append(neighbor)
            self._dfs_paths(neighbor, target, path, paths, cutoff)
            path.pop()

    def _format_edges(self, edges: Iterable[Tuple[str, str]]) -> str:
        lines = []
        for source, target in edges:
            label = self.edge_attrs.get((source, target), {}).get("label", "control_flow")
            lines.append(f"- {source} --({label})--> {target}")
        return "\n".join(lines) if lines else "None"

    def _format_attributes(self, attrs: Dict[str, Any]) -> str:
        lines = []
        for key in sorted(attrs):
            value = attrs[key]
            if isinstance(value, list):
                lines.append(f"{key}:" if value else f"{key}: []")
                lines.extend(f"  - {item}" for item in value)
            elif isinstance(value, dict):
                lines.append(f"{key}: {value}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines) if lines else "None"

    def _add_global_note(self, note: str) -> None:
        for node in self.nodes.values():
            node.setdefault("telemetry_notes", []).append(note)
            break

    @staticmethod
    def _fmt(value: Any) -> str:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return str(value)
        if not math.isfinite(number):
            return str(value)
        if abs(number) >= 1000:
            return f"{number:.3f}"
        if abs(number) >= 1:
            return f"{number:.4f}"
        return f"{number:.6f}"


class InjectTimeServiceGraphToolRuntime(ServiceGraphToolRuntime):
    """KG tool runtime that uses the case failure reference to pre-attach telemetry summaries."""


class RangeWindowServiceGraphToolRuntime(ServiceGraphToolRuntime):
    """KG tool runtime that retrieves telemetry only for Controller-selected timestamp windows."""

    def __init__(self, case: Case) -> None:
        self.case = case
        self.case_context = case.agent_context(time_context="range")
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edge_attrs: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self.out_edges: Dict[str, List[str]] = defaultdict(list)
        self.in_edges: Dict[str, List[str]] = defaultdict(list)
        self._metrics_df: Optional[pd.DataFrame] = None
        self._logs_df: Optional[pd.DataFrame] = None
        self._traces_df: Optional[pd.DataFrame] = None

        self._load_topology(self.case_context.get("service_dependency_graph", {}))

    def get_node_attributes(self, node: str, start_time: Any = None, end_time: Any = None) -> str:
        start, end = self._parse_window(start_time, end_time)
        resolved = self._resolve_node(node)
        if resolved not in self.nodes:
            return f"Node `{node}` not found in the knowledge graph."

        payload = {
            "node": resolved,
            "requested_window": self._window_payload(start, end),
            "static_attributes": dict(self.nodes[resolved]),
            "metric_summaries": self._summarize_metrics_for_service(resolved, start, end),
            "log_summaries": self._summarize_logs_for_service(resolved, start, end),
        }
        return f"Windowed attributes of node `{resolved}`:\n{json_dumps(payload)}"

    def get_edge_attributes(self, node1: str, node2: str, start_time: Any = None, end_time: Any = None) -> str:
        start, end = self._parse_window(start_time, end_time)
        source = self._resolve_node(node1)
        target = self._resolve_node(node2)
        missing = [node for node in (node1, node2) if self._resolve_node(node) not in self.nodes]
        if missing:
            return f"Node(s) not found in the knowledge graph: {', '.join(missing)}."

        attrs = self.edge_attrs.get((source, target))
        reverse_attrs = self.edge_attrs.get((target, source))
        if attrs is None:
            if reverse_attrs is not None:
                return f"No edge found from `{source}` to `{target}`. Reverse edge `{target}` -> `{source}` exists."
            return f"No edge found between `{source}` and `{target}`."

        payload = {
            "edge": {"source": source, "target": target, "label": attrs.get("label", "control_flow")},
            "requested_window": self._window_payload(start, end),
            "trace_summaries": self._summarize_traces_for_edge(source, target, start, end),
        }
        return f"Windowed attributes of edge `{source} --({attrs.get('label', 'control_flow')})--> {target}`:\n{json_dumps(payload)}"

    def _dispatch(self, name: str, args: Dict[str, Any]) -> str:
        if name == "check_node_existence":
            return self.check_node_existence(str(args.get("node", "")))
        if name == "get_node_attributes":
            return self.get_node_attributes(
                str(args.get("node", "")),
                args.get("start_time"),
                args.get("end_time"),
            )
        if name == "get_all_instances_of_entity_type":
            entity_type = args.get("type", args.get("entity_type", ""))
            return self.get_all_instances_of_entity_type(str(entity_type))
        if name == "get_edge_attributes":
            node1 = args.get("node1", args.get("source", ""))
            node2 = args.get("node2", args.get("target", ""))
            return self.get_edge_attributes(
                str(node1),
                str(node2),
                args.get("start_time"),
                args.get("end_time"),
            )
        if name == "get_node_neighborhood":
            return self.get_node_neighborhood(str(args.get("node", "")), int(args.get("r", 3)))
        if name == "get_all_simple_paths":
            return self.get_all_simple_paths(str(args.get("source", "")), str(args.get("target", "")))
        raise ValueError(f"Unknown tool `{name}`.")

    def _parse_window(self, start_time: Any, end_time: Any) -> Tuple[float, float]:
        if start_time is None or end_time is None:
            raise ValueError("`start_time` and `end_time` are required for telemetry tools in range mode.")
        try:
            start = float(start_time)
            end = float(end_time)
        except (TypeError, ValueError) as exc:
            raise ValueError("`start_time` and `end_time` must be numeric Unix seconds.") from exc
        if not math.isfinite(start) or not math.isfinite(end):
            raise ValueError("`start_time` and `end_time` must be finite Unix seconds.")
        if start >= end:
            raise ValueError("`start_time` must be smaller than `end_time`.")
        return start, end

    def _window_payload(self, start: float, end: float) -> Dict[str, Any]:
        return {
            "start_time": int(start) if start.is_integer() else start,
            "end_time": int(end) if end.is_integer() else end,
            "unit": "unix_seconds",
        }

    def _load_metrics_df(self) -> Optional[pd.DataFrame]:
        if self._metrics_df is not None:
            return self._metrics_df
        path = self.case.metric_path
        if not path or not os.path.exists(path):
            return None
        try:
            self._metrics_df = pd.read_csv(path)
        except Exception as exc:
            self._add_global_note(f"Metric load failed: {exc}")
            return None
        return self._metrics_df

    def _load_logs_df(self) -> Optional[pd.DataFrame]:
        if self._logs_df is not None:
            return self._logs_df
        path = self.case.logs_path
        if not path or not os.path.exists(path):
            return None
        try:
            self._logs_df = pd.read_csv(path, low_memory=False)
        except Exception as exc:
            self._add_global_note(f"Log load failed: {exc}")
            return None
        return self._logs_df

    def _load_traces_df(self) -> Optional[pd.DataFrame]:
        if self._traces_df is not None:
            return self._traces_df
        path = self.case.traces_path
        if not path or not os.path.exists(path):
            return None
        needed = [
            "traceID",
            "spanID",
            "parentSpanID",
            "serviceName",
            "operationName",
            "duration",
            "statusCode",
            "startTimeMillis",
        ]
        try:
            self._traces_df = pd.read_csv(path, usecols=lambda col: col in needed)
        except Exception as exc:
            self._add_global_note(f"Trace load failed: {exc}")
            return None
        return self._traces_df

    def _summarize_metrics_for_service(self, service: str, start: float, end: float) -> Dict[str, Any]:
        df = self._load_metrics_df()
        if df is None:
            return {"available": False, "reason": "metrics file is unavailable"}
        if "time" not in df.columns:
            return {"available": False, "reason": "metrics file has no `time` column"}

        times = pd.to_numeric(df["time"], errors="coerce")
        window = df[(times >= start) & (times <= end)].copy()
        summaries: List[Tuple[float, Dict[str, Any]]] = []
        if window.empty:
            return {"available": True, "matched_rows": 0, "items": []}

        for column in df.columns:
            parsed = self._parse_metric_column(column)
            if parsed is None:
                continue
            column_service, metric = parsed
            if self._normalize_service(column_service) != service:
                continue

            values = pd.to_numeric(window[column], errors="coerce").dropna()
            if values.empty:
                continue
            first = float(values.iloc[0])
            last = float(values.iloc[-1])
            mean = float(values.mean())
            std = float(values.std(ddof=0))
            min_value = float(values.min())
            max_value = float(values.max())
            delta = last - first
            relative_delta = abs(delta) / (abs(first) + 1e-9)
            peak_distance = max(abs(max_value - mean), abs(min_value - mean))
            dispersion_score = peak_distance / (abs(mean) + 1e-9)
            score = max(relative_delta, dispersion_score, abs(std) / (abs(mean) + 1e-9))
            peak_idx = values.abs().idxmax()
            peak_time = window.loc[peak_idx, "time"] if peak_idx in window.index else "unknown"
            peak_value = window.loc[peak_idx, column] if peak_idx in window.index else "unknown"
            summaries.append(
                (
                    score,
                    {
                        "metric": f"{service}_{metric}",
                        "column": column,
                        "count": int(values.shape[0]),
                        "mean": self._number(mean),
                        "std": self._number(std),
                        "min": self._number(min_value),
                        "max": self._number(max_value),
                        "first": self._number(first),
                        "last": self._number(last),
                        "delta": self._number(delta),
                        "peak_time": self._number(peak_time),
                        "peak_value": self._number(peak_value),
                    },
                )
            )

        return {
            "available": True,
            "matched_rows": int(window.shape[0]),
            "items": [item for _, item in sorted(summaries, key=lambda entry: entry[0], reverse=True)[:8]],
        }

    def _summarize_logs_for_service(self, service: str, start: float, end: float) -> Dict[str, Any]:
        df = self._load_logs_df()
        if df is None:
            return {"available": False, "reason": "logs file is unavailable"}
        if "timestamp" not in df.columns or "container_name" not in df.columns:
            return {"available": False, "reason": "logs file lacks `timestamp` or `container_name`"}

        seconds = pd.to_numeric(df["timestamp"], errors="coerce") / 1_000_000_000
        work = df[(seconds >= start) & (seconds <= end)].copy()
        if work.empty:
            return {"available": True, "matched_rows": 0, "level_counts": {}, "top_templates": []}
        work["_service"] = work["container_name"].map(self._normalize_service)
        work = work[work["_service"] == service].copy()
        if work.empty:
            return {"available": True, "matched_rows": 0, "level_counts": {}, "top_templates": []}

        if "level" not in work.columns:
            work["level"] = "unknown"
        template_col = "log_template" if "log_template" in work.columns else "message"
        if template_col not in work.columns:
            return {"available": True, "matched_rows": int(work.shape[0]), "level_counts": {}, "top_templates": []}
        work["_template"] = work[template_col].fillna("").astype(str).str.slice(0, 300)
        level_counts = {
            str(level): int(count)
            for level, count in work["level"].fillna("unknown").astype(str).value_counts().head(10).items()
        }
        grouped = (
            work.groupby(["level", "_template"], dropna=False)
            .size()
            .reset_index(name="count")
        )
        grouped["_severity"] = grouped["level"].astype(str).str.lower().map(
            lambda level: 2 if "error" in level else 1 if "warn" in level else 0
        )
        grouped = grouped.sort_values(["_severity", "count"], ascending=[False, False])
        top_templates = [
            {
                "level": str(row["level"]),
                "count": int(row["count"]),
                "template": str(row["_template"]),
            }
            for _, row in grouped.head(8).iterrows()
        ]
        return {
            "available": True,
            "matched_rows": int(work.shape[0]),
            "level_counts": level_counts,
            "top_templates": top_templates,
        }

    def _summarize_traces_for_edge(self, source: str, target: str, start: float, end: float) -> Dict[str, Any]:
        df = self._load_traces_df()
        if df is None:
            return {"available": False, "reason": "traces file is unavailable"}
        required = {"traceID", "spanID", "parentSpanID", "serviceName", "startTimeMillis"}
        if not required.issubset(df.columns):
            return {"available": False, "reason": "traces file lacks required span columns"}

        seconds = pd.to_numeric(df["startTimeMillis"], errors="coerce") / 1000
        spans = df.dropna(subset=["traceID", "spanID", "serviceName"]).copy()
        spans["_service"] = spans["serviceName"].map(self._normalize_service)
        spans["_seconds"] = seconds.loc[spans.index]
        window_spans = spans[(spans["_seconds"] >= start) & (spans["_seconds"] <= end)].copy()
        if window_spans.empty:
            return {"available": True, "matched_spans": 0}

        parents = spans[["traceID", "spanID", "_service"]].rename(
            columns={"spanID": "parentSpanID", "_service": "_parent_service"}
        )
        merged = window_spans.merge(parents, on=["traceID", "parentSpanID"], how="inner")
        if merged.empty:
            return {"available": True, "matched_spans": 0}
        edge_spans = merged[(merged["_parent_service"] == source) & (merged["_service"] == target)].copy()
        if edge_spans.empty:
            return {"available": True, "matched_spans": 0}

        durations = pd.to_numeric(edge_spans.get("duration"), errors="coerce").dropna()
        statuses = pd.to_numeric(edge_spans.get("statusCode"), errors="coerce").fillna(0)
        status_counts = {
            str(int(status) if float(status).is_integer() else status): int(count)
            for status, count in statuses.value_counts().head(10).items()
        }
        operations: List[Dict[str, Any]] = []
        if "operationName" in edge_spans.columns:
            operations = [
                {"operation": str(op), "count": int(count)}
                for op, count in edge_spans["operationName"].fillna("unknown").astype(str).value_counts().head(8).items()
            ]
        if durations.empty:
            duration_summary = {
                "avg_duration": 0.0,
                "p90_duration": 0.0,
                "max_duration": 0.0,
            }
        else:
            duration_summary = {
                "avg_duration": self._number(float(durations.mean())),
                "p90_duration": self._number(float(durations.quantile(0.9))),
                "max_duration": self._number(float(durations.max())),
            }
        return {
            "available": True,
            "matched_spans": int(edge_spans.shape[0]),
            "error_count": int((statuses != 0).sum()),
            **duration_summary,
            "status_counts": status_counts,
            "top_operations": operations,
        }

    @staticmethod
    def _number(value: Any) -> Any:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return value
        if not math.isfinite(number):
            return str(value)
        if number.is_integer():
            return int(number)
        return round(number, 6)


def json_dumps(payload: Any) -> str:
    import json

    return json.dumps(payload, ensure_ascii=False, indent=2)
