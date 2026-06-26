# Qwen3.5-9B Correct/Wrong Case Split

- Source: `/data/260619/output/api_onlineboutique_90_qwen35_9b_0624_merged`
- 기본 정답 기준: `Top@1 Both` = 첫 번째 예측의 `(component, reason)` 쌍이 정답과 일치
- 보조 기준: `Top@5 Both`, `Top@1/5 Component`, `Top@1/5 Reason`도 함께 기록

## Summary

| Criterion | Correct | Wrong | Accuracy |
|---|---:|---:|---:|
| top_1_component | 85 | 5 | 94.4% |
| top_1_reason | 50 | 40 | 55.6% |
| top_1_both | 47 | 43 | 52.2% |
| top_5_component | 87 | 3 | 96.7% |
| top_5_reason | 66 | 24 | 73.3% |
| top_5_both | 65 | 25 | 72.2% |

## Top 1 Both

- Correct (47): case_000001, case_000002, case_000003, case_000006, case_000009, case_000010, case_000011, case_000012, case_000013, case_000014, case_000015, case_000022, case_000023, case_000024, case_000026, case_000027, case_000028, case_000029, case_000030, case_000031, case_000033, case_000037, case_000038, case_000040, case_000041, case_000042, case_000043, case_000044, case_000045, case_000048, case_000049, case_000050, case_000051, case_000055, case_000058, case_000059, case_000060, case_000063, case_000064, case_000065, case_000067, case_000076, case_000078, case_000079, case_000080, case_000081, case_000083
- Wrong (43): case_000004, case_000005, case_000007, case_000008, case_000016, case_000017, case_000018, case_000019, case_000020, case_000021, case_000025, case_000032, case_000034, case_000035, case_000036, case_000039, case_000046, case_000047, case_000052, case_000053, case_000054, case_000056, case_000057, case_000061, case_000062, case_000066, case_000068, case_000069, case_000070, case_000071, case_000072, case_000073, case_000074, case_000075, case_000077, case_000082, case_000084, case_000085, case_000086, case_000087, case_000088, case_000089, case_000090

## Top 5 Both

- Correct (65): case_000001, case_000002, case_000003, case_000004, case_000005, case_000006, case_000009, case_000010, case_000011, case_000012, case_000013, case_000014, case_000015, case_000021, case_000022, case_000023, case_000024, case_000026, case_000027, case_000028, case_000029, case_000030, case_000031, case_000032, case_000033, case_000034, case_000037, case_000038, case_000039, case_000040, case_000041, case_000042, case_000043, case_000044, case_000045, case_000046, case_000047, case_000048, case_000049, case_000050, case_000051, case_000054, case_000055, case_000056, case_000057, case_000058, case_000059, case_000060, case_000063, case_000064, case_000065, case_000067, case_000073, case_000075, case_000076, case_000077, case_000078, case_000079, case_000080, case_000081, case_000083, case_000084, case_000086, case_000087, case_000090
- Wrong (25): case_000007, case_000008, case_000016, case_000017, case_000018, case_000019, case_000020, case_000025, case_000035, case_000036, case_000052, case_000053, case_000061, case_000062, case_000066, case_000068, case_000069, case_000070, case_000071, case_000072, case_000074, case_000082, case_000085, case_000088, case_000089

## Top 1 Component

- Correct (85): case_000001, case_000002, case_000003, case_000006, case_000007, case_000008, case_000009, case_000010, case_000011, case_000012, case_000013, case_000014, case_000015, case_000016, case_000017, case_000018, case_000019, case_000020, case_000021, case_000022, case_000023, case_000024, case_000025, case_000026, case_000027, case_000028, case_000029, case_000030, case_000031, case_000032, case_000033, case_000034, case_000035, case_000036, case_000037, case_000038, case_000039, case_000040, case_000041, case_000042, case_000043, case_000044, case_000045, case_000046, case_000047, case_000048, case_000049, case_000050, case_000051, case_000052, case_000053, case_000054, case_000055, case_000056, case_000057, case_000058, case_000059, case_000060, case_000061, case_000062, case_000063, case_000064, case_000065, case_000067, case_000068, case_000070, case_000071, case_000072, case_000073, case_000074, case_000075, case_000076, case_000077, case_000078, case_000079, case_000080, case_000081, case_000083, case_000084, case_000085, case_000086, case_000087, case_000088, case_000089, case_000090
- Wrong (5): case_000004, case_000005, case_000066, case_000069, case_000082

