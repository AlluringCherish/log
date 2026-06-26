import csv
import glob
import json
import os
from dataclasses import dataclass
from statistics import mean, median
from typing import Dict, Iterable, List, Optional, Tuple


FAULT_TO_METRIC = {
    "cpu": "cpu",
    "mem": "mem",
    "delay": "latency",
    "loss": "latency",
    "disk": "diskio",
    "socket": "socket",
}


@dataclass(frozen=True)
class Case:
    case_id: str
    case_dir: str
    metric_path: str
    inject_time: int
    service: str
    fault: str
    logs_path: Optional[str]
    traces_path: Optional[str]
    tracets_err_path: Optional[str]
    tracets_lat_path: Optional[str]
    source_case_id: Optional[str] = None
    source_group: Optional[str] = None

    @property
    def name(self) -> str:
        return self.case_id

    @property
    def answer_metric(self) -> str:
        return FAULT_TO_METRIC.get(self.fault, self.fault)

    @property
    def answer_rank(self) -> str:
        return f"{self.service}_{self.answer_metric}"

    def agent_context(self, time_context: str = "inject") -> Dict[str, object]:
        files = {
            "metrics": self.metric_path,
            "logs": self.logs_path,
            "traces": self.traces_path,
        }
        context: Dict[str, object] = {
            "case_name": self.name,
            "case_dir": self.case_dir,
            "time_context": time_context,
            "available_files": {k: v for k, v in files.items() if v},
            "possible_root_cause_components": [
                "checkoutservice",
                "currencyservice",
                "emailservice",
                "productcatalogservice",
                "recommendationservice",
            ],
            "possible_root_cause_reasons": ["cpu", "mem", "diskio", "latency", "socket"],
            "possible_root_cause_services": [
                "checkoutservice",
                "currencyservice",
                "emailservice",
                "productcatalogservice",
                "recommendationservice",
            ],
            "possible_root_cause_metrics": ["cpu", "mem", "diskio", "latency", "socket"],
            "service_dependency_graph": _load_service_dependency_graph(self.case_dir),
            "prediction_format": (
                "Return ranked root causes as objects with `time` as Unix seconds, "
                "`component` as a candidate root cause service, and `reason` as a candidate root cause metric."
            ),
            "dataset": "Online Boutique",
        }
        if time_context == "inject":
            context["inject_time"] = self.inject_time
        elif time_context == "api":
            context["telemetry_time_range"] = self.telemetry_time_range()
            context["available_read_apis"] = ["read_logs", "read_metrics", "read_traces"]
        elif time_context == "evidence":
            context["telemetry_time_range"] = self.telemetry_time_range()
            context["available_read_apis"] = ["get_evidence"]
            context["evidence_time_unit"] = "relative_seconds_from_case_start"
        elif time_context == "range":
            context["telemetry_time_range"] = self.telemetry_time_range()
        else:
            raise ValueError(f"Unsupported time_context: {time_context}")
        return context

    def telemetry_time_range(self) -> Dict[str, object]:
        sources: Dict[str, Dict[str, object]] = {}
        metric_range = _numeric_column_range(self.metric_path, "time", divisor=1)
        if metric_range is not None:
            sources["metrics"] = {
                "column": "time",
                "unit": "unix_seconds",
                **metric_range,
            }
        if self.logs_path:
            log_range = _numeric_column_range(self.logs_path, "timestamp", divisor=1_000_000_000)
            if log_range is not None:
                sources["logs"] = {
                    "column": "timestamp",
                    "original_unit": "unix_nanoseconds",
                    "normalized_unit": "unix_seconds",
                    **log_range,
                }
        if self.traces_path:
            trace_range = _numeric_column_range(self.traces_path, "startTimeMillis", divisor=1000)
            if trace_range is not None:
                sources["traces"] = {
                    "column": "startTimeMillis",
                    "original_unit": "unix_milliseconds",
                    "normalized_unit": "unix_seconds",
                    **trace_range,
                }

        starts = [float(item["start_time"]) for item in sources.values()]
        ends = [float(item["end_time"]) for item in sources.values()]
        if not starts or not ends:
            return {
                "unit": "unix_seconds",
                "start_time": None,
                "end_time": None,
                "sources": sources,
            }
        return {
            "unit": "unix_seconds",
            "start_time": int(min(starts)),
            "end_time": int(max(ends)),
            "sources": sources,
        }


def _optional_file(case_dir: str, *names: str) -> Optional[str]:
    for name in names:
        path = os.path.join(case_dir, name)
        if os.path.exists(path):
            return path
    return None


