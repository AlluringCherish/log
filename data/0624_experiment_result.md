# 0624 OnlineBoutique RCA Experiment Result

## 실험환경

- Dataset: `/data/260619/Benchmarks/OnlineBoutique`
- Cases: 90개
- Case distribution: component 5종 각 18개, reason 분포 `latency=30`, `cpu=15`, `mem=15`, `diskio=15`, `socket=15`
- Models:
  - Qwen3-8B: `/data/models/Qwen3-8B`
  - Qwen3.5-9B: `/data/models/Qwen3.5-9B`
- Hardware: NVIDIA GeForce RTX 3090, 24576 MiB
- Runtime: local Hugging Face `transformers`, `torch 2.6.0+cu124`, `pandas 2.3.3`
- Execution command pattern: `python3 Main.py --time-context api --llm-backend local --max-steps 3 --max-new-tokens 768 --temperature 0`
- Qwen3.5-9B retry: raw run had 15 final JSON schema failures; failed cases were rerun with compact final prompt. `case_000060` required `--max-new-tokens 2048`. Final merged result has 90/90 valid cases.

## Offline AIOpsLab API 구성

- Controller에 live `get_*` 함수는 제공하지 않았고, offline CSV 기반 read API만 제공했다.
- 제공 API:
  - `read_metrics`: `simple_metrics.csv`를 읽고 post-injection window와 baseline을 비교한다.
  - `read_logs`: `logs.csv`를 읽고 서비스별 log level/template 요약을 반환한다.
  - `read_traces`: `traces.csv`를 읽고 service/edge latency와 error 요약을 반환한다.
- 구현 파일:
  - `/data/260619/Tools/offline_aiopslab_tools.py`
  - `/data/260619/common/prompts.py`
  - `/data/260619/Main.py`
- Output directories:
  - Qwen3-8B: `/data/260619/output/api_onlineboutique_90_qwen3_8b_0624`
  - Qwen3.5-9B merged: `/data/260619/output/api_onlineboutique_90_qwen35_9b_0624_merged`

## 평가 기준

- Component: 정답 component가 Top@K 예측 component 집합 안에 있으면 성공.
- Reason: 정답 reason이 Top@K 예측 reason 집합 안에 있으면 성공.
- Both: 정답 `(component, reason)` pair가 Top@K ranked pair 안에 있으면 성공.
- 출력 ranking은 `component_reason` pair 기준으로 정규화했다.

## 실험 결과

| Model | K | Component | Reason | Both |
|---|---:|---:|---:|---:|
| Qwen3-8B | 1 | 85.6% | 48.9% | 40.0% |
| Qwen3-8B | 2 | 94.4% | 64.4% | 56.7% |
| Qwen3-8B | 3 | 95.6% | 70.0% | 66.7% |
| Qwen3-8B | 4 | 95.6% | 73.3% | 70.0% |
| Qwen3-8B | 5 | 95.6% | 73.3% | 70.0% |
| Qwen3.5-9B | 1 | 94.4% | 55.6% | 52.2% |
| Qwen3.5-9B | 2 | 96.7% | 67.8% | 65.6% |
| Qwen3.5-9B | 3 | 96.7% | 72.2% | 70.0% |
| Qwen3.5-9B | 4 | 96.7% | 73.3% | 72.2% |
| Qwen3.5-9B | 5 | 96.7% | 73.3% | 72.2% |

## Reason별 결과

| Model | Reason | N | Top@1 Component | Top@1 Reason | Top@1 Both | Top@5 Both |
|---|---|---:|---:|---:|---:|---:|
| Qwen3-8B | cpu | 15 | 86.7% | 26.7% | 26.7% | 60.0% |
| Qwen3-8B | mem | 15 | 86.7% | 46.7% | 46.7% | 93.3% |
| Qwen3-8B | diskio | 15 | 100.0% | 60.0% | 60.0% | 66.7% |
| Qwen3-8B | latency | 30 | 70.0% | 80.0% | 53.3% | 86.7% |
| Qwen3-8B | socket | 15 | 100.0% | 0.0% | 0.0% | 26.7% |
| Qwen3.5-9B | cpu | 15 | 100.0% | 40.0% | 40.0% | 80.0% |
| Qwen3.5-9B | mem | 15 | 93.3% | 60.0% | 60.0% | 80.0% |
| Qwen3.5-9B | diskio | 15 | 100.0% | 66.7% | 66.7% | 66.7% |
| Qwen3.5-9B | latency | 30 | 86.7% | 83.3% | 73.3% | 93.3% |
| Qwen3.5-9B | socket | 15 | 100.0% | 0.0% | 0.0% | 20.0% |

## 결과 분석

- Qwen3.5-9B가 모든 K에서 Qwen3-8B보다 높은 Both 점수를 보였다.
- Top@1 Both: Qwen3.5-9B 52.2% vs Qwen3-8B 40.0% (+12.2 pp)
- Top@2 Both: Qwen3.5-9B 65.6% vs Qwen3-8B 56.7% (+8.9 pp)
- Top@3 Both: Qwen3.5-9B 70.0% vs Qwen3-8B 66.7% (+3.3 pp)
- Top@4 Both: Qwen3.5-9B 72.2% vs Qwen3-8B 70.0% (+2.2 pp)
- Top@5 Both: Qwen3.5-9B 72.2% vs Qwen3-8B 70.0% (+2.2 pp)
- Component 식별은 두 모델 모두 높다. Top@1 Component는 Qwen3-8B 85.6%, Qwen3.5-9B 94.4%이며, Top@5에서는 각각 95.6%, 96.7%다.
- Reason 식별이 병목이다. 특히 `socket` reason은 두 모델 모두 Top@1 Both 0.0%이고 Top@5 Both도 Qwen3-8B 26.7%, Qwen3.5-9B 20.0%로 낮다.
- `latency`는 가장 잘 맞는 reason이다. Qwen3.5-9B는 latency Top@1 Both 73.3%, Top@5 Both 93.3%를 기록했다.
- `cpu`, `mem`, `diskio`에서는 Qwen3.5-9B가 Top@1 Both 기준으로 Qwen3-8B보다 각각 +13.3 pp, +13.3 pp, +6.7 pp 높다.
- 전반적으로 read API 한 번의 broad telemetry 조회만으로도 component localization은 강하지만, resource reason 분류에서는 latency symptom을 root reason으로 과대 선택하는 경향이 있다.
- Qwen3.5-9B는 정확도는 더 높지만, final 응답을 장황하게 생성해 JSON schema 실패가 발생했다. compact final prompt와 재시도로 해결했으며 최종 병합 결과의 error count는 0이다.

## 산출물 검증

- Qwen3-8B predictions: 90 records, errors 0
- Qwen3.5-9B raw predictions: 90 records, errors 15
- Qwen3.5-9B retry batch: 15 records, errors 1
- Qwen3.5-9B retry case_000060: 1 record, errors 0
- Qwen3.5-9B merged predictions: 90 records, errors 0
