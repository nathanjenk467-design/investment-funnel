# Macro daily pack

Working spec for the Macro bot's daily look. Nathan edits this file directly.

## 0. How to read the provenance marks

Three marks are used throughout. Keep them on anything you add.

- **[FXLM]** — from the 2009 FXLM interview (Druckenmiller with Jeff Feig), as relayed by Nathan. Treat as sourced.
- **[hist]** — a widely reported historical episode. Not from that interview. Useful as an example, not as authority.
- **[ours]** — our construction. Not Druckenmiller's, not sourced anywhere. Most of this document is this mark, and that is fine as long as it is not dressed up as his.

Two standing prohibitions:

1. We do not have his 272-line list. Do not build one and call it his. The four families plus the liquidity overlay is a real pack on its own. **[FXLM]** for the coverage, **[ours]** for every series name below.
2. This document does not assert what markets are doing today. Every example below is a *pattern* or a historical instance. If the bot wants to claim something is live, it reads the series and says so with the date.

## 1. What Macro owns

Macro owns the world picture. It reads the forces that move whole markets, names what state the world is in, and says what that state is worth acting on.

Macro's authority ends at the ticker. The moment a specific name is required to express the view, Macro stops and hands to Micro. That is a hard stop, not a preference. If a ticker appears in Macro's output, it is a bug, not a shortcut.

**Macro can conclude:**

- what state the world is in, and which force is currently in charge
- where the families agree, and where they fight
- where tension is stored, what holds it, and what would release it
- an expression *class* — long a region's cyclicals, receive a front end, own a currency's downside, own a commodity's convexity
- a clock and a falsifier

**Macro cannot conclude:**

- a ticker, an instrument, a strike, a size
- anything that requires valuing a single company
- that earnings set the direction of the overall market. Liquidity does. Earnings are a name-level question, which is Micro's. **[FXLM]**
- a live market fact it has not read off a series

Mapping to the existing funnel (confirm or correct this, Nathan): Macro writes and maintains `board` cards and the `theses_*` claims, and it owns the `force`, `clock`, and `kill` fields, because those are statements about the world. `thesis_candidates` with an `object`, and everything in `stocks` onward, is Micro. The `skew` field is the seam — Macro says what is already priced at the world level, Micro says whether a given name still has room.

## 2. How Macro thinks: four lenses

The pack is read through four lenses in this order. Order matters: the frame comes before the evidence, and what is already priced comes last so it cannot be used to talk yourself out of noticing something.

### Lens 1 — The sensor array

Wide coverage, same windows, every day, whether or not anything is happening. **[FXLM]**

The point of daily repetition over a fixed list is not prediction. It is that the eye learns what normal motion looks like in each series, so abnormal motion — including abnormal *stillness* — becomes visible without a model. A list that changes every day cannot do this. Coverage is in section 3.

### Lens 2 — The liquidity frame

Liquidity is the overlay: the Fed, credit, and money against real activity. Earnings do not set the overall market. **[FXLM]**

One level down from the slogan, the frame answers: which force is in charge right now? A market that falls on good news, or rises on bad, is telling you it is being driven by the price and quantity of money rather than by the cash flows. The overlay is read first because it determines how to interpret everything in the four families. The same copper chart means different things when liquidity is expanding and when it is being withdrawn.

The frame also has a rule-level and a level-level reading, and the rule level matters more. Not just *how much* liquidity, but *what rule is generating it* — see T7.

### Lens 3 — Tension and coiled springs

This is where the edge concentrates. Section 4 is the whole of it. **[ours]**

The short version: agreement across the families is usually already in the price. What is not in the price is a situation where something is being held in place by a mechanism with a finite cost, while the market prices the hold continuing. Those situations pay convexly when they break, because the hold itself suppresses volatility and makes the option cheap while it lasts.

### Lens 4 — What is already priced

About 75–80% of ideas start from the fundamental, and the chart confirms or vetoes. If the picture is good and the tape stinks, do not do it. Sometimes the chart moves first and the story is found afterward. **[FXLM]**

Both directions are legitimate and the bot logs which one it used, because they have different failure modes. Fundamental-first fails by being early and stubborn. Chart-first fails by retrofitting a story onto a move that already happened. A chart-first idea must be labeled as such and is held to a harder falsifier.

The veto is not advisory. A good picture with a bad tape does not get sent to Micro. It goes to the ledger as waiting on tape.

## 3. The pack

Four families plus the overlay. Coverage claim is **[FXLM]**; the series names are **[ours]** and are a starting list for Nathan to cut and extend.

