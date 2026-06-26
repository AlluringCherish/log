## PAST_REASONING_MEMORY

The following content is raw past agent reasoning from previous RCA cases.
Use it only as examples of investigation behavior and evidence interpretation.
Do not treat any past component, reason, timestamp, or final answer as evidence for the current case.
Current case observations override this memory.
Do not copy the past answer. Follow the investigation pattern only.

### Selection note

These snippets were selected from Qwen3.5-9B successful top1-both cases because they address the common reasoner failures: cpu/socket/mem being overwritten by latency or mem, and primary KPI evidence being treated as secondary.

### CPU over latency/mem

#### case_000002 | answer=checkoutservice_cpu | prediction_top1=checkoutservice_cpu

- Step 6 rankings: checkoutservice_cpu

```text
Checked 720-900s checkoutservice metrics. CPU dev +53-58% and latency.p90 dev +27-29% confirm severe resource contention. Traces show high self_p99 latency. Logs show normal order flow. Root cause is checkoutservice CPU saturation.
```

- Step 8 rankings: checkoutservice_cpu, currencyservice_latency, emailservice_mem

```text
Checkoutservice CPU saturation (dev +58.5%) and latency (dev +29.8%) in 720-900s confirm root cause. Traces and logs validate high load without flow errors. Final ranking prioritizes checkoutservice CPU.
```

#### case_000003 | answer=checkoutservice_cpu | prediction_top1=checkoutservice_cpu

- Step 5 rankings: checkoutservice_cpu, checkoutservice_mem, checkoutservice_latency

```text
Checked 720-900s metrics. Strongest anomalies: checkoutservice cpu dev+250.6, mem dev+28.6, latency p90 dev+24.8. Implication: checkoutservice resource exhaustion (CPU/Mem) drives latency; redis/productcatalogservice mem anomalies resolved. Ranking top1=checkoutservice_cpu
```

- Step 9 rankings: checkoutservice_cpu, checkoutservice_mem, checkoutservice_latency

```text
Checked 1260-1440s checkoutservice metrics. CPU dev+246-253, mem dev+27-30, latency p90 dev+24-27 persist. Traces show internal self-loops (GetProduct) with high latency. Logs confirm successful payments. Implication: checkoutservice resource exhaustion (CPU/Mem) drives latency. Ranking top1=checkoutservice_cpu
```

- Step 10 rankings: checkoutservice_cpu, checkoutservice_mem, checkoutservice_latency

```text
Checkoutservice CPU and memory exhaustion (dev+250/28) drove high latency. Traces confirm internal self-loop delays. Logs show successful downstream operations, validating checkoutservice as the bottleneck.
```

#### case_000037 | answer=emailservice_cpu | prediction_top1=emailservice_cpu

- Step 9 rankings: emailservice_cpu, checkoutservice_latency, emailservice_latency

```text
Checked 1260-1440s emailservice metrics. Sustained CPU dev=+587 to +635 confirms resource exhaustion as root cause. Trace latency spikes (up to 15ms) are propagation effects. Ranking updated to emailservice_cpu first.
```

- Step 10 rankings: emailservice_cpu, checkoutservice_latency, currencyservice_latency

```text
Final RCA confirms emailservice CPU exhaustion (dev>+600) as primary root cause. Trace latency spikes and normal logs validate propagation. Checkoutservice latency is secondary effect.
```

### Socket over mem/latency

#### case_000016 | answer=checkoutservice_socket | prediction_top1=checkoutservice_socket

- Step 8 rankings: checkoutservice_socket

```text
Checked 1260-1440s metrics. checkoutservice shows sustained high socket (dev=+13) and mem (dev=+9.4 to +10.4). CPU spikes absent. Memory/socket pressure persists as root cause.
```

- Step 9 rankings: checkoutservice_socket

```text
Checked 1260-1440s checkoutservice metrics. Socket dev=+13.0 and mem dev=+9.4 to +10.4 persist across all windows. CPU remains low (dev<+1). Traces show normal internal latency. Root cause is socket pressure.
```

- Step 10 rankings: checkoutservice_socket

```text
Checked 1260-1440s checkoutservice metrics. Socket dev=+13.0 persists across all windows, while mem dev=+9.4 to +10.4 and cpu remain low. Traces show normal internal latency. Root cause is socket pressure.
```

- Step 11 rankings: checkoutservice_socket, currencyservice_latency, emailservice_mem

```text
Final RCA confirms checkoutservice socket pressure (dev=+13.0) as primary cause. Currencyservice and emailservice show secondary latency/mem anomalies. Socket metric validates root cause over trace latency.
```

### Memory over latency

#### case_000014 | answer=checkoutservice_mem | prediction_top1=checkoutservice_mem

- Step 6 rankings: checkoutservice_mem, currencyservice_latency, shippingservice_latency

```text
Checked 900-990s metrics. Checkoutservice shows massive memory spikes (dev=+1194-+1218) and CPU spikes (dev=+202-+294) across all windows, with latency.p90 dev=+80-+142. This confirms checkoutservice as the root cause with memory exhaustion driving latency. Ranking top1=checkoutservice_mem
```

- Step 8 rankings: checkoutservice_mem, checkoutservice_cpu, checkoutservice_latency

```text
Metrics confirm checkoutservice memory exhaustion (dev=+1194) as primary root cause. CPU spikes and latency degradation follow. No other candidate services show comparable anomalies.
```

#### case_000031 | answer=currencyservice_mem | prediction_top1=currencyservice_mem

- Step 5 rankings: currencyservice_mem, currencyservice_latency, recommendationservice_latency

