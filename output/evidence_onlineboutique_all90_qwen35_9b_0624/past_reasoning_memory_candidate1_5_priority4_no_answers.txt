## PAST_REASONING_MEMORY

The following are previous observation -> analysis -> ranking examples.
Use them as in-context demonstrations only when their observation pattern is relevant to the current case.
For the current case, use only the current observation and current state as evidence.
Do not copy past component names, reasons, timestamps, evidence ids, metric values, or answers.

### Example 1

observation:
```text
{
  "tool_observations": [
    {
      "tool_call": {
        "name": "get_evidence",
        "args": {
          "start_time": 1260,
          "end_time": 1440,
          "components": [
            "checkoutservice"
          ]
        },
        "reasoning": "Validating the top candidate checkoutservice with focused metrics, traces, and logs for the 1260-1440s window where socket and mem anomalies were detected."
      },
      "status": true,
      "observation": "{\n  \"telemetry\": \"evidence\",\n  \"time_unit\": \"relative_seconds_from_case_start\",\n  \"query\": {\n    \"start_time\": 1260,\n    \"end_time\": 1440,\n    \"components\": [\n      \"checkoutservice\"\n    ]\n  },\n  \"component_filter_rule\": {\n    \"metrics\": \"component matches\",\n    \"logs\": \"component matches\",\n    \"traces\": \"caller or callee matches\"\n  },\n  \"selection_policy\": \"components=[] returns metrics-only broad overview; component-filtered calls return metrics first, then traces, then logs\",\n  \"ordering\": \"window asc, modality metrics->traces->logs, abs(dev) desc within a window/modality\",\n  \"per_window_modality_limit\": 3,\n  \"latency_self_p99_definition\": \"callee span exclusive latency p99, computed as span duration minus direct child span durations\",\n  \"returned_count\": 54,\n  \"matched_count\": 474,\n  \"truncated\": false,\n  \"returned_windows\": [\n    {\n      \"start_time\": 1260,\n      \"end_time\": 1290\n    },\n    {\n      \"start_time\": 1290,\n      \"end_time\": 1320\n    },\n    {\n      \"start_time\": 1320,\n      \"end_time\": 1350\n    },\n    {\n      \"start_time\": 1350,\n      \"end_time\": 1380\n    },\n    {\n      \"start_time\": 1380,\n      \"end_time\": 1410\n    },\n    {\n      \"start_time\": 1410,\n      \"end_time\": 1440\n    }\n  ],\n  \"next_start_time\": null,\n  \"lines\": [\n    \"[metrics] id=M3113 window=1260-1290 component=checkoutservice signal=socket value=22 unit=count dev=+13.0 n=30\",\n    \"[metrics] id=M3114 window=1260-1290 component=checkoutservice signal=mem value=14843630.9 unit=bytes dev=+10.4 n=30\",\n    \"[metrics] id=M3120 window=1260-1290 component=checkoutservice signal=latency.p50 value=0.0853175 unit=s dev=-1.6 n=30\",\n    \"[traces] id=T4873 window=1260-1290 edge=checkoutservice>checkoutservice op=GetCart signal=latency.p99 value=10366.7 unit=us dev=+1.7 n=15\",\n    \"[traces] id=T4874 window=1260-1290 edge=checkoutservice>checkoutservice op=GetCart signal=latency.self_p99 value=10366.7 unit=us dev=+1.7 n=15\",\n    \"[traces] id=T4875 window=1260-1290 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.p99 value=344.2 unit=us dev=-1.4 n=15\",\n    \"[logs] id=L19303 window=1260-1290 component=checkoutservice template_id=2843 level=info signal=log.count value=2 unit=count dev=+2.0 template=\\\"[PlaceOrder] user_id=\\\\\\\"fdebbb24-0949-4cad-8a1f-69d6a2de04e8\\\\\\\" user_currency=\\\\\\\"JPY\\\\\\\"\\\"\",\n    \"[logs] id=L19352 window=1260-1290 component=checkoutservice template_id=11818 level=info signal=log.count value=1 unit=count dev=+1.0 template=\\\"payment went through (transaction_id: 129ddd6d-5483-4604-9a15-4478adee2210)\\\"\",\n    \"[logs] id=L19353 window=1260-1290 component=checkoutservice template_id=11877 level=info signal=log.count value=1 unit=count dev=+1.0 template=\\\"payment went through (transaction_id: 2dcc73a8-3235-48ad-8745-d0d4fa0ca618)\\\"\",\n    \"[metrics] id=M3186 window=1290-1320 component=checkoutservice signal=socket value=22 unit=count dev=+13.0 n=30\",\n    \"[metrics] id=M3187 window=1290-1320 component=checkoutservice signal=mem value=14417373.9 unit=bytes dev=+9.5 n=30\",\n    \"[metrics] id=M3210 window=1290-1320 component=checkoutservice signal=latency.p50 value=0.104028 unit=s dev=-0.5 n=30\",\n    \"[traces] id=T4998 window=1290-1320 edge=checkoutservice>productcatalogservice op=GetProduct signal=latency.p99 value=21 unit=us dev=-1.4 n=30\",\n    \"[traces] id=T4999 window=1290-1320 edge=checkoutservice>productcatalogservice op=GetProduct signal=latency.self_p99 value=21 unit=us dev=-1.4 n=30\",\n    \"[traces] id=T5000 window=1290-1320 edge=checkoutservice>checkoutservice op=ShipOrder signal=latency.p99 value=3389.9 unit=us dev=-1.3 n=10\",\n    \"[logs] id=L19780 window=1290-1320 component=checkoutservice template_id=2762 level=info signal=log.count value=2 unit=count dev=+2.0 template=\\\"[PlaceOrder] user_id=\\\\\\\"a54783f7-af86-4c6a-ab73-90331c9eb377\\\\\\\" user_currency=\\\\\\\"USD\\\\\\\"\\\"\",\n    \"[logs] id=L19800 window=1290-1320 component=checkoutservice template_id=11779 level=info signal=log.count value=10 unit=count dev=-1.1 template=\\\"order confirmation email sent to \\\\\\\"someone@example.com\\\\\\\"\\\"\",\n    \"[logs] id=L19839 window=1290-1320 component=checkoutservice template_id=11791 level=info signal=log.count value=1 unit=count dev=+1.0 template=\\\"payment went through (transaction_id: 05f39727-9470-489d-a5f0-7efd3ef052b2)\\\"\",\n    \"[metrics] id=M3259 window=1320-1350 component=checkoutservice signal=socket value=22 unit=count dev=+13.0 n=30\",\n    \"[metrics] id=M3260 window=1320-1350 component=checkoutservice signal=mem value=14468573.9 unit=bytes dev=+9.6 n=30\",\n    \"[metrics] id=M3275 window=1320-1350 component=checkoutservice signal=workload value=0.639933 unit=rps dev=-1.0 n=30\",\n    \"[traces] id=T5106 window=1320-1350 edge=checkoutservice>productcatalogservice op=GetProduct signal=latency.p99 value=114.3 unit=us dev=+4.5 n=23\",\n    \"[traces] id=T5107 window=1320-1350 edge=checkoutservice>productcatalogservice op=GetProduct signal=latency.self_p99 value=114.3 unit=us dev=+4.5 n=23\",\n    \"[traces] id=T5108 window=1320-1350 edge=checkoutservice>checkoutservice op=GetProduct signal=latency.p99 value=6454.8 unit=us dev=+4.3 n=23\",\n    \"[logs] id=L20200 window=1320-1350 component=checkoutservice template_id=2663 level=info signal=log.count value=2 unit=count dev=+2.0 template=\\\"[PlaceOrder] user_id=\\\\\\\"005726c0-8887-496c-95ce-304f652797ac\\\\\\\" user_currency=\\\\\\\"JPY\\\\\\\"\\\"\",\n    \"[logs] id=L20219 window=1320-1350 component=checkoutservice template_id=11779 level=info signal=log.count value=10 unit=count dev=-1.1 template=\\\"order confirmation email sent to \\\\\\\"someone@example.com\\\\\\\"\\\"\",\n    \"[logs] id=L20251 window=1320-1350 component=checkoutservice template_id=11790 level=info signal=log.count value=1 unit=count dev=+1.0 template=\\\"payment went through (transaction_id: 059e382a-2345-49d5-8168-3f0087efd782)\\\"\",\n    \"[metrics] id=M3332 window=1350-1380 component=checkoutservice signal=socket value=22 unit=count dev=+13.0 n=30\",\n    \"[metrics] id=M3333 window=1350-1380 component=checkoutservice signal=mem value=14347468.8 unit=bytes dev=+9.4 n=30\",\n    \"[metrics] id=M3349 window=1350-1380 component=checkoutservice signal=cpu value=0.327523 unit=percent dev=-0.9 n=30\",\n    \"[traces] id=T5222 window=1350-1380 edge=checkoutservice>checkoutservice op=GetCart signal=call.count value=19 unit=count dev=+1.4 n=19\",\n    \"[traces] id=T5223 window=1350-1380 edge=frontend>checkoutservice op=PlaceOrder signal=call.count value=19 unit=count dev=+1.4 n=19\",\n    \"[traces] id=T5225 window=1350-1380 edge=checkoutservice>checkoutservice op=Charge signal=call.count value=19 unit=count dev=+1.4 n=19\",\n    \"[logs] id=L20621 window=1350-1380 component=checkoutservice template_id=2662 level=info signal=log.count value=2 unit=count dev=+1.7 template=\\\"[PlaceOrder] user_id=\\\\\\\"005726c0-8887-496c-95ce-304f652797ac\\\\\\\" user_currency=\\\\\\\"EUR\\\\\\\"\\\"\",\n    \"[logs] id=L20629 window=1350-1380 component=checkoutservice template_id=11779 level=info signal=log.count value=19 unit=count dev=+1.4 template=\\\"order confirmation email sent to \\\\\\\"someone@example.com\\\\\\\"\\\"\",\n    \"[logs] id=L20685 window=1350-1380 component=checkoutservice template_id=11821 level=info signal=log.count value=1 unit=count dev=+1.0 template=\\\"payment went through (transaction_id: 159d5299-77d6-4b8d-9540-0249b1787f4a)\\\"\",\n    \"[metrics] id=M3405 window=1380-1410 component=checkoutservice signal=socket value=22 unit=count dev=+13.0 n=30\",\n    \"[metrics] id=M3406 window=1380-1410 component=checkoutservice signal=mem value=14846361.6 unit=bytes dev=+10.4 n=30\",\n    \"[metrics] id=M3418 window=1380-1410 component=checkoutservice signal=cpu value=0.457216 unit=percent dev=+0.8 n=30\",\n    \"[traces] id=T5345 window=1380-1410 edge=checkoutservice>checkoutservice op=GetCart signal=call.count value=9 unit=count dev=-1.4 n=9\",\n    \"[traces] id=T5346 window=1380-1410 edge=frontend>checkoutservice op=PlaceOrder signal=call.count value=9 unit=count dev=-1.4 n=9\",\n    \"[traces] id=T5348 window=1380-1410 edge=checkoutservice>checkoutservice op=Charge signal=call.count value=9 unit=count dev=-1.4 n=9\",\n    \"[logs] id=L21133 window=1380-1410 component=checkoutservice template_id=11779 level=info signal=log.count value=9 unit=count dev=-1.4 template=\\\"order confirmation email sent to \\\\\\\"someone@example.com\\\\\\\"\\\"\",\n    \"[logs] id=L21177 window=1380-1410 component=checkoutservice template_id=11786 level=info signal=log.count value=1 unit=count dev=+1.0 template=\\\"payment went through (transaction_id: 034e7812-8649-4450-840c-bb1f06412456)\\\"\",\n    \"[logs] id=L21178 window=1380-1410 component=checkoutservice template_id=11797 level=info signal=log.count value=1 unit=count dev=+1.0 template=\\\"payment went through (transaction_id: 088201f8-f5a3-4f54-8a64-11e976139f40)\\\"\",\n    \"[metrics] id=M3478 window=1410-1440 component=checkoutservice signal=socket value=22 unit=count dev=+13.0 n=30\",\n    \"[metrics] id=M3479 window=1410-1440 component=checkoutservice signal=mem value=14569472 unit=bytes dev=+9.8 n=30\",\n    \"[metrics] id=M3488 window=1410-1440 component=checkoutservice signal=latency.p50 value=0.0897075 unit=s dev=-1.3 n=30\",\n    \"[traces] id=T5460 window=1410-1440 edge=checkoutservice>productcatalogservice op=GetProduct signal=latency.p99 value=21 unit=us dev=-1.4 n=33\",\n    \"[traces] id=T5461 window=1410-1440 edge=checkoutservice>productcatalogservice op=GetProduct signal=latency.self_p99 value=21 unit=us dev=-1.4 n=33\",\n    \"[traces] id=T5463 window=1410-1440 edge=checkoutservice>checkoutservice op=ShipOrder signal=latency.p99 value=3583.8 unit=us dev=-1.2 n=12\",\n    \"[logs] id=L21586 window=1410-1440 component=checkoutservice template_id=11974 level=info signal=log.count value=1 unit=count dev=+1.0 template=\\\"payment went through (transaction_id: 53eecd51-cc33-4e40-a026-44bc11f3f6cc)\\\"\",\n    \"[logs] id=L21587 window=1410-1440 component=checkoutservice template_id=12123 level=info signal=log.count value=1 unit=count dev=+1.0 template=\\\"payment went through (transaction_id: 931246eb-acd4-4c1e-aafe-d29f326aab54)\\\"\",\n    \"[logs] id=L21588 window=1410-1440 component=checkoutservice template_id=12160 level=info signal=log.count value=1 unit=count dev=+1.0 template=\\\"payment went through (transaction_id: a0c26c48-9a16-4ab0-9bd2-9de1e872b2be)\\\"\"\n  ]\n}"
    }
  ]
}
```