### 3.1 Windows

Every series is looked at in three windows: daily, weekly, monthly, each roughly 8–20 bars. **[FXLM]** ("roughly" is his, keep it — do not harden it into an exact bar count.)

The three windows do different jobs, and this is what makes the pack more than a dashboard:

- **Daily (~8–20 days)** — is something happening now.
- **Weekly (~8–20 weeks)** — is it a move or a wiggle.
- **Monthly (~8–20 months)** — is the *level* somewhere unusual, and has this thing been still for a long time while its drivers moved. The monthly window is where pins become visible. A series flat for a year while everything that should drive it moved a long way is the single most useful observation the pack produces.

A disagreement between windows in the same series is itself information: daily up against monthly down is a rally in a downtrend, not a turn, until the weekly agrees.

### 3.2 Family 1 — Equity groups

Read as the market's vote on growth, and on which part of the cycle is being paid.

- **US index level:** S&P 500, Nasdaq 100, Russell 2000, S&P 500 equal weight against cap weight
- **US cyclical groups:** semiconductors, banks, regional banks, homebuilders, transports, autos, airlines, retail, industrials, materials, energy, oil services, copper miners
- **US defensive groups:** staples, utilities, healthcare, REITs, telecom
- **Non-US:** Euro Stoxx 50, DAX, FTSE 100, Nikkei 225, TOPIX, TOPIX banks, Hang Seng, HSCEI, CSI 300, KOSPI, TAIEX, Nifty 50, Bovespa, Mexico IPC, TSX, ASX 200
- **Ratios, which often read cleaner than levels:** cyclicals against defensives, small against large, equal weight against cap weight, semis against the index, banks against the index, KOSPI and TAIEX against world equity

KOSPI, TAIEX, semis, transports and copper miners are in here as global cycle instruments, not as country or sector bets.

### 3.3 Family 2 — Commodities

Read as the physical world's answer, which cannot be talked up.

- **Energy:** WTI, Brent, the WTI curve front against twelve months out, US natural gas, European TTF, gasoline crack, distillate crack
- **Industrial metals:** LME copper, aluminium, zinc, nickel, iron ore, met coal
- **Precious:** gold, silver, platinum, gold against silver, gold priced in EUR and in JPY
- **Ags:** corn, soybeans, wheat, sugar, coffee, cotton, live cattle
- **Composites and ratios:** a broad commodity index, copper against gold

Curve shape and inventories belong with this family and are not price charts — see T2. Backwardation against contango tells you whether the tightness is now or expected, and they are frequently the same series disagreeing with itself.

### 3.4 Family 3 — FX crosses

"Every currency cross he cares about" **[FXLM]** — the qualifier is the point. This is an explicitly chosen subset, not a matrix.

- **Dollar and majors:** broad dollar index, EURUSD, USDJPY, GBPUSD, USDCHF, USDCAD, AUDUSD, NZDUSD
- **Crosses without the dollar, which isolate the non-dollar story:** EURJPY, AUDJPY, CADJPY, EURCHF, EURGBP, AUDNZD
- **Asia:** USDCNH, the CNY fix against CNH, USDKRW, USDTWD, USDINR, USDIDR
- **Commodity and high-carry EM:** USDMXN, USDBRL, USDZAR, USDCLP, USDTRY
- **Reads:** AUDJPY as a risk and cycle proxy, USDCLP against copper, USDKRW and USDTWD against semis

Where a cross is managed rather than floating, it belongs in the tension ledger as well as here, because a managed price gives information through the *cost of managing it* rather than through its level.

### 3.5 Family 4 — Global fixed income

"Every fixed income market around the world" **[FXLM]**. This family carries the price of money, and it is the family most likely to be right when it fights the equity family.

- **US:** 3-month bills, 2y, 5y, 10y, 30y; 2s10s and 5s30s; 10y real yield; 5y5y breakeven; the implied policy path from dated OIS; MOVE
- **Europe:** German 2y, 10y, 30y; Italy 10y and the BTP–Bund spread; the OAT–Bund spread; UK 10y and 30y; Swiss 10y
- **Japan:** JGB 2y, 10y, 30y
- **Other developed:** Canada 10y, Australia 3y and 10y, New Zealand 10y
- **EM local:** Mexico 10y, Brazil 2y and 10y, South Africa 10y, India 10y, Korea 3y and 10y, China 2y, 10y, 30y
- **Credit, which is part of this family and not a separate one:** US investment grade and high yield spreads, CCC against BB, European Main and Crossover, EM sovereign spreads, leveraged loans, a bank CDS basket

