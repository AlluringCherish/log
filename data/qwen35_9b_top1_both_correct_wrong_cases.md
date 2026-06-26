# Qwen3.5-9B Top@1 Both Correct/Wrong Cases

- Criterion: Top@1 Both
- Correct means first prediction exactly matches answer `(component, reason)`.
- Correct: 47 / 90
- Wrong: 43 / 90

## Correct Cases

| Case | Answer | Top@1 Prediction |
|---|---|---|
| case_000001 | checkoutservice_cpu | checkoutservice_cpu |
| case_000002 | checkoutservice_cpu | checkoutservice_cpu |
| case_000003 | checkoutservice_cpu | checkoutservice_cpu |
| case_000006 | checkoutservice_latency | checkoutservice_latency |
| case_000009 | checkoutservice_diskio | checkoutservice_diskio |
| case_000010 | checkoutservice_latency | checkoutservice_latency |
| case_000011 | checkoutservice_latency | checkoutservice_latency |
| case_000012 | checkoutservice_latency | checkoutservice_latency |
| case_000013 | checkoutservice_mem | checkoutservice_mem |
| case_000014 | checkoutservice_mem | checkoutservice_mem |
| case_000015 | checkoutservice_mem | checkoutservice_mem |
| case_000022 | currencyservice_latency | currencyservice_latency |
| case_000023 | currencyservice_latency | currencyservice_latency |
| case_000024 | currencyservice_latency | currencyservice_latency |
| case_000026 | currencyservice_diskio | currencyservice_diskio |
| case_000027 | currencyservice_diskio | currencyservice_diskio |
| case_000028 | currencyservice_latency | currencyservice_latency |
| case_000029 | currencyservice_latency | currencyservice_latency |
| case_000030 | currencyservice_latency | currencyservice_latency |
| case_000031 | currencyservice_mem | currencyservice_mem |
| case_000033 | currencyservice_mem | currencyservice_mem |
| case_000037 | emailservice_cpu | emailservice_cpu |
| case_000038 | emailservice_cpu | emailservice_cpu |
| case_000040 | emailservice_latency | emailservice_latency |
| case_000041 | emailservice_latency | emailservice_latency |
| case_000042 | emailservice_latency | emailservice_latency |
| case_000043 | emailservice_diskio | emailservice_diskio |
| case_000044 | emailservice_diskio | emailservice_diskio |
| case_000045 | emailservice_diskio | emailservice_diskio |
| case_000048 | emailservice_latency | emailservice_latency |
| case_000049 | emailservice_mem | emailservice_mem |
| case_000050 | emailservice_mem | emailservice_mem |
| case_000051 | emailservice_mem | emailservice_mem |
| case_000055 | productcatalogservice_cpu | productcatalogservice_cpu |
| case_000058 | productcatalogservice_latency | productcatalogservice_latency |
| case_000059 | productcatalogservice_latency | productcatalogservice_latency |
| case_000060 | productcatalogservice_latency | productcatalogservice_latency |
| case_000063 | productcatalogservice_diskio | productcatalogservice_diskio |
| case_000064 | productcatalogservice_latency | productcatalogservice_latency |
| case_000065 | productcatalogservice_latency | productcatalogservice_latency |
| case_000067 | productcatalogservice_mem | productcatalogservice_mem |
| case_000076 | recommendationservice_latency | recommendationservice_latency |
| case_000078 | recommendationservice_latency | recommendationservice_latency |
| case_000079 | recommendationservice_diskio | recommendationservice_diskio |
| case_000080 | recommendationservice_diskio | recommendationservice_diskio |
| case_000081 | recommendationservice_diskio | recommendationservice_diskio |
| case_000083 | recommendationservice_latency | recommendationservice_latency |

## Wrong Cases

