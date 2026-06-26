# Qwen3.5 9B Past Reasoning Memory Run 분석

## 실행 경로

- baseline: `/data/260619/output/evidence_onlineboutique_all90_qwen35_9b_0624`
- memory run: `/data/260619/output/evidence_onlineboutique_all90_qwen35_9b_0625_memory_priority4`
- model: `/data/models/Qwen3.5-9B`
- max_new_tokens: `1024`, temperature: `0`, max_steps: `10`, time_context: `evidence`
- past reasoning memory: `past_reasoning_memory_candidate1_5_priority4_no_answers.txt`

주의: memory 예시는 같은 benchmark의 이전 성공 raw reasoning에서 가져온 in-context demonstration이다. 정답 문자열과 case id는 prompt에 넣지 않았지만, 엄밀한 held-out generalization 실험은 아니다.

## 전체 결과

| metric | baseline | memory | delta |
|---|---:|---:|---:|
| top1 component | 83/90 (92.2%) | 84/90 (93.3%) | +1 |
| top1 reason | 54/90 (60.0%) | 57/90 (63.3%) | +3 |
| top1 both | 49/90 (54.4%) | 52/90 (57.8%) | +3 |
| top2 both | 61/90 (67.8%) | 60/90 (66.7%) | -1 |
| top3 both | 61/90 (67.8%) | 65/90 (72.2%) | +4 |

핵심 변화는 top1-both가 `49/90 -> 52/90`으로 `+3` 오른 것이다. component 정확도는 `83/90 -> 84/90`, reason 정확도는 `54/90 -> 57/90`으로 같이 올랐다. top2-both는 `61/90 -> 60/90`으로 1개 낮아졌지만, top3-both는 `61/90 -> 65/90`으로 올랐다.

## Baseline 기준 split

| subset | cases | memory top1-both correct | changed top1 | 해석 |
|---|---:|---:|---:|---|
| baseline wrong | 41 | 6 | 8 | 기존 오답 41개 중 6개를 정답으로 회복했고, 2개는 다른 오답으로 이동 |
| baseline correct | 49 | 46 | 3 | 기존 정답 49개 중 46개는 유지, 3개는 회귀 |

## 변화 케이스 요약

| bucket | count | cases |
|---|---:|---|
| wrong -> correct | 6 | case_000004, case_000011, case_000034, case_000038, case_000086, case_000087 |
| correct -> wrong | 3 | case_000008, case_000065, case_000079 |
| wrong -> wrong changed | 2 | case_000030, case_000054 |

## Reason별 변화

| answer reason | n | baseline correct | memory correct | wrong->correct | correct->wrong |
|---|---:|---:|---:|---:|---:|
| cpu | 15 | 4 | 5 | 1 | 0 |
| diskio | 15 | 15 | 13 | 0 | 2 |
| latency | 30 | 20 | 21 | 2 | 1 |
| mem | 15 | 9 | 11 | 2 | 0 |
| socket | 15 | 1 | 2 | 1 | 0 |

memory는 `cpu`, `mem`, `socket`, `latency` 정답에서 각각 일부 개선을 만들었다. 반대로 `diskio`는 15/15에서 13/15로 떨어졌는데, diskio와 mem이 같이 큰 경우를 memory exhaustion으로 과잉 해석한 케이스가 있었다.

## 변화 케이스 상세

### wrong -> correct

#### case_000004

- answer: `checkoutservice_latency`
- baseline top1: `emailservice_latency` / memory top1: `checkoutservice_latency`
- baseline focused calls: `1260-1440:emailservice`
- memory focused calls: `1260-1440:emailservice | 1260-1440:checkoutservice`
- scenario: 기존은 emailservice latency.p90의 큰 편차를 그대로 root로 확정했다. memory run은 emailservice focused check에서 self latency가 정상이라 propagation이라고 해석했고, 추가로 checkoutservice를 focused check하여 self-latency spike를 확인한 뒤 checkoutservice_latency로 뒤집었다.
- baseline final: Final RCA confirms emailservice as root cause due to sustained high latency.p90 deviations (dev>+5900) in 1260-1440s window. Traces and logs validate this metric-led hypothesis without indicating upstream propagation.
- memory final: Final RCA confirms checkoutservice latency (dev=+360-+410) as primary cause. Emailservice shows secondary latency spikes (dev=+5600-+5900) as propagation. Traces validate checkoutservice self-latency spike. Ranking finalized.