Long-end yields and sovereign spreads are also the market's verdict on fiscal credibility, which is why a rising long end alongside a weakening currency is a different animal from a rising long end with a firming currency.

### 3.6 The liquidity overlay

The overlay concept is **[FXLM]**; this construction is **[ours]**.

- **Fed:** the implied policy path, balance sheet size, reserve balances, the reverse repo facility, the Treasury's cash balance, emergency facility usage
- **Other central banks:** ECB, BoJ and PBoC balance sheets, PBoC open market operations, and the aggregate of major balance sheets converted to dollars
- **Credit creation, which is the part that actually reaches the economy:** bank lending by category, lending standards surveys, investment grade and high yield issuance, CLO issuance, fund flows, commercial paper spreads
- **Money against real activity:** money supply growth against nominal growth, and money growth against industrial production — the gap, not either line alone
- **The dollar as the world's liquidity:** the broad dollar, cross-currency basis in EUR and JPY, repo against the policy rate
- **Leverage and positioning:** dealer positions, margin debt, futures positioning, MOVE and VIX against realized volatility

Money against real activity is the overlay's most useful single read, because when they diverge one of them is wrong, and which one is wrong is a tradable question.

## 4. Tension and coiled springs

**[ours]** throughout, except where marked.

### 4.1 What a spring is

A coiled spring is not a stretched chart. It is a specific structure with four parts:

1. **Something is being held** away from where its drivers say it would otherwise be.
2. **Something holds it** — a policy, a buffer, a contract, a crowded position, a correlation, a subsidy.
3. **The hold has a cost**, paid by an identifiable party, and that cost is measurable and finite.
4. **The market prices the hold continuing**, which is what makes the position cheap.

If you cannot name all four, you do not have a spring. You have a chart you like. This test is the whole discipline, and it is what separates this from "things look stretched."

The canonical instance is sterling in the ERM in 1992 **[hist]**: a currency held inside a band by a central bank whose defense cost was visible and finite, at a level its domestic economy could not tolerate, while the market priced the band holding. Every part of the structure was nameable in advance.

Why springs are where the edge is: the hold suppresses realized volatility, and suppressed volatility makes the option on the break cheap at exactly the moment the break becomes more likely. You are not paid for being right about direction, which is usually priced. You are paid for the market having mistaken a temporary hold for a permanent state.

### 4.2 The stillness rule

Most macro processes look at what moved. The Macro bot also looks, every day, at **what did not move that should have**.

A series flat across the monthly window while its drivers moved a long way is the primary signal. The daily pass has an explicit step for this (section 5, step 4), because it will never happen by itself — nothing draws the eye to a flat line.

### 4.3 The types

Each type lists what is held, what holds it, and the measurable cost of the hold. Examples are patterns and historical instances; whether any is live today is a question for the pack, not for this document.

**T1. Administered price, peg, band, or curve control.**
A price set by policy rather than cleared by supply and demand. Currency pegs and bands, managed fixings, yield curve control, deposit rate caps, subsidised energy tariffs, price caps, capital controls.
*Cost of the hold:* reserves spent, balance sheet expansion, the size of the position the defender has been forced to take, how long the defense has run, the gap between the onshore and offshore price of the same thing.
*Release:* discontinuous. The move on the break is usually a multiple of the daily range that preceded it, because the pin suppressed the range. **[hist]** ERM 1992, the Swiss floor in 2015.

**T2. A buffer running out.**
A price held by a stock that is being drawn down, or capped by a stock being built. Inventories, spare production capacity, strategic reserves, storage, and any queue with a finite length.
*Cost of the hold:* the buffer's remaining size in days of cover, and its rate of change. This type is unusually honest because the buffer is countable.
*Release:* when the buffer empties, price stops being set by inventory and starts being set by flow, and the flow-clearing price can be far away. Curve shape usually moves before the level does.

**T3. Scheduled repricing.**
A price frozen by contract that must meet spot on a known date. Debt maturity walls, fixed-rate borrowing rolling to current rates, hedges expiring, power and supply contracts, wage rounds, index rebalances, fiscal provisions lapsing.
*Cost of the hold:* nothing, which is what makes this type distinctive — the hold is free until the date, then it is total.
*Release:* dated. This is the only type that reliably supplies its own clock, which makes it the best fit for the `clock` field and the easiest to size. Its failure mode is that the date is known to everyone, so check whether it is priced before assuming it is edge.

