# Funnel workflows — which to run when

These files are the desk. They are how Macro and the Investment Architect run Nathan’s Funnel board without re-deriving the 15 August 2026 session.

This is not a UI rewrite. This is not a publish of the live local board. Do not copy the private board files into this repo.

## Run the pipe now

Waiting for 8am is not a pipeline. `lastRunAt` being null means it never ran.

```bash
python3 scripts/daily_pipe.py run-now
python3 scripts/daily_pipe.py run-now --frozen
python3 scripts/daily_pipe.py self-test
```

Same engine at 8am Hong Kong (Grok Bot cron and GitHub `0 0 * * *` UTC). See [`daily-pipe.md`](daily-pipe.md).

**Hard order:** Board intake (must grow or fail) → one thesis draft or a written duplicate-stop → Investment Ideas from a keep and from pair-forks → Micro names (2–4) for every new idea.

A frozen Board (card count/identity unchanged) is a fail. A new Investment Idea **forces** 2–4 names. A thesis keep is not names. Nathan asking is not a gate.

## Tomorrow morning (Hong Kong)

Architect talks to Nathan. Macro is silent toward Nathan.

1. Open [`standing-rules.md`](standing-rules.md) if anyone is new to the desk. Otherwise skip; the rules are always on.
2. Architect: put the cooked handoff where the runner can read it. Run [`board-intake.md`](board-intake.md) via the pipe. Intake must grow or the day fails.
3. Macro, 8am Hong Kong **or now**: the pipe runs [`thesis-daily.md`](thesis-daily.md) once. End with a keep/fold offer **or** a written duplicate-stop.
4. If Nathan keeps (Architect tells Macro, keep file present): the pipe runs [`investment-ideas.md`](investment-ideas.md), then [`notebook.md`](notebook.md), then Macro owns [`refine.md`](refine.md) on that card.
5. If Nathan folds, parks, or sits: run [`notebook.md`](notebook.md) only. Do not write ideas. Do not write names (a keep never happened, so no idea landed).
6. When a new Investment Idea lands: the pipe runs [`names.md`](names.md). **2–4 discussable names** on the Candidates tab for that idea. A sit-off idea still gets stay-off names. An honest empty needs a why. A thesis keep by itself is not this step. Do not wait to be asked.

That is a complete day. Sitting with a written stop is a complete day. Adding theses and names by hand in chat is not a run.

## Which file to open

| When | Who | File |
| --- | --- | --- |
| Prove the pipe / 8am clock | Runner | [`daily-pipe.md`](daily-pipe.md) |
| Always | Everyone | [`standing-rules.md`](standing-rules.md) |
| Board arrives, or the day starts | Architect reads; Macro reads; runner enforces grow-or-fail | [`board-intake.md`](board-intake.md) |
| 8am Hong Kong **or run-now**, all seven days | Macro / runner | [`thesis-daily.md`](thesis-daily.md) |
| Nathan just kept a thesis | Macro | [`investment-ideas.md`](investment-ideas.md) |
| A new Investment Idea just landed | Micro — forced, not asked | [`names.md`](names.md) |
| The world moved against a live thesis | Macro | [`refine.md`](refine.md) |
| After any keep, fold, park, sit, or duplicate-stop | Macro writes; Architect stores locally | [`notebook.md`](notebook.md) |
| You found the old Board-to-thesis playbook | Stop; use this index | [`board-to-thesis.md`](board-to-thesis.md) |

Sibling specs (other jobs, not this run):

- `docs/macro-daily-pack.md` (PR 2, if present) — the daily tape look. Do not run it inside thesis creation.
- `docs/fundamental-momentum.md` (PR 3, if present) — the name screen. Use when a new Investment Idea has landed (see [`names.md`](names.md)).

## Why this split

The 15 August session listed objects: Board, Thesis, Investment Ideas, notebook, roles. A desk does not run by object name. It runs by **when** and **who**.

So the files follow the day:

- **Daily pipe** is the executable. Run-now and 8am are the same order.
- **Standing rules** are always on, so the other files stay short.
- **Board intake** is a read of a cooked handoff, not a live pull and not a thesis. It must change card count or identity or the pipe fails.
- **Thesis daily** is the judgement job: one judgement, board-measure, tension, keep/fold, or a written stop. The clock invokes it; it does not wait for the clock.
- **Investment Ideas** fire only after a keep, from that thesis alone and then from every live pair as a full fork. They are not names.
- **Refine** is ownership of a kept card when the world moves. It is not a second mint.
- **Notebook** is memory in Nathan’s words. Later drafts read it first.
- **Names** fire when a new Investment Idea lands. Micro only. 2–4 discussable names, or an honest empty with a why. A thesis keep is not the trigger. “Names only if asked” is retired.

That is a better split than cloning the session’s object list. The session is evidence. The day is the run.

## What a reader can run

Board intake (must grow or fail) → thesis draft → board-measure → tension → keep/fold → daily mint or duplicate-stop → Investment Ideas from one thesis and from pair-forks → **names (2–4 per new idea, forced)** → refine → notebook.

The pair/fork rule lives in [`investment-ideas.md`](investment-ideas.md). It uses the 15 August TH-01 × TH-02 example (plants stay scarce vs circular funding will not hold; factory paid or unpaid × paper holds or breaks). It does not dump the live board.

## What this set is not

- Not a trading system. No size, no order, no entry recipe.
- Not a copy of a Narrative card with a new label.
- Not a publish of `/Users/max/Documents/Project Investment Thinktank/funnel/index.html` or its `board.json`.
- Not a rewrite of the public `index.html` on this repo.
- Not “wait for 8am and then chat.”
