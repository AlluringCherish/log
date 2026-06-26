import json
import math
import os
import re
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from Benchmarks.re2_ob import Case


ToolObservation = Dict[str, Any]


DEFAULT_TIMESTAMP_REGEX = (
    r"(?:"
    r"\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)"
    r"|"
    r"\d{4}-[A-Z][a-z]{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?"
    r"|"
    r"\b\d{2}:\d{2}:\d{2}\b"
    r"|"
    r"\b\d+m(?:\d+s)?\b"
    r"|"
    r"\b\d+s\b"
    r"|"
    r"[A-Z][a-z]{2} [A-Z][a-z]{2} \d{2} \d{2}:\d{2}:\d{2} \d{4}"
    r")"
)
DEFAULT_TS_RX = re.compile(DEFAULT_TIMESTAMP_REGEX)


def _timestamp_spans(line: str) -> List[Tuple[int, int]]:
    return [match.span() for match in DEFAULT_TS_RX.finditer(line)]


def _make_blocks(lines: List[str], block_size: int) -> List[str]:
    return ["\n".join(lines[index:index + block_size]) for index in range(0, len(lines), block_size)]


def _mask_timestamps(text: str, spans: List[Tuple[int, int]]) -> str:
    parts: List[str] = []
    last_end = 0
    for start, end in spans:
        parts.append(text[last_end:start])
        parts.append(" " * (end - start))
        last_end = end
    parts.append(text[last_end:])
    return "".join(parts)


def _greedy_compress_pass(lines: List[str], block_size: int) -> List[str]:
    if not lines:
        return []

    blocks = _make_blocks(lines, block_size)
    result = [blocks[0]]
    previous_spans = _timestamp_spans(blocks[0])

    for block in blocks[1:]:
        spans = _timestamp_spans(block)
        if (
            not previous_spans
            or not spans
            or len(spans) != len(previous_spans)
            or [span[0] for span in spans] != [span[0] for span in previous_spans]
        ):
            result.append(block)
            previous_spans = spans
            continue

        if _mask_timestamps(result[-1], previous_spans) == _mask_timestamps(block, spans):
            result[-1] = block
        else:
            result.append(block)
        previous_spans = spans

    return result


def _greedy_compress_lines_like_aiopslab(raw_text: str) -> str:
    try:
        log_trim = int(os.environ.get("LOG_TRIM", "0"))
    except ValueError:
        log_trim = 0
    if log_trim <= 0:
        return raw_text

    result = raw_text.splitlines()
    for block_size in range(1, log_trim + 1):
        result = _greedy_compress_pass(result, block_size)
    return "\n".join(result)


def _format_table(df: pd.DataFrame) -> str:
    with pd.option_context("display.max_columns", None, "display.width", 240, "display.max_colwidth", 160):
        return df.to_string(index=False)


def _format_lines(lines: List[str]) -> str:
    return "\n".join(lines)