**T4. Suppressed volatility and crowded carry.**
Realized volatility falls because a large agent is absorbing supply, or because selling volatility has become a business, or because a carry trade has become consensus. Position sizes then grow, because risk models read low volatility as low risk.
*Cost of the hold:* the size of the position being carried, the carry earned against the volatility being sold, implied against realized volatility, and how much of the market's stability depends on one participant continuing.
*Release:* nonlinear and self-feeding, because the unwind removes the agent that was suppressing the volatility.

**T5. Crowding, and its mirror.**
Everyone already owns it. The fundamental can then improve without the price rising, because there is no marginal buyer left; and a small disappointment produces a large move, because the exit is the same door for everyone.
*Cost of the hold:* concentration of ownership and positioning, and how much of the story is in the price already.
*Release:* the interesting version of this type is the **mirror** — an asset that is hated, under-owned and cheap, whose fundamental has quietly turned. That is a spring pointing up, and it is systematically easier to find than a top. The existing `skew` field on theses is doing this job at the name level; Macro does it at the world level.

**T6. Two prices for one risk.**
The same risk trading at two prices because of a segmentation. Onshore against offshore currency, local against hard currency sovereign debt, physical against paper commodity, cash against futures, cross-currency basis, credit spread against the equity volatility of the same capital structure.
*Cost of the hold:* whoever is financing the gap is paying to keep it open — name them. **If you cannot name who pays, the gap is structural and is not a spring.** Some segmentations are permanent and this type produces the most false positives of any on the list.
*Release:* usually when the financing of the gap becomes expensive, not when the gap becomes wide.

**T7. A policy rule about to change.**
Not the level of liquidity but the rule generating it. A central bank or government whose stated reaction function is becoming incompatible with its data or its politics.
*Cost of the hold:* the credibility being spent, and the growing distance between the rule's implied action and what the data calls for.
*Release:* every asset priced off the old rule reprices at once, which is why this type has the widest blast radius. This is Lens 2 read one level down, and it is the most valuable use of the overlay.

**T8. A leverage premise expiring.**
Leverage sized on a correlation that is about to stop holding. The clearest case is bonds hedging equities, which requires inflation to be quiet; when inflation leads instead, the hedge fails and strategies sized on the old relationship must sell both legs at once.
*Cost of the hold:* how much leverage depends on the relationship, and whether the condition that produced the relationship still exists.
*Release:* things fall together that are not supposed to fall together. Correlation regime changes are visible in the monthly window before they are explicable.

**T9. The bottleneck moving.**
The obvious scarce thing gets priced. The spring is in the input to the input, which nobody has re-rated. Power and grid equipment behind computing demand, tools and substrates behind chips, refining behind crude.
*Cost of the hold:* none. This is a knowledge gap rather than a held price, so it belongs to the ledger but is a weaker member of this list — it is edge from looking one step further down a chain, and it decays as others look.
*Release:* gradual re-rating rather than a break, so expect no clock and size accordingly.

**T10. A reflexive loop, as an amplifier on any of the above.**
Price affecting fundamentals affecting price. Dollar debt against a falling currency, a sovereign's yields against its solvency, collateral values against lending capacity. **[hist]** This is Soros's contribution and should be labeled as such, not folded into Druckenmiller.
*Cost of the hold:* whatever is currently interrupting the loop.
*Release:* the loop changes sign, and the move overshoots what the fundamental justifies in both directions.

### 4.4 The tension ledger

The ledger is the Macro bot's memory and its main deliverable over time. Springs mature over months, so a process that only produces a daily opinion cannot hold one. Each entry carries:

- what is held, and away from what
- what holds it, and which type from 4.3
- the cost of the hold, and the direction that cost is moving
- what the market currently prices
- what would release it, and what would prove it wrong
- the clock, or an explicit "no clock"
- state: **holding / pressure rising / defense weakening / released / dead**
- the expression class, and the note that Micro owns the instrument

Two disciplines that keep the ledger honest:

**A spring with no clock and no releasing mechanism is a trap, not an idea.** A pin can hold far longer than a position can be carried. Cheap convexity with no clock is a slow bleed, and the bot should say so in the entry rather than discovering it later.

**"Released" and "dead" must be written down.** A ledger that only accumulates is a list of grudges. When a spring releases, the entry records what the move actually was against what was expected, and that is the only way this process learns anything.

## 5. The daily pass

Same order every day. Steps 4 and 6 are the ones that do not happen unless they are forced, so they are numbered steps rather than good intentions.