#### case_000011

- answer: `checkoutservice_latency`
- baseline top1: `emailservice_mem` / memory top1: `checkoutservice_latency`
- baseline focused calls: `1260-1440:emailservice`
- memory focused calls: `1260-1440:checkoutservice`
- scenario: 기존은 emailservice mem 편차를 root로 보았지만 checkoutservice latency 검증이 약했다. memory run은 full scan 단계부터 checkoutservice latency를 1순위로 유지했고, focused trace에서 checkoutservice internal latency를 확인해 latency root로 확정했다.
- baseline final: Final RCA confirms emailservice memory pressure (dev +34.5) as primary root cause, with checkoutservice and currencyservice latency as propagated effects.
- memory final: Final RCA confirms checkoutservice latency (dev=+243.7) as primary cause. Emailservice mem (dev=+2.3) is secondary. Traces validate internal latency propagation. Ranking finalized.

#### case_000034

- answer: `currencyservice_socket`
- baseline top1: `currencyservice_mem` / memory top1: `currencyservice_socket`
- baseline focused calls: `1260-1440:currencyservice`
- memory focused calls: `1260-1440:currencyservice`
- scenario: 기존은 currencyservice의 mem/socket 동시 이상에서 mem을 우선했다. memory run은 latency가 정상이고 socket 편차가 지속되는 패턴을 socket pressure로 해석하여 currencyservice_socket을 1순위로 올렸다.
- baseline final: Final RCA confirms currencyservice memory exhaustion as primary root cause, with emailservice and checkoutservice latency as propagated effects.
- memory final: Final RCA confirms currencyservice socket pressure (dev=+5.0) and memory growth (dev=+4.8 to +10.2) as primary causes. Traces and logs validate normal propagation. Top root cause is currencyservice socket.

#### case_000038

- answer: `emailservice_cpu`
- baseline top1: `emailservice_latency` / memory top1: `emailservice_cpu`
- baseline focused calls: `1260-1440:emailservice`
- memory focused calls: `1260-1440:emailservice`
- scenario: 기존은 emailservice에서 CPU와 latency가 같이 튀자 latency를 1순위로 두었다. memory run은 component-local CPU sustained anomaly가 latency를 유발한다고 해석해 emailservice_cpu를 1순위로 바꿨다.
- baseline final: Final RCA confirms emailservice as root cause. Extreme latency and CPU spikes in metrics, supported by trace propagation from checkoutservice, indicate resource exhaustion. Ranking prioritizes latency as primary driver.
- memory final: Final RCA confirms emailservice CPU exhaustion (dev=+684 to +711) as primary cause. Sustained high CPU drives latency spikes. Traces and logs validate propagation effects. Top root cause is emailservice_cpu.

#### case_000086

- answer: `recommendationservice_mem`
- baseline top1: `recommendationservice_latency` / memory top1: `recommendationservice_mem`
- baseline focused calls: `1260-1440:recommendationservice`
- memory focused calls: `1080-1260:recommendationservice`
- scenario: 기존은 recommendationservice latency와 mem이 같이 큰 상황에서 latency를 우선했다. memory run은 mem 편차가 훨씬 지속적이고 CPU는 낮은 점을 근거로 memory exhaustion이 latency를 만든다고 해석했다.
- baseline final: recommendationservice shows extreme latency and memory anomalies; currencyservice latency is secondary; emailservice memory is minor. Final ranking prioritizes recommendationservice.
- memory final: Final RCA confirms recommendationservice memory exhaustion (dev=+1844 to +7201) as primary cause. Sustained mem spikes drive latency anomalies. Traces and logs validate propagation effects. Top root cause is recommendationservice_mem.