| Case | Answer | Top@1 Prediction | Full Prediction |
|---|---|---|---|
| case_000004 | checkoutservice_latency | emailservice_latency | emailservice_latency, checkoutservice_latency |
| case_000005 | checkoutservice_latency | emailservice_latency | emailservice_latency, checkoutservice_latency, productcatalogservice_latency |
| case_000007 | checkoutservice_diskio | checkoutservice_mem | checkoutservice_mem |
| case_000008 | checkoutservice_diskio | checkoutservice_mem | checkoutservice_mem, checkoutservice_cpu, checkoutservice_latency |
| case_000016 | checkoutservice_socket | checkoutservice_cpu | checkoutservice_cpu, checkoutservice_mem |
| case_000017 | checkoutservice_socket | checkoutservice_mem | checkoutservice_mem, checkoutservice_cpu |
| case_000018 | checkoutservice_socket | checkoutservice_cpu | checkoutservice_cpu, checkoutservice_mem, checkoutservice_latency |
| case_000019 | currencyservice_cpu | currencyservice_diskio | currencyservice_diskio |
| case_000020 | currencyservice_cpu | currencyservice_latency | currencyservice_latency |
| case_000021 | currencyservice_cpu | currencyservice_latency | currencyservice_latency, checkoutservice_latency, currencyservice_mem, currencyservice_cpu |
| case_000025 | currencyservice_diskio | currencyservice_latency | currencyservice_latency, currencyservice_mem, checkoutservice_latency, recommendationservice_latency |
| case_000032 | currencyservice_mem | currencyservice_diskio | currencyservice_diskio, currencyservice_mem, currencyservice_latency, checkoutservice_latency, recommendationservice_latency |
| case_000034 | currencyservice_socket | currencyservice_mem | currencyservice_mem, currencyservice_socket |
| case_000035 | currencyservice_socket | currencyservice_diskio | currencyservice_diskio, currencyservice_latency, checkoutservice_latency, recommendationservice_latency, currencyservice_mem |
| case_000036 | currencyservice_socket | currencyservice_latency | currencyservice_latency |
| case_000039 | emailservice_cpu | emailservice_mem | emailservice_mem, emailservice_cpu, emailservice_latency, checkoutservice_latency |
| case_000046 | emailservice_latency | emailservice_mem | emailservice_mem, emailservice_latency, checkoutservice_latency |
| case_000047 | emailservice_latency | emailservice_mem | emailservice_mem, emailservice_latency, checkoutservice_latency |
| case_000052 | emailservice_socket | emailservice_mem | emailservice_mem, emailservice_latency, emailservice_cpu |
| case_000053 | emailservice_socket | emailservice_mem | emailservice_mem, emailservice_latency, emailservice_cpu |
| case_000054 | emailservice_socket | emailservice_mem | emailservice_mem, emailservice_cpu, emailservice_latency, emailservice_socket |
| case_000056 | productcatalogservice_cpu | productcatalogservice_latency | productcatalogservice_latency, productcatalogservice_cpu, productcatalogservice_mem, recommendationservice_latency, checkoutservice_latency |
| case_000057 | productcatalogservice_cpu | productcatalogservice_latency | productcatalogservice_latency, recommendationservice_latency, productcatalogservice_cpu, productcatalogservice_mem |
| case_000061 | productcatalogservice_diskio | productcatalogservice_latency | productcatalogservice_latency, productcatalogservice_mem, productcatalogservice_cpu |
| case_000062 | productcatalogservice_diskio | productcatalogservice_latency | productcatalogservice_latency, recommendationservice_latency |
| case_000066 | productcatalogservice_latency | recommendationservice_latency | recommendationservice_latency |
| case_000068 | productcatalogservice_mem | productcatalogservice_latency | productcatalogservice_latency, recommendationservice_latency |
| case_000069 | productcatalogservice_mem | recommendationservice_latency | recommendationservice_latency |
| case_000070 | productcatalogservice_socket | productcatalogservice_mem | productcatalogservice_mem, productcatalogservice_cpu, productcatalogservice_latency, recommendationservice_latency |
| case_000071 | productcatalogservice_socket | productcatalogservice_latency | productcatalogservice_latency, productcatalogservice_mem, productcatalogservice_cpu |
| case_000072 | productcatalogservice_socket | productcatalogservice_latency | productcatalogservice_latency, recommendationservice_latency |
| case_000073 | recommendationservice_cpu | recommendationservice_latency | recommendationservice_latency, recommendationservice_cpu |
| case_000074 | recommendationservice_cpu | recommendationservice_diskio | recommendationservice_diskio |
| case_000075 | recommendationservice_cpu | recommendationservice_latency | recommendationservice_latency, recommendationservice_mem, recommendationservice_cpu |
| case_000077 | recommendationservice_latency | recommendationservice_diskio | recommendationservice_diskio, recommendationservice_latency, recommendationservice_mem, productcatalogservice_latency |
| case_000082 | recommendationservice_latency | currencyservice_mem | currencyservice_mem |
| case_000084 | recommendationservice_latency | recommendationservice_diskio | recommendationservice_diskio, recommendationservice_mem, recommendationservice_latency |
| case_000085 | recommendationservice_mem | recommendationservice_latency | recommendationservice_latency |
| case_000086 | recommendationservice_mem | recommendationservice_latency | recommendationservice_latency, recommendationservice_mem, recommendationservice_cpu |
| case_000087 | recommendationservice_mem | recommendationservice_diskio | recommendationservice_diskio, recommendationservice_mem, recommendationservice_latency, recommendationservice_cpu |
| case_000088 | recommendationservice_socket | recommendationservice_latency | recommendationservice_latency |
| case_000089 | recommendationservice_socket | recommendationservice_diskio | recommendationservice_diskio |
| case_000090 | recommendationservice_socket | recommendationservice_latency | recommendationservice_latency, recommendationservice_mem, recommendationservice_socket, recommendationservice_cpu, emailservice_mem |
