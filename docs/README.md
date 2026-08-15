# Funnel workflows — which to run when

These files are the desk. They are how Macro and the Investment Architect run Nathan’s Funnel board without re-deriving the 15 August 2026 session.

This is not a UI rewrite. This is not a publish of the live local board. Do not copy the private board files into this repo.

## Tomorrow morning (16 Aug 2026, Hong Kong)

Architect talks to Nathan. Macro is silent toward Nathan.

1. Open [`standing-rules.md`](standing-rules.md) if anyone is new to the desk. Otherwise skip; the rules are always on.
2. Architect: confirm the cooked Board is on the local board. Run [`board-intake.md`](board-intake.md).
3. Macro, 8am Hong Kong: run [`thesis-daily.md`](thesis-daily.md) once. End with a keep/fold offer **or** a written duplicate-stop.
4. If Nathan keeps (Architect tells Macro): run [`investment-ideas.md`](investment-ideas.md), then [`notebook.md`](notebook.md), then Macro owns [`refine.md`](refine.md) on that card.
5. If Nathan folds, parks, or sits: run [`notebook.md`](notebook.md) only. Do not write ideas. Do not write names (a keep never happened, so no idea landed).
6. When a new Investment Idea lands: Micro runs [`names.md`](names.md). **2–4 discussable names** on the Candidates tab for that idea. A sit-off idea still gets stay-off names. An honest empty needs a why. A thesis keep by itself is not this step.

That is a complete day. Sitting with a written stop is a complete day.

## Which file to open

| When | Who | File |
| --- | --- | --- |
| Always | Everyone | [`standing-rules.md`](standing-rules.md) |
| Board arrives, or the day starts | Architect reads; Macro reads | [`board-intake.md`](board-intake.md) |
| 8am Hong Kong, all seven days | Macro | [`thesis-daily.md`](thesis-daily.md) |
| Nathan just kept a thesis | Macro | [`investment-ideas.md`](investment-ideas.md) |
| A new Investment Idea just landed | Micro | [`names.md`](names.md) |
| The world moved against a live thesis | Macro | [`refine.md`](refine.md) |
| After any keep, fold, park, sit, or duplicate-stop | Macro writes; Architect stores locally | [`notebook.md`](notebook.md) |
| You found the old Board-to-thesis playbook | Stop; use this index | [`board-to-thesis.md`](board-to-thesis.md) |

Sibling specs (other jobs, not this run):

- `docs/macro-daily-pack.md` (PR 2, if present) — the daily tape look. Do not run it inside thesis creation.
- `docs/fundamental-momentum.md` (PR 3, if present) — the name screen. Use when a new Investment Idea has landed (see [`names.md`](names.md)).

## Why this split

The 15 August session listed objects: Board, Thesis, Investment Ideas, notebook, roles. A desk does not run by object name. It runs by **when** and **who**.

So the files follow the day:

- **Standing rules** are always on, so the other files stay short.
- **Board intake** is a read of a cooked handoff, not a live pull and not a thesis.
- **Thesis daily** is the 8am job: one judgement, board-measure, tension, keep/fold, or a written stop.
- **Investment Ideas** fire only after a keep, from that thesis alone and then from every live pair as a full fork. They are not names.
- **Refine** is ownership of a kept card when the world moves. It is not a second mint.
- **Notebook** is memory in Nathan’s words. Later drafts read it first.
- **Names** fire when a new Investment Idea lands. Micro only. 2–4 discussable names, or an honest empty with a why. A thesis keep is not the trigger.

That is a better split than cloning the session’s object list. The session is evidence. The day is the run.

## What a reader can run

Board intake → thesis draft → board-measure → tension → keep/fold → daily mint or duplicate-stop → Investment Ideas from one thesis and from pair-forks → **names (2–4 per new idea)** → refine → notebook.

The pair/fork rule lives in [`investment-ideas.md`](investment-ideas.md). It uses the 15 August TH-01 × TH-02 example (plants stay scarce vs circular funding will not hold; factory paid or unpaid × paper holds or breaks). It does not dump the live board.

## What this set is not

- Not a trading system. No size, no order, no entry recipe.
- Not a copy of a Narrative card with a new label.
- Not a publish of `/Users/max/Documents/Project Investment Thinktank/funnel/index.html` or its `board.json`.
- Not a rewrite of the public `index.html` on this repo.
