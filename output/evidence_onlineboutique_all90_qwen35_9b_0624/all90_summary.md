# OnlineBoutique Evidence All-90 Qwen3.5-9B Summary

## Overall Accuracy

| metric | top1 | top2 | top3 |
|---|---:|---:|---:|
| component | 83/90 (0.922) | 90/90 (1.000) | 90/90 (1.000) |
| reason | 54/90 (0.600) | 64/90 (0.711) | 64/90 (0.711) |
| both | 49/90 (0.544) | 61/90 (0.678) | 61/90 (0.678) |

## Workflow

- total_cases: 90
- workflow_ok_count: 72
- full_metrics_scan_count: 84
- broad_metrics_only_count: 90
- focus_metrics_first_count: 88
- focus_has_trace_log_count: 75
- alternative_compare_count: 19
- multiple_focus_backtrack_like_count: 21
- retry_case_count: 1
- failed_call_case_count: 0

Backtracking policy is enabled in the Controller prompt. Operationally, `alternative_compare_count` counts focused calls with multiple components, and `multiple_focus_backtrack_like_count` counts cases that performed more than one focused investigation after the metrics scan.

## By Reason Top1/Top3 Both

| reason | count | top1_both | top3_both |
|---|---:|---:|---:|
| cpu | 15 | 4/15 (0.267) | 5/15 (0.333) |
| diskio | 15 | 15/15 (1.000) | 15/15 (1.000) |
| latency | 30 | 20/30 (0.667) | 26/30 (0.867) |
| mem | 15 | 9/15 (0.600) | 11/15 (0.733) |
| socket | 15 | 1/15 (0.067) | 4/15 (0.267) |

## Cases With Workflow Warnings

| case | reason | full_scan | focus_trace_log | failed_calls | error |
|---|---|---:|---:|---:|---|
| case_000001 | checkoutservice_cpu | False | True | 0 | None |
| case_000002 | checkoutservice_cpu | False | True | 0 | None |
| case_000005 | checkoutservice_latency | True | False | 0 | None |
| case_000014 | checkoutservice_mem | False | False | 0 | None |
| case_000022 | currencyservice_latency | True | False | 0 | None |
| case_000023 | currencyservice_latency | True | False | 0 | None |
| case_000024 | currencyservice_latency | True | False | 0 | None |
| case_000055 | productcatalogservice_cpu | True | False | 0 | None |
| case_000057 | productcatalogservice_cpu | True | False | 0 | None |
| case_000061 | productcatalogservice_diskio | True | False | 0 | None |
| case_000062 | productcatalogservice_diskio | True | False | 0 | None |
| case_000063 | productcatalogservice_diskio | True | False | 0 | None |
| case_000067 | productcatalogservice_mem | False | False | 0 | None |
| case_000068 | productcatalogservice_mem | True | False | 0 | None |
| case_000070 | productcatalogservice_socket | True | False | 0 | None |
| case_000071 | productcatalogservice_socket | False | False | 0 | None |
| case_000072 | productcatalogservice_socket | True | False | 0 | None |
| case_000080 | recommendationservice_diskio | False | True | 0 | None |

## Files

- predictions.json
- evaluation.json
- all90_analysis_summary.json
- all90_case_results.csv
- all90_workflow_checks.csv
- all90_step_workflow_checks.csv
- all90_step_workflow_summary.md