analysis:
```text
Checked 1260-1440s checkoutservice metrics. Socket dev=+13.0 and mem dev=+9.4 to +10.4 persist across all windows. CPU remains low (dev<+1). Traces show normal internal latency. Root cause is socket pressure.
```

ranking:
```json
{
  "rankings": [
    {
      "rank": 1,
      "component": "checkoutservice",
      "reason": "socket"
    }
  ]
}
```

### Example 2

observation:
```text
Controller marked analysis complete.
```

analysis:
```text
Final RCA confirms checkoutservice socket pressure (dev=+13.0) as primary cause. Currencyservice and emailservice show secondary latency/mem anomalies. Socket metric validates root cause over trace latency.
```

ranking:
```json
{
  "final_ranking": [
    {
      "time": 1260,
      "component": "checkoutservice",
      "reason": "socket"
    },
    {
      "time": 1260,
      "component": "currencyservice",
      "reason": "latency"
    },
    {
      "time": 1260,
      "component": "emailservice",
      "reason": "mem"
    }
  ]
}
```

### Example 3

observation:
```text
{
  "tool_observations": [
    {
      "tool_call": {
        "name": "get_evidence",
        "args": {
          "start_time": 1260,
          "end_time": 1440,
          "components": [
            "emailservice"
          ]
        },
        "reasoning": "Validating the top candidate emailservice with component-filtered evidence to confirm CPU and latency anomalies and check for trace/log support."
      },
      "status": true,
      "observation": "{\n  \"telemetry\": \"evidence\",\n  \"time_unit\": \"relative_seconds_from_case_start\",\n  \"query\": {\n    \"start_time\": 1260,\n    \"end_time\": 1440,\n    \"components\": [\n      \"emailservice\"\n    ]\n  },\n  \"component_filter_rule\": {\n    \"metrics\": \"component matches\",\n    \"logs\": \"component matches\",\n    \"traces\": \"caller or callee matches\"\n  },\n  \"selection_policy\": \"components=[] returns metrics-only broad overview; component-filtered calls return metrics first, then traces, then logs\",\n  \"ordering\": \"window asc, modality metrics->traces->logs, abs(dev) desc within a window/modality\",\n  \"per_window_modality_limit\": 3,\n  \"latency_self_p99_definition\": \"callee span exclusive latency p99, computed as span duration minus direct child span durations\",\n  \"returned_count\": 42,\n  \"matched_count\": 72,\n  \"truncated\": false,\n  \"returned_windows\": [\n    {\n      \"start_time\": 1260,\n      \"end_time\": 1290\n    },\n    {\n      \"start_time\": 1290,\n      \"end_time\": 1320\n    },\n    {\n      \"start_time\": 1320,\n      \"end_time\": 1350\n    },\n    {\n      \"start_time\": 1350,\n      \"end_time\": 1380\n    },\n    {\n      \"start_time\": 1380,\n      \"end_time\": 1410\n    },\n    {\n      \"start_time\": 1410,\n      \"end_time\": 1440\n    }\n  ],\n  \"next_start_time\": null,\n  \"lines\": [\n    \"[metrics] id=M3025 window=1260-1290 component=emailservice signal=cpu value=19.58 unit=percent dev=+625.2 n=30\",\n    \"[metrics] id=M3026 window=1260-1290 component=emailservice signal=latency.p90 value=0.0214842 unit=s dev=+596.6 n=30\",\n    \"[metrics] id=M3027 window=1260-1290 component=emailservice signal=latency.p50 value=0.00958441 unit=s dev=+418.7 n=30\",\n    \"[traces] id=T4873 window=1260-1290 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.p99 value=5351.5 unit=us dev=+35.5 n=7\",\n    \"[traces] id=T4874 window=1260-1290 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.self_p99 value=5351.5 unit=us dev=+35.5 n=7\",\n    \"[traces] id=T4892 window=1260-1290 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=call.count value=7 unit=count dev=-1.6 n=7\",\n    \"[logs] id=L1268 window=1260-1290 component=emailservice template_id=28 level=INFO signal=log.count value=7 unit=count dev=-1.6 template=\\\"emailservice A request to send order confirmation email to someone@example.com has been received.\\\"\",\n    \"[metrics] id=M3097 window=1290-1320 component=emailservice signal=cpu value=19.68 unit=percent dev=+628.4 n=30\",\n    \"[metrics] id=M3098 window=1290-1320 component=emailservice signal=latency.p90 value=0.021272 unit=s dev=+589.1 n=30\",\n    \"[metrics] id=M3099 window=1290-1320 component=emailservice signal=latency.p50 value=0.00974588 unit=s dev=+429.0 n=30\",\n    \"[traces] id=T4989 window=1290-1320 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.p99 value=10283.9 unit=us dev=+71.1 n=15\",\n    \"[traces] id=T4990 window=1290-1320 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.self_p99 value=10283.9 unit=us dev=+71.1 n=15\",\n    \"[traces] id=T5023 window=1290-1320 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=call.count value=15 unit=count dev=+0.7 n=15\",\n    \"[logs] id=L1306 window=1290-1320 component=emailservice template_id=28 level=INFO signal=log.count value=15 unit=count dev=+0.7 template=\\\"emailservice A request to send order confirmation email to someone@example.com has been received.\\\"\",\n    \"[metrics] id=M3169 window=1320-1350 component=emailservice signal=latency.p50 value=0.0136252 unit=s dev=+675.9 n=30\",\n    \"[metrics] id=M3170 window=1320-1350 component=emailservice signal=latency.p90 value=0.022725 unit=s dev=+640.5 n=30\",\n    \"[metrics] id=M3171 window=1320-1350 component=emailservice signal=cpu value=19.91 unit=percent dev=+635.9 n=30\",\n    \"[traces] id=T5105 window=1320-1350 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.p99 value=12229.6 unit=us dev=+85.1 n=25\",\n    \"[traces] id=T5106 window=1320-1350 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.self_p99 value=12229.6 unit=us dev=+85.1 n=25\",\n    \"[traces] id=T5115 window=1320-1350 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=call.count value=25 unit=count dev=+3.6 n=25\",\n    \"[logs] id=L1328 window=1320-1350 component=emailservice template_id=28 level=INFO signal=log.count value=25 unit=count dev=+3.6 template=\\\"emailservice A request to send order confirmation email to someone@example.com has been received.\\\"\",\n    \"[metrics] id=M3241 window=1350-1380 component=emailservice signal=latency.p90 value=0.0221011 unit=s dev=+618.5 n=30\",\n    \"[metrics] id=M3242 window=1350-1380 component=emailservice signal=cpu value=18.42 unit=percent dev=+587.5 n=30\",\n    \"[metrics] id=M3243 window=1350-1380 component=emailservice signal=latency.p50 value=0.0105204 unit=s dev=+478.3 n=30\",\n    \"[traces] id=T5221 window=1350-1380 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.p99 value=12023.8 unit=us dev=+83.6 n=13\",\n    \"[traces] id=T5222 window=1350-1380 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.self_p99 value=12023.8 unit=us dev=+83.6 n=13\",\n    \"[traces] id=T5298 window=1350-1380 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=call.count value=13 unit=count dev=+0.1 n=13\",\n    \"[logs] id=L1375 window=1350-1380 component=emailservice template_id=28 level=INFO signal=log.count value=13 unit=count dev=+0.1 template=\\\"emailservice A request to send order confirmation email to someone@example.com has been received.\\\"\",\n    \"[metrics] id=M3313 window=1380-1410 component=emailservice signal=latency.p90 value=0.0225557 unit=s dev=+634.5 n=30\",\n    \"[metrics] id=M3314 window=1380-1410 component=emailservice signal=latency.p50 value=0.0127786 unit=s dev=+622.0 n=30\",\n    \"[metrics] id=M3315 window=1380-1410 component=emailservice signal=cpu value=19.05 unit=percent dev=+608.0 n=30\",\n    \"[traces] id=T5337 window=1380-1410 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.p99 value=8676.8 unit=us dev=+59.5 n=17\",\n    \"[traces] id=T5338 window=1380-1410 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.self_p99 value=8676.8 unit=us dev=+59.5 n=17\",\n    \"[traces] id=T5352 window=1380-1410 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=call.count value=17 unit=count dev=+1.3 n=17\",\n    \"[logs] id=L1389 window=1380-1410 component=emailservice template_id=28 level=INFO signal=log.count value=17 unit=count dev=+1.3 template=\\\"emailservice A request to send order confirmation email to someone@example.com has been received.\\\"\",\n    \"[metrics] id=M3385 window=1410-1440 component=emailservice signal=cpu value=19.79 unit=percent dev=+631.9 n=30\",\n    \"[metrics] id=M3386 window=1410-1440 component=emailservice signal=latency.p90 value=0.0220014 unit=s dev=+614.9 n=30\",\n    \"[metrics] id=M3387 window=1410-1440 component=emailservice signal=latency.p50 value=0.0103689 unit=s dev=+468.6 n=30\",\n    \"[traces] id=T5453 window=1410-1440 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.p99 value=15777.6 unit=us dev=+110.7 n=19\",\n    \"[traces] id=T5454 window=1410-1440 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=latency.self_p99 value=15777.6 unit=us dev=+110.7 n=19\",\n    \"[traces] id=T5465 window=1410-1440 edge=checkoutservice>emailservice op=SendOrderConfirmation signal=call.count value=19 unit=count dev=+1.8 n=19\",\n    \"[logs] id=L1424 window=1410-1440 component=emailservice template_id=28 level=INFO signal=log.count value=19 unit=count dev=+1.8 template=\\\"emailservice A request to send order confirmation email to someone@example.com has been received.\\\"\"\n  ]\n}"
    }
  ]
}
```