## Top 1 Reason

- Correct (50): case_000001, case_000002, case_000003, case_000004, case_000005, case_000006, case_000009, case_000010, case_000011, case_000012, case_000013, case_000014, case_000015, case_000022, case_000023, case_000024, case_000026, case_000027, case_000028, case_000029, case_000030, case_000031, case_000033, case_000037, case_000038, case_000040, case_000041, case_000042, case_000043, case_000044, case_000045, case_000048, case_000049, case_000050, case_000051, case_000055, case_000058, case_000059, case_000060, case_000063, case_000064, case_000065, case_000066, case_000067, case_000076, case_000078, case_000079, case_000080, case_000081, case_000083
- Wrong (40): case_000007, case_000008, case_000016, case_000017, case_000018, case_000019, case_000020, case_000021, case_000025, case_000032, case_000034, case_000035, case_000036, case_000039, case_000046, case_000047, case_000052, case_000053, case_000054, case_000056, case_000057, case_000061, case_000062, case_000068, case_000069, case_000070, case_000071, case_000072, case_000073, case_000074, case_000075, case_000077, case_000082, case_000084, case_000085, case_000086, case_000087, case_000088, case_000089, case_000090

## Case Details

| Case | Answer | Prediction | Top@1 Both | Top@5 Both |
|---|---|---|---:|---:|
| case_000001 | checkoutservice_cpu | checkoutservice_cpu | True | True |
| case_000002 | checkoutservice_cpu | checkoutservice_cpu | True | True |
| case_000003 | checkoutservice_cpu | checkoutservice_cpu | True | True |
| case_000004 | checkoutservice_latency | emailservice_latency, checkoutservice_latency | False | True |
| case_000005 | checkoutservice_latency | emailservice_latency, checkoutservice_latency, productcatalogservice_latency | False | True |
| case_000006 | checkoutservice_latency | checkoutservice_latency | True | True |
| case_000007 | checkoutservice_diskio | checkoutservice_mem | False | False |
| case_000008 | checkoutservice_diskio | checkoutservice_mem, checkoutservice_cpu, checkoutservice_latency | False | False |
| case_000009 | checkoutservice_diskio | checkoutservice_diskio | True | True |
| case_000010 | checkoutservice_latency | checkoutservice_latency | True | True |
| case_000011 | checkoutservice_latency | checkoutservice_latency | True | True |
| case_000012 | checkoutservice_latency | checkoutservice_latency | True | True |
| case_000013 | checkoutservice_mem | checkoutservice_mem, checkoutservice_cpu, checkoutservice_latency | True | True |
| case_000014 | checkoutservice_mem | checkoutservice_mem, checkoutservice_cpu, checkoutservice_latency | True | True |
| case_000015 | checkoutservice_mem | checkoutservice_mem, checkoutservice_cpu, checkoutservice_latency | True | True |
| case_000016 | checkoutservice_socket | checkoutservice_cpu, checkoutservice_mem | False | False |
| case_000017 | checkoutservice_socket | checkoutservice_mem, checkoutservice_cpu | False | False |
| case_000018 | checkoutservice_socket | checkoutservice_cpu, checkoutservice_mem, checkoutservice_latency | False | False |
| case_000019 | currencyservice_cpu | currencyservice_diskio | False | False |
| case_000020 | currencyservice_cpu | currencyservice_latency | False | False |
| case_000021 | currencyservice_cpu | currencyservice_latency, checkoutservice_latency, currencyservice_mem, currencyservice_cpu | False | True |
| case_000022 | currencyservice_latency | currencyservice_latency, checkoutservice_latency | True | True |
| case_000023 | currencyservice_latency | currencyservice_latency, checkoutservice_latency | True | True |
| case_000024 | currencyservice_latency | currencyservice_latency, checkoutservice_latency | True | True |
| case_000025 | currencyservice_diskio | currencyservice_latency, currencyservice_mem, checkoutservice_latency, recommendationservice_latency | False | False |
| case_000026 | currencyservice_diskio | currencyservice_diskio, currencyservice_mem, currencyservice_latency, checkoutservice_latency | True | True |
| case_000027 | currencyservice_diskio | currencyservice_diskio, currencyservice_mem, currencyservice_latency, checkoutservice_latency | True | True |
| case_000028 | currencyservice_latency | currencyservice_latency, currencyservice_mem, checkoutservice_latency, recommendationservice_latency | True | True |
| case_000029 | currencyservice_latency | currencyservice_latency, checkoutservice_latency, recommendationservice_latency | True | True |
| case_000030 | currencyservice_latency | currencyservice_latency | True | True |
| case_000031 | currencyservice_mem | currencyservice_mem, currencyservice_latency, recommendationservice_latency, checkoutservice_latency | True | True |
| case_000032 | currencyservice_mem | currencyservice_diskio, currencyservice_mem, currencyservice_latency, checkoutservice_latency, recommendationservice_latency | False | True |
| case_000033 | currencyservice_mem | currencyservice_mem, currencyservice_latency, checkoutservice_latency, recommendationservice_latency, emailservice_latency | True | True |
| case_000034 | currencyservice_socket | currencyservice_mem, currencyservice_socket | False | True |
| case_000035 | currencyservice_socket | currencyservice_diskio, currencyservice_latency, checkoutservice_latency, recommendationservice_latency, currencyservice_mem | False | False |
| case_000036 | currencyservice_socket | currencyservice_latency | False | False |
| case_000037 | emailservice_cpu | emailservice_cpu, emailservice_latency | True | True |
| case_000038 | emailservice_cpu | emailservice_cpu, emailservice_latency, checkoutservice_latency | True | True |
| case_000039 | emailservice_cpu | emailservice_mem, emailservice_cpu, emailservice_latency, checkoutservice_latency | False | True |
| case_000040 | emailservice_latency | emailservice_latency, checkoutservice_latency | True | True |
| case_000041 | emailservice_latency | emailservice_latency, checkoutservice_latency | True | True |
| case_000042 | emailservice_latency | emailservice_latency | True | True |
| case_000043 | emailservice_diskio | emailservice_diskio, emailservice_mem, emailservice_cpu, emailservice_latency | True | True |
| case_000044 | emailservice_diskio | emailservice_diskio, emailservice_mem, emailservice_cpu, emailservice_latency, checkoutservice_latency | True | True |
| case_000045 | emailservice_diskio | emailservice_diskio, emailservice_mem, emailservice_cpu, emailservice_latency | True | True |
| case_000046 | emailservice_latency | emailservice_mem, emailservice_latency, checkoutservice_latency | False | True |
| case_000047 | emailservice_latency | emailservice_mem, emailservice_latency, checkoutservice_latency | False | True |
| case_000048 | emailservice_latency | emailservice_latency, emailservice_mem, emailservice_cpu, checkoutservice_latency | True | True |
| case_000049 | emailservice_mem | emailservice_mem, emailservice_latency, checkoutservice_latency | True | True |
| case_000050 | emailservice_mem | emailservice_mem | True | True |
| case_000051 | emailservice_mem | emailservice_mem, emailservice_latency, checkoutservice_latency | True | True |
| case_000052 | emailservice_socket | emailservice_mem, emailservice_latency, emailservice_cpu | False | False |
| case_000053 | emailservice_socket | emailservice_mem, emailservice_latency, emailservice_cpu | False | False |
| case_000054 | emailservice_socket | emailservice_mem, emailservice_cpu, emailservice_latency, emailservice_socket | False | True |
| case_000055 | productcatalogservice_cpu | productcatalogservice_cpu, productcatalogservice_latency, recommendationservice_latency | True | True |
| case_000056 | productcatalogservice_cpu | productcatalogservice_latency, productcatalogservice_cpu, productcatalogservice_mem, recommendationservice_latency, checkoutservice_latency | False | True |
| case_000057 | productcatalogservice_cpu | productcatalogservice_latency, recommendationservice_latency, productcatalogservice_cpu, productcatalogservice_mem | False | True |
| case_000058 | productcatalogservice_latency | productcatalogservice_latency, recommendationservice_latency | True | True |
| case_000059 | productcatalogservice_latency | productcatalogservice_latency, recommendationservice_latency, checkoutservice_latency | True | True |
| case_000060 | productcatalogservice_latency | productcatalogservice_latency, recommendationservice_latency, checkoutservice_latency | True | True |
| case_000061 | productcatalogservice_diskio | productcatalogservice_latency, productcatalogservice_mem, productcatalogservice_cpu | False | False |
| case_000062 | productcatalogservice_diskio | productcatalogservice_latency, recommendationservice_latency | False | False |
| case_000063 | productcatalogservice_diskio | productcatalogservice_diskio, productcatalogservice_latency, recommendationservice_latency | True | True |
| case_000064 | productcatalogservice_latency | productcatalogservice_latency, recommendationservice_latency | True | True |
| case_000065 | productcatalogservice_latency | productcatalogservice_latency, recommendationservice_latency, recommendationservice_mem, checkoutservice_latency | True | True |
| case_000066 | productcatalogservice_latency | recommendationservice_latency | False | False |
| case_000067 | productcatalogservice_mem | productcatalogservice_mem, productcatalogservice_latency | True | True |
| case_000068 | productcatalogservice_mem | productcatalogservice_latency, recommendationservice_latency | False | False |
| case_000069 | productcatalogservice_mem | recommendationservice_latency | False | False |
| case_000070 | productcatalogservice_socket | productcatalogservice_mem, productcatalogservice_cpu, productcatalogservice_latency, recommendationservice_latency | False | False |
| case_000071 | productcatalogservice_socket | productcatalogservice_latency, productcatalogservice_mem, productcatalogservice_cpu | False | False |
| case_000072 | productcatalogservice_socket | productcatalogservice_latency, recommendationservice_latency | False | False |
| case_000073 | recommendationservice_cpu | recommendationservice_latency, recommendationservice_cpu | False | True |
| case_000074 | recommendationservice_cpu | recommendationservice_diskio | False | False |
| case_000075 | recommendationservice_cpu | recommendationservice_latency, recommendationservice_mem, recommendationservice_cpu | False | True |
| case_000076 | recommendationservice_latency | recommendationservice_latency | True | True |
| case_000077 | recommendationservice_latency | recommendationservice_diskio, recommendationservice_latency, recommendationservice_mem, productcatalogservice_latency | False | True |
| case_000078 | recommendationservice_latency | recommendationservice_latency | True | True |
| case_000079 | recommendationservice_diskio | recommendationservice_diskio | True | True |
| case_000080 | recommendationservice_diskio | recommendationservice_diskio, recommendationservice_mem, recommendationservice_latency, recommendationservice_cpu | True | True |
| case_000081 | recommendationservice_diskio | recommendationservice_diskio, recommendationservice_mem, recommendationservice_latency, recommendationservice_cpu | True | True |
| case_000082 | recommendationservice_latency | currencyservice_mem | False | False |
| case_000083 | recommendationservice_latency | recommendationservice_latency, recommendationservice_mem, productcatalogservice_latency, emailservice_mem, currencyservice_latency | True | True |
| case_000084 | recommendationservice_latency | recommendationservice_diskio, recommendationservice_mem, recommendationservice_latency | False | True |
| case_000085 | recommendationservice_mem | recommendationservice_latency | False | False |
| case_000086 | recommendationservice_mem | recommendationservice_latency, recommendationservice_mem, recommendationservice_cpu | False | True |
| case_000087 | recommendationservice_mem | recommendationservice_diskio, recommendationservice_mem, recommendationservice_latency, recommendationservice_cpu | False | True |
| case_000088 | recommendationservice_socket | recommendationservice_latency | False | False |
| case_000089 | recommendationservice_socket | recommendationservice_diskio | False | False |
| case_000090 | recommendationservice_socket | recommendationservice_latency, recommendationservice_mem, recommendationservice_socket, recommendationservice_cpu, emailservice_mem | False | True |
