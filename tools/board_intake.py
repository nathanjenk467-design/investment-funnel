#!/usr/bin/env python3
"""Board intake: grow the Board or fail.

Input:  a cooked Narrative docket + current Board titles/ids.
Output: new Board card payloads for situations not already on the Board.
Fail:   zero new cards, or a reprint of the frozen set.

Stories stay stories. This tool does not mint a thesis.
It does not write the private local board.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_BOARD_FROZEN = 2

FROZEN_SITUATION_KEYS = (
    "plant",
    "july-scare",
    "old-cards",
    "capital-to-plants",
    "circular-paper",
    "power-fight",
    "mid-august-prints",
)

# Distinctive titles / phrases from the public first-walk Board.
# Used to catch a reprint. Not used to fold a new situation onto an old card.
FROZEN_TITLE_PHRASES = (
    "ai chip factories are still dramatically under-built",
    "in july the market panicked",
    "compute is getting dearer, and old cards still earn",
    "the money is going to the plants, not the next model",
    "ordinary funding may be exhausted",
    "power is the problem. nobody agrees what happens next",
    "mid-august prints",
    "mid august prints",
    "new tapes this week",
)

KIND_TO_BOARD = {
    "kept_situation": "board_card",
    "housed_story": "board_card",
    "fresh_print": "board_card",
    "open_call": "prediction",
    "observation": "observation",
    "board_card": "board_card",
    "prediction": "prediction",
}

THESIS_FIELDS = (
    "claim",
    "from_board",
    "clock",
    "kill",
    "priced",
    "desk",
    "horizon",
    "on_desk",
    "related_predictions",
    "skew",
    "thesis",
    "spawns",
)

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
REPO_ROOT = HERE.parent


def normalize_title(text: str) -> str:
    text = (text or "").casefold()
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"BOARD INTAKE FAILED: file not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"BOARD INTAKE FAILED: not JSON: {path}: {exc}") from None


def as_item_list(data: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = None
        for key in keys:
            if isinstance(data.get(key), list):
                items = data[key]
                break
        if items is None:
            raise SystemExit(
                "BOARD INTAKE FAILED: expected a list, or an object with "
                + " / ".join(keys)
                + "."
            )
    else:
        raise SystemExit("BOARD INTAKE FAILED: expected a JSON object or list.")
    out: list[dict[str, Any]] = []
    for raw in items:
        if isinstance(raw, dict):
            out.append(raw)
    if not out:
        raise SystemExit("BOARD INTAKE FAILED: no items in the file.")
    return out


def load_board(path: Path) -> list[dict[str, str]]:
    data = load_json(path)
    cards = []
    for raw in as_item_list(data, "cards", "board"):
        card_id = str(raw.get("id") or "").strip()
        title = str(raw.get("title") or "").strip()
        if not card_id or not title:
            continue
        cards.append(
            {
                "id": card_id,
                "title": title,
                "title_norm": normalize_title(title),
                "situation_key": str(raw.get("situation_key") or "").strip(),
            }
        )
    if not cards:
        raise SystemExit("BOARD INTAKE FAILED: Board file has no id/title cards.")
    return cards


def load_docket(path: Path) -> list[dict[str, Any]]:
    data = load_json(path)
    items = as_item_list(data, "items", "board")
    out = []
    for raw in items:
        title = str(raw.get("title") or "").strip()
        if not title:
            continue
        kind = str(raw.get("kind") or "kept_situation").strip()
        out.append(
            {
                "docket_id": str(
                    raw.get("docket_id") or raw.get("id") or ""
                ).strip(),
                "kind": kind,
                "title": title,
                "story": str(raw.get("story") or "").strip(),
                "force": str(raw.get("force") or "").strip(),
                "from": str(raw.get("from") or "").strip(),
                "situation_key": str(raw.get("situation_key") or "").strip(),
                "updates_board_id": str(
                    raw.get("updates_board_id")
                    or raw.get("existing_board_id")
                    or ""
                ).strip(),
                "id": str(raw.get("id") or "").strip(),
                "call": str(raw.get("call") or "").strip(),
                "wrong_if": str(raw.get("wrong_if") or "").strip(),
                "call_by": str(raw.get("call_by") or "").strip(),
            }
        )
    if not out:
        raise SystemExit("BOARD INTAKE FAILED: docket has no titled items.")
    return out


def frozen_key_for(item: dict[str, Any]) -> str | None:
    key = (item.get("situation_key") or "").strip()
    if key in FROZEN_SITUATION_KEYS:
        return key
    title_norm = normalize_title(item.get("title") or "")
    phrase_to_key = {
        "ai chip factories are still dramatically under built": "plant",
        "in july the market panicked": "july-scare",
        "compute is getting dearer and old cards still earn": "old-cards",
        "the money is going to the plants not the next model": "capital-to-plants",
        "ordinary funding may be exhausted": "circular-paper",
        "power is the problem nobody agrees what happens next": "power-fight",
        "mid august prints": "mid-august-prints",
        "mid-august prints": "mid-august-prints",
        "new tapes this week": "mid-august-prints",
    }
    for phrase, key in phrase_to_key.items():
        phrase_norm = normalize_title(phrase)
        if phrase_norm and phrase_norm in title_norm:
            return key
    return None


def find_existing(item: dict[str, Any], board: list[dict[str, str]]) -> dict[str, str] | None:
    """Strict identity only. Shared words are not a match."""
    named = item.get("updates_board_id") or ""
    if named:
        for card in board:
            if card["id"] == named:
                return card
    own_id = item.get("id") or ""
    if own_id:
        for card in board:
            if card["id"] == own_id:
                return card
    title_norm = normalize_title(item.get("title") or "")
    if title_norm:
        for card in board:
            if card["title_norm"] == title_norm:
                return card
    key = (item.get("situation_key") or "").strip()
    if key:
        for card in board:
            if card["situation_key"] and card["situation_key"] == key:
                return card
    return None


def board_kind_for(docket_kind: str) -> str:
    return KIND_TO_BOARD.get(docket_kind, "board_card")


def new_card_payload(item: dict[str, Any], index: int) -> dict[str, Any]:
    kind = board_kind_for(item["kind"])
    payload: dict[str, Any] = {
        "proposed_id": f"PROPOSED-{index}",
        "kind": kind,
        "title": item["title"],
        "story": item["story"],
        "from_docket": item["docket_id"] or None,
        "lifecycle_on_board": "emerging",
        "note": (
            "Architect assigns the live id on the local board. "
            "Not a thesis. Not live."
        ),
    }
    if item["force"]:
        payload["force"] = item["force"]
    if item["from"]:
        payload["from"] = item["from"]
    if item["situation_key"]:
        payload["situation_key"] = item["situation_key"]
    if kind == "prediction":
        if item["call"]:
            payload["call"] = item["call"]
        if item["wrong_if"]:
            payload["wrong_if"] = item["wrong_if"]
        if item["call_by"]:
            payload["call_by"] = item["call_by"]
    for banned in THESIS_FIELDS:
        payload.pop(banned, None)
    return payload


def run_intake(docket: list[dict[str, Any]], board: list[dict[str, str]]) -> dict[str, Any]:
    new_cards: list[dict[str, Any]] = []
    updates: list[dict[str, Any]] = []
    reprints: list[dict[str, Any]] = []

    for item in docket:
        named_id = (item.get("updates_board_id") or "").strip()
        named_card = None
        if named_id:
            named_card = next((c for c in board if c["id"] == named_id), None)
        existing = find_existing(item, board)
        frozen = frozen_key_for(item)

        # An explicit print on a named id may update. A frozen-set reissue
        # without that name is a reprint, even if the old title still matches.
        if named_card is not None:
            updates.append(
                {
                    "docket_id": item["docket_id"] or None,
                    "title": item["title"],
                    "updates_board_id": named_card["id"],
                    "existing_title": named_card["title"],
                    "reason": "fresh print named an existing Board id",
                }
            )
            continue
        if frozen:
            reprints.append(
                {
                    "docket_id": item["docket_id"] or None,
                    "title": item["title"],
                    "situation_key": frozen,
                    "reason": "reprint of the frozen set; not a new card",
                }
            )
            continue
        if existing is not None:
            updates.append(
                {
                    "docket_id": item["docket_id"] or None,
                    "title": item["title"],
                    "updates_board_id": existing["id"],
                    "existing_title": existing["title"],
                    "reason": "strict identity: same id, same title, or same situation_key",
                }
            )
            continue
        new_cards.append(new_card_payload(item, len(new_cards) + 1))

    result = {
        "ok": bool(new_cards),
        "new_card_count": len(new_cards),
        "new_cards": new_cards,
        "updates": updates,
        "reprints_rejected": reprints,
        "board_would_stay_the_same": not bool(new_cards),
    }
    if not new_cards:
        if reprints and not updates:
            result["fail"] = (
                "BOARD INTAKE FAILED: reprint of the frozen set "
                "(plant / July-scare / old-cards / capital-to-plants / "
                "circular-paper / power-fight / mid-August-prints). "
                "A reprint is a failed run, not a success."
            )
        elif updates and not reprints:
            result["fail"] = (
                "BOARD INTAKE FAILED: zero new Board cards. "
                "Fresh prints were folded onto old cards. "
                "The Board would look the same as yesterday."
            )
        elif reprints and updates:
            result["fail"] = (
                "BOARD INTAKE FAILED: zero new Board cards. "
                "Reprint of the frozen set, and prints on old cards. "
                "The Board would look the same as yesterday."
            )
        else:
            result["fail"] = (
                "BOARD INTAKE FAILED: zero new Board cards. "
                "The Board would look the same as yesterday."
            )
    return result


def emit_result(result: dict[str, Any], out_path: Path | None) -> int:
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if out_path is not None:
        out_path.write_text(text, encoding="utf-8")
    if result["ok"]:
        sys.stdout.write(text)
        return EXIT_OK
    sys.stderr.write(result["fail"] + "\n")
    sys.stdout.write(text)
    return EXIT_BOARD_FROZEN


def run_paths(docket_path: Path, board_path: Path, out_path: Path | None) -> int:
    return emit_result(run_intake(load_docket(docket_path), load_board(board_path)), out_path)


def _expect(cond: bool, message: str) -> None:
    if not cond:
        raise SystemExit(f"SELF-TEST FAILED: {message}")


def self_test() -> int:
    board = load_board(FIXTURES / "board-titles.json")

    grew = run_intake(load_docket(FIXTURES / "docket-new-situation.json"), board)
    _expect(grew["ok"] is True, "new-situation docket must succeed")
    _expect(grew["new_card_count"] == 1, "new-situation must mint exactly one card")
    card = grew["new_cards"][0]
    _expect(card["kind"] == "board_card", "stories/situations stay Board cards")
    _expect(card["proposed_id"].startswith("PROPOSED-"), "ids are proposed, not live")
    _expect("claim" not in card, "must not mint a thesis claim")
    _expect("clock" not in card, "must not mint a thesis clock")
    _expect(card["title"].startswith("The desert plant"), "payload title missing")
    sys.stdout.write("SELF-TEST: new situation → 1 new Board card payload\n")
    sys.stdout.write(json.dumps(card, indent=2, ensure_ascii=False) + "\n")

    mixed = run_intake(load_docket(FIXTURES / "docket-mixed.json"), board)
    _expect(mixed["ok"] is True, "mixed docket must succeed")
    _expect(mixed["new_card_count"] == 1, "mixed docket must mint one new card")
    _expect(len(mixed["updates"]) == 1, "mixed docket must record the print as an update")
    _expect(mixed["updates"][0]["updates_board_id"] == "15", "print must stay on card 15")
    sys.stdout.write("SELF-TEST: mixed docket → 1 new card + 1 update (not a second card)\n")

    reprint = run_intake(load_docket(FIXTURES / "docket-reprint-frozen.json"), board)
    _expect(reprint["ok"] is False, "frozen reprint must fail")
    _expect(reprint["new_card_count"] == 0, "frozen reprint must produce zero new cards")
    _expect(
        "reprint of the frozen set" in reprint["fail"].casefold(),
        "frozen fail text missing",
    )
    sys.stderr.write(reprint["fail"] + "\n")
    sys.stdout.write("SELF-TEST: frozen reprint → hard fail (zero new cards)\n")

    prints = run_intake(load_docket(FIXTURES / "docket-prints-only.json"), board)
    _expect(prints["ok"] is False, "prints-only must fail")
    _expect(prints["new_card_count"] == 0, "prints-only must produce zero new cards")
    _expect("same as yesterday" in prints["fail"], "prints-only fail text missing")
    sys.stderr.write(prints["fail"] + "\n")
    sys.stdout.write("SELF-TEST: prints-only → hard fail (Board would stay the same)\n")

    call_docket = [
        {
            "docket_id": "N-SYNTH-CALL",
            "kind": "open_call",
            "title": "By winter the denied water right still blocks the desert plant",
            "story": "Method fixture. An open call, not a thesis.",
            "force": "the water right stays the gate.",
            "from": "synthetic intake fixture",
            "situation_key": "desert-water-call",
            "updates_board_id": "",
            "id": "",
            "call": "By 31 December 2026 the basin has not granted the water.",
            "wrong_if": "the water is granted and the plant takes it.",
            "call_by": "2026-12-31",
        }
    ]
    call_result = run_intake(call_docket, board)
    _expect(call_result["ok"] is True, "open call must become a new Board item")
    _expect(call_result["new_cards"][0]["kind"] == "prediction", "open call stays a call")
    _expect("claim" not in call_result["new_cards"][0], "open call must not grow a thesis")
    sys.stdout.write("SELF-TEST: open call → prediction Board payload, not a thesis\n")

    walk = REPO_ROOT / "first-walk.json"
    if walk.is_file():
        same = run_intake(load_docket(walk), load_board(walk))
        _expect(same["ok"] is False, "feeding first-walk as the docket must fail")
        _expect(same["new_card_count"] == 0, "first-walk reprint must be zero new cards")
        sys.stdout.write("SELF-TEST: first-walk.json as docket+board → hard fail\n")

    sys.stdout.write("SELF-TEST: all checks passed.\n")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Board intake: new Board cards for new situations. "
            "Fails if the Board would stay the same."
        )
    )
    parser.add_argument(
        "--docket",
        type=Path,
        help="Cooked Narrative docket (JSON). Kept situations, open calls, housed stories.",
    )
    parser.add_argument(
        "--board",
        type=Path,
        help="Current Board card titles and ids (JSON). Not the private local board.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Optional path to write the JSON result.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the fixture contract: grow, then hard-fail a reprint.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.docket or not args.board:
        parser.print_help()
        sys.stderr.write(
            "\nBOARD INTAKE FAILED: --docket and --board are required "
            "(or pass --self-test).\n"
        )
        return EXIT_USAGE
    return run_paths(args.docket, args.board, args.out)


if __name__ == "__main__":
    sys.exit(main())
