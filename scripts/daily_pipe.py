#!/usr/bin/env python3
"""Daily investment pipe — run now, or on the 8am Hong Kong clock.

Waiting for 8am is not a pipeline. This runner is.

Order (hard):
  1. Board intake — must grow or fail
  2. One thesis draft, or a written duplicate-stop
  3. Investment Ideas from a keep and from pair-forks (if a keep is present)
  4. Micro names: 2–4 for every new idea (a keep is not names)

A frozen Board (card count/identity unchanged) is a hard fail.
Does not publish the private local board. Specs and scripts only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

HKT = timezone(timedelta(hours=8))
ROOT = Path(__file__).resolve().parents[1]
PIPE_DIR = ROOT / "pipe"
FIXTURES = PIPE_DIR / "fixtures"
DEFAULT_LAST_RUN = ROOT / "runs" / "last-run.json"
DEFAULT_OUT = ROOT / "runs" / "out"

FROZEN = "frozen_board"
MISSING_NAMES = "new_idea_missing_names"
NO_THESIS_OUTPUT = "no_draft_or_duplicate_stop"


class PipeFail(Exception):
    def __init__(self, reason: str, message: str):
        super().__init__(message)
        self.reason = reason
        self.message = message


def now_hkt() -> datetime:
    return datetime.now(HKT)


def iso_hkt(dt: datetime | None = None) -> str:
    stamp = dt or now_hkt()
    return stamp.isoformat(timespec="seconds")


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def board_cards(data: dict) -> list[dict]:
    cards = data.get("board") or []
    return [c for c in cards if isinstance(c, dict) and c.get("id")]


def live_theses(data: dict) -> list[dict]:
    theses = data.get("theses") or data.get("theses_6_12") or []
    out = []
    for t in theses:
        if not isinstance(t, dict) or not t.get("id"):
            continue
        if t.get("lifecycle", "live") == "live":
            out.append(t)
    return out


def board_identity(data: dict) -> dict:
    cards = board_cards(data)
    rows = []
    for card in sorted(cards, key=lambda c: str(c["id"])):
        rows.append(f"{card['id']}\t{card.get('title', '')}")
    fingerprint = hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()[:16]
    ids = sorted(str(c["id"]) for c in cards)
    return {"count": len(cards), "ids": ids, "fingerprint": fingerprint}


def identities_equal(a: dict | None, b: dict | None) -> bool:
    if a is None or b is None:
        return False
    return (
        a.get("count") == b.get("count")
        and a.get("ids") == b.get("ids")
        and a.get("fingerprint") == b.get("fingerprint")
    )


def load_handoff(path: Path | None) -> list[dict]:
    if path is None or not path.exists():
        return []
    data = load_json(path)
    if isinstance(data, list):
        return [c for c in data if isinstance(c, dict) and c.get("id")]
    cards = data.get("cards") or data.get("board") or []
    return [c for c in cards if isinstance(c, dict) and c.get("id")]


def load_inbox(inbox: Path | None) -> list[dict]:
    if inbox is None or not inbox.is_dir():
        return []
    cards: list[dict] = []
    for path in sorted(inbox.glob("*.json")):
        cards.extend(load_handoff(path))
    return cards


def intake(board: dict, handoff: list[dict], last_identity: dict | None) -> dict:
    """Merge cooked handoff cards. Board must grow or this is a hard fail."""
    before = board_identity(board)
    existing = {str(c["id"]): i for i, c in enumerate(board_cards(board))}
    added: list[str] = []
    updated: list[str] = []

    if "board" not in board or not isinstance(board["board"], list):
        board["board"] = list(board_cards(board))

    for card in handoff:
        cid = str(card["id"])
        if cid not in existing:
            board["board"].append(deepcopy(card))
            existing[cid] = len(board["board"]) - 1
            added.append(cid)
            continue
        idx = existing[cid]
        prev = board["board"][idx]
        merged = deepcopy(prev)
        merged.update(deepcopy(card))
        if merged.get("title") != prev.get("title") or merged.get("story") != prev.get("story"):
            board["board"][idx] = merged
            updated.append(cid)

    after = board_identity(board)
    if identities_equal(before, after):
        raise PipeFail(
            FROZEN,
            "Board intake did not grow: card count/identity unchanged. "
            f"count={after['count']} ids={after['ids']} fingerprint={after['fingerprint']}. "
            "A frozen Board is a fail. Waiting for 8am is not intake.",
        )
    if last_identity and identities_equal(after, last_identity):
        raise PipeFail(
            FROZEN,
            "Board identity matches last run. Intake must change count or identity.",
        )
    return {
        "before": before,
        "after": after,
        "added": added,
        "updated": updated,
        "jobs": [
            {
                "id": str(c["id"]),
                "job": c.get("job") or "story_observation",
                "title": c.get("title", ""),
            }
            for c in board_cards(board)
        ],
    }


def _measure_card(card: dict, draft_from: set[str]) -> str:
    cid = str(card["id"])
    if cid in draft_from:
        return "strengthens"
    job = card.get("job") or ""
    if job == "fight" or "fight" in (card.get("tags") or []):
        return "weakens"
    if job == "already_a_live_theme":
        return "different_flavor"
    return "leave_it_alone"


def write_draft(board: dict, candidate: dict, run_at: str) -> dict:
    from_ids = [str(candidate["id"])]
    from_set = set(from_ids)
    live = live_theses(board)
    measures = []
    for card in board_cards(board):
        mark = _measure_card(card, from_set)
        measures.append({"id": str(card["id"]), "mark": mark, "title": card.get("title", "")})
    tensions = []
    if not live:
        tensions.append("no live thesis to tension against")
    for th in live:
        tensions.append(
            f"We notice the tension with {th['id']}. They may or may not contradict. "
            "We think this is a different call, not a cousin of that card."
        )
    left = [m["id"] for m in measures if m["id"] not in from_set]
    return {
        "id": "DRAFT-PIPE-1",
        "kind": "thesis_draft",
        "live": False,
        "judgement": (
            f"{candidate.get('title', 'A new call')}: "
            f"{candidate.get('force') or candidate.get('story') or 'a forward-looking call'}."
        ),
        "what_it_is_not": (
            "Not a mechanism. Not a fact. Not a copy of a Board story with a new label. "
            "Not a name. Not an Investment Idea."
        ),
        "from_board": from_ids,
        "left_on_the_board": left,
        "board_measure": measures,
        "tension_notes": tensions,
        "clock": "6-12 months",
        "what_would_make_this_false": (
            "A world print that the model and the payment have already joined up "
            "on yesterday's rails, with no new winner."
        ),
        "what_is_not_a_reason_to_fold": (
            "A scare in the shares. A podcast. A cousin headline."
        ),
        "already_in_the_price_or_not_checked": "not checked",
        "objection": (
            "The obvious rails may absorb the traffic. Then this is a story, not a call."
        ),
        "notebook": "notebook empty or not published",
        "asked_of_nathan": "keep / fold / park / sit / join to an existing theme",
        "written_at": run_at,
    }


def write_duplicate_stop(board: dict, run_at: str) -> dict:
    ids = [str(c["id"]) for c in board_cards(board)]
    th_ids = [str(t["id"]) for t in live_theses(board)]
    return {
        "kind": "duplicate_stop",
        "sentence": (
            "Another card would only duplicate a narrative already on the Board or in a live thesis."
        ),
        "would_duplicate_board": ids,
        "would_duplicate_theses": th_ids,
        "written_at": run_at,
        "timezone": "Asia/Hong_Kong",
    }


def thesis_stage(board: dict, intake_result: dict, run_at: str) -> dict:
    added = set(intake_result.get("added") or [])
    candidates = [
        c
        for c in board_cards(board)
        if str(c["id"]) in added and c.get("job") == "candidate_judgement"
    ]
    if candidates:
        draft = write_draft(board, candidates[0], run_at)
        return {"kind": "draft", "draft": draft, "duplicate_stop": None}
    stop = write_duplicate_stop(board, run_at)
    return {"kind": "duplicate_stop", "draft": None, "duplicate_stop": stop}


def _sit_from_thesis(th: dict) -> str:
    title = th.get("title") or th.get("claim") or th["id"]
    return f"Sit with the shape of {title}, not the famous shortcut name."


def alone_idea(kept: dict) -> dict:
    kid = kept["id"]
    return {
        "id": "IDEA-PIPE-ALONE",
        "kind": "investment_idea",
        "parents": [kid],
        "branch": None,
        "sit": _sit_from_thesis(kept),
        "sit_off": False,
        "what_it_is_not": (
            "Not a stock. Not a buy. Not a ticker. Not the next model. "
            "Not the famous name everyone already uses as a shortcut."
        ),
        "what_has_to_stay_true": kept.get("claim") or kept.get("judgement") or kept.get("title"),
        "how_this_sit_can_be_false_even_if_thesis_true": (
            "The landlord does not get paid. The surplus stays with the customer. "
            "The queue is mostly phantom."
        ),
        "clock": kept.get("clock") or "6-12 months",
        "already_in_the_price_or_not_checked": "not checked",
    }


def pair_fork(kept: dict, other: dict) -> list[dict]:
    """Every live branch of a fighting pair. Do not pick a winner."""
    a, b = kept["id"], other["id"]
    branches = [
        ("A", f"{a} holds, {b} holds", "both hold", "leave it"),
        ("B", f"{a} holds, {b} fails", f"{a} holds and {b} does not", "force a look at the other thesis"),
        ("C", f"{a} fails, {b} holds", f"{b} holds and {a} does not", "force a look at the kept thesis"),
        ("D", f"{a} fails, {b} fails", "both fail", "sit in tension; they may or may not contradict"),
    ]
    ideas = []
    for letter, cell, sit, effect in branches:
        ideas.append(
            {
                "id": f"IDEA-PIPE-{a}-{b}-{letter}",
                "kind": "investment_idea",
                "parents": [a, b],
                "branch": cell,
                "sit": f"Sit for this branch only: {sit}.",
                "sit_off": letter in {"C", "D"},
                "what_it_is_not": (
                    "Not the sit that assumes the other branch. Not a winner. Not a ticker."
                ),
                "what_has_to_stay_true": cell,
                "what_would_make_this_branch_false": f"A world print that {cell} is not the world.",
                "what_this_branch_does_to_the_other_thesis": effect,
                "already_in_the_price_or_not_checked": "not checked",
            }
        )
    return ideas


def ideas_stage(board: dict, thesis_result: dict, keep: dict | None) -> dict:
    if not keep or not keep.get("kept"):
        return {
            "skipped": True,
            "why": "No keep. A draft or duplicate-stop is not a keep. Silence is not a keep.",
            "ideas": [],
        }
    draft = thesis_result.get("draft")
    if keep.get("fixture") and draft:
        kept = {
            "id": keep.get("draft_id") or draft["id"],
            "title": draft.get("judgement"),
            "claim": draft.get("judgement"),
            "clock": draft.get("clock"),
            "fixture_keep": True,
        }
    elif keep.get("thesis_id"):
        found = next((t for t in live_theses(board) if t["id"] == keep["thesis_id"]), None)
        if not found:
            raise PipeFail("keep_missing_thesis", f"Keep names {keep['thesis_id']} but that thesis is not live.")
        kept = found
    elif draft:
        kept = {
            "id": draft["id"],
            "title": draft.get("judgement"),
            "claim": draft.get("judgement"),
            "clock": draft.get("clock"),
        }
    else:
        return {
            "skipped": True,
            "why": "Keep present but no draft and no live thesis_id. Cannot write ideas from a stop.",
            "ideas": [],
        }

    ideas = [alone_idea(kept)]
    others = [t for t in live_theses(board) if t["id"] != kept["id"]]
    if not others:
        pair_note = "no pair yet"
    else:
        pair_note = f"{len(others)} pair(s); every live branch written; no winner picked"
        for other in others:
            ideas.extend(pair_fork(kept, other))
    return {"skipped": False, "why": None, "kept": kept, "pair_note": pair_note, "ideas": ideas}


def _name_slots(idea: dict) -> list[dict]:
    parents = "-".join(idea.get("parents") or [idea["id"]])
    branch = idea.get("branch") or "alone"
    sit_off = bool(idea.get("sit_off"))
    labels = [
        ("the factory landlord", "Owns or rents the scarce physical thing."),
        ("the power landlord", "Owns the electricity that turns the plants on."),
        ("the paper wrapper", "Sits on the circular paper of the build."),
        ("the rail", "Moves payment to the model."),
    ]
    # Two discussable names per idea. Not a tour. Not a buy.
    picked = labels[:2]
    names = []
    for i, (label, makes_money) in enumerate(picked, start=1):
        names.append(
            {
                "id": f"ST-PIPE-{idea['id']}-{i}",
                "kind": "name",
                "parent_idea": idea["id"],
                "parent_theses": idea.get("parents") or [],
                "branch": branch,
                "name": f"{label} (discussable fixture, not a buy)",
                "sit_with_or_stay_off": "stay-off" if sit_off else "sit-with",
                "how_it_makes_money": makes_money,
                "how_this_name_can_be_a_bad_sit_even_if_thesis_true": (
                    "The name is crowded, or the surplus never reaches this seat."
                ),
                "understand_or_too_hard": "discussable; not screened as a buy",
                "already_in_the_price_or_not_checked": "not checked",
                "what_would_make_us_leave": "Inherited from the idea, or the vehicle is not the idea.",
                "disposition": "stay-off" if sit_off else "unfinished",
                "buy": False,
                "note": "A new Investment Idea forces 2–4 names. A thesis keep is not names.",
            }
        )
    return names


def names_stage(ideas_result: dict) -> dict:
    ideas = ideas_result.get("ideas") or []
    if ideas_result.get("skipped"):
        return {"skipped": True, "why": ideas_result.get("why"), "names": [], "by_idea": {}}
    by_idea: dict[str, list[dict]] = {}
    all_names: list[dict] = []
    missing: list[str] = []
    for idea in ideas:
        slots = _name_slots(idea)
        why = idea.get("honest_empty_why")
        if why:
            by_idea[idea["id"]] = []
            continue
        if not (2 <= len(slots) <= 4):
            missing.append(idea["id"])
            continue
        by_idea[idea["id"]] = slots
        all_names.extend(slots)
    if missing:
        raise PipeFail(
            MISSING_NAMES,
            "A new Investment Idea forces 2–4 names. "
            f"These ideas have no names and no honest-empty why: {missing}. "
            "A thesis keep is not names. Nathan asking is not the trigger.",
        )
    return {"skipped": False, "why": None, "names": all_names, "by_idea": by_idea}


def empty_last_run() -> dict:
    return {
        "lastRunAt": None,
        "timezone": "Asia/Hong_Kong",
        "trigger": None,
        "result": None,
        "failReason": None,
        "board": None,
        "stages": None,
        "note": "Pipe has never run.",
    }


def read_last_run(path: Path) -> dict:
    if not path.exists():
        return empty_last_run()
    data = load_json(path)
    if not isinstance(data, dict):
        return empty_last_run()
    return data


def write_last_run(path: Path, record: dict) -> None:
    write_json(path, record)


def run_pipe(
    *,
    board_path: Path,
    handoff_path: Path | None,
    inbox_path: Path | None,
    keep_path: Path | None,
    last_run_path: Path,
    out_dir: Path,
    trigger: str,
) -> dict:
    run_at = iso_hkt()
    prior = read_last_run(last_run_path)
    last_identity = (prior.get("board") or None) if prior.get("result") == "pass" else None

    board = deepcopy(load_json(board_path))
    if not isinstance(board, dict):
        raise PipeFail("bad_board", f"Board file is not an object: {board_path}")

    handoff = load_handoff(handoff_path)
    handoff.extend(load_inbox(inbox_path))

    keep = load_json(keep_path) if keep_path and keep_path.exists() else None

    out_dir.mkdir(parents=True, exist_ok=True)
    stages: dict[str, Any] = {}

    try:
        intake_result = intake(board, handoff, last_identity)
        stages["intake"] = {
            "result": "pass",
            "added": intake_result["added"],
            "updated": intake_result["updated"],
            "before": intake_result["before"],
            "after": intake_result["after"],
        }
        write_json(out_dir / "intake.json", intake_result)

        thesis_result = thesis_stage(board, intake_result, run_at)
        if thesis_result["kind"] not in {"draft", "duplicate_stop"}:
            raise PipeFail(NO_THESIS_OUTPUT, "Thesis stage produced neither a draft nor a duplicate-stop.")
        stages["thesis"] = thesis_result["kind"]
        write_json(out_dir / "thesis.json", thesis_result)

        ideas_result = ideas_stage(board, thesis_result, keep)
        stages["ideas"] = (
            "skipped_no_keep"
            if ideas_result.get("skipped")
            else f"{len(ideas_result['ideas'])} written"
        )
        write_json(out_dir / "ideas.json", ideas_result)

        names_result = names_stage(ideas_result)
        stages["names"] = (
            "skipped_no_ideas"
            if names_result.get("skipped")
            else f"{len(names_result['names'])} written for {len(names_result['by_idea'])} ideas"
        )
        write_json(out_dir / "names.json", names_result)

        identity = intake_result["after"]
        record = {
            "lastRunAt": run_at,
            "timezone": "Asia/Hong_Kong",
            "trigger": trigger,
            "result": "pass",
            "failReason": None,
            "board": identity,
            "stages": stages,
            "note": "Pipe ran. Frozen Board would have been a fail.",
        }
        write_last_run(last_run_path, record)
        write_json(out_dir / "last-run.json", record)
        write_json(out_dir / "working-board.json", board)
        return record
    except PipeFail as exc:
        identity = board_identity(board)
        record = {
            "lastRunAt": run_at,
            "timezone": "Asia/Hong_Kong",
            "trigger": trigger,
            "result": "fail",
            "failReason": exc.reason,
            "board": identity,
            "stages": stages,
            "note": exc.message,
        }
        write_last_run(last_run_path, record)
        write_json(out_dir / "last-run.json", record)
        raise


def print_report(record: dict) -> None:
    result = record.get("result")
    print(f"result: {result}")
    print(f"lastRunAt: {record.get('lastRunAt')}")
    print(f"trigger: {record.get('trigger')}")
    if record.get("failReason"):
        print(f"failReason: {record['failReason']}")
    board = record.get("board") or {}
    print(f"board.count: {board.get('count')}")
    print(f"board.ids: {board.get('ids')}")
    print(f"board.fingerprint: {board.get('fingerprint')}")
    stages = record.get("stages") or {}
    for key in ("intake", "thesis", "ideas", "names"):
        if key in stages:
            print(f"stage.{key}: {stages[key]}")
    if record.get("note"):
        print(f"note: {record['note']}")


def cmd_run(args: argparse.Namespace) -> int:
    last_run_path = Path(args.last_run)
    out_dir = Path(args.out)
    try:
        record = run_pipe(
            board_path=Path(args.board),
            handoff_path=Path(args.handoff) if args.handoff else None,
            inbox_path=Path(args.inbox) if args.inbox else None,
            keep_path=Path(args.keep) if args.keep else None,
            last_run_path=last_run_path,
            out_dir=out_dir,
            trigger=args.trigger,
        )
        print_report(record)
        return 0
    except PipeFail as exc:
        print(f"FAIL: {exc.reason}", file=sys.stderr)
        print(exc.message, file=sys.stderr)
        if last_run_path.exists():
            print_report(load_json(last_run_path))
        return 1


def cmd_run_now(args: argparse.Namespace) -> int:
    """Prove the pipe immediately. Do not wait for 8am."""
    work = Path(args.work)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    last_run_path = work / "last-run.json"
    write_json(last_run_path, empty_last_run())

    if args.frozen:
        args_ns = argparse.Namespace(
            board=str(FIXTURES / "board.json"),
            handoff=str(FIXTURES / "handoff-empty.json"),
            inbox=None,
            keep=None,
            last_run=str(last_run_path),
            out=str(work / "out"),
            trigger="run-now-frozen",
        )
        code = cmd_run(args_ns)
        if code == 1 and last_run_path.exists():
            rec = load_json(last_run_path)
            if rec.get("failReason") == FROZEN and rec.get("lastRunAt"):
                print("PROVE: frozen Board is a fail. lastRunAt is set.")
                return 0
        print("PROVE FAILED: frozen Board did not hard-fail with a last-run record.", file=sys.stderr)
        return 2

    args_ns = argparse.Namespace(
        board=str(FIXTURES / "board.json"),
        handoff=str(FIXTURES / "handoff-grow.json"),
        inbox=None,
        keep=str(FIXTURES / "keep.json"),
        last_run=str(last_run_path),
        out=str(work / "out"),
        trigger="run-now",
    )
    return cmd_run(args_ns)


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def cmd_self_test(_args: argparse.Namespace) -> int:
    """Engine proof: frozen fails; grow+keep writes ideas and 2–4 names; lastRunAt is written."""
    failures: list[str] = []

    def check(name: str, fn) -> None:
        try:
            fn()
            print(f"PASS  {name}")
        except Exception as exc:  # noqa: BLE001 — report every case
            failures.append(f"{name}: {exc}")
            print(f"FAIL  {name}: {exc}")

    def frozen_is_fail() -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            last = tmp_path / "last-run.json"
            write_json(last, empty_last_run())
            _assert(read_last_run(last)["lastRunAt"] is None, "example lastRunAt should start null")
            try:
                run_pipe(
                    board_path=FIXTURES / "board.json",
                    handoff_path=FIXTURES / "handoff-empty.json",
                    inbox_path=None,
                    keep_path=None,
                    last_run_path=last,
                    out_dir=tmp_path / "out",
                    trigger="self-test-frozen",
                )
                raise AssertionError("frozen Board must not pass")
            except PipeFail as exc:
                _assert(exc.reason == FROZEN, f"expected frozen_board, got {exc.reason}")
            rec = load_json(last)
            _assert(rec["result"] == "fail", rec)
            _assert(rec["failReason"] == FROZEN, rec)
            _assert(rec["lastRunAt"], "failed run must still write lastRunAt")
            _assert(rec["board"]["count"] == 3, rec["board"])

    def grow_keep_names() -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            last = tmp_path / "last-run.json"
            write_json(last, empty_last_run())
            rec = run_pipe(
                board_path=FIXTURES / "board.json",
                handoff_path=FIXTURES / "handoff-grow.json",
                inbox_path=None,
                keep_path=FIXTURES / "keep.json",
                last_run_path=last,
                out_dir=tmp_path / "out",
                trigger="self-test-grow",
            )
            _assert(rec["result"] == "pass", rec)
            _assert(rec["lastRunAt"], "pass must write lastRunAt")
            _assert(rec["board"]["count"] == 4, rec["board"])
            _assert("B-04" in rec["board"]["ids"], rec["board"])
            thesis = load_json(tmp_path / "out" / "thesis.json")
            _assert(thesis["kind"] == "draft", thesis)
            _assert(thesis["draft"]["id"] == "DRAFT-PIPE-1", thesis)
            ideas = load_json(tmp_path / "out" / "ideas.json")
            _assert(not ideas["skipped"], ideas)
            # 1 alone + 4 branches × 2 live theses
            _assert(len(ideas["ideas"]) == 9, len(ideas["ideas"]))
            names = load_json(tmp_path / "out" / "names.json")
            _assert(not names["skipped"], names)
            for idea in ideas["ideas"]:
                slots = names["by_idea"][idea["id"]]
                _assert(2 <= len(slots) <= 4, f"{idea['id']} has {len(slots)} names")
            _assert(len(names["names"]) == 18, len(names["names"]))

    def already_grown_empty_handoff_fails() -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            last = tmp_path / "last-run.json"
            board_copy = tmp_path / "board.json"
            grown = load_json(FIXTURES / "board.json")
            grown["board"].extend(load_handoff(FIXTURES / "handoff-grow.json"))
            write_json(board_copy, grown)
            write_json(last, empty_last_run())
            try:
                run_pipe(
                    board_path=board_copy,
                    handoff_path=FIXTURES / "handoff-empty.json",
                    inbox_path=None,
                    keep_path=None,
                    last_run_path=last,
                    out_dir=tmp_path / "out",
                    trigger="self-test-already-grown",
                )
                raise AssertionError("empty handoff on a still Board must fail")
            except PipeFail as exc:
                _assert(exc.reason == FROZEN, exc.reason)

    def grow_no_keep_is_draft_without_names() -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            last = tmp_path / "last-run.json"
            write_json(last, empty_last_run())
            rec = run_pipe(
                board_path=FIXTURES / "board.json",
                handoff_path=FIXTURES / "handoff-grow.json",
                inbox_path=None,
                keep_path=None,
                last_run_path=last,
                out_dir=tmp_path / "out",
                trigger="self-test-no-keep",
            )
            _assert(rec["result"] == "pass", rec)
            _assert(rec["stages"]["thesis"] == "draft", rec["stages"])
            _assert(rec["stages"]["ideas"] == "skipped_no_keep", rec["stages"])
            _assert(rec["stages"]["names"] == "skipped_no_ideas", rec["stages"])

    def grow_story_is_duplicate_stop() -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            last = tmp_path / "last-run.json"
            write_json(last, empty_last_run())
            rec = run_pipe(
                board_path=FIXTURES / "board.json",
                handoff_path=FIXTURES / "handoff-story.json",
                inbox_path=None,
                keep_path=None,
                last_run_path=last,
                out_dir=tmp_path / "out",
                trigger="self-test-dup-stop",
            )
            _assert(rec["result"] == "pass", rec)
            _assert(rec["board"]["count"] == 4, rec["board"])
            _assert(rec["stages"]["thesis"] == "duplicate_stop", rec["stages"])
            stop = load_json(tmp_path / "out" / "thesis.json")["duplicate_stop"]
            _assert("duplicate a narrative" in stop["sentence"], stop)

    def names_gate() -> None:
        ideas_result = {
            "skipped": False,
            "ideas": [
                {
                    "id": "IDEA-BAD",
                    "parents": ["TH-01"],
                    "sit_off": False,
                    "honest_empty_why": None,
                }
            ],
        }
        # monkey: force zero names by using a why-less idea and patching _name_slots
        original = globals()["_name_slots"]

        def _none(_idea: dict) -> list[dict]:
            return []

        globals()["_name_slots"] = _none
        try:
            try:
                names_stage(ideas_result)
                raise AssertionError("missing names must fail")
            except PipeFail as exc:
                _assert(exc.reason == MISSING_NAMES, exc.reason)
        finally:
            globals()["_name_slots"] = original

    check("frozen Board is a fail and writes lastRunAt", frozen_is_fail)
    check("grow + keep writes draft, pair-forks, and 2–4 names each", grow_keep_names)
    check("empty handoff on an unchanged Board is a fail", already_grown_empty_handoff_fails)
    check("grow without a keep is a draft, not names", grow_no_keep_is_draft_without_names)
    check("grow with a story reprint is a written duplicate-stop", grow_story_is_duplicate_stop)
    check("new idea without names is a fail", names_gate)

    if failures:
        print(f"\n{len(failures)} self-test failure(s).")
        return 1
    print("\nself-test: all passed. Frozen Board is a fail. Run-now does not wait for 8am.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Daily investment pipe. Run now or at 8am HKT.")
    sub = p.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Live or fixture run. Same engine as 8am.")
    run.add_argument("--board", required=True, help="Path to a board JSON (local; do not publish).")
    run.add_argument("--handoff", help="Cooked handoff JSON that must grow the Board.")
    run.add_argument("--inbox", help="Directory of cooked handoff JSON files.")
    run.add_argument("--keep", help="Keep file. Absent means no keep. Silence is not a keep.")
    run.add_argument("--last-run", default=str(DEFAULT_LAST_RUN))
    run.add_argument("--out", default=str(DEFAULT_OUT))
    run.add_argument("--trigger", default="run")
    run.set_defaults(func=cmd_run)

    now = sub.add_parser("run-now", help="Prove the pipe immediately. Do not wait for 8am.")
    now.add_argument("--work", default=str(ROOT / "runs" / "run-now"))
    now.add_argument(
        "--frozen",
        action="store_true",
        help="Prove a frozen Board is a fail (exit 0 if the fail is correct).",
    )
    now.set_defaults(func=cmd_run_now)

    test = sub.add_parser("self-test", help="Frozen fail + grow/keep/names proof.")
    test.set_defaults(func=cmd_self_test)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