```text
Checked 720-900s metrics. currencyservice mem dev=+143.4 to +430.8 (strong anomaly); latency.p50 dev=+383.8 to +613.4 (supports latency). currencyservice mem is root cause.
```

- Step 9 rankings: currencyservice_mem, currencyservice_latency, recommendationservice_latency

```text
Rechecked 1260-1440s currencyservice. Mem dev=+294.9 to +430.8 (strong anomaly); latency.p50 dev=+489.2 to +628.7 (supports latency). Mem remains root cause.
```

- Step 10 rankings: currencyservice_mem, currencyservice_latency, recommendationservice_latency

```text
Final RCA confirms currencyservice memory exhaustion as primary root cause, supported by high dev scores and trace latency propagation.
```

#### case_000049 | answer=emailservice_mem | prediction_top1=emailservice_mem

- Step 5 rankings: emailservice_mem, checkoutservice_latency, currencyservice_mem

```text
Checked 720-900s metrics. Anomalies: emailservice mem (M1705, M1776, etc.) and latency (M1706, M1777, etc.) show massive deviations. Implication: emailservice memory exhaustion drives latency spikes. Ranking: emailservice_mem.
```

- Step 9 rankings: emailservice_mem, checkoutservice_latency, currencyservice_mem

```text
Rechecked 1260-1440s emailservice metrics. Massive memory deviations (dev+85k to +95k) persist, confirming memory exhaustion as root cause. Traces show high latency correlated with memory spikes. Ranking: emailservice_mem.
```

- Step 10 rankings: emailservice_mem, checkoutservice_latency, currencyservice_mem

```text
Final RCA confirms emailservice memory exhaustion as primary root cause. Traces show latency propagation to checkoutservice. Currency service memory spike is secondary. Ranking: emailservice_mem, checkoutservice_latency, currencyservice_mem.
```

### Latency only when component-local latency is dominant

#### case_000058 | answer=productcatalogservice_latency | prediction_top1=productcatalogservice_latency

- Step 9 rankings: productcatalogservice_latency, recommendationservice_latency, frontend_latency

```text
Checked 1260-1440s productcatalogservice metrics. latency.p90 dev=+12367-12389 consistently dominates; p50 dev=+44-941 secondary. Implication: productcatalogservice remains root cause. Top candidate: productcatalogservice latency.
```

- Step 10 rankings: productcatalogservice_latency, recommendationservice_latency, frontend_latency

```text
Checked 1260-1440s productcatalogservice, recommendationservice, frontend. productcatalogservice latency.p90 dev=+12367-12389 dominates; recommendationservice dev=+3400-3430 secondary. Implication: productcatalogservice is root cause. Top candidate: productcatalogservice latency.
```

- Step 11 rankings: productcatalogservice_latency, recommendationservice_latency, frontend_latency

```text
Final RCA confirms productcatalogservice latency anomaly (dev >12000) as primary root cause, supported by trace propagation to frontend. Recommendationservice and frontend show secondary latency deviations. Final ranking prioritizes productcatalogservice.
```

#### case_000076 | answer=recommendationservice_latency | prediction_top1=recommendationservice_latency

- Step 9 rankings: recommendationservice_latency, frontend_latency, checkoutservice_latency

```text
Checked 1260-1440s recommendationservice. Metrics show sustained latency.p90 dev ~7570-7600 and latency.p50 dev ~4400-4500, confirming severe internal latency anomaly. Traces show self_p99 spikes (205k-382k us) supporting local latency. Logs normal. Implication: recommendationservice is root cause due to latency.
```

- Step 10 rankings: recommendationservice_latency, frontend_latency, checkoutservice_latency

```text
Checked 1260-1440s recommendationservice. Metrics show sustained latency.p90 dev ~7570-7600 and latency.p50 dev ~4400-4500, confirming severe internal latency anomaly. Traces show self_p99 spikes (205k-382k us) supporting local latency. Logs normal. Implication: recommendationservice is root cause due to latency.
```

- Step 11 rankings: recommendationservice_latency, frontend_latency, checkoutservice_latency

```text
Final RCA confirms recommendationservice as primary root cause due to severe sustained latency.p90 anomalies (dev >7500). Traces and logs validate local latency without external propagation. Secondary impacts on frontend and checkoutservice are downstream effects.
```

### Primary KPI over secondary latency

#### case_000007 | answer=checkoutservice_diskio | prediction_top1=checkoutservice_diskio

- Step 9 rankings: checkoutservice_diskio

```text
Checked 1260-1440s checkoutservice metrics. Diskio dev=+10.3B-10.6B persists, confirming saturation. CPU and mem also elevated but secondary. Root cause is checkoutservice diskio.
```

- Step 10 rankings: checkoutservice_diskio, emailservice_latency, currencyservice_latency

```text
Checkoutservice diskio saturation (dev>+10B) is the primary anomaly, confirmed by elevated CPU and trace latency. Emailservice and currencyservice show secondary latency deviations. Final ranking prioritizes checkoutservice diskio.
```

#### case_000080 | answer=recommendationservice_diskio | prediction_top1=recommendationservice_diskio

- Step 8 rankings: recommendationservice_diskio, recommendationservice_mem, recommendationservice_latency

```text
Checked 1080-1260s recommendationservice metrics. Sustained diskio ~9.4GB/s and mem ~450MB with latency.p90 +5000% confirm resource exhaustion as root cause.
```

- Step 9 rankings: recommendationservice_diskio, recommendationservice_mem, recommendationservice_latency

```text
Recommendationservice shows sustained diskio ~9.8GB/s and mem spikes, confirming resource exhaustion as root cause. Traces validate propagation to frontend.
```
