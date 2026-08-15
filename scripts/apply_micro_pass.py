#!/usr/bin/env python3
"""Apply 15 Aug 2026 Micro desk pass to first-walk.json and index.html EMBEDDED."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    walk = json.loads((ROOT / "first-walk.json").read_text())
    walk.update(
        {
            "walk": "micro-15aug",
            "date": "2026-08-15",
            "lede": "Funnel is world pictures and thesis candidates (expressions). Candidates tab is names (spawned or thrown), then Screen after analysis, then monitor / action / book. Reload for the latest walk.",
        }
    )
    walk["meta"].update(
        {
            "live_prices": True,
            "price_asof": "2026-08-14",
            "book": "empty",
            "pass": "Micro desk. Themes already written. Named vehicles, then both views.",
        }
    )
    walk["candidates_tab"]["columns"] = [
        {
            "id": "stocks",
            "name": "Stocks",
            "subtitle": "spawned from a thesis candidate, or a name you threw. Not analyzed yet. Not a buy.",
        },
        {
            "id": "screen",
            "name": "Screen",
            "subtitle": "after a pick is analyzed.",
            "empty": "Named stocks move here once priced.",
        },
        {
            "id": "monitor",
            "name": "Monitor",
            "subtitle": "waitlist. Both conditions must print.",
        },
        {
            "id": "action",
            "name": "Action",
            "subtitle": "conditions already met. Should act.",
            "empty": "None. Conditions have not hit.",
        },
        {
            "id": "book",
            "name": "Book",
            "subtitle": "decided to act.",
            "empty": "Nothing on the book. No execution this walk.",
        },
    ]

    # Refresh thesis desk lines after the priced pass. Do not mint new theses.
    by_id = {t["id"]: t for t in walk["theses_6_12"]}
    by_id["TH-01"].update(
        {
            "priced": "Checked 14 Aug 2026 Yahoo last prints. Default plant names already assume a lot of the good case: TSM $426.35 is −10.7% from the 30 Jun high and +13.8% off the 29 Jul scare close; MU $971.66 is +240% YTD and +31.5% off the 29 Jul close $739. Power tape did not run with them in 2026 (VST −8.2% YTD, −32% from the Sep 2025 high). Physical still tight. Not a buy on the spent names.",
            "desk": "not on desk as a buy — plant tape spent; power is the less-spent vehicle and still a wait",
        }
    )
    by_id["TH-02"].update(
        {
            "priced": "Checked 14 Aug 2026. Chinese magnet landlords did not run this year (JL MAG 6680.HK HK$17.16, −7% YTD, −40% from the Oct 2025 high). The Western second-source names (MP, Lynas) are the kill side, not the hold.",
            "skew": "The obvious long — a US-listed humanoid — is the expensive side of the same fact. The magnet landlord is now named (ST-03) and is a wait. Trailing-edge socket still unnamed.",
            "desk": "not on desk as a buy — expression now written (CA-02); magnet name is a wait, trailing-edge socket still unnamed",
        }
    )

    walk["thesis_candidates"] = [ca01(), ca02()]
    walk["stocks"] = [st04()]
    walk["screen"] = [st01(), st02(), st08(), st03(), st12()]
    walk["monitor"] = [wl01(), wl02(), wl03(), wl04()]
    walk["action"] = []
    walk["book"] = []
    walk["judge"] = {
        "pass": "micro-15aug",
        "notes": [
            "Micro desk, 15 Aug 2026. Themes left as Macro wrote them. No new thesis. Physical side of TH-01 still confirmed (HBM/DRAM booked through 2027; MU FQ3 DRAM prices +low-60s% QoQ; Texas large-load queue ~474 GW with an Abbott audit pause 3 Aug). Plant equities spent. Power is the less-spent tape and still not a buy. TH-02 now has a written magnet vehicle. Trailing-edge socket stays unnamed (too hard). TH-03 still failed skew. Four waitlists, all needing both conditions. Action empty. Book empty. TSM, MU, and VST are one TH-01 factor, not three bets. MP dies as the kill side of TH-02."
        ],
    }

    (ROOT / "first-walk.json").write_text(json.dumps(walk, indent=2, ensure_ascii=False) + "\n")
    embedded = build_embedded(walk)
    patch_index(embedded)
    print("wrote first-walk.json and patched index.html")


def ca01() -> dict:
    return {
        "id": "CA-01",
        "kind": "thesis_candidate",
        "lifecycle": "thesis_candidate",
        "unfinished": False,
        "buy": False,
        "title": "Plant-and-power landlords",
        "object": "An expression of TH-01, not a stock, not a buy. Sit with whoever owns the scarce physical thing — the foundry, the memory plants, the power landlords. This pass named the vehicles and screened them. None of them are a buy.",
        "what_it_is": "A thesis candidate. The shape of how TH-01 would be held.",
        "what_it_is_not": "A stock. A buy. A ticker. The next model. A spender. A tool-maker or a test-side consumable.",
        "why_unfinished": "The hold is written. The names are screened. Sit remains the desk answer because plant tape is spent and power still waits on both conditions.",
        "clock_kill": "The plants that make the leading chips, and the electricity that turns them on, stay scarce. Utilization stays high. Memory prices and GPU rents do not collapse. Big build programs at foundries / memory / power queue are not cancelled. A second scare in the shares, by itself, is not a kill.",
        "thesis": "TH-01",
        "spawns": ["ST-01", "ST-02", "ST-08"],
        "world_state": "confirmed on the physical; spent on the default plant names; fade/wait on power",
        "order": "fundamental-first",
        "note": "ST-01, ST-02, and ST-08 are one factor. Power is the less-spent tape. Do not treat three monitors as three bets.",
        "tape": "14 Aug 2026 Yahoo lasts. Physical agreeing: DigiTimes (mid-Aug) says 2027 DRAM/HBM from the three memory plants is booked; Micron 12 Aug said 2027 tighter than 2026 and DRAM is the constraint, not power. Plant tape spent: TSM $426.35 is +40% YTD and already bought back the July scare; MU $971.66 is +240% YTD and +31.5% off 29 Jul $739. Power tape did not run with them: VST $148.13 is −8.2% YTD and −32% from 22 Sep 2025 $217.92. Texas pause (Abbott 3 Aug, ERCOT Batch Zero delayed, PUCT 20 Aug) is a queue audit, not a print that the landlord already gets paid. Sit.",
        "how_the_hold_fails": "Even if TH-01 is true, the plant can stay scarce and the landlord still not get paid (customer keeps the surplus; memory contracts already locked the rent; the Texas queue is mostly phantom — Vistra’s own CEO said 8 Aug he wants the queue culled). Power load that is real is a 2027–28 hookup. That is late for a 6–12 month clock.",
        "desk": "Sit. Hang is real. Plant names spent. Power is a wait, not an action.",
    }


def ca02() -> dict:
    return {
        "id": "CA-02",
        "kind": "thesis_candidate",
        "lifecycle": "thesis_candidate",
        "unfinished": True,
        "buy": False,
        "title": "Ugly-input landlords",
        "object": "Expression of TH-02. Sit with whoever already owns the magnet. Not a US-listed humanoid. Not a Western rare-earth second source — that is the kill, so MP and Lynas die if thrown as longs.",
        "what_it_is": "Input / squeeze side of TH-02. Magnet vehicle is now named (ST-03). Trailing-edge socket is still unnamed.",
        "what_it_is_not": "A US humanoid. A Western mine or magnet second source. A fabless MCU with a robot slide.",
        "why_unfinished": "Magnet name is screened and waiting. Trailing-edge socket: GigaDevice is fabless plus a product story, not a verified robot socket we can stand behind. Hua Hong / SMIC is a China-foundry factor this desk does not understand well enough this pass. Too hard is a legal disposition.",
        "clock_kill": "inherits TH-02 — magnet export relief plus a real Western second source, or Chinese humanoid shipments fail in public numbers.",
        "thesis": "TH-02",
        "spawns": ["ST-03", "ST-04"],
        "world_state": "early",
        "order": "fundamental-first",
        "tape": "14 Aug 2026. China still makes most of the permanent magnets a motor needs. JL MAG 6680.HK HK$17.16, −7% YTD, −40% from 13 Oct 2025. The tape of the landlord is not running. MP $58.74 bounced +42% off its 29 Jul low — that is the kill-side name catching a bid, not our hold.",
        "how_the_hold_fails": "Even if China still owns the magnet, the listed landlord can be an EV-cycle stock (JL MAG’s FY2025 magnet revenue was mostly NEV, robot rotors still small-batch). Export licences can sit with the state, not the shareholder. A Made-in-USA label after substantial transformation is not a second mine, but a real Western magnet plant would be the kill.",
        "desk": "Magnet vehicle written. Socket unnamed. Sit. Not a buy.",
    }


def st01() -> dict:
    return {
        "id": "ST-01",
        "kind": "screen",
        "lifecycle": "screened",
        "unfinished": False,
        "buy": False,
        "ticker": "TSM",
        "title": "Taiwan Semiconductor (TSM) — hang is real, skew is not",
        "object": "The default foundry name for CA-01. Honest vehicle for the scarce plant. Already the name everyone uses. Not a buy at this tape.",
        "from": "CA-01",
        "thesis": "TH-01",
        "thinking": "6/10",
        "hang": "TH-01 / CA-01. They own the leading-edge plants. Customer cannot leave that node for a long time. This is a franchise, and the asking price already assumes a lot of the good case.",
        "how_it_makes_money": "Customers pay to have leading-edge chips made in plants almost nobody else can copy. That is the scarce slot.",
        "invert": "The good case is the default Wall Street hold. A true bottleneck can still leave no unused skew. One customer set (AI accelerators) can keep the surplus. Geopolitics is a company risk, not the TH-01 kill.",
        "world_state": "confirmed physical, spent on this name",
        "priced": "14 Aug 2026 Yahoo last $426.35. +40.3% YTD from 31 Dec 2025 $303.89. 30 Jun $477.57 (the 52-week high in this window). 29 Jul scare close $374.67. Now +13.8% off that close and only −10.7% from the high. July was a wiggle, already bought back.",
        "downside": "Retest of 29 Jul $374.67 is about 12% from $426. A real TH-01 kill is larger than that. Do not write 10x down.",
        "upside": "Back to $477.57 is about 12%. Residual if P1 holds to Christmas. Also what the default foundry holder already owns.",
        "clock": "TH-01 6–12 months, overlaps P1 (bottleneck still true at Christmas).",
        "kill": "Inherited: utilization down, rental and memory prices down, large capex cancelled. None have printed.",
        "other_vehicle": "Same factor as ST-02 and ST-08. Power is the less-spent tape. Memory (MU) bounced harder. Sitting is the other use of the same capital.",
        "disposition": "MONITOR via WL-01. Hang is real. Skew is not, after the July scare was bought back.",
        "desk": "Not a buy. Wait for both conditions.",
    }


def st02() -> dict:
    return {
        "id": "ST-02",
        "kind": "screen",
        "lifecycle": "screened",
        "unfinished": False,
        "buy": False,
        "ticker": "VST",
        "title": "Vistra (VST) — power landlord, clocks do not match",
        "object": "The named power vehicle for CA-01. Texas merchant generator plus a 20-year 1.2 GW Comanche Peak PPA with Amazon from 2027. Closest US equity to ‘owns the electrons.’ CEG, NRG, and TLN are the same factor — do not stack them.",
        "from": "CA-01",
        "thesis": "TH-01",
        "thinking": "7/10",
        "hang": "TH-01 / CA-01, power side. They already own plants on ERCOT. The Texas large-load queue is the physical tell. Not a turbine vendor (GEV) and not a cooling vendor (VRT).",
        "how_it_makes_money": "They make electricity and sell it, retail and wholesale, and they hedge. The Amazon nuclear PPA is the piece a hyperscaler cannot easily leave once hooked. The rest is a commodity cycle with a hedge book.",
        "invert": "CEO James Burke, 8 Aug earnings: 2026 ERCOT wholesale is soft, data-center hookup is 2027–28, and he wants the 474 GW queue culled. That is CA-01’s phantom-queue failure, said out loud. The Amazon PPA was announced 29 Sep 2025 during the run to $217.92. Load-growth talk was cut to 4–6% from 5–6%. PJM price-cap talk. This is a cycle plus one dated PPA, not a foundry franchise. Clock mismatch: TH-01 is a 6–12 month chip-plant bet; Vistra’s data-center load is a 2027–28 hookup.",
        "world_state": "physical queue is real and also phantom; name tape is a 2026 fade after a 2025 AI-power run",
        "priced": "14 Aug 2026 Yahoo last $148.13. −8.2% YTD from 31 Dec 2025 $161.33. 22 Sep 2025 high $217.92 (−32%). 19 May 2026 low $134.71. 29 Jul $142.81, now +3.7%. About $55B cap on mid-Aug 2026 reads. Q2 2026 ongoing adj. EBITDA $1.767B; 2026 guide $6.8–7.6B reaffirmed. Back to $217.92 is about +47%. Not desk skew.",
        "downside": "Retest of 19 May $134.71 is about 9% from $148. Further if 2027 ERCOT forwards stay below their midpoint opportunity. Do not write 10x down — integrated retail plus hedges.",
        "upside": "Old high $217.92 is +47%. That is a 2025 story getting re-rated, not unused TH-01 skew. Street already used Vistra as the default AI-power name last year.",
        "clock": "Company clock is 2027–28 hookup and the PUCT 20 Aug good-cause meeting on Batch Zero. TH-01’s Christmas bottleneck does not transfer cleanly onto 2027 load.",
        "kill": "Do not inherit the chip-plant kill onto a generator without a sentence. This name dies if contracted data-center load slips, ERCOT stays soft into the PPA start, or the queue audit shows the 474 GW was mostly phantom and nothing real replaces it. A second semi scare without those prints is not this name’s kill.",
        "other_vehicle": "CEG / NRG / TLN are the same factor. TSM and MU are the plant side of the same theme, already spent. Sit is the other use of the capital.",
        "disposition": "MONITOR via WL-03. Hang is the best power join. Skew is not. Clocks do not match. Not Action.",
        "desk": "Not a buy. Same shape as the other waits: both conditions, or nothing.",
    }


def st08() -> dict:
    return {
        "id": "ST-08",
        "kind": "screen",
        "lifecycle": "screened",
        "unfinished": False,
        "buy": False,
        "ticker": "MU",
        "title": "Micron (MU) — hang is real, skew is not",
        "object": "Memory plants, not the foundry default and not the power slot. Memory is already in TH-01’s kill language. Honest hang. Crowded/priced is the gate. Same factor as TSM. SK hynix 000660.KS is the other vehicle (14 Aug ₩1,645,000, −43.6% from 22 Jun high) — deeper drawdown, still one bet, Korean listing. Do not spawn it as a second name.",
        "from": "CA-01",
        "thesis": "TH-01",
        "thinking": "8/10",
        "hang": "TH-01 / CA-01. They own the memory plants. 12 Aug: Sadana said 2027 tighter than 2026, DRAM the number-one constraint, not power. FQ3 DRAM prices +low-60s% QoQ on low-single-digit bits.",
        "how_it_makes_money": "They sell memory from plants that take years to copy. HBM displaces several bits of ordinary DRAM. That is a cycle with a scarce slot, not a software franchise.",
        "invert": "Peak-cycle earnings look cheap and are not a gift. 2018 trailing P/E was 4.6–7.4. Customer can dual-source SK hynix and Samsung. Contracts can lock the rent before the shareholder gets the squeeze.",
        "world_state": "confirmed physical, spent on this name",
        "priced": "14 Aug 2026 Yahoo last $971.66. 13 Aug close in the prior walk was $949.83. 31 Dec 2025 $285.41, YTD +240%. 25 Jun high $1,213.56 (−19.9%). 29 Jul close $739.00, now +31.5% off that trough. July scare was in the shares and has been more than half-bought-back. Functionally the default US memory-tight equity.",
        "downside": "Retest of 29 Jul $739 is about 24% from $972. A real TH-01 kill is a cycle-break name, not a 10% dip.",
        "upside": "52-week high $1,213.56 is +25% from $972. Residual if P1 holds to Christmas. Also what the crowded holder already owns.",
        "clock": "TH-01 6–12 months, overlaps P1. Next company print ~22–23 Sep (FQ4). 2027 bookings are the physical clock.",
        "kill": "Utilization down, rental and memory prices down, large capex cancelled. None have printed. A second share-price scare without those prints is not a kill.",
        "other_vehicle": "SK hynix is the same factor with a deeper July hole. TSM is the foundry default. VST is the less-spent tape. Sit is allowed.",
        "disposition": "MONITOR via WL-02. Hang is real. Skew is not, at $972 after +240% YTD and a bounce of the July close.",
        "desk": "Not a buy. Wait for both conditions.",
    }


def st03() -> dict:
    return {
        "id": "ST-03",
        "kind": "screen",
        "lifecycle": "screened",
        "unfinished": False,
        "buy": False,
        "ticker": "6680.HK",
        "title": "JL MAG (6680.HK) — magnet landlord, still an EV cycle",
        "object": "The named magnet vehicle for CA-02. Dual-listed 300748.SZ / 6680.HK. They make the NdFeB magnets a motor needs. Not a US humanoid. Not MP. Northern Rare Earth 600111.SS is upstream of the same chain (A-share only this pass).",
        "from": "CA-02",
        "thesis": "TH-02",
        "thinking": "6/10",
        "hang": "TH-02 / CA-02 / OB-03. They already make the magnet. FY2025 magnet blanks 34,400 tonnes; NEV was about half of revenue; humanoid motor magnet assemblies were small-batch, not the P&L.",
        "how_it_makes_money": "Customers pay for sintered NdFeB magnets and rotors. Switching a qualified magnet line is slow. That is the slot. The customer set today is mostly car and wind, not robots.",
        "invert": "This can be a true China-owns-the-magnet fact and still be an NEV cycle stock. Export licences sit with the state. H-share liquidity and CCP risk are company facts, not the theme. Back to the Oct 2025 high is about +67%, not 10x. Robot rotors are a slide until they print.",
        "world_state": "early on the input; name tape faded from 2025, not a 2026 melt-up",
        "priced": "14 Aug 2026 Yahoo last HK$17.16 (6680.HK). −7.0% YTD from 31 Dec 2025 HK$18.45. 13 Oct 2025 high HK$28.72 (−40.3%). 30 Jul 2026 low HK$16.04. 29 Jul HK$16.31, now +5.2%. A-share 300748.SZ CNY 27.66, −18.9% YTD. The tape of the landlord is quiet.",
        "downside": "Retest of HK$16.04 is about 7%. A real TH-02 kill (Western second source that works) is larger. Do not write 10x down.",
        "upside": "Old high HK$28.72 is +67%. That is a 2025 rare-earth bounce, not unused robot-squeeze skew.",
        "clock": "TH-02 6–12 months. Company clock is whether robot rotor shipments leave small-batch in the next prints, and whether export licences stay ordinary.",
        "kill": "Inherited: magnet export relief plus a real Western second source, or Chinese humanoid shipments fail in public numbers. Also dies if NEV magnet volumes roll over and robots never show up in the mix.",
        "other_vehicle": "Northern Rare Earth is the same chain, harder listing. MP is the kill side. Socket (ST-04) stays unnamed. Sit is allowed.",
        "disposition": "MONITOR via WL-04. Hang is the magnet. Skew is not desk-grade until robots are more than a slide.",
        "desk": "Not a buy. Wait for both conditions.",
    }


def st04() -> dict:
    return {
        "id": "ST-04",
        "kind": "stock",
        "lifecycle": "unfinished",
        "unfinished": True,
        "buy": False,
        "ticker": None,
        "title": "Trailing-edge robot MCU sockets (names not picked)",
        "object": "Generic slot under CA-02. No ticker this pass. GigaDevice 3986.HK is fabless plus a humanoid product story (14 Aug HK$511, −58.8% from 29 Jun HK$1,241, +129% from the 13 Jan listing print) — not a verified socket we can stand behind. Hua Hong 1347.HK / SMIC 0981.HK are China trailing-edge plants and a geopolitics factor this desk does not understand well enough. NXP / Infineon are the side that is supposed to be losing the socket. Too hard. Unnamed is cleaner than a fake screen.",
        "what_it_is": "A stock-shaped slot spawned by CA-02. Names not picked.",
        "why_unfinished": "No ticker chosen. Circle of competence, not a missing column.",
        "from": "CA-02",
        "thesis": "TH-02",
        "live_price": None,
        "note": "Do not invent a specific ticker. Generic card on purpose.",
        "desk": "Not a buy. Lifecycle: unfinished stock.",
    }


def st12() -> dict:
    return {
        "id": "ST-12",
        "kind": "screen",
        "lifecycle": "screened",
        "unfinished": False,
        "buy": False,
        "ticker": "MP",
        "title": "MP Materials (MP) dies",
        "object": "Thrown as a rare-earth long. That is the Western second source. TH-02’s kill is magnet export relief plus a real Western second source. Longing MP is the expensive side of the same fact, not the hold.",
        "from": "thrown",
        "thesis": None,
        "thinking": "2/10",
        "hang": "None. Wrong side of TH-02 / CA-02.",
        "how_it_makes_money": "They mine and are trying to make magnets in the US. That is the second-source project the thesis says does not yet exist as a real substitute.",
        "invert": "If MP works, TH-02 dies. If MP does not work, this equity is the failed project, not the China landlord.",
        "priced": "14 Aug 2026 Yahoo last $58.74. +16.3% YTD. 14 Oct 2025 high $98.65 (−40.5%). 29 Jul low $38.10, now +54% off that low. The bounce is the kill-side name catching a bid.",
        "downside": "Retest $38.10 is about 35%. Company project risk, not a theme we are holding.",
        "upside": "Old high $98.65 is +68%. That would be the kill printing.",
        "clock": "TH-02 clock does not transfer onto the kill-side name as a long.",
        "kill": "No thesis kill to inherit as a long.",
        "disposition": "dies",
        "desk": "Not a buy. Failed join. Do not invent a parent.",
    }


def wl01() -> dict:
    return {
        "id": "WL-01",
        "kind": "waitlist",
        "lifecycle": "waitlist",
        "title": "Watches ST-01 TSM. Arms only on two conditions",
        "object": "Hang is already written. It does not arm because the picture is true. It arms only if both conditions print on this name.",
        "watches": ["ST-01"],
        "arms_only_if_both": [
            "a real second drawdown in TSM — toward or through the 29 Jul close $374.67. A price that has already moved, not a headline.",
            "factory / rental / memory prints still tight. If the prints ease, this dies with TH-01.",
        ],
        "size": None,
        "entry": None,
        "note": "No size. No entry until both. One condition is not enough. Same factor as WL-02 and WL-03.",
        "from": "CA-01",
        "thesis": "TH-01",
    }


def wl02() -> dict:
    return {
        "id": "WL-02",
        "kind": "waitlist",
        "lifecycle": "waitlist",
        "title": "Watches ST-08 MU. Arms only on two conditions",
        "object": "Hang is already written. It does not arm because the picture is true. It arms only if both conditions print on this name.",
        "watches": ["ST-08"],
        "arms_only_if_both": [
            "a real second drawdown in MU — toward or through the 29 Jul close $739. A price that has already moved, not a headline.",
            "factory / rental / memory prints still tight. If the prints ease, this dies with TH-01.",
        ],
        "size": None,
        "entry": None,
        "note": "No size. No entry until both. One condition is not enough. Same factor as WL-01 and WL-03.",
        "from": "CA-01",
        "thesis": "TH-01",
    }


def wl03() -> dict:
    return {
        "id": "WL-03",
        "kind": "waitlist",
        "lifecycle": "waitlist",
        "title": "Watches ST-02 VST. Arms only on two conditions",
        "object": "Hang is already written. It does not arm because Texas paused the queue. It arms only if both conditions print on this name.",
        "watches": ["ST-02"],
        "arms_only_if_both": [
            "a real further drawdown in VST — toward or through the 19 May 2026 low $134.71 — or a contracted-load print that is not phantom (Amazon 2027 hookup still dated, or the ERCOT audit actually culls the 474 GW to real MW). A price or a filing, not a headline.",
            "TH-01 physical still tight (utilization, rents, memory, no cancelled plant capex). If the chip-plant variable breaks, this dies with the theme even if ERCOT looks busy.",
        ],
        "size": None,
        "entry": None,
        "note": "No size. No entry until both. The 20 Aug PUCT meeting is a date, not a condition. Same factor as WL-01 and WL-02.",
        "from": "CA-01",
        "thesis": "TH-01",
    }


def wl04() -> dict:
    return {
        "id": "WL-04",
        "kind": "waitlist",
        "lifecycle": "waitlist",
        "title": "Watches ST-03 JL MAG. Arms only on two conditions",
        "object": "Hang is already written. It does not arm because China owns the magnet. It arms only if both conditions print on this name.",
        "watches": ["ST-03"],
        "arms_only_if_both": [
            "robot / servo magnet revenue leaves small-batch in a public print, or a further drawdown through the 30 Jul HK$16.04 low. A filing or a price, not a humanoid headline.",
            "China still owns the magnet chain — no magnet export relief plus a real Western second source. If that kill prints, this dies with TH-02.",
        ],
        "size": None,
        "entry": None,
        "note": "No size. No entry until both. One condition is not enough.",
        "from": "CA-02",
        "thesis": "TH-02",
    }


def card(src: dict, extra: dict | None = None) -> dict:
    tags = extra.pop("tags") if extra and "tags" in extra else src.get("tags")
    out = {"id": src["id"], "title": src["title"]}
    if tags:
        out["tags"] = tags
    if extra:
        out.update(extra)
    for k in ("story", "claim", "from", "desk", "desk_fail", "kind", "unfinished", "buy"):
        if k in src and k not in out:
            out[k] = src[k]
    return out


def fields(*pairs: tuple[str, str]) -> list[dict]:
    return [{"label": a, "text": b} for a, b in pairs]


def build_embedded(walk: dict) -> dict:
    board_cards = []
    for b in walk["board"]:
        kind = b["kind"]
        if kind == "board_card":
            tags = [{"label": "board card", "class": "kind"}]
            if "fight" in b.get("tags", []):
                tags.append({"label": "fight", "class": "fail"})
            board_cards.append(
                {
                    "id": b["id"],
                    "kind": "board_card",
                    "tags": tags,
                    "title": b["title"],
                    "story": b["story"],
                    "from": "From: " + b.get("from", ""),
                }
            )
        elif kind == "prediction":
            board_cards.append(
                {
                    "id": b["id"],
                    "kind": "prediction",
                    "tags": [{"label": "prediction", "class": "kind"}],
                    "title": b["title"],
                    "story": b["story"],
                    "fields": fields(("Call", b.get("call", "")), ("Wrong if", b.get("wrong_if", ""))),
                }
            )
        elif kind == "observation":
            board_cards.append(
                {
                    "id": b["id"],
                    "kind": "observation",
                    "tags": [{"label": "observation", "class": "kind"}],
                    "title": b["title"],
                    "story": b["story"],
                    "from": "From: " + b.get("from", ""),
                }
            )

    theses = []
    for t in walk["theses_6_12"]:
        tags = [{"label": "live", "class": "live"}]
        if "failed skew" in (t.get("desk") or ""):
            tags.append({"label": "failed skew", "class": "fail"})
        theses.append(
            {
                "id": t["id"],
                "kind": "thesis",
                "tags": tags,
                "title": t["title"],
                "claim": t["claim"],
                "from": "From board: " + ", ".join(t.get("from_board", [])),
                "fields": fields(
                    ("Clock", t.get("clock", "")),
                    ("Kill", t.get("kill", "")),
                    ("Priced", t.get("priced", "")),
                ),
                "desk": "Desk: " + t.get("desk", ""),
                "desk_fail": True,
            }
        )

    def expr_card(c: dict) -> dict:
        tags = [{"label": "expression", "class": "expr"}]
        if c.get("unfinished"):
            tags.append({"label": "unfinished", "class": "unfinished"})
        return {
            "id": c["id"],
            "kind": "thesis_candidate",
            "unfinished": c.get("unfinished", False),
            "buy": False,
            "tags": tags,
            "title": c["title"],
            "story": c["object"],
            "from": "From: " + c.get("thesis", ""),
            "fields": fields(
                ("What it is", c.get("what_it_is", "")),
                ("What it is not", c.get("what_it_is_not", "")),
                ("World", c.get("world_state", "") + ((" · " + c.get("order", "")) if c.get("order") else "")),
                ("Tape", c.get("tape", "")),
                ("How the hold fails", c.get("how_the_hold_fails", "")),
                ("Spawns", ", ".join(c.get("spawns", []))),
            ),
            "desk": c.get("desk", ""),
            "desk_fail": True,
        }

    def stock_card(s: dict) -> dict:
        tags = [{"label": "stock", "class": "stock"}, {"label": "unfinished", "class": "unfinished"}]
        return {
            "id": s["id"],
            "kind": "stock",
            "unfinished": True,
            "buy": False,
            "tags": tags,
            "title": s["title"],
            "story": s["object"],
            "from": "From: " + s.get("from", ""),
            "desk": s.get("desk", "Not a buy. Lifecycle: unfinished stock."),
            "desk_fail": True,
        }

    def screen_card(s: dict) -> dict:
        disp = (s.get("disposition") or "").upper()
        tags = [{"label": "screen", "class": "kind"}]
        if "DIES" in disp and "HOLD" in disp:
            tags.append({"label": "dies as a hold", "class": "fail"})
        elif disp.startswith("DIES"):
            tags.append({"label": "dies", "class": "fail"})
        elif "MONITOR" in disp:
            tags.append({"label": "monitor", "class": "wait"})
        if s.get("from") == "thrown":
            tags.append({"label": "thrown", "class": "unfinished"})
        return {
            "id": s["id"],
            "kind": "screen",
            "tags": tags,
            "title": s["title"],
            "story": f"Thinking {s.get('thinking', '')}. Hang: {s.get('hang', '')}",
            "from": "From: " + (s.get("from") or "thrown"),
            "fields": fields(
                ("Priced", s.get("priced", "")),
                ("Downside", s.get("downside", "")),
                ("Upside", s.get("upside", "")),
                ("Clock", s.get("clock", "")),
                ("Kill", s.get("kill", "")),
                ("Disposition", s.get("disposition", "")),
            ),
            "desk": s.get("desk", "Not a buy."),
            "desk_fail": not str(s.get("disposition", "")).upper().startswith("MONITOR"),
        }

    def wait_card(w: dict) -> dict:
        conds = w.get("arms_only_if_both") or []
        return {
            "id": w["id"],
            "kind": "waitlist",
            "tags": [{"label": "waitlist", "class": "wait"}],
            "title": w["title"],
            "story": w["object"],
            "from": "Watches: " + ", ".join(w.get("watches", [])) + ". From: " + w.get("from", ""),
            "fields": fields(
                ("(a)", conds[0] if len(conds) > 0 else ""),
                ("(b)", conds[1] if len(conds) > 1 else ""),
                ("Not written", w.get("note", "")),
            ),
            "desk": "Lifecycle: waitlist. Waiting is the action.",
            "desk_fail": False,
        }

    return {
        "rev": 6,
        "title": walk["title"],
        "lede": walk["lede"],
        "meta": "15 Aug 2026. Micro pass. Named VST and JL MAG. Four waits. MP dies. Book empty.",
        "judge": walk["judge"]["notes"][0],
        "tabs": [
            {
                "id": "funnel",
                "name": "Funnel",
                "default": True,
                "legend": [
                    {"color": "#1e3a5f", "label": "Board"},
                    {"color": "#1a4d2e", "label": "Theses 6–12 months"},
                    {"color": "#5c4a1f", "label": "Theses now"},
                    {"color": "#1a3d4d", "label": "Thesis candidates"},
                    {"color": "#2a2222", "label": "Dead / parked"},
                ],
                "legend_note": "labels: board card · live · expression",
                "layout": "funnel",
                "columns": [
                    {
                        "id": "board",
                        "name": "Board",
                        "class": "board",
                        "subtitle": "cooked Trend-board cards + P1–P3 + OB-01/02/03. Not narratives.",
                        "cards": board_cards,
                    },
                    {
                        "id": "theses",
                        "name": "Theses 6–12 months",
                        "class": "theses",
                        "subtitle": "forward pictures minted from the board. Not already moving the world.",
                        "cards": theses,
                    },
                    {
                        "id": "now",
                        "name": "Theses now",
                        "class": "now",
                        "subtitle": "dominating / rising / peaking in the world right now. Not a 6–12 month bet.",
                        "empty": "None. A now-thesis is already moving the world; it is not a forward picture.",
                        "cards": [],
                    },
                    {
                        "id": "thesis-cands",
                        "name": "Thesis candidates",
                        "class": "thesis-cands",
                        "subtitle": "expressions of a live thesis. Not a name. Not a buy. Spawns stock rows.",
                        "cards": [expr_card(c) for c in walk["thesis_candidates"]],
                    },
                ],
                "strips": [
                    {
                        "id": "dead",
                        "name": "Dead / parked",
                        "class": "deadstrip",
                        "subtitle": "killed or parked pictures. Held / off-desk is not dead.",
                        "empty": "None this walk.",
                        "cards": [],
                    }
                ],
            },
            {
                "id": "candidates",
                "name": "Candidates",
                "default": False,
                "legend": [
                    {"color": "#1a3d4d", "label": "Stocks"},
                    {"color": "#5c4a1f", "label": "Screen"},
                    {"color": "#3d3d3d", "label": "Monitor"},
                    {"color": "#1a4d2e", "label": "Action"},
                    {"color": "#2a2222", "label": "Book"},
                ],
                "legend_note": "labels: unfinished · waitlist · dies",
                "layout": "candidates",
                "columns": [
                    {
                        "id": "stocks",
                        "name": "Stocks",
                        "class": "stocks",
                        "subtitle": "spawned from a thesis candidate, or a name you threw. Not analyzed yet. Not a buy.",
                        "cards": [stock_card(s) for s in walk["stocks"]],
                    },
                    {
                        "id": "screen",
                        "name": "Screen",
                        "class": "screen",
                        "subtitle": "after a pick is analyzed.",
                        "cards": [screen_card(s) for s in walk["screen"]],
                    },
                    {
                        "id": "monitor",
                        "name": "Monitor",
                        "class": "monitor",
                        "subtitle": "waitlist. Both conditions must print.",
                        "cards": [wait_card(w) for w in walk["monitor"]],
                    },
                    {
                        "id": "action",
                        "name": "Action",
                        "class": "action",
                        "subtitle": "conditions already met. Should act.",
                        "empty": "None. Conditions have not hit.",
                        "cards": [],
                    },
                    {
                        "id": "book",
                        "name": "Book",
                        "class": "book",
                        "subtitle": "decided to act.",
                        "empty": "Nothing on the book. No execution this walk.",
                        "cards": [],
                    },
                ],
            },
        ],
    }


def patch_index(embedded: dict) -> None:
    path = ROOT / "index.html"
    html = path.read_text()
    html = html.replace(
        "<!-- funnel-shell rev=6 2026-08-14T23:50HKT CA-01 sit -->",
        "<!-- funnel-shell rev=7 2026-08-15 micro pass: named vehicles, four waits -->",
    )
    payload = json.dumps(embedded, ensure_ascii=False, separators=(",", ":"))
    html2, n = re.subn(
        r"var EMBEDDED=\{.*?\};\n",
        "var EMBEDDED=" + payload + ";\n",
        html,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"expected one EMBEDDED replacement, got {n}")
    path.write_text(html2)


if __name__ == "__main__":
    main()
