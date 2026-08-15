# Board intake — Board first, Board must grow

Run **now**, and every day, when a cooked Narrative docket arrives.

This is the missing first step. It is not a thesis pass. It is not the 8am Hong Kong Grok routine. That routine has never fired and is not a working intake.

---

## What failed

The Board column on the local Funnel did not grow. Fresh prints were folded onto old cards. The list looked the same as yesterday.

Nathan’s rule: if the list looks the same as yesterday, the pipeline is broken.

A reprint of this set is a **failed run**, not a success:

- plant
- July-scare
- old-cards
- capital-to-plants
- circular-paper
- power-fight
- mid-August-prints

---

## What this step is

**Input**

1. A cooked Narrative docket: kept situations, open calls, housed stories (and, if present, observations and fresh prints).
2. The current Board card titles and ids. Not the private board files themselves.

**Output**

- New Board card **payloads** for situations that are not already on the Board.
- Optional update notes when a fresh print belongs on an old card.

A new situation **must** become a new card. A fresh print **may** update an old card. Those are not the same job.

**Hard fail**

The run fails if it produces zero new Board cards. Updates-only is a fail. A reprint of the frozen set is a fail. Quiet success with yesterday’s list is a bug.

Stories stay stories. Do not mint a thesis here.

---

## What this step is not

- Not a live pull of Narrative. The docket is already cooked. If it is not cooked, Architect cooks it, then runs this file.
- Not a wait for 8am Grok. Do not sit on a calendar for intake.
- Not a thesis draft, a keep, an Investment Idea, or a name.
- Not a copy of a Narrative card with a new label.
- Not a trading system. No ticker, no size, no order.
- Not a publish of `/Users/max/Documents/Project Investment Thinktank/funnel/` or live `board.json` / local `index.html`.
- Not a mint of a new Board card only because a print agreed with a situation already there.

---

## Who does what

**Architect** runs the tool. Architect writes accepted new cards onto the **local** board only. Architect assigns the live id there. Never publish those files here.

**Macro** may read the new payloads and the grown Board. Macro does not add a Board card “because a print agreed.” Macro does not mint a thesis in this step.

**Micro** does not touch the Board.

---

## Identity (why the Board froze)

Folding used soft sameness: shared newspaper words, “this week,” the same plant. That is how a new situation disappeared into an old card.

This pipeline uses **strict identity** to fold, and a **named frozen set** to fail a reprint.

A docket item updates an old card only when one of these is true:

1. It names the existing Board id (`updates_board_id` / `existing_board_id` / the same `id`).
2. Its title matches a current Board title after ordinary normalisation (case, punctuation, spacing).
3. It carries a `situation_key` that an existing Board card already carries.

Shared words are not identity. “Plant,” “power,” “AI,” or “this week” is not a match.

A docket item is a **reprint of the frozen set** (never a new card) when its `situation_key` is one of the seven names above, or its title is that old card (or that old card plus a suffix such as “updated” / “this week”).

If a fresh print does not meet strict identity, it is not a print. It is a new situation. Write a new card.

---

## Card shape (Board, not thesis)

A new payload is a Board item. Allow only:

| Field | On |
| --- | --- |
| `proposed_id` | `PROPOSED-*`. Not live. Architect assigns the real id on the local board. |
| `kind` | `board_card`, `prediction`, or `observation` — from the docket kind. Never `thesis`. |
| `title` | The argument a person would say out loud. |
| `story` | The housed account. |
| `force` | What makes this situation this situation. Required on a kept situation. |
| `from` | Where the cooked docket got it. |
| `from_docket` | Docket id, so the handoff is traceable. |
| `situation_key` | Stable slug if the docket had one. |
| `lifecycle_on_board` | `emerging` on a new card. |
| Prediction-only | `call`, `wrong_if`, `call_by` if the docket already had them. |

Strip everything else. No `claim`, no clock, no “what would make this false,” no priced line, no desk, no ticker, no `TH-*`.

| Docket kind | Board kind |
| --- | --- |
| `kept_situation` | `board_card` |
| `housed_story` | `board_card` |
| `open_call` | `prediction` (still a Board item, not a thesis) |
| `observation` | `observation` |
| `fresh_print` that failed identity | `board_card` |