def _json_dumps(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


class OfflineAIOpsLabAPIRuntime:
    """Offline AIOpsLab-style telemetry API runtime for one benchmark case."""

    TOOL_NAMES = {"read_logs", "read_metrics", "read_traces"}
    CANDIDATE_COMPONENTS = {
        "checkoutservice",
        "currencyservice",
        "emailservice",
        "productcatalogservice",
        "recommendationservice",
    }
    SUPPORTING_COMPONENTS = {
        "frontend",
        "adservice",
        "cartservice",
        "redis",
        "paymentservice",
        "shippingservice",
    }
    SERVICE_ALIASES = {
        "frontendservice": "frontend",
        "frontend-external": "frontend",
        "redis-cart": "redis",
    }

    def __init__(self, case: Case) -> None:
        self.case = case
        self._metrics_df: Optional[pd.DataFrame] = None
        self._logs_df: Optional[pd.DataFrame] = None
        self._traces_df: Optional[pd.DataFrame] = None

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
                    raise ValueError(f"Unknown API `{name}`. Available APIs: {', '.join(sorted(self.TOOL_NAMES))}.")
                result["observation"] = self._dispatch(name, args)
                result["status"] = True
            except Exception as exc:
                result["observation"] = f"API call {index} failed: {exc}"
            observations.append(result)
        return observations

    def read_metrics(
        self,
        component: Any = None,
        start_time: Any = None,
        end_time: Any = None,
    ) -> str:
        df = self._load_metrics_df()
        if df is None:
            return "error: Metrics file is unavailable."
        if "time" not in df.columns:
            return "Failed to read metrics: metrics file has no `time` column."

        times = pd.to_numeric(df["time"], errors="coerce")
        telemetry_start = float(times.min())
        telemetry_end = float(times.max())
        start, end = self._resolve_time_window(start_time, end_time, telemetry_start, telemetry_end)
        selected_component = self._normalize_service(component) if component else None
        if not selected_component:
            raise ValueError("`component` is required for read_metrics.")

        work = df[(times >= start) & (times <= end)].copy()
        metric_columns = [
            column
            for column in self._metric_columns_for_component(df, selected_component)
            if column != "time"
        ]
        items: List[Dict[str, Any]] = []
        for column in metric_columns:
            values = pd.to_numeric(work[column], errors="coerce").dropna()
            stats = self._numeric_summary(values)
            items.append(
                {
                    "metric": column,
                    "count": stats["count"],
                    "mean": stats["mean"],
                    "std": stats["std"],
                    "min": stats["min"],
                    "max": stats["max"],
                    "p95": stats["p95"],
                    "p99": stats["p99"],
                }
            )

        return _json_dumps(
            {
                "telemetry": "metrics",
                "component": selected_component,
                "window": self._window_payload(start, end),
                "matched_rows": int(work.shape[0]),
                "items": items,
            }
        )

    def read_logs(
        self,
        component: Any = None,
        start_time: Any = None,
        end_time: Any = None,
    ) -> str:
        df = self._load_logs_df()
        if df is None:
            return "error: Logs file is unavailable."
        if "timestamp" not in df.columns or "container_name" not in df.columns:
            return "Failed to read logs: logs file lacks `timestamp` or `container_name`."

        seconds = pd.to_numeric(df["timestamp"], errors="coerce") / 1_000_000_000
        telemetry_start = float(seconds.min())
        telemetry_end = float(seconds.max())
        start, end = self._resolve_time_window(start_time, end_time, telemetry_start, telemetry_end)
        selected_component = self._normalize_service(component) if component else None
        if not selected_component:
            raise ValueError("`component` is required for read_logs.")

        work = df[(seconds >= start) & (seconds <= end)].copy()
        if work.empty:
            return ""

        work["_component"] = work["container_name"].map(self._normalize_service)
        work = work[work["_component"] == selected_component].copy()
        if work.empty:
            return _json_dumps(
                {
                    "telemetry": "logs",
                    "component": selected_component,
                    "window": self._window_payload(start, end),
                    "total_count": 0,
                    "count_by_level": {},
                    "top_templates": [],
                }
            )

        level_values = work["level"] if "level" in work.columns else pd.Series(["unknown"] * len(work), index=work.index)
        work["_level"] = level_values.fillna("unknown").astype(str).replace("", "unknown")
        template_column = "log_template" if "log_template" in work.columns else "message"
        if template_column in work.columns:
            work["_template"] = work[template_column].fillna("").astype(str).replace("", "<empty>")
        else:
            work["_template"] = "<missing>"

        count_by_level = {
            str(level): int(count)
            for level, count in work["_level"].value_counts().sort_values(ascending=False).items()
        }
        grouped = (
            work.groupby(["_template", "_level"], dropna=False)
            .size()
            .reset_index(name="count")
            .sort_values(["count", "_template", "_level"], ascending=[False, True, True])
            .head(10)
        )
        top_templates = [
            {
                "template": str(row["_template"]),
                "level": str(row["_level"]),
                "count": int(row["count"]),
            }
            for _, row in grouped.iterrows()
        ]

        return _json_dumps(
            {
                "telemetry": "logs",
                "component": selected_component,
                "window": self._window_payload(start, end),
                "total_count": int(work.shape[0]),
                "count_by_level": count_by_level,
                "top_templates": top_templates,
            }
        )

    def read_traces(
        self,
        component: Any = None,
        start_time: Any = None,
        end_time: Any = None,
    ) -> str:
        df = self._load_traces_df()
        if df is None:
            return "error: Traces file is unavailable."
        required = {"traceID", "spanID", "parentSpanID", "serviceName", "startTimeMillis"}
        if not required.issubset(df.columns):
            missing = sorted(required - set(df.columns))
            return f"Failed to read traces: traces file lacks required columns {missing}."

        seconds = pd.to_numeric(df["startTimeMillis"], errors="coerce") / 1000
        telemetry_start = float(seconds.min())
        telemetry_end = float(seconds.max())
        start, end = self._resolve_time_window(start_time, end_time, telemetry_start, telemetry_end)
        selected_component = self._normalize_service(component) if component else None
        if not selected_component:
            raise ValueError("`component` is required for read_traces.")

        spans = df[(seconds >= start) & (seconds <= end)].copy()
        if spans.empty:
            return _json_dumps(
                {
                    "telemetry": "traces",
                    "component": selected_component,
                    "expansion": "downstream_recursive",
                    "window": self._window_payload(start, end),
                    "matched_spans": 0,
                    "downstream_components": [],
                    "edge_count": 0,
                    "summary_row_count": 0,
                    "returned_row_count": 0,
                    "error_predicate": "statusCode != 0",
                    "operation_summaries": [],
                }
            )

        spans["_service"] = spans["serviceName"].map(self._normalize_service)
        trace_ids = spans["traceID"].fillna("").astype(str)
        span_ids = spans["spanID"].fillna("").astype(str)
        parent_ids = spans["parentSpanID"].fillna("").astype(str)
        span_keys = trace_ids + "|" + span_ids
        parent_keys = trace_ids + "|" + parent_ids
        empty = spans.drop(columns=["_service"]).iloc[0:0]

        parent_service_by_key = dict(zip(span_keys, spans["_service"]))
        parent_services = parent_keys.map(parent_service_by_key).fillna("")
        spans["_parent_service"] = parent_services
        edge_spans = spans[
            (spans["_parent_service"] != "")
            & (spans["_service"] != "")
            & (spans["_parent_service"] != spans["_service"])
        ].copy()

        adjacency: Dict[str, set[str]] = defaultdict(set)
        for caller, callee in edge_spans[["_parent_service", "_service"]].itertuples(index=False):
            adjacency[str(caller)].add(str(callee))

        downstream_components = self._downstream_components(selected_component, adjacency)
        selected_components = {selected_component, *downstream_components}
        work = edge_spans[
            edge_spans["_parent_service"].isin(selected_components)
            & edge_spans["_service"].isin(selected_components)
        ].copy()

        if work.empty:
            return _json_dumps(
                {
                    "telemetry": "traces",
                    "component": selected_component,
                    "expansion": "downstream_recursive",
                    "window": self._window_payload(start, end),
                    "matched_spans": 0,
                    "downstream_components": sorted(downstream_components),
                    "edge_count": 0,
                    "summary_row_count": 0,
                    "returned_row_count": 0,
                    "error_predicate": "statusCode != 0",
                    "operation_summaries": [],
                }
            )

        operation_column = "operationName" if "operationName" in work.columns else "methodName"
        if operation_column in work.columns:
            work["_operation"] = work[operation_column].fillna("").astype(str).replace("", "<unknown>")
        else:
            work["_operation"] = "<unknown>"

        summaries: List[Dict[str, Any]] = []
        for (caller, callee, operation), group in work.groupby(["_parent_service", "_service", "_operation"], dropna=False):
            durations = (
                pd.to_numeric(group["duration"], errors="coerce").dropna()
                if "duration" in group.columns
                else pd.Series(dtype="float64")
            )
            status_codes = (
                pd.to_numeric(group["statusCode"], errors="coerce")
                if "statusCode" in group.columns
                else pd.Series([0] * len(group), index=group.index)
            )
            error_count = int((status_codes.fillna(0) != 0).sum())
            item = {
                "caller_component": str(caller),
                "callee_component": str(callee),
                "operation": str(operation),
                "count": int(group.shape[0]),
                "error_count": error_count,
            }
            duration_stats = self._duration_summary(durations)
            item.update(
                {
                    "mean": duration_stats["duration_mean"],
                    "max": duration_stats["duration_max"],
                    "p95": duration_stats["p95"],
                    "p99": duration_stats["p99"],
                }
            )
            summaries.append(item)

        summaries.sort(key=lambda item: (item["error_count"], item.get("p95") or 0, item["count"]), reverse=True)
        return _json_dumps(
            {
                "telemetry": "traces",
                "component": selected_component,
                "expansion": "downstream_recursive",
                "window": self._window_payload(start, end),
                "matched_spans": int(work.shape[0]),
                "downstream_components": sorted(downstream_components),
                "edge_count": int(work[["_parent_service", "_service"]].drop_duplicates().shape[0]),
                "summary_row_count": int(len(summaries)),
                "returned_row_count": int(min(len(summaries), 10)),
                "error_predicate": "statusCode != 0",
                "operation_summaries": summaries[:10],
            }
        )

    def _dispatch(self, name: str, args: Dict[str, Any]) -> str:
        if name == "read_metrics":
            self._require_exact_args(name, args, {"start_time", "end_time", "component"})
            return self.read_metrics(
                component=args.get("component"),
                start_time=args.get("start_time"),
                end_time=args.get("end_time"),
            )
        if name == "read_logs":
            self._require_exact_args(name, args, {"start_time", "end_time", "component"})
            return self.read_logs(
                component=args.get("component"),
                start_time=args.get("start_time"),
                end_time=args.get("end_time"),
            )
        if name == "read_traces":
            self._require_exact_args(name, args, {"start_time", "end_time", "component"})
            return self.read_traces(
                component=args.get("component"),
                start_time=args.get("start_time"),
                end_time=args.get("end_time"),
            )
        raise ValueError(f"Unknown API `{name}`.")

    def _load_metrics_df(self) -> Optional[pd.DataFrame]:
        if self._metrics_df is not None:
            return self._metrics_df
        path = self.case.metric_path
        if not path or not os.path.exists(path):
            return None
        self._metrics_df = pd.read_csv(path, low_memory=False)
        return self._metrics_df

    def _load_logs_df(self) -> Optional[pd.DataFrame]:
        if self._logs_df is not None:
            return self._logs_df
        path = self.case.logs_path
        if not path or not os.path.exists(path):
            return None
        self._logs_df = pd.read_csv(path, low_memory=False)
        return self._logs_df

    def _load_traces_df(self) -> Optional[pd.DataFrame]:
        if self._traces_df is not None:
            return self._traces_df
        path = self.case.traces_path
        if not path or not os.path.exists(path):
            return None
        self._traces_df = pd.read_csv(path, low_memory=False)
        return self._traces_df

    def _window_payload(self, start: float, end: float) -> Dict[str, Any]:
        return {
            "start_time": self._number(start),
            "end_time": self._number(end),
        }

    def _numeric_summary(self, values: pd.Series) -> Dict[str, Any]:
        if values.empty:
            return {
                "count": 0,
                "sum": None,
                "mean": None,
                "std": None,
                "min": None,
                "max": None,
                "p50": None,
                "p90": None,
                "p95": None,
                "p99": None,
            }
        quantiles = values.quantile([0.50, 0.90, 0.95, 0.99])
        return {
            "count": int(values.shape[0]),
            "sum": self._number(values.sum()),
            "mean": self._number(values.mean()),
            "std": self._number(values.std(ddof=0)),
            "min": self._number(values.min()),
            "max": self._number(values.max()),
            "p50": self._number(quantiles.loc[0.50]),
            "p90": self._number(quantiles.loc[0.90]),
            "p95": self._number(quantiles.loc[0.95]),
            "p99": self._number(quantiles.loc[0.99]),
        }

    def _duration_summary(self, values: pd.Series) -> Dict[str, Any]:
        stats = self._numeric_summary(values)
        return {
            "duration_sum": stats["sum"],
            "duration_mean": stats["mean"],
            "duration_std": stats["std"],
            "duration_min": stats["min"],
            "duration_max": stats["max"],
            "p50": stats["p50"],
            "p90": stats["p90"],
            "p95": stats["p95"],
            "p99": stats["p99"],
        }

    @staticmethod
    def _number(value: Any) -> Any:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return value
        if not math.isfinite(number):
            return None
        if number.is_integer():
            return int(number)
        return round(number, 6)

    def _metric_columns_for_component(self, df: pd.DataFrame, component: str) -> List[str]:
        columns: List[str] = []
        if "time" in df.columns:
            columns.append("time")
        for column in df.columns:
            if column == "time" or "_" not in column:
                continue
            raw_component, _ = column.split("_", 1)
            if self._normalize_service(raw_component) == component:
                columns.append(column)
        return columns

    @staticmethod
    def _downstream_components(component: str, adjacency: Dict[str, set[str]]) -> set[str]:
        downstream: set[str] = set()
        seen = {component}
        queue: deque[str] = deque([component])
        while queue:
            current = queue.popleft()
            for child in adjacency.get(current, set()):
                if child in seen:
                    continue
                seen.add(child)
                downstream.add(child)
                queue.append(child)
        return downstream

    def _resolve_time_window(
        self,
        start_time: Any,
        end_time: Any,
        telemetry_start: float,
        telemetry_end: float,
    ) -> Tuple[float, float]:
        if start_time is None or end_time is None:
            raise ValueError("Both `start_time` and `end_time` are required.")
        try:
            start = float(start_time)
            end = float(end_time)
        except (TypeError, ValueError) as exc:
            raise ValueError("`start_time` and `end_time` must be numeric Unix seconds.") from exc
        if not math.isfinite(start) or not math.isfinite(end):
            raise ValueError("`start_time` and `end_time` must be finite Unix seconds.")
        if start >= end:
            raise ValueError("`start_time` must be smaller than `end_time`.")
        start = max(start, telemetry_start)
        end = min(end, telemetry_end)
        if start >= end:
            raise ValueError("Requested window does not overlap the available telemetry range.")
        return start, end

    def _normalize_service(self, value: Any) -> str:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return ""
        raw = str(value).strip()
        lowered = raw.lower()
        if lowered in self.SERVICE_ALIASES:
            return self.SERVICE_ALIASES[lowered]
        all_components = self.CANDIDATE_COMPONENTS | self.SUPPORTING_COMPONENTS
        if lowered in all_components:
            return lowered
        for component in sorted(all_components, key=len, reverse=True):
            if lowered.startswith(component):
                return component
        stripped = re.sub(r"[-_]\d+$", "", lowered)
        stripped = re.sub(r"2[-_]\d+$", "", stripped)
        if stripped in all_components:
            return stripped
        return lowered

    def _normalize_tool_call(self, raw_call: Any) -> Dict[str, Any]:
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

    @staticmethod
    def _require_exact_args(name: str, args: Dict[str, Any], required: set[str]) -> None:
        missing = sorted(key for key in required if key not in args or args.get(key) is None)
        unsupported = sorted(key for key in args if key not in required)
        if missing:
            raise ValueError(f"Missing required args for `{name}`: {missing}. Required args: {sorted(required)}.")
        if unsupported:
            raise ValueError(f"Unsupported args for `{name}`: {unsupported}. Required args: {sorted(required)}.")

    @staticmethod
    def _cell_text(row: pd.Series, column: str) -> str:
        if column not in row:
            return ""
        value = row.get(column)
        if value is None or pd.isna(value):
            return ""
        return str(value).strip()


class OfflineEvidenceRuntime:
    """Offline precomputed evidence runtime for one benchmark case."""

    TOOL_NAMES = {"get_evidence"}
    MAX_LINES = 300
    PER_WINDOW_MODALITY_LIMIT = 3
    MODALITY_ORDER = {"metrics": 0, "traces": 1, "logs": 2}
    SERVICE_ALIASES = OfflineAIOpsLabAPIRuntime.SERVICE_ALIASES
    CANDIDATE_COMPONENTS = OfflineAIOpsLabAPIRuntime.CANDIDATE_COMPONENTS
    SUPPORTING_COMPONENTS = OfflineAIOpsLabAPIRuntime.SUPPORTING_COMPONENTS

    def __init__(self, case: Case) -> None:
        self.case = case
        self._records: Optional[List[Dict[str, Any]]] = None
        self._meta: Optional[Dict[str, Any]] = None

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
            result: ToolObservation = {
                "tool_call": call,
                "status": False,
                "observation": "",
            }
            try:
                name = call.get("name", "")
                args = call.get("args", {})
                if name not in self.TOOL_NAMES:
                    raise ValueError(f"Unknown API `{name}`. Available APIs: get_evidence.")
                self._require_exact_args(name, args, {"start_time", "end_time", "components"})
                result["observation"] = self.get_evidence(
                    start_time=args.get("start_time"),
                    end_time=args.get("end_time"),
                    components=args.get("components"),
                )
                result["status"] = True
            except Exception as exc:
                result["observation"] = f"API call {index} failed: {exc}"
            observations.append(result)
        return observations

    def get_evidence(self, start_time: Any, end_time: Any, components: Any) -> str:
        records = self._load_records()
        meta = self._load_meta()
        start, end = self._resolve_time_window(start_time, end_time, meta)
        selected_components = self._normalize_components(components)

        selected = [
            record
            for record in records
            if start <= int(record.get("window_start", -1)) < end
            and self._matches_components(record, selected_components)
            and self._matches_broad_scan_policy(record, selected_components)
        ]
        matched_count = len(selected)
        selected.sort(
            key=lambda item: (
                int(item.get("window_start", 0)),
                self.MODALITY_ORDER.get(str(item.get("modality")), 99),
                -abs(float(item.get("dev", 0.0))),
                str(item.get("line", "")),
            )
        )
        selected = self._top_records_per_window_modality(selected)

        returned, truncated, next_start_time = self._cap_by_window(selected, end)
        windows = sorted({int(item.get("window_start", 0)) for item in returned})
        payload = {
            "telemetry": "evidence",
            "time_unit": meta.get("time_unit", "relative_seconds_from_case_start"),
            "query": {
                "start_time": start,
                "end_time": end,
                "components": sorted(selected_components),
            },
            "component_filter_rule": {
                "metrics": "component matches",
                "logs": "component matches",
                "traces": "caller or callee matches",
            },
            "selection_policy": (
                "components=[] returns metrics-only broad overview; "
                "component-filtered calls return metrics first, then traces, then logs"
            ),
            "ordering": "window asc, modality metrics->traces->logs, abs(dev) desc within a window/modality",
            "per_window_modality_limit": self.PER_WINDOW_MODALITY_LIMIT,
            "latency_self_p99_definition": meta.get("latency_self_p99_definition"),
            "returned_count": len(returned),
            "matched_count": matched_count,
            "truncated": truncated,
            "returned_windows": self._returned_window_payload(windows, meta),
            "next_start_time": next_start_time,
            "lines": [str(item.get("line", "")) for item in returned],
        }
        return _json_dumps(payload)

    @staticmethod
    def _matches_broad_scan_policy(record: Dict[str, Any], components: set[str]) -> bool:
        if components:
            return True
        return record.get("modality") == "metrics"

    def _top_records_per_window_modality(self, selected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        grouped: Dict[Tuple[int, str], List[Dict[str, Any]]] = defaultdict(list)
        for record in selected:
            key = (int(record.get("window_start", 0)), str(record.get("modality", "")))
            grouped[key].append(record)

        limited: List[Dict[str, Any]] = []
        for key in sorted(grouped, key=lambda item: (item[0], self.MODALITY_ORDER.get(item[1], 99))):
            limited.extend(grouped[key][: self.PER_WINDOW_MODALITY_LIMIT])
        limited.sort(
            key=lambda item: (
                int(item.get("window_start", 0)),
                self.MODALITY_ORDER.get(str(item.get("modality")), 99),
                -abs(float(item.get("dev", 0.0))),
                str(item.get("line", "")),
            )
        )
        return limited

    def _cap_by_window(
        self,
        selected: List[Dict[str, Any]],
        requested_end: int,
    ) -> Tuple[List[Dict[str, Any]], bool, Optional[int]]:
        if len(selected) <= self.MAX_LINES:
            return selected, False, None
        returned: List[Dict[str, Any]] = []
        for window_start in sorted({int(item.get("window_start", 0)) for item in selected}):
            window_records = [item for item in selected if int(item.get("window_start", 0)) == window_start]
            if not returned and len(window_records) > self.MAX_LINES:
                returned = window_records[: self.MAX_LINES]
                window_end = max(int(item.get("window_end", window_start + 1)) for item in window_records)
                return returned, True, min(window_end, requested_end)
            if len(returned) + len(window_records) > self.MAX_LINES:
                return returned, True, window_start
            returned.extend(window_records)
        return returned, len(returned) < len(selected), None

    def _returned_window_payload(self, windows: List[int], meta: Dict[str, Any]) -> List[Dict[str, int]]:
        window_size = int(meta.get("window_size_seconds") or 30)
        return [{"start_time": window, "end_time": window + window_size} for window in windows]

    def _load_records(self) -> List[Dict[str, Any]]:
        if self._records is not None:
            return self._records
        path = os.path.join(self.case.case_dir, "evidence.jsonl")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Evidence file does not exist: {path}")
        records: List[Dict[str, Any]] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        self._records = records
        return self._records

    def _load_meta(self) -> Dict[str, Any]:
        if self._meta is not None:
            return self._meta
        path = os.path.join(self.case.case_dir, "evidence_meta.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self._meta = json.load(f)
        else:
            self._meta = {"start_time": 0, "end_time": 1440, "window_size_seconds": 30}
        return self._meta

    def _resolve_time_window(self, start_time: Any, end_time: Any, meta: Dict[str, Any]) -> Tuple[int, int]:
        if start_time is None or end_time is None:
            raise ValueError("Both `start_time` and `end_time` are required.")
        try:
            start = int(start_time)
            end = int(end_time)
        except (TypeError, ValueError) as exc:
            raise ValueError("`start_time` and `end_time` must be integer relative seconds.") from exc
        if start >= end:
            raise ValueError("`start_time` must be smaller than `end_time`.")
        telemetry_start = int(meta.get("start_time", 0))
        telemetry_end = int(meta.get("end_time", 1440))
        start = max(start, telemetry_start)
        end = min(end, telemetry_end)
        if start >= end:
            raise ValueError("Requested window does not overlap the available telemetry range.")
        return start, end

    def _normalize_components(self, components: Any) -> set[str]:
        if components is None:
            raise ValueError("`components` is required. Use [] for all components.")
        if not isinstance(components, list):
            raise ValueError("`components` must be an array. Use [] for all components.")
        return {self._normalize_service(component) for component in components if self._normalize_service(component)}

    def _matches_components(self, record: Dict[str, Any], components: set[str]) -> bool:
        if not components:
            return True
        modality = record.get("modality")
        if modality in {"metrics", "logs"}:
            return self._normalize_service(record.get("component")) in components
        if modality == "traces":
            caller = self._normalize_service(record.get("caller"))
            callee = self._normalize_service(record.get("callee"))
            return caller in components or callee in components
        return False

    def _normalize_tool_call(self, raw_call: Any) -> Dict[str, Any]:
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

    @staticmethod
    def _require_exact_args(name: str, args: Dict[str, Any], required: set[str]) -> None:
        missing = sorted(key for key in required if key not in args or args.get(key) is None)
        unsupported = sorted(key for key in args if key not in required)
        if missing:
            raise ValueError(f"Missing required args for `{name}`: {missing}. Required args: {sorted(required)}.")
        if unsupported:
            raise ValueError(f"Unsupported args for `{name}`: {unsupported}. Required args: {sorted(required)}.")

    def _normalize_service(self, value: Any) -> str:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return ""
        raw = str(value).strip()
        lowered = raw.lower()
        if lowered in self.SERVICE_ALIASES:
            return self.SERVICE_ALIASES[lowered]
        all_components = self.CANDIDATE_COMPONENTS | self.SUPPORTING_COMPONENTS
        if lowered in all_components:
            return lowered
        for component in sorted(all_components, key=len, reverse=True):
            if lowered.startswith(component):
                return component
        stripped = re.sub(r"[-_]\d+$", "", lowered)
        stripped = re.sub(r"2[-_]\d+$", "", stripped)
        if stripped in all_components:
            return stripped
        return lowered
