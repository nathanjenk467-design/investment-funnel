# Daily pipe — run now, and at 8am Hong Kong

Waiting for 8am is not a pipeline. `lastRunAt` being null means the pipe never ran.

This runner is the pipe. The 8am Grok Bot cron and a person at the desk invoke the **same** command. The clock does not invent a second process.

## Run it now

```bash
python3 scripts/daily_pipe.py run-now
# or
scripts/run-now
```

That is a pass/fail. It does not wait for morning.

To see that a frozen Board is a fail:

```bash
python3 scripts/daily_pipe.py run-now --frozen
```

Engine proof (frozen fail + grow + keep + pair-forks + 2–4 names):

```bash
python3 scripts/daily_pipe.py self-test
```

## The run order (hard)

1. **Board intake** — must grow or fail. Card count or identity must change. See [`board-intake.md`](board-intake.md).
2. **One thesis draft**, or a **written duplicate-stop**. See [`thesis-daily.md`](thesis-daily.md).
3. **Investment Ideas** from a keep, then from every live pair as a full fork. No keep → no ideas. A keep is not names. See [`investment-ideas.md`](investment-ideas.md).
4. **Micro names: 2–4 for every new idea.** A new Investment Idea forces names. Nathan asking is not a gate. A thesis keep is not this step. See [`names.md`](names.md).

A frozen Board is a hard fail. The runner writes `lastRunAt` on pass **and** on fail, so a null `lastRunAt` can only mean the pipe never executed.

## Live 8am (same engine)

```bash
python3 scripts/daily_pipe.py run \
  --board "$LOCAL_BOARD_JSON" \
  --handoff "$COOKED_HANDOFF_JSON" \
  --keep "$KEEP_FILE_IF_NATHAN_KEPT" \
  --last-run runs/last-run.json \
  --out runs/out \
  --trigger cron-8am-hkt
```

- `$LOCAL_BOARD_JSON` lives with the private local board. Do not copy it into this repo.
- If the handoff is empty and the Board did not change, the command exits 1 with `failReason: frozen_board`.
- Do not pass `--keep` unless Architect recorded a keep. Silence is not a keep. The runner will not mint a live `TH-*`.

The Grok Bot cron at 8am Hong Kong must **execute this command**. It must not wait, chat, or add theses by hand.

GitHub Actions also fires at `0 0 * * *` (midnight UTC = 8am HKT) and runs `self-test` plus `run-now`. That proves the engine. It does not publish the private board.

## Last-run record

Schema (see `pipe/last-run.example.json`):

| Field | Meaning |
| --- | --- |
| `lastRunAt` | Hong Kong ISO time the runner finished. `null` = never ran. |
| `timezone` | `Asia/Hong_Kong` |
| `trigger` | `run-now`, `cron-8am-hkt`, `self-test-*`, or `run` |
| `result` | `pass` or `fail` |
| `failReason` | `frozen_board` when count/identity did not change |
| `board.count` / `board.ids` / `board.fingerprint` | identity after intake |
| `stages` | intake, thesis (`draft` or `duplicate_stop`), ideas, names |

The live file is `runs/last-run.json`. That directory is gitignored. Do not commit a private board or a notebook.

Identity is card **count** plus sorted **ids** plus a fingerprint of `id` + `title`. Same count with a new id is growth. Same ids and titles is frozen.

## What this is not

- Not a publish of `/Users/max/Documents/Project Investment Thinktank/funnel/` or its `board.json`.
- Not a rewrite of `index.html`.
- Not a trading system.
- Not “names only if asked.”
