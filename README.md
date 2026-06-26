# Reasoner-Controller RCA Agent

This is an independent test harness inspired by OpenRCA's RCA-Agent structure, adapted for local Online Boutique data. The current runtime removes the code-writing Executor path and lets the Controller call deterministic KG tools directly.

## Structure

- `Reasoner/`: analyzes KG tool observations and maintains diagnostic results only.
- `Controller/`: chooses one or more KG tool calls, or terminates the diagnosis.
- `Tools/`: loads the service dependency graph, attaches case telemetry summaries, and executes KG tools.
- `Executor/`: legacy code-writing executor, no longer used by `Main.py`.
- `Benchmarks/`: loads cases and evaluates `service_metric` rankings.
- `Main.py`: CLI entrypoint.

## Run with local Qwen3-8B

The default backend is the local Qwen3-8B model at `/data/models/Qwen3-8B`.

Create the anonymized benchmark copy first. The copied case directories are stored
under `cases/` as `case_000001`, `case_000002`, ... and the internal answer map is
stored in `problem.json` at the anonymized benchmark root.

```bash
python3 Benchmarks/anonymize_benchmark.py \
  --source-root Benchmarks/RE2-OB \
  --target-root Benchmarks/OnlineBoutique \
  --overwrite
```

```bash
python3 Main.py --data-root Benchmarks/OnlineBoutique --case-limit 1 --max-steps 3
```

Equivalent explicit command:

```bash
python3 Main.py \
  --llm-backend local \
  --local-model /data/models/Qwen3-8B \
  --data-root Benchmarks/OnlineBoutique \
  --case-limit 1 \
  --max-steps 3
```

Outputs are written under `output/`.

The Controller may issue multiple tool calls in one step. If any tool call fails because of an invalid tool name or arguments, the failed observation is fed back to the Controller and the same step is retried with corrected tool calls before the Reasoner receives the final observation bundle.

## Run with OpenAI-compatible endpoint

```bash
export OPENAI_API_KEY=...
export OPENAI_MODEL=...
# optional
export OPENAI_BASE_URL=...
```

```bash
python3 Main.py --llm-backend openai --data-root Benchmarks/OnlineBoutique --case-limit 1 --max-steps 3
```