analysis:
```text
Checked 1260-1440s emailservice metrics. Sustained CPU dev=+587 to +635 confirms resource exhaustion as root cause. Trace latency spikes (up to 15ms) are propagation effects. Ranking updated to emailservice_cpu first.
```

ranking:
```json
{
  "rankings": [
    {
      "rank": 1,
      "component": "emailservice",
      "reason": "cpu"
    },
    {
      "rank": 2,
      "component": "checkoutservice",
      "reason": "latency"
    },
    {
      "rank": 3,
      "component": "emailservice",
      "reason": "latency"
    }
  ]
}
```

### Example 4

observation:
```text
{
  "tool_observations": [
    {
      "tool_call": {
        "name": "get_evidence",
        "args": {
          "start_time": 900,
          "end_time": 990,
          "components": []
        },
        "reasoning": "Completing the full telemetry range scan with the final 90-990s chunk to ensure no anomalies are missed before focusing on the top candidate."
      },
      "status": true,
      "observation": "{\n  \"telemetry\": \"evidence\",\n  \"time_unit\": \"relative_seconds_from_case_start\",\n  \"query\": {\n    \"start_time\": 900,\n    \"end_time\": 990,\n    \"components\": []\n  },\n  \"component_filter_rule\": {\n    \"metrics\": \"component matches\",\n    \"logs\": \"component matches\",\n    \"traces\": \"caller or callee matches\"\n  },\n  \"selection_policy\": \"components=[] returns metrics-only broad overview; component-filtered calls return metrics first, then traces, then logs\",\n  \"ordering\": \"window asc, modality metrics->traces->logs, abs(dev) desc within a window/modality\",\n  \"per_window_modality_limit\": 3,\n  \"latency_self_p99_definition\": \"callee span exclusive latency p99, computed as span duration minus direct child span durations\",\n  \"returned_count\": 9,\n  \"matched_count\": 223,\n  \"truncated\": false,\n  \"returned_windows\": [\n    {\n      \"start_time\": 900,\n      \"end_time\": 930\n    },\n    {\n      \"start_time\": 930,\n      \"end_time\": 960\n    },\n    {\n      \"start_time\": 960,\n      \"end_time\": 990\n    }\n  ],\n  \"next_start_time\": null,\n  \"lines\": [\n    \"[metrics] id=M2221 window=900-930 component=checkoutservice signal=mem value=238797619.2 unit=bytes dev=+1194.7 n=30\",\n    \"[metrics] id=M2222 window=900-930 component=checkoutservice signal=cpu value=19.36 unit=percent dev=+294.8 n=30\",\n    \"[metrics] id=M2223 window=900-930 component=checkoutservice signal=latency.p90 value=2.2037 unit=s dev=+142.0 n=30\",\n    \"[metrics] id=M2295 window=930-960 component=checkoutservice signal=mem value=238467891.2 unit=bytes dev=+1193.0 n=30\",\n    \"[metrics] id=M2296 window=930-960 component=checkoutservice signal=cpu value=13.44 unit=percent dev=+202.7 n=30\",\n    \"[metrics] id=M2297 window=930-960 component=checkoutservice signal=latency.p90 value=2.2016 unit=s dev=+141.9 n=30\",\n    \"[metrics] id=M2369 window=960-990 component=checkoutservice signal=mem value=243179520 unit=bytes dev=+1218.0 n=30\",\n    \"[metrics] id=M2370 window=960-990 component=checkoutservice signal=latency.p90 value=1.3463 unit=s dev=+80.9 n=30\",\n    \"[metrics] id=M2371 window=960-990 component=checkoutservice signal=cpu value=1.2323 unit=percent dev=+12.8 n=30\"\n  ]\n}"
    }
  ]
}
```

analysis:
```text
Checked 900-990s metrics. Checkoutservice shows massive memory spikes (dev=+1194-+1218) and CPU spikes (dev=+202-+294) across all windows, with latency.p90 dev=+80-+142. This confirms checkoutservice as the root cause with memory exhaustion driving latency. Ranking top1=checkoutservice_mem
```

ranking:
```json
{
  "rankings": [
    {
      "rank": 1,
      "component": "checkoutservice",
      "reason": "mem"
    },
    {
      "rank": 2,
      "component": "currencyservice",
      "reason": "latency"
    },
    {
      "rank": 3,
      "component": "shippingservice",
      "reason": "latency"
    }
  ]
}
```