def _numeric_column_range(path: Optional[str], column: str, divisor: float) -> Optional[Dict[str, object]]:
    if not path or not os.path.exists(path):
        return None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    count = 0
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or column not in reader.fieldnames:
                return None
            for row in reader:
                raw = row.get(column)
                if raw is None or raw == "":
                    continue
                try:
                    value = float(raw) / divisor
                except ValueError:
                    continue
                if minimum is None or value < minimum:
                    minimum = value
                if maximum is None or value > maximum:
                    maximum = value
                count += 1
    except OSError:
        return None
    if minimum is None or maximum is None:
        return None
    return {
        "start_time": int(minimum),
        "end_time": int(maximum),
        "row_count": count,
    }


def _parse_service_fault(metric_path: str) -> Tuple[str, str, str]:
    case_dir = os.path.dirname(metric_path)
    case_id = os.path.basename(case_dir)
    parent_name = os.path.basename(os.path.dirname(case_dir))
    parts = parent_name.split("_")
    if len(parts) < 2:
        raise ValueError(f"Cannot parse service/fault from path: {metric_path}")
    return parts[0], parts[1], case_id


def _load_problem_map(data_root: str) -> Dict[str, Dict[str, object]]:
    problem_path = os.path.join(data_root, "problem.json")
    if not os.path.exists(problem_path):
        return {}
    with open(problem_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    cases = payload.get("cases", payload)
    if isinstance(cases, dict):
        iterable = cases.values()
    else:
        iterable = cases
    problems: Dict[str, Dict[str, object]] = {}
    for item in iterable:
        if not isinstance(item, dict):
            continue
        case_id = item.get("case_id")
        if isinstance(case_id, str) and case_id:
            problems[case_id] = item
    return problems


def _load_service_dependency_graph(case_dir: str) -> Dict[str, object]:
    graph_path = ""
    search_dir = os.path.abspath(case_dir)
    for _ in range(4):
        candidate = os.path.join(search_dir, "service_dependency_graph.json")
        if os.path.exists(candidate):
            graph_path = candidate
            break
        parent = os.path.dirname(search_dir)
        if parent == search_dir:
            break
        search_dir = parent
    if not os.path.exists(graph_path):
        return {"nodes": [], "edges": [], "available": False}
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)
    return {
        "nodes": graph.get("nodes", []),
        "edges": graph.get("edges", []),
        "available": True,
    }


def discover_cases(data_root: str, case_limit: Optional[int] = None) -> List[Case]:
    if not os.path.isdir(data_root):
        raise FileNotFoundError(f"Data root does not exist: {data_root}")

    problems = _load_problem_map(data_root)
    candidates = glob.glob(os.path.join(data_root, "**", "data.csv"), recursive=True)
    candidates += glob.glob(os.path.join(data_root, "**", "simple_metrics.csv"), recursive=True)

    by_dir: Dict[str, str] = {}
    for path in sorted(candidates):
        case_dir = os.path.dirname(path)
        current = by_dir.get(case_dir)
        if current is None or os.path.basename(path) == "data.csv":
            by_dir[case_dir] = path

    cases: List[Case] = []
    for metric_path in sorted(by_dir.values()):
        case_dir = os.path.dirname(metric_path)
        inject_path = os.path.join(case_dir, "inject_time.txt")
        if not os.path.exists(inject_path):
            continue
        public_case_id = os.path.basename(case_dir)
        problem = problems.get(public_case_id)
        if problem:
            case_id = public_case_id
            service = str(problem["service"])
            fault = str(problem["fault"])
            source_case_id = str(problem.get("source_case_id", ""))
            source_group = str(problem.get("source_group", ""))
        else:
            service, fault, raw_case_id = _parse_service_fault(metric_path)
            case_id = f"{service}_{fault}_{raw_case_id}"
            source_case_id = raw_case_id
            source_group = os.path.basename(os.path.dirname(case_dir))
        with open(inject_path, "r", encoding="utf-8") as f:
            inject_time = int(f.read().strip())
        cases.append(
            Case(
                case_id=case_id,
                case_dir=case_dir,
                metric_path=metric_path,
                inject_time=inject_time,
                service=service,
                fault=fault,
                logs_path=_optional_file(case_dir, "logs.csv", "log.csv"),
                traces_path=_optional_file(case_dir, "traces.csv", "trace.csv"),
                tracets_err_path=_optional_file(case_dir, "tracets_err.csv"),
                tracets_lat_path=_optional_file(case_dir, "tracets_lat.csv"),
                source_case_id=source_case_id or None,
                source_group=source_group or None,
            )
        )

    if case_limit is not None:
        cases = cases[:case_limit]
    if not cases:
        raise FileNotFoundError(f"No cases found under {data_root}")
    return cases


def normalize_rank_item(item: object) -> Optional[str]:
    if isinstance(item, dict):
        service = item.get("service") or item.get("entity") or item.get("component")
        metric = item.get("metric") or item.get("fault") or item.get("reason")
        if service and metric:
            item = f"{service}_{metric}"
        else:
            return None
    if not isinstance(item, str):
        return None
    item = item.strip().replace(" ", "_")
    if not item or item.lower() in {"unknown", "none", "null"}:
        return None
    item = item.replace("_latency-90", "_latency").replace("_lat_90", "_latency")
    return item


