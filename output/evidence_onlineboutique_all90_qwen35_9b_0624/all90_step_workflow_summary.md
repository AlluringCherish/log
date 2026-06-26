# All-90 Per-Step Workflow Checks

## case_000001 (checkoutservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK component focus metrics->trace->log get_evidence(1080,1260,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 9: OK completed final=["checkoutservice_cpu", "currencyservice_latency", "emailservice_latency"]

## case_000002 (checkoutservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK component focus metrics->trace->log get_evidence(720,900,["checkoutservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->logs->metrics->logs->metrics->logs->metrics->logs
- step 7: OK component focus metrics->trace->log get_evidence(720,900,["checkoutservice", "currencyservice", "emailservice", "productcatalogservice", "recommendationservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->logs->metrics->logs->metrics->logs->metrics->logs
- step 8: OK completed final=["checkoutservice_cpu", "currencyservice_latency", "emailservice_mem"]

## case_000003 (checkoutservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["checkoutservice_cpu", "checkoutservice_mem", "checkoutservice_latency"]

## case_000004 (checkoutservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_latency", "checkoutservice_latency", "currencyservice_latency"]

## case_000005 (checkoutservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK completed final=["emailservice_latency", "checkoutservice_latency", "shippingservice_latency"]
- step 10: OK completed final=["emailservice_latency", "checkoutservice_latency", "shippingservice_latency"]

## case_000006 (checkoutservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["shippingservice"]) returned=36 order=metrics->logs->metrics->logs->metrics->logs->metrics->logs->metrics->logs->metrics->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["shippingservice", "checkoutservice", "paymentservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["shippingservice_latency", "checkoutservice_latency", "paymentservice_latency"]

## case_000007 (checkoutservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["checkoutservice_diskio", "emailservice_latency", "currencyservice_latency"]

## case_000008 (checkoutservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice", "emailservice", "productcatalogservice", "recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["checkoutservice_diskio", "emailservice_mem", "currencyservice_latency"]

## case_000009 (checkoutservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["checkoutservice_diskio", "currencyservice_latency", "paymentservice_latency"]

## case_000010 (checkoutservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["checkoutservice_latency", "currencyservice_latency", "emailservice_latency"]

## case_000011 (checkoutservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "checkoutservice_latency", "currencyservice_latency"]

## case_000012 (checkoutservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice", "emailservice", "productcatalogservice", "recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["checkoutservice_latency", "currencyservice_latency", "emailservice_latency"]

## case_000013 (checkoutservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["checkoutservice_mem", "currencyservice_latency", "emailservice_mem"]

## case_000014 (checkoutservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,990,[]) returned=9 order=metrics
- step 7: OK completed final=["checkoutservice_mem", "checkoutservice_cpu", "checkoutservice_latency"]
- step 8: OK completed final=["checkoutservice_mem", "checkoutservice_cpu", "checkoutservice_latency"]

## case_000015 (checkoutservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["checkoutservice_mem", "currencyservice_latency", "emailservice_mem"]

## case_000016 (checkoutservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice", "currencyservice", "emailservice", "productcatalogservice", "recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["checkoutservice_socket", "currencyservice_latency", "emailservice_mem"]

## case_000017 (checkoutservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["checkoutservice_mem", "checkoutservice_socket", "currencyservice_latency"]

## case_000018 (checkoutservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice", "currencyservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["checkoutservice_mem", "emailservice_mem", "currencyservice_mem"]

## case_000019 (currencyservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_latency", "checkoutservice_latency", "frontend_latency"]

## case_000020 (currencyservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_latency", "emailservice_mem", "cartservice_latency"]

## case_000021 (currencyservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice", "frontend", "cartservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["currencyservice_latency", "frontend_latency", "cartservice_latency"]

## case_000022 (currencyservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["currencyservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["currencyservice_latency", "checkoutservice_latency", "frontend_latency"]

## case_000023 (currencyservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["currencyservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["currencyservice_latency", "frontend_latency", "checkoutservice_latency"]

## case_000024 (currencyservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["currencyservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["currencyservice_latency", "checkoutservice_latency", "emailservice_latency"]

## case_000025 (currencyservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1080,1260,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_diskio", "currencyservice_latency", "currencyservice_mem"]

## case_000026 (currencyservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_diskio", "currencyservice_mem", "currencyservice_latency"]

## case_000027 (currencyservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1080,1260,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_diskio", "currencyservice_mem", "currencyservice_latency"]

## case_000028 (currencyservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=33 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics
- step 10: OK completed final=["currencyservice_latency", "frontend_latency", "recommendationservice_latency"]

## case_000029 (currencyservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=49 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_latency", "checkoutservice_latency", "frontend_latency"]

## case_000030 (currencyservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["checkoutservice_latency", "currencyservice_latency", "recommendationservice_latency"]

## case_000031 (currencyservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_mem", "currencyservice_latency", "recommendationservice_latency"]

## case_000032 (currencyservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice", "checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["currencyservice_mem", "currencyservice_latency", "checkoutservice_latency"]

## case_000033 (currencyservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_mem", "checkoutservice_latency", "emailservice_latency"]

## case_000034 (currencyservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_mem", "emailservice_latency", "checkoutservice_latency"]

## case_000035 (currencyservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_latency", "emailservice_mem", "checkoutservice_latency"]

## case_000036 (currencyservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["currencyservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["currencyservice_latency", "emailservice_mem", "checkoutservice_latency"]

## case_000037 (emailservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_cpu", "checkoutservice_latency", "currencyservice_latency"]

## case_000038 (emailservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_latency", "emailservice_cpu", "emailservice_mem"]

## case_000039 (emailservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "checkoutservice_latency", "currencyservice_latency"]

## case_000040 (emailservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice", "checkoutservice", "currencyservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["emailservice_latency", "checkoutservice_latency", "currencyservice_latency"]

## case_000041 (emailservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_latency", "checkoutservice_latency", "currencyservice_latency"]

## case_000042 (emailservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["checkoutservice", "currencyservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["emailservice_latency", "checkoutservice_latency", "currencyservice_latency"]

## case_000043 (emailservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_diskio", "checkoutservice_latency", "currencyservice_latency"]

## case_000044 (emailservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_diskio", "checkoutservice_latency", "currencyservice_mem"]

## case_000045 (emailservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=26 order=metrics->traces->logs->metrics->traces->logs->metrics
- step 10: OK completed final=["emailservice_diskio", "checkoutservice_latency", "currencyservice_latency"]

## case_000046 (emailservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=39 order=metrics->traces->logs->metrics->traces->logs->metrics->logs->metrics->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "checkoutservice_latency", "currencyservice_latency"]

## case_000047 (emailservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=46 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "checkoutservice_latency", "currencyservice_latency"]

## case_000048 (emailservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=44 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "checkoutservice_latency", "currencyservice_latency"]

## case_000049 (emailservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "checkoutservice_latency", "currencyservice_mem"]

## case_000050 (emailservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "checkoutservice_latency", "currencyservice_latency"]

## case_000051 (emailservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "checkoutservice_latency", "currencyservice_latency"]

## case_000052 (emailservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "currencyservice_latency", "checkoutservice_latency"]

## case_000053 (emailservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "checkoutservice_latency", "cartservice_mem"]

## case_000054 (emailservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["emailservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["emailservice_mem", "checkoutservice_latency", "currencyservice_latency"]

## case_000055 (productcatalogservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["productcatalogservice_latency", "recommendationservice_latency", "currencyservice_latency"]

## case_000056 (productcatalogservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["productcatalogservice", "recommendationservice", "checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["productcatalogservice_latency", "recommendationservice_latency", "checkoutservice_latency"]

## case_000057 (productcatalogservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["productcatalogservice_latency", "recommendationservice_latency", "checkoutservice_mem"]

## case_000058 (productcatalogservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["productcatalogservice", "recommendationservice", "frontend"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["productcatalogservice_latency", "recommendationservice_latency", "frontend_latency"]

## case_000059 (productcatalogservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["productcatalogservice", "recommendationservice", "frontend"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["productcatalogservice_latency", "recommendationservice_latency", "frontend_latency"]

## case_000060 (productcatalogservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["productcatalogservice", "recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 11: OK completed final=["productcatalogservice_latency", "recommendationservice_latency", "emailservice_mem"]

## case_000061 (productcatalogservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["productcatalogservice_diskio", "recommendationservice_latency", "emailservice_mem"]

## case_000062 (productcatalogservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["productcatalogservice_diskio", "checkoutservice_latency", "currencyservice_latency"]

## case_000063 (productcatalogservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["productcatalogservice_diskio", "recommendationservice_latency", "checkoutservice_latency"]

## case_000064 (productcatalogservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->logs->metrics->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->logs
- step 10: OK completed final=["productcatalogservice_latency", "recommendationservice_latency", "currencyservice_latency"]

## case_000065 (productcatalogservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["productcatalogservice"]) returned=43 order=metrics->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["productcatalogservice", "recommendationservice", "checkoutservice"]) returned=51 order=metrics->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["productcatalogservice_latency", "recommendationservice_latency", "checkoutservice_latency"]

## case_000066 (productcatalogservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["productcatalogservice"]) returned=39 order=metrics->traces->metrics->traces->logs->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["recommendationservice_latency", "productcatalogservice_latency", "checkoutservice_latency"]

## case_000067 (productcatalogservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: WARN component focus metrics-first but trace/log missing get_evidence(1080,1260,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 9: OK completed final=["productcatalogservice_latency", "recommendationservice_latency", "checkoutservice_latency"]

## case_000068 (productcatalogservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["productcatalogservice_latency", "checkoutservice_latency", "currencyservice_socket"]

## case_000069 (productcatalogservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=48 order=metrics->traces->logs->metrics->logs->metrics->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice", "productcatalogservice"]) returned=48 order=metrics->traces->logs->metrics->logs->metrics->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["recommendationservice_latency", "productcatalogservice_latency", "currencyservice_latency"]

## case_000070 (productcatalogservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["productcatalogservice_latency", "recommendationservice_latency", "checkoutservice_latency"]

## case_000071 (productcatalogservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: WARN component focus metrics-first but trace/log missing get_evidence(1080,1260,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 9: OK completed final=["productcatalogservice_mem", "recommendationservice_latency", "currencyservice_latency"]

## case_000072 (productcatalogservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: WARN component focus metrics-first but trace/log missing get_evidence(1260,1440,["productcatalogservice"]) returned=36 order=metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces->metrics->traces
- step 10: OK completed final=["productcatalogservice_mem", "productcatalogservice_socket", "emailservice_mem"]

## case_000073 (recommendationservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_latency", "currencyservice_latency", "emailservice_mem"]

## case_000074 (recommendationservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_latency", "recommendationservice_mem", "currencyservice_latency"]

## case_000075 (recommendationservice_cpu)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_latency"]

## case_000076 (recommendationservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice", "frontend", "checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["recommendationservice_latency", "frontend_latency", "checkoutservice_latency"]

## case_000077 (recommendationservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_latency", "frontend_latency", "emailservice_latency"]

## case_000078 (recommendationservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_latency", "currencyservice_latency", "emailservice_mem"]

## case_000079 (recommendationservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_diskio", "currencyservice_latency", "frontend_latency"]

## case_000080 (recommendationservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK component focus metrics->trace->log get_evidence(1080,1260,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 9: OK completed final=["recommendationservice_diskio", "recommendationservice_mem", "recommendationservice_latency"]

## case_000081 (recommendationservice_diskio)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_diskio", "recommendationservice_mem", "recommendationservice_latency"]

## case_000082 (recommendationservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=23 order=metrics->traces->logs
- step 10: OK completed final=["recommendationservice_mem", "emailservice_mem", "frontend_socket"]

## case_000083 (recommendationservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=48 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics
- step 10: OK completed final=["recommendationservice_latency", "checkoutservice_latency", "currencyservice_latency"]

## case_000084 (recommendationservice_latency)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_latency", "recommendationservice_diskio", "recommendationservice_mem"]

## case_000085 (recommendationservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=42 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_latency", "emailservice_socket", "checkoutservice_socket"]

## case_000086 (recommendationservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_latency", "recommendationservice_mem", "currencyservice_latency"]

## case_000087 (recommendationservice_mem)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice", "currencyservice", "emailservice", "productcatalogservice", "checkoutservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["recommendationservice_latency", "recommendationservice_mem", "recommendationservice_diskio"]

## case_000088 (recommendationservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=29 order=metrics->traces->metrics->traces->logs->metrics->traces->logs
- step 10: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice", "productcatalogservice"]) returned=32 order=metrics->traces->metrics->traces->metrics->traces->logs->metrics->traces->logs
- step 11: OK completed final=["recommendationservice_latency", "recommendationservice_mem", "frontend_latency"]

## case_000089 (recommendationservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_mem", "currencyservice_latency", "emailservice_mem"]

## case_000090 (recommendationservice_socket)
- step 1: OK metrics-only broad scan get_evidence(0,180,[]) returned=18 order=metrics
- step 2: OK metrics-only broad scan get_evidence(180,360,[]) returned=18 order=metrics
- step 3: OK metrics-only broad scan get_evidence(360,540,[]) returned=18 order=metrics
- step 4: OK metrics-only broad scan get_evidence(540,720,[]) returned=18 order=metrics
- step 5: OK metrics-only broad scan get_evidence(720,900,[]) returned=18 order=metrics
- step 6: OK metrics-only broad scan get_evidence(900,1080,[]) returned=18 order=metrics
- step 7: OK metrics-only broad scan get_evidence(1080,1260,[]) returned=18 order=metrics
- step 8: OK metrics-only broad scan get_evidence(1260,1440,[]) returned=18 order=metrics
- step 9: OK component focus metrics->trace->log get_evidence(1260,1440,["recommendationservice"]) returned=54 order=metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs->metrics->traces->logs
- step 10: OK completed final=["recommendationservice_mem", "recommendationservice_socket", "recommendationservice_latency"]