#### case_000087

- answer: `recommendationservice_mem`
- baseline top1: `recommendationservice_latency` / memory top1: `recommendationservice_mem`
- baseline focused calls: `1260-1440:recommendationservice | 1260-1440:recommendationservice+currencyservice+emailservice+productcatalogservice+checkoutservice`
- memory focused calls: `1080-1260:recommendationservice`
- scenario: case_000086과 유사하게 기존은 latency를 우선했지만, memory run은 mem spike가 먼저이고 더 강한 원인 신호라고 해석해 recommendationservice_mem으로 변경했다.
- baseline final: Recommendationservice shows massive latency and memory spikes in metrics, confirmed by trace propagation. It is the primary root cause.
- memory final: Final RCA confirms recommendationservice memory exhaustion (dev=+6373 to +11239) as primary cause. Sustained mem spikes drive latency propagation. Traces and logs validate the memory-driven latency hypothesis.

### correct -> wrong

#### case_000008

- answer: `checkoutservice_diskio`
- baseline top1: `checkoutservice_diskio` / memory top1: `checkoutservice_mem`
- baseline focused calls: `1260-1440:checkoutservice | 1260-1440:currencyservice+emailservice+productcatalogservice+recommendationservice`
- memory focused calls: `1260-1440:checkoutservice`
- scenario: 회귀 케이스다. 기존은 checkoutservice diskio dev가 압도적이라고 보고 정답을 맞췄다. memory run은 diskio와 mem이 동시에 큰 패턴을 memory exhaustion driving disk pressure로 해석해 checkoutservice_mem을 1순위로 올렸다.
- baseline final: Final RCA confirms checkoutservice diskio as primary root cause with extreme deviations. Emailservice mem and currencyservice latency are secondary propagation effects validated by traces.
- memory final: Final RCA confirms checkoutservice memory exhaustion (dev>+1100) as primary cause, with diskio and CPU as secondary effects. Traces and logs validate propagation.

#### case_000065

- answer: `productcatalogservice_latency`
- baseline top1: `productcatalogservice_latency` / memory top1: `recommendationservice_latency`
- baseline focused calls: `1260-1440:productcatalogservice | 1260-1440:productcatalogservice+recommendationservice+checkoutservice`
- memory focused calls: `900-1080:recommendationservice | 900-1080:recommendationservice+productcatalogservice`
- scenario: 회귀 케이스다. 기존은 productcatalogservice focused check와 비교 check에서 context deadline exceeded 로그를 보고 productcatalogservice_latency를 확정했다. memory run은 900-1080 구간의 recommendationservice latency/self trace에 먼저 고정되고 productcatalogservice root 검증이 약해졌다.
- baseline final: Productcatalogservice shows extreme latency.p90 deviations and 'context deadline exceeded' logs, confirming it as the primary root cause. Recommendationservice and checkoutservice exhibit propagation delays. Final ranking prioritizes productcatalogservice.
- memory final: Final RCA confirms recommendationservice latency (dev=+220k to +375k) as primary cause, supported by trace self_p99 spikes and productcatalogservice propagation. Ranking finalized.

#### case_000079

- answer: `recommendationservice_diskio`
- baseline top1: `recommendationservice_diskio` / memory top1: `recommendationservice_mem`
- baseline focused calls: `1260-1440:recommendationservice`
- memory focused calls: `1260-1440:recommendationservice`
- scenario: 회귀 케이스다. 기존은 recommendationservice diskio sustained spike를 root로 유지했다. memory run은 diskio와 mem 동시 이상을 memory exhaustion driving disk I/O로 해석해 recommendationservice_mem을 1순위로 바꿨다.
- baseline final: Final RCA confirms recommendationservice diskio as root cause; currencyservice latency and frontend latency are propagation effects validated by traces.
- memory final: Final RCA confirms recommendationservice memory exhaustion (dev=+4201-+5021) and disk I/O (dev=+9.1B-+10.2B) as primary cause. Trace latency spikes are propagation effects. Root cause is memory pressure driving disk I/O.