1. **Frame.** Read the overlay. What force is in charge, and did that change? Everything after this is interpreted through the answer.
2. **Read the four families** in their three windows. Direction per family, and any window disagreement inside a family. Words, not scores.
3. **What agrees.** Where two or more families say the same thing about the same underlying question — the world's growth rate, the price of money, the dollar, a specific region. Agreement establishes the picture, but note plainly that agreement is usually priced, so it is rarely the trade.
4. **What did not move.** The stillness step (4.2). Which series are flat across the monthly window while their drivers moved. Every candidate here gets tested against the four-part structure in 4.1 before it is allowed into the ledger.
5. **What fights.** Where two families say opposite things about the same question. Do not average them. Name the fight, name which series would resolve it, and say which family you would believe if forced — fixed income fighting equities is usually fixed income being right, but say it rather than assuming it. A fight is a candidate spring, because a fight means something is being held against pressure.
6. **Update the ledger.** Every open entry gets its state confirmed or changed today. Entries that nobody touched are the ones that quietly go stale, so a silent day still requires the pass.
7. **Write a picture, or sit.**

### 5.1 Writing a picture

A picture is only written when there is something to write. It contains:

- the world claim, in plain language, with the mechanism — the `force`, not the label
- which families support it and which fight it
- the liquidity frame it depends on
- whether it came fundamental-first or chart-first, labeled
- the tape check, and whether the tape confirms or vetoes
- what is already priced, and where there is still skew
- the clock and the falsifier
- the expression class, with no ticker
- any ledger entry it belongs to

### 5.2 Sitting

Sitting is a real output and is recorded with its reason. If the overlay is unclear, or the families mostly fight without a nameable spring, the answer is to sit, and that is not a failed day. What is not allowed is a blank day: the ledger still gets its pass, because the value of the pack is cumulative and comes from having looked at the same things yesterday.

### 5.3 The veto

Good picture, bad tape: do not do it. **[FXLM]** The picture is still written, and it sits in the ledger as waiting on tape with the tape condition named. This is the most commonly ignored rule in the whole document and the cheapest one to follow.

## 6. Hand-off to Micro

Macro hands over a world state, an expression class, a clock, a falsifier, and constraints. Micro finds the instrument.

Macro does not suggest a ticker, does not rank names, and does not soften the boundary with "for example." If the expression class cannot be stated without naming something, the class is not yet clear enough to hand over, and that is Macro's problem to fix, not Micro's.

Nathan to confirm: the hand-off object is a `theses_*` card with `claim`, `force`, `clock`, `kill` and `skew` filled, and Micro's work begins at `thesis_candidates`.

## 7. Against fake precision

- No composite macro score, no single number for the world. The pack is read, not scored.
- No numeric triggers unless Nathan sets them. Not "copper up 3% in five days."
- No claimed chart count. Ours is smaller than 272 and that is deliberate.
- No asserting a current market fact without having read the series, with the date.
- Words for state — up, down, flat, turning, unclear. "Unclear" is a permitted and often correct answer.
- Where a number is genuinely countable — days of cover, reserves spent, a maturity date — use it, because that is the opposite of this failure and it is what makes section 4 work.

## 8. Known failure modes of this design

Written down so they can be checked for rather than discovered.

- Calling a permanent segmentation a spring. Guard: T6 requires naming who pays.
- Averaging fights into a mush that sounds balanced and says nothing. Guard: step 5 forbids averaging.
- Retrofitting a story onto a move that already happened. Guard: chart-first must be labeled and gets a harder falsifier.
- Carrying a clockless spring until it bleeds out. Guard: the trap rule in 4.4.
- A ledger that only grows. Guard: released and dead are written.
- Letting the pack drift so the eye never learns normal. Guard: the list is stable and changes are deliberate edits to this file.
- Treating "liquidity, not earnings" as a slogan rather than doing the work in 3.6 and T7.
- Drifting toward the name. Guard: a ticker in Macro's output is a bug.

## 9. Open questions for Nathan

1. Is the funnel mapping in section 1 right — does Macro own `board` and `theses_*` outright?
2. `heat` is already an integer on board cards. Should ledger entries reuse it, or stay with the state words in 4.4?
3. Does the ledger live in this repo as its own file, or as cards in the existing board?
4. Which of the four families do you want cut first if the daily pass is too long to actually do? A pack that gets skipped is worse than a smaller one that runs every day.
5. Is T9 worth keeping, given it has no cost-of-hold and therefore fails the 4.1 test?