def normalize_ranking(ranking: Iterable[object], limit: int = 5) -> List[str]:
    seen = set()
    result = []
    for raw in ranking or []:
        item = normalize_rank_item(raw)
        if item and item not in seen:
            seen.add(item)
            result.append(item)
        if len(result) >= limit:
            break
    return result


def split_rank(rank: str) -> Tuple[str, str]:
    if "_" not in rank:
        return rank, "unknown"
    service, metric = rank.split("_", 1)
    if metric in {"delay", "loss"}:
        metric = "latency"
    if metric == "disk":
        metric = "diskio"
    return service.replace("-db", ""), metric


def evaluate_cases(records: List[Dict[str, object]]) -> Dict[str, object]:
    rows = []
    summary: Dict[str, Dict[str, float]] = {}

    for record in records:
        case: Case = record["case"]  # type: ignore[assignment]
        prediction = normalize_ranking(record.get("prediction", []))
        components = []
        reasons = []
        fine = []
        for rank in prediction:
            component, reason = split_rank(rank)
            if component not in components:
                components.append(component)
            if reason not in reasons:
                reasons.append(reason)
            fine.append((component, reason))

        answer_component = case.service.replace("-db", "")
        answer_reason = case.answer_metric
        answer_fine = (answer_component, answer_reason)
        timing_s = record.get("timing_s", {})
        elapsed_s = timing_s.get("all") if isinstance(timing_s, dict) else None
        row = {
            "case": case.name,
            "answer": case.answer_rank,
            "prediction": prediction,
            "steps": len(record.get("steps", [])),
            "time_s": elapsed_s,
        }
        for k in range(1, 6):
            row[f"top_{k}_component"] = answer_component in components[:k]
            row[f"top_{k}_reason"] = answer_reason in reasons[:k]
            row[f"top_{k}_both"] = answer_fine in fine[:k]
            row[f"top_{k}_service"] = row[f"top_{k}_component"]
            row[f"top_{k}_metric"] = row[f"top_{k}_reason"]
        rows.append(row)

    group_names = ["overall"] + sorted({r["answer"].split("_", 1)[1] for r in rows})
    for group_name in group_names:
        group_rows = rows if group_name == "overall" else [r for r in rows if r["answer"].endswith(f"_{group_name}")]
        if not group_rows:
            continue
        summary[group_name] = {}
        for k in range(1, 6):
            summary[group_name][f"top_{k}_component"] = sum(bool(r[f"top_{k}_component"]) for r in group_rows) / len(group_rows)
            summary[group_name][f"top_{k}_reason"] = sum(bool(r[f"top_{k}_reason"]) for r in group_rows) / len(group_rows)
            summary[group_name][f"top_{k}_both"] = sum(bool(r[f"top_{k}_both"]) for r in group_rows) / len(group_rows)
            summary[group_name][f"top_{k}_service"] = summary[group_name][f"top_{k}_component"]
            summary[group_name][f"top_{k}_metric"] = summary[group_name][f"top_{k}_reason"]
        time_values = [float(r["time_s"]) for r in group_rows if r.get("time_s") is not None]
        if time_values:
            summary[group_name]["time_s_total"] = sum(time_values)
            summary[group_name]["time_s_mean"] = mean(time_values)
            summary[group_name]["time_s_median"] = median(time_values)

    return {"summary": summary, "rows": rows}


def write_outputs(output_dir: str, records: List[Dict[str, object]]) -> None:
    os.makedirs(output_dir, exist_ok=True)
    serializable = []
    for record in records:
        case: Case = record["case"]  # type: ignore[assignment]
        serializable.append(
            {
                "case": case.name,
                "answer": case.answer_rank,
                "prediction": normalize_ranking(record.get("prediction", [])),
                "final_ranking": record.get("final_ranking", []),
                "error": record.get("error"),
                "steps": record.get("steps", []),
                "timing_s": record.get("timing_s"),
                "time_context": record.get("time_context"),
            }
        )
    with open(os.path.join(output_dir, "predictions.json"), "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

    evaluation = evaluate_cases(records)
    with open(os.path.join(output_dir, "evaluation.json"), "w", encoding="utf-8") as f:
        json.dump(evaluation, f, ensure_ascii=False, indent=2)

    csv_path = os.path.join(output_dir, "predictions.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["case", "answer", "prediction", "error"])
        writer.writeheader()
        for row in serializable:
            writer.writerow(
                {
                    "case": row["case"],
                    "answer": row["answer"],
                    "prediction": json.dumps(row["prediction"]),
                    "error": row["error"],
                }
            )