### wrong -> wrong changed

#### case_000030

- answer: `currencyservice_latency`
- baseline top1: `checkoutservice_latency` / memory top1: `recommendationservice_latency`
- baseline focused calls: `1260-1440:checkoutservice`
- memory focused calls: `1080-1260:recommendationservice`
- scenario: 오답 간 변경이다. 기존은 마지막 1260-1440 구간의 checkoutservice latency peak에 끌렸고, memory run은 1080-1260 구간 recommendationservice latency/self trace에 고정됐다. 정답 currencyservice_latency까지는 둘 다 도달하지 못했다.
- baseline final: Checkoutservice latency.p90 peaked at 18.23s (M3376) with high self_p99 traces, confirming it as the primary bottleneck. Currencyservice and recommendationservice showed elevated latency but lower deviation, supporting checkoutservice as the root cause.
- memory final: Final RCA confirms recommendationservice latency (dev=+1849 to +2115) as primary cause. Traces show self_p99 spikes (70-88ms) validating internal latency. Frontend and currencyservice show secondary latency effects.

#### case_000054

- answer: `emailservice_socket`
- baseline top1: `emailservice_mem` / memory top1: `emailservice_latency`
- baseline focused calls: `1260-1440:emailservice`
- memory focused calls: `720-900:emailservice`
- scenario: 오답 간 변경이다. 기존은 emailservice_mem으로 갔고, memory run은 720-900 구간의 emailservice latency spike에 더 일찍 수렴했다. 정답 socket을 보려면 socket metric을 latency/mem보다 우선 비교해야 했는데 둘 다 그 패턴을 놓쳤다.
- baseline final: Final RCA confirms emailservice memory exhaustion (dev >1000) as primary root cause. Traces show normal self-latency, validating memory as the bottleneck. Secondary latency spikes in checkoutservice and currencyservice are propagation effects.
- memory final: Final RCA confirms emailservice latency (dev=+3109) and mem (dev=+893) as primary causes. Traces validate internal bottleneck. Checkoutservice latency is secondary propagation.

## Reasoner vs Controller 관점

- 대부분의 변화는 controller toolset 변경보다 reasoner의 해석/랭킹 변경에서 발생했다. full scan 흐름은 거의 같고, 차이는 focused validation 후보가 바뀐 부분에서 커졌다.
- 성공 전환 6개는 memory가 `latency를 무조건 root로 보지 말고 component-local CPU/mem/socket/diskio metric을 우선한다`는 패턴을 강화한 효과가 컸다.
- 특히 `case_000004`는 reasoner가 emailservice latency를 propagation으로 재해석하면서 controller가 checkoutservice focused call을 추가했고, 그 결과 정답으로 이동했다. 이 케이스는 reasoner 변경이 controller 경로까지 바꾼 예다.
- 회귀 3개는 memory 패턴이 과하게 적용된 경우다. `diskio + mem` 동시 이상에서 실제 정답이 diskio인 케이스를 memory exhaustion으로 해석하거나, `case_000065`처럼 중간 구간 recommendationservice latency에 먼저 수렴해 productcatalogservice 로그 검증이 약해졌다.

## Timing

- memory run case total: `11826.877s` (197.1 min)
- step count with timing: `893`
- controller total: `3092.570s`
- reasoner total: `8714.068s`
- tool total: `19.790s`
- step all total: `11826.550s`

## 결론

past reasoning memory는 이번 run에서 top1-both를 `+3` 개선했다. 개선은 주로 reasoner가 latency propagation과 component-local resource metric을 더 잘 구분한 데서 나왔다. 다만 diskio 정답 케이스에서 mem 우선으로 회귀한 사례가 있어, memory prompt나 예시를 추가할 때는 `diskio가 압도적이고 지속적이면 mem보다 diskio를 우선한다`는 demonstration을 보강하는 것이 필요하다.
