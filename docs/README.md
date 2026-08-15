# Funnel workflows — start here

The Board is first. The Board must grow.

PR 5 wrote the rest of the day (thesis draft, ideas, names, notebook). Those files assume a cooked Board is already on the local machine. That assumption failed: the Board column did not grow, fresh prints were folded onto old cards, and the 8am Hong Kong Grok pass never fired. If the list looks the same as yesterday, the pipeline is broken.

This folder is the missing first step. Specs and a runnable tool only. It does not publish the private local board.

## What to run

| When | Who | File |
| --- | --- | --- |
| Now, and every day, when a cooked Narrative docket arrives | Architect runs the tool; Macro may read the payloads | [`board-intake.md`](board-intake.md) |
| You found the old Board-to-thesis playbook | Stop. That is a later job. Do not mint a thesis here. | [`board-to-thesis.md`](board-to-thesis.md) |

A reader can:

```bash
python3 tools/board_intake.py --self-test
```

That prints new card payloads on a growing docket, and a hard fail when the Board would stay the same (reprint of the plant / July-scare / old-cards / capital-to-plants / circular-paper / power-fight / mid-August-prints set, or prints folded onto old cards).

Then point the same tool at a local docket and the current Board titles/ids. See [`board-intake.md`](board-intake.md).

## After the Board grew

Only then does the rest of the desk exist. Those later files live in PR 5 (`cursor/funnel-board-workflows-2ab1`) if they are not on this branch yet:

1. Read the grown Board and mark jobs — the second half of [`board-intake.md`](board-intake.md).
2. 8am Hong Kong: `docs/thesis-daily.md` (Macro). A thesis is a judgement. Stories stay stories.
3. If Nathan keeps: Investment Ideas, then notebook, then refine.
4. When a new Investment Idea lands: names (Micro).

Do not wait for 8am Grok to do intake. Intake is this folder. Thesis-daily is a later job and is not a working intake.

## What this folder is not

- Not a trading system. No size, no order, no ticker.
- Not a thesis mint. Do not copy a Narrative card and rename it.
- Not a publish of `/Users/max/Documents/Project Investment Thinktank/funnel/` or live `board.json` / local `index.html`.
- Not a rewrite of the public `index.html` on this repo.