A housed story stays a housed story. An open call stays an open call. Neither is a thesis.

---

## How to run

The tool is `tools/board_intake.py`. No extra packages. Python 3.

Prove the contract (new payloads, and a hard fail when the Board would stay the same):

```bash
python3 tools/board_intake.py --self-test
```

Run a real handoff. Keep the docket and the Board snapshot **on the local machine**. Do not commit them here.

```bash
python3 tools/board_intake.py \
  --docket /path/to/local/narrative-docket.json \
  --board  /path/to/local/board-titles.json
```

`--board` may be a slim titles/ids file, or a house walk that already has a `board` array (for example the public `first-walk.json` on this repo). The tool reads **id and title only**. It does not write the local board.

Write the machine payload somewhere local:

```bash
python3 tools/board_intake.py \
  --docket /path/to/local/narrative-docket.json \
  --board  /path/to/local/board-titles.json \
  --out    /tmp/board-intake.json
```

Exit `0` only when at least one new Board card was produced. Exit `2` when the Board would stay the same. Exit `1` on a bad file or a bad flag.

### Docket file

```json
{
  "as_of": "2026-08-16",
  "items": [
    {
      "docket_id": "N-01",
      "kind": "kept_situation",
      "title": "…",
      "story": "…",
      "force": "…",
      "from": "…",
      "situation_key": "optional-slug",
      "updates_board_id": null
    }
  ]
}
```

`kind` is one of: `kept_situation`, `open_call`, `housed_story`, `observation`, `fresh_print`.

A board-shaped file with a `board` array is also accepted as a docket (each Board item becomes a docket item). Feeding yesterday’s Board back in is how you prove the fail: zero new cards.

### Board file

```json
{
  "cards": [
    { "id": "15", "title": "AI chip factories are still dramatically under-built" }
  ]
}
```

`board` (house-walk shape) or a bare list of `{id, title}` is also accepted. Optional `situation_key` on a card tightens identity. Titles and ids are enough.

Method fixtures (not a live board, not a publish):

- `tools/fixtures/board-titles.json`
- `tools/fixtures/docket-new-situation.json` — grows
- `tools/fixtures/docket-mixed.json` — one new card plus updates
- `tools/fixtures/docket-reprint-frozen.json` — hard fail
- `tools/fixtures/docket-prints-only.json` — hard fail

---

## After the Board grew

Architect puts accepted `PROPOSED-*` payloads on the **local** Board with real ids. Then, and only then, read the grown Board.

For each Board item, mark one job in words. Not a score. Do not draft in this file.

| Job | Meaning | What happens next |
| --- | --- | --- |
| **Already a live theme** | Same force as a kept thesis | Sit the print on that thesis. Not a new thesis. |
| **Candidate judgement** | Might be one forward-looking call | Later: thesis-daily (PR 5). Not this step. |
| **Story / observation** | True enough to house; not a call | Stays on the Board |
| **Fight** | The problem is agreed; the path is not | Stays a fight. Do not resolve it here. |
| **Neighbor** | Near a candidate; a different print would make it false | Write it down so you do not join it later |
| **Noise** | Tape wiggle, slogan, reprint | Leave it |

If nothing is a candidate judgement, say so in the day’s notes. The later thesis pass still owes a written duplicate-stop. That is not this file’s job, and it does not turn a frozen Board into a successful intake.

---

## Failure modes (check these)

1. **Zero new cards.** The Board would look the same as yesterday. Fail. Do not call updates a success.
2. **Reprint of the frozen set.** plant / July-scare / old-cards / capital-to-plants / circular-paper / power-fight / mid-August-prints. Fail.
3. **Folding a new situation onto an old card** because they share a week or a word.
4. **Waiting for 8am Grok** instead of running this tool.
5. **Copying a Narrative card** and renaming it a Board card or a thesis.
6. **Minting a thesis** (clock, priced, `TH-*`, Investment Idea, name).
7. **Publishing** the local board or pasting live `board.json` into this repo.
8. **A ticker** in the output.
