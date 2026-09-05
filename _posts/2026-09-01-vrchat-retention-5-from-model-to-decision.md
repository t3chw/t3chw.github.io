---
layout: post
title: "VRChat Retention, Part 5: From a Survival Model to a Product Decision"
date: 2026-09-01 08:00:00 +0000
categories: [Data Science, VRChat Retention]
tags: [Bayesian, Survival Analysis, NumPyro, Product Analytics, VRChat, Case Study]
math: true
image:
  path: /assets/img/vrchat-retention/p5-value.png
  alt: Expected active days per segment under two definitions, and where the value is concentrated
---

> **VRChat Retention** — a Bayesian survival analysis of 267,903 VRChat **reviewers on Steam**
> (not all players — see [Part 1](/posts/vrchat-retention-1-a-defensible-question/)), built entirely from public data. Headline: churn risk collapses in the first 90 days and then goes flat for
> three years, and the five engagement segments are on genuinely different clocks.
>
> [Part 1 — the estimand](/posts/vrchat-retention-1-a-defensible-question/) · [Part 2 — three regimes](/posts/vrchat-retention-2-what-the-data-said/) · [Part 3 — when simple models fail](/posts/vrchat-retention-3-when-simple-models-fail/) · [Part 4 — five lifecycles](/posts/vrchat-retention-4-beyond-the-average-user/) · **Part 5 — from model to decision**
{: .prompt-info }

## The short version

**The single most useful sentence in the project:** churn risk is concentrated *in time* in the first 90 days, and *in people* in the weakest segments. That is where a timed intervention has leverage.

It is not where most of the loss is. Nearly twice as many people leave after day 90 as before it. That larger loss is spread evenly across three years, so it needs an always-on product mechanism rather than a campaign. Confusing those two is the easiest expensive mistake to make with this data, and [Part 2](/posts/vrchat-retention-2-what-the-data-said/) spells it out.

**The base, in one line.** Those 267,903 reviewers carry roughly **702,000 user-years** of expected retained time over five years. **18.5% of them — about 49,500 people — are gone inside 90 days**, counting the 8.5% who had already stopped before they wrote their review. After that the rate flattens to about 1.5% a month and stays there for three years.

*(Retained time means days on the roster before someone goes quiet, not hours played. It is the number you would multiply a revenue rate by, not revenue itself. The 702,000 figure is the model's per-reviewer expected days added up across segments. Two other routes that assume no model at all give about 704,000 and 697,000, so it is good to roughly ±0.7%.)*

![Where the base is lost, and where a point of retention is worth most](/assets/img/vrchat-retention/p5-where-to-spend.png)
_Left: how much of each band is inactive by day 90, counting everyone in the band. Right: the user-years bought by raising day-90 survival one percentage point. The per-user prize varies only 1.7× across bands while headcount varies 6.4×, so headcount is the lever — which puts the biggest one in the 1–20h band._

### The nine things I would put in front of a product leadership team

| # | Finding | Confidence | What I would do about it |
|---|---|---|---|
| **1** | Risk is front-loaded *in rate*: a 212× collapse over 90 days, then a plateau varying by only 1.16× for three years. But 18.5% of the base is lost in those 90 days against 35.4% over the three years that follow | **High.** Measured non-parametrically before any model; survives every sensitivity | Put *timed* interventions in the first 90 days, where there is a spike to aim at. Treat the later loss as a continuous problem — an always-on product mechanism, not a campaign with a start date |
| **2** | A third of everything the weakest segment will ever lose, it loses in the first 90 days. For the strongest it is 2.5% | **High** | Set segment-specific review windows: days 7 / 30 / 90 for the light bands, annual for the heavy ones. One shared "day-30 retention" KPI hides both stories |
| **3** | Value tracks headcount almost exactly. The heaviest band is only **1.63×** over-represented, against a structural ceiling of 1.91× at a five-year horizon | **Medium-high.** Depends on which average you take — the error in §1 | Do *not* build a whale strategy on this. It is the finding that makes row 4 work: since value per user barely varies, the prize follows the headcount. Also: average a band over everyone in it, not just the still-active — that inflates the weakest band by 72% |
| **4** | The largest addressable prize is the **1–20h band** — roughly 7,700 user-years for a 10% conversion, against ~5,000 at the top of the ladder | **Medium.** An observational upper bound, not a treatment effect | Run the first onboarding experiment there. The per-user prize is roughly flat across bands, so band size is the whole story, and 1–20h holds 102,299 people |
| **5** | +1 percentage point of day-90 survival in the two weakest bands is worth about **2,800 user-years** — 1% × 118,202 people × ~870 expected remaining days over the rest of the five-year horizon, ÷ 365 | **Medium** | Use it as the unit of account for any onboarding experiment, so cost and benefit are in the same currency before anything gets built. The per-band arithmetic is in the figure above |
| **6** | Expected remaining life *rises* with tenure for weak users (+28.8% by day 90) and is flat for strong ones (+0.1%) | **High** | An LTV model that depreciates new users as they age has the sign backwards. For established users, age is close to irrelevant |
| **7** | Among the five signals Steam exposes, playtime at review swamps the rest: ×2.11 per standard deviation against ×1.30 for the next-largest (games owned) | **High**, but narrow in scope | This is a statement about *Steam's metadata*, not about features in general. First-party behavioural signals — first-week friend adds, populated-instance entries, session length — are untested here and are where I would look next. Note the asymmetry: recommending the game barely predicts *staying* (×1.10) but strongly predicts having *already left* (odds ratio 0.57) |
| **8** | 8.5% of reviews are written by people who had *already stopped playing*, and they are 1.89× as likely to be negative (2.36× within playtime band). They are 8.5% of reviewers and 14.9% of negative reviews | **High** | Split review sentiment by whether the reviewer was still active. A falling score may be a lagging churn signal rather than a satisfaction signal — see [Part 1](/posts/vrchat-retention-1-a-defensible-question/) |
| **9** | Steam sees only about half the platform, so an unknown share of "churn" is migration to standalone hardware | **Low on magnitude, high on direction** | The segment *ordering* survives every false-churn scenario I can construct; the 3.9× spread does not (2.3×–4.0×). This is fixed by first-party instrumentation, not by more modelling |

The evidence for each is below. Sections 1–3 are what the numbers say. **§4 is why the model should be believed**, including the two places it fails. §5 and §6 are the two limits I would raise before anyone acts on this. Along the way there is one error in my own work that changed a headline number by 72% and reversed the recommendation in row 4.

---

## 1. What a user is worth — and the error in my own table

![Gross versus net expected days, and where the value sits](/assets/img/vrchat-retention/p5-value.png)
_Left: expected active days averaged two ways — over every reviewer in the band, and over only those still playing when they reviewed. Right: share of reviewers against share of expected retained time._

Here is a mistake that survived the first write-up and was caught by the audit.

The value table mixed **two different definitions** without saying so. In plain language:

- **Per still-active reviewer** (the *gross* figure) — the average over only the people who were still playing when they wrote their review.
- **Per reviewer in the band** (the *net* figure) — the average over everyone in the band, including the 8.5% who had already gone and therefore contribute zero days.

I published the first under a heading that reads as the second, and then computed the "% of value" column from the second. Read plainly: *averaged over every reviewer in the weakest band, a user is worth 399 days. Averaged over only the ones still playing when they reviewed, 687.* The first is the one to quote, because 41.9% of that band had already gone.

(These are the model's figures. Part 2's table — 401 / 686 / 961 / 1,252 / 1,561 — is the same quantity measured straight from the data with no model at all, and the two agree to within 0.5%. Quote either, but not both in one document.)

| Segment | published (gross) | **correct (net)** | overstatement |
|---|---:|---:|---:|
| under 1h | 687 | **399** | **+72.1%** |
| 1–20h | 781 | 685 | +14.1% |
| 20–100h | 1,000 | 958 | +4.3% |
| 100–1000h | 1,269 | 1,248 | +1.6% |
| 1000h+ | 1,563 | 1,557 | +0.4% |

The distortion is largest exactly where it matters most, because 41.9% of the weakest segment had already gone. It also squashes the headline:

| Spread, weakest → strongest | |
|---|---:|
| published (gross) | 2.28× |
| **correct (net)** | **3.90×** |
| non-parametric Kaplan–Meier check | 3.90× |

One caveat to carry with that 3.90× wherever it is quoted. §6 shows it moving between **2.3× and 4.0×** once Steam-only false churn is allowed for. The *ordering* holds in every scenario. The size of the gap depends on an assumption, so it is not a measured quantity.

The Part 2 benchmark — 401 to 1,561 days, measured without a model — matches NET. That is what identifies NET as the figure comparable to the raw data. Two sections of the project had been quoting different numbers for the same thing, and a cross-check that was sitting there all along resolved it.

**The correction strengthens the business case**, and it points somewhere unexpected. Value is more concentrated than the published figures showed. But the striking thing is how *little* concentration there is in absolute terms:

| Segment | % of users | % of expected future engagement | concentration |
|---|---:|---:|---:|
| under 1h | 5.9% | 2.5% | 0.42× |
| 1–20h | 38.2% | 27.3% | 0.72× |
| 20–100h | 21.9% | 22.0% | 1.00× |
| 100–1000h | 21.9% | 28.6% | 1.31× |
| **1000h+** | **12.1%** | **19.6%** | **1.63×** |

That 1.63× is worth pausing on. Expected days are capped at the five-year horizon of 1,825 days, against a population average of 956. So **no band can exceed 1.91×**, whatever the data says. The heaviest band is at 85% of that ceiling, and the concentration curve is close to flat.

"Value is concentrated" invites a Pareto reading this data does not support. **Value tracks headcount almost exactly.** That is a more useful finding than a whale story, and it is precisely why §3's biggest prize turns out to sit in the biggest band rather than the richest one.

## 2. Where the risk actually lives

![Risk concentration and expected remaining life](/assets/img/vrchat-retention/p5-risk.png)
_Left: how much of each band's five-year churn happens in the first 90 days — both bars are conditional on not having already left at the origin, so numerator and denominator match. Right: expected active days in the next 365, given survival to a point._

| Segment | churn by day 90, **conditional** | churn by day 90, **unconditional** | churn by 5 years | share of 5-yr churn in the first 90 days |
|---|---:|---:|---:|---:|
| under 1h | 29.6% | **59.1%** | 85.7% | **34.6%** |
| 1–20h | 19.0% | 29.0% | 86.2% | 22.1% |
| 20–100h | 8.7% | 12.5% | 79.9% | 10.9% |
| 100–1000h | 3.1% | 4.6% | 66.2% | 4.6% |
| 1000h+ | 1.0% | 1.4% | 39.6% | **2.5%** |

Columns 1, 3 and 4 count only people who had not already left at the origin. Column 2 includes them, and it is the one to quote for "what fraction of this band is gone by day 90". The final column keeps the top and bottom of the fraction on the same basis, which is why it is not mixed.

> **A third of everything the weakest segment will ever lose, it loses in the first 90 days.** For the strongest segment it is 2.5%.
{: .prompt-tip }

Read that against Part 2's plateau: after roughly day 90 the hazard is flat for three years. Post-90 churn is not a danger *window*. It is a constant background rate, so a campaign timed at it buys the same outcome whenever it runs. **Timed** retention effort therefore belongs on new and low-playtime users, and should be judged on a 90-day window.

That is not the same as saying the later loss is small. In headcount it is nearly twice as large. Reducing it is a question of how the product is built, not of when a campaign runs.

### Surviving makes you more valuable — but only if you were fragile

> ### A second correction from the audit
>
> The original "expected remaining life" table added up the curve out to a fixed end point, 1,825 days **from the origin**. So the window shrank as tenure grew: 1,825 days of runway at day 0, but only 1,095 at day 730. Later rows were being measured over a shorter span, which manufactured an apparent decline in value after day 90.
>
> Re-derived on a **fixed 365-day forward window**, so every row is measured over the same span:
>
> | Survived to | under 1h | 1–20h | 20–100h | 100–1000h | 1000h+ |
> |---|---:|---:|---:|---:|---:|
> | day 0 | 237 | 273 | 316 | 344 | 358 |
> | day 90 | **306** | 310 | 327 | 346 | 359 |
> | day 365 | 316 | 314 | 326 | 342 | 357 |
>
> | Segment | day 0 → day 90 |
> |---|---:|
> | **under 1h** | **+28.8%** |
> | 1–20h | +13.3% |
> | 20–100h | +3.6% |
> | 100–1000h | +0.3% |
> | 1000h+ | +0.1% |
>
> **The rise is real and survives the correction. The decline was largely the window closing, not users losing value.**
{: .prompt-warning }

The corrected version is also a sharper statement than the original. The effect is **almost entirely confined to the weak segments**. Heavy users were never at meaningful risk, so surviving 90 days tells you nothing new about them. "Users become more valuable with tenure" is true — for newcomers.

Which has a direct consequence: **an LTV model that depreciates new users as they age has the sign backwards.** For established users, age is close to irrelevant.

## 3. The line this analysis will not cross

The most valuable-looking table in the project is the one that sizes onboarding. It is also where the per-reviewer correction of §1 does the most damage.

| Move | Extra expected days, **gross** | Extra expected days, **net** | 95% CrI (net) |
|---|---:|---:|---|
| under 1h → 1–20h | +94 | **+286** | [277, 295] |
| 1–20h → 20–100h | +218 | **+274** | [267, 280] |
| 20–100h → 100–1000h | +269 | **+290** | [283, 297] |
| 100–1000h → 1000h+ | +295 | **+308** | [301, 316] |

The published version of this table was built by differencing the still-active column. On the corrected net basis the picture changes in a way that matters:

- **The steps are roughly flat** — 274 to 308 days — not a ramp from 94 to 295. The gross version understated the bottom rung by a factor of three, because it quietly excluded the 41.9% of that band who had already gone.
- So **the per-user value of moving someone up a band is close to constant across the ladder**. That means the size of the prize is driven by *how many people are in the band*, not by which rung they sit on.

That reverses the recommendation. Sizing a 10% conversion at each rung:

| Move | People in the lower band | 10% converted, at the net step |
|---|---:|---:|
| under 1h → 1–20h | 15,903 | 1,245 user-years |
| **1–20h → 20–100h** | **102,299** | **7,667 user-years** |
| 20–100h → 100–1000h | 58,730 | 4,665 user-years |
| 100–1000h → 1000h+ | 58,686 | 4,959 user-years |

The published conclusion was that the largest prize sits at the top of the ladder — 100–1000h → 1000h+, 4,738 user-years. That was wrong for **two independent reasons**, and it is worth separating them because only one is the correction above.

**The objective was wrong.** The code picked the band with the largest *per-user step*, and only then multiplied by that band's headcount. It never looked for the band with the largest headcount × step. Doing that correctly on the *original gross* numbers already picks 1–20h → 20–100h at **6,121 user-years**, against 4,738 at the top rung. So the gross/net correction did not flip the band. A coding error did, and the flip was available before any of this.

**The basis was also wrong.** Moving to the correct per-reviewer figures then changes the winning band's magnitude from 6,121 to **7,667 user-years**, and compresses the ladder from a 94→295 ramp to a roughly flat 274→308.

Both matter. Running them together would have credited the statistical correction with a fix that belonged to a `max()` on the wrong key.

It also resolves a tension the original created. §2 says the addressable risk is early and in the weak segments, while the published onboarding table pointed at the strongest segment. Corrected on both counts, the two agree.

Every one of these numbers is still an **observational gap**, not a treatment effect. The framing that survives is:

> An intervention cannot be worth more than the observed gap. If 7,700 user-years does not justify the engineering cost, the idea can be dropped now, without further work. If it does, the next step is **an experiment, not more observational modelling.**
{: .prompt-warning }

One caveat specific to the net figures. Part of the gap between adjacent bands comes from a lower chance of having *already gone at the origin*: 41.9% in the weakest band against 12.4% in the next. An intervention can only capture that part if it reaches people before they stop, which is a harder product problem than retaining someone who is still active. So the net step is an upper bound in that sense too.

## 4. Does the model deserve to be believed?

Everything above rests on a 91-parameter Bayesian model, so this is where I show why it should be trusted — and the two places it should not.

Convergence is necessary and nowhere near sufficient. R̂ and ESS answer one question: *did the sampler explore the model I wrote properly?* They do not answer *is this the right model?* A perfectly converged model can be systematically wrong. So the project checks four separate things.

**Does it reproduce the data?** M5's within-segment survival tracks the Kaplan–Meier curve to a mean absolute error of 0.10 pp across 45 segment-horizon cells, worst case 1.1 pp at day 1,825 in the heaviest segment. M3's pooled fit is 0.22 pp on a daily grid (see Part 3 — the 0.03 pp I originally published was measured only at the model's own knots).

> **A check I have to withdraw.** Earlier versions of this project cited `(1 − π₀) × S₍t>0₎(t)` reproducing the all-users curve to 0.03 pp, and called it the evidence for splitting the population in two. It is not evidence of anything.
>
> When every zero-duration record is an event at t = 0, that relationship holds **as a matter of algebra**, whatever the data looks like. I checked it at twelve horizons and the ratio is constant to 5e-14. All it re-tests is whether M3 fits the `t > 0` curve, which an 18-parameter model does by construction. The two-part structure is justified by the *shape* of the data — a smooth curve cannot put weight on a single point — and by the fact that the atom behaves differently. Not by that identity.

**Does the complexity generalise?** Every model is scored on the same fixed 25,000 people. Compared person by person against its nearest rival, M5 is ahead by 2,493 ± 66 — 38 standard errors. A second method, which asks what mixture of the seven models predicts best, gives M5 a weight of 0.948. That is a second summary of the same evidence, not a second source of it.

**Are the intervals honest?** Partly. Part 4 showed that M5's interval for the population-wide number does not contain the value measured from the data. I report that rather than only the tests it passes.

**Do the priors matter?**

![Churn-rule and prior sensitivity](/assets/img/vrchat-retention/p5-robustness.png)
_Left: the 5-year expected-days table (Kaplan–Meier, all users) re-estimated under four definitions of churn. Right: the 5-year gross RMST per segment re-estimated under four priors._

The model was refit under four priors — a 50× span on the hierarchical scale and 17× on the level — including one deliberately centred on a hazard **55× too high**. **The largest movement in any published number was 0.09%.** (The saved table is rounded to a tenth of a day, so 0.09% is as precise as it can honestly be stated; at full precision it is 0.092%.)

That converts "the prior is defensible" into "the prior does not matter", and only the second can be tested. But I should be honest about what it proves: **almost nothing.**

With 245,102 people and 748 events in the thinnest interval, no prior of this kind could have moved the answer. I make exactly that argument in Part 3 to dismiss the random-walk smoothing prior, so presenting the same foregone conclusion here as evidence would be having it both ways. It is a null result I expected.

**The test that could actually have failed is the interval grid.** Every result in this series rests on 18 hand-chosen cut points, placed where Part 2 said the hazard was moving. If the answers depend on that choice, nothing else matters.

So I refitted on four grids: the published one, a coarser 9-interval grid, a 35-interval grid with extra cuts in between, and a 19-interval grid spaced by powers of ten and deliberately *not* lined up with Part 2's bands.

| Grid | Intervals | Plateau variation | S(90), lightest band | 5-year net days, lightest → heaviest | Spread |
|---|---:|---:|---:|---:|---:|
| published | 18 | 1.08× | 70.4% | 399 → 1,557 | 3.90× |
| coarse | 9 | 1.03× | 70.3% | 397 → 1,548 | 3.90× |
| fine | 35 | 1.12× | 70.4% | 399 → 1,559 | 3.91× |
| log-spaced, unaligned | 19 | 1.08× | 70.4% | 398 → 1,549 | 3.89× |

Survival at day 90 is identical to a tenth of a point across all four. The segment spread moves by 0.5%. The plateau is flat on every grid. That one could have gone the other way, and it did not.

The churn rule gets the same treatment. At 7, 14, 21 and 30 days of inactivity the *levels* move by up to 8.3%, as they must — a 7-day rule labels more people churned. But the **ordering of segments and the direction of every conclusion are unchanged across the whole range**, and the top-to-bottom spread stays between 3.80× and 3.96×.

The decisions rest on the ordering, so they survive. Absolute figures should always be quoted with the rule attached: "median 962 days on a 14-day inactivity rule".

> **The audit, in numbers.** 177 automated checks, all of which I re-ran while writing this series. 30/30 likelihood checks: eight are direct comparisons against SciPy, at ordinary values *and* deep in the censored tail, agreeing to machine epsilon; the rest are internal identities, of which the loosest is a numerical-quadrature check agreeing to 2.8e−5. 30/30 estimator checks against independent implementations — Kaplan–Meier against `lifelines` to about 1e-13, RMST to about 2e-14 (both are worst-case relative differences, and both sit a hair above the round tolerance I used to quote). 117/117 published-number checks against the saved posteriors. And a clean 23-step re-run from an empty output directory, which I *did* execute for this write-up: 21/21 tables and every posterior byte-identical, because the MCMC is seeded.
>
> **And none of those checks found any of the errors reported in this series.** Automated checks catch arithmetic. They do not catch a quantity being defined two ways in two sections, or a fit statistic scored against the wrong population. That is what the manual audit is for, and it is why reproducibility is not the same thing as correctness.
>
> **The count was itself wrong, which is the smallest possible version of the same lesson.** This series first said 97, on the assumption that the published-number gate ran 37 checks. It ran 28 — so the project's original figure of 88 had been right, and "97" was a correction that made things worse. The gate has since been extended to cover every quantity the audit disputed (the net onboarding steps and which band maximises headcount × step, the unconditional day-90 churn, the 18.5/35.4 split, the concentration ceiling, and M3 scored on a daily grid), which is what it should have covered all along. It now runs 117 — including gates on the two claims a later pass retracted, so they cannot be quietly restored, and on the four things a fifth pass found — and the total is 177. I found that by running the script instead of reading the claim about it.
{: .prompt-tip }

## 5. One coefficient that is genuinely not identified

46% of Steam profiles are private, so `games_owned` is missing for nearly half the sample. Two defensible treatments give two different answers:

| Treatment | multiplier |
|---|---:|
| median imputation (published) | ×1.30 |
| complete cases only | ×1.44 |

An 11% span, and nothing in this data prefers one end. The honest statement is not a single number. It is that this coefficient is not pinned down better than about ±5% around its midpoint, and every version of it should be read that way.

A third treatment, filling in the missing values from a model, returns ×1.20. I am *not* offering it as a third estimate, and the project's own script says why not. The filling-in model ignores everything else about the person (`log_games ~ Normal(μ, σ)`, with no other covariates and no outcome). That breaks a standard requirement of the method and pushes the pooled coefficient toward zero — exactly the direction observed.

What that run *does* produce, and what is worth keeping, is where the uncertainty comes from: **43.6% of this coefficient's uncertainty is caused by the missingness itself**, against 0.6% for playtime.

Even a correctly built version would close only the *statistical* gap and leave the deeper one wide open. The method assumes the missing values are missing at random, and people who hide their Steam profile are almost certainly not a random subset. Public data gives no way to test that, and saying so is more useful than picking whichever number reads best.

> Two more known issues, uncorrected because they are immaterial: 115 people (0.043%) sit in the under-1h segment because their playtime was *unknown* rather than low — imputation being read as data. ~~And a piecewise-exponential with playtime as a *proportional* covariate on a shared baseline was never fitted.~~ **It has been now — [Part 4 §7](/posts/vrchat-retention-4-beyond-the-average-user/) fits it.** It separates the two things M5 confounds: knowing the playtime band is worth +1,905 elpd, letting its effect move over time only +581 more (23% of the margin). On the published per-segment number, though, the proportional version is 20× worse — 58.0 days of error against 2.9.
{: .prompt-info }

## 6. The threat I actually worry about, and a scenario sweep on it

The priors move the published numbers by 0.09%. The churn rule moves the levels by 8%. Neither is the thing that could break this analysis.

The thing that could break it is that **churn here is Steam-only**. A user who buys a standalone Quest and never opens Steam again is recorded as churned while still playing. That is false churn, it is almost certainly not evenly spread across segments, and no amount of prior sensitivity touches it.

One thing I should not do is pretend to have measured it. Steam accounts for about 51.9% of VRChat's concurrent users (median across 31,936 hourly observations since 2023), and it is tempting to read that as a limit on the damage. **It is not.**

That statistic describes the platform mix of the whole player base, most of which never used the Steam build at all. The number I actually need is the rate at which *Steam reviewers* — people who by definition owned and used the Steam build — later abandon Steam for standalone hardware. That is unmeasured, and nothing in public data measures it.

So this is a **scenario sweep**, not a bound. Suppose some fraction of each segment's *observed* churn events are really migrations off Steam, and re-label that fraction as censored:

![Expected days and the segment spread under four false-churn scenarios](/assets/img/vrchat-retention/p5-falsechurn.png)
_Scenario A is the plausible one — heavier users are the likeliest to own a standalone headset. B is deliberately adverse to the finding. C is a flat 20%._

| Scenario | under 1h | 1000h+ | spread |
|---|---:|---:|---:|
| published (no false churn) | 401 | 1,561 | 3.90× |
| A · rises with playtime (2/5/10/20/35%) | 414 | 1,646 | 3.98× |
| B · falls with playtime (35/20/10/5/2%) | 689 | 1,566 | **2.27×** |
| C · flat 20% | 548 | 1,609 | 2.94× |

Two things come out of this, and only one of them is comfortable.

**The ordering never changes.** In all four scenarios the five segments rank identically, and every level rises. So the published figures are the pessimistic ones. Every recommendation in this post rests on the ordering rather than on the levels, which is why they survive.

**The size of the gap is genuinely uncertain.** The spread runs from 2.3× to 4.0×, depending on an assumption I cannot test. So "3.9×" should be read as "3.9×, if going quiet on Steam means going quiet", not as a measured quantity. Scenario B is the implausible direction — it requires light users to be *more* likely to have moved to standalone hardware — and even it leaves a 2.3× gap.

This is the largest threat to validity in the series. It is not bounded, only swept — and it is the one first-party data would eliminate outright.

It now has a companion, and that one is *not* so tidy. §8 describes a second measurement problem in the same family: because `last_played` is one timestamp rather than a history, **the 14-day rule mislabels more of a recent cohort than an old one**. Excluding the cohort it cannot correct moves the published figures by **2–6%** — but **not all in the same direction**: S(90) and the median improve, while the segment spread narrows from 3.90× to 3.76×, so *that* headline is the optimistic one rather than the pessimistic one. Both are instrumentation problems and neither is fixed by modelling — but only the sweep above pushes uniformly one way, and I should not have said otherwise.

## 7. Three metrics, and the winner changes — plus the rule that follows

| Metric | Winner | What it is asking |
|---|---|---|
| PSIS-LOO elpd | **M5** | which model predicts individual event times best |
| population-average RMST | **M3** (−2 d vs +8 d) | which model gets the marginal number closest |
| S(90), population | **M3** (−0.024 pp vs −0.033 pp) | which model gets the 90-day survival closest |
| segment-level RMST | **M5**, by 26× over M4 | which model gets the *published* numbers closest |

**M3 wins two of the four.** All four measurements are correct. They disagree because they ask different questions, and publishing any one alone would have justified a different model choice.

The honest headline is not that M5 sweeps. It is that **M5 is chosen for the segment-level numbers and pays for it on every population-wide one**, which is exactly the trade the project made on purpose. (The project's own log calls this "three metrics, three winners". Across those three there are two distinct winners, which is one fewer than advertised.)

> **The rule this project follows: score the model on the quantity you will actually use.** elpd picked the right model here, but partly by luck — the population-RMST comparison would have picked the wrong one, and it is the more natural thing to reach for.
{: .prompt-tip }

## 8. What I would do next, in order

![The complete journey](/assets/img/vrchat-retention/p5-journey.png)
_How the argument got here, and the two things that follow from it. Everything above the green row is done; the green row is what this post argues for next._

**1. Run the experiment this model sized.** Randomise an early-engagement intervention among low-playtime users; the outcome stays survival-based (time to operational churn), so the analysis machinery transfers directly. That converts an upper bound into a treatment effect.

Two bridges have to be built before that number is decision-ready, and neither of them is statistical.

**First, units.** User-years are not money. Multiply by your own revenue per active day: at a made-up \$0.05 per active day, 7,700 user-years is about \$140,000 — the figure to hold against engineering cost. I use a made-up rate deliberately. The point is the mechanics, and the real rate is something only VRChat has.

**Second, reaching the people.** The 102,299 people in the 1–20h band are *reviewers*, identified by their playtime at the moment they wrote a review. To run the experiment you need to find the equivalent users in advance, from your own telemetry, without waiting for them to write anything. That is an instrumentation task, and it is the same one that fixes the Steam-only blind spot.

**2. ~~Validate across time, not just across people.~~ Done — and it found something.** The model comparison here holds out a random sample, which assumes one year's cohort behaves like another's. Part 2 shows that assumption is false — it is what kills the year-3 hazard rise. So the score tells you the model predicts a held-out 2019 reviewer from other 2019 reviewers, not that it predicts next year's from this year's.

I have since run it, and it took four attempts to read correctly — the first three were wrong.

**What it supports:** cross-cohort error is **1.8–4.4 percentage points** of mean error in S(90) per segment, against **0.30 pp** (sd 0.13 over 200 seeds) for a random hold-out *within* cohorts. So **every elpd in this series understates the error you would get on a genuinely different cohort** by roughly an order of magnitude — and a different cohort is the only thing a retention team ever predicts. The ranking does not change, and stratification still helps.

**What it does not support** — and I claimed it for a while — is that the model degrades specifically going *forward in time*. Placebo forward splits run entirely inside the fully-observed region give 1.77–4.39 pp; the headline 3.43 pp sits inside that range. Nor is any tidy "8.7× degradation" defensible: its denominator was a single random draw from a 0.07–0.69 pp distribution.

> **And it turned up a data problem worth more than the validation.** `last_played` is a single timestamp, not a session history. For a reviewer we have only watched briefly, any lull in the 14 days before collection is recorded as terminal churn — while an identical lull by an old reviewer is invisible, because they came back and the timestamp moved forward. **So the churn rule's error rate depends on how long we have watched someone.** Measured S(90) by review cohort runs 87.0% (2020) down to **57.7%** for 2026, which has 149 days of median exposure; hold the observation window fixed and the collapse disappears entirely.
>
> The 2026 cohort has no reviewer with even a full year of follow-up, so it cannot be corrected — only excluded. Excluding it moves the published figures by **2–6%**, and **not all the same way**: S(90) 81.5% → 83.2% and the median 962 → 1,015 days, but the segment spread 3.90× → 3.76×, so *that* headline is the optimistic end rather than the pessimistic one. The day-zero atom is not part of this at all — it is fixed at review time with no follow-up, so it cannot be a window artefact. Ordering and every recommendation are unchanged. It is a limitation, not a retraction.
>
> **Three corrections on my own reading of my own test, which is the more useful story.**
>
> I first "capped the observation window at 365 days" and credited that with removing a bias. **It removes nothing** — every statistic here is at day 90, and censoring at day 365 cannot change a survival curve at day 90. Measured: max difference 0.000e+00, over every subset and every cohort. The work was being done by the *eligibility filter* that came with it, which — because exposure is fixed by review month — is really a cohort filter.
>
> I then took a monotone decay in the train/test gap (−2.14 → −0.42 pp) as evidence the leftover drift was artefact too. It is not: each cohort is **flat** under that filter. Raising the bar does not move a cohort toward the training set, it **drops the worst cohorts out of the test set**.
>
> And I quoted a degradation multiple to three significant figures when its denominator was one random split. **A control that changes the population is not the same as a control that removes a bias, and both produce a tidy monotone line.**
{: .prompt-warning }

**3. Move the clock to first meaningful activity.** Every limitation in Part 1 traces back to the origin being a self-selected review. With first-party data the clock starts at signup, the sample stops being reviewers, and the estimand becomes account lifetime rather than a proxy for it.

**4. Attach a value rate.** Expected active days is not money. Given a revenue rate `r(t)`, the expected value over a horizon is `∫ S(t) r(t) dt`, and the survival curve is already the hard half of that. The dataset here simply has no revenue in it, so the project stops one step short and says so.

**5. Fix the platform blind spot.** §6 *sweeps* it — deliberately not a bound, for the reason given there. Only first-party data eliminates it. Everything in this series would be sharper if "active" meant active on the platform rather than active on Steam.

## 9. What this actually establishes

| Supported | Not supported |
|---|---|
| Post-review retention has three regimes; risk is front-loaded | That this is account lifetime |
| Segments follow different lifecycles, not one scaled curve | That the differences are caused by playtime |
| Addressable risk is concentrated in the first 90 days | That post-90 campaigns can move the flat rate |
| Value is concentrated: 12.1% of users, 19.6% of engagement | That engagement equals revenue |
| The *ordering* of segments is robust to the churn rule, the priors and every false-churn scenario | That the year-3+ hazard rise is behavioural |
| | That the **3.9× spread** is a measured magnitude — it is 2.3×–4.0× depending on false churn |

## 10. What I would take away from this

The final model is a hierarchical Bayesian survival model with 91 sampled parameters generating 90 hazard cells, and it is the least interesting thing in this series.

What decided the outcome happened earlier, and mostly in plain language. What one row represents. When the clock starts. What counts as an event. Which observations are cut short and why. Which features existed at the moment of prediction. Who the sample actually represents. And which apparent findings are side-effects of how the data was collected.

The models are just those answers written down formally. Each rung on the ladder exists because the data rejected the assumption below it, never because a more complicated model would look better in a write-up.

And several numbers in this series are different from the ones I first published, because I went back and checked my own work hard enough to find out they were wrong. The per-segment value table quoted the still-active average as if it covered everyone: +72% on the weakest segment. The expected-remaining-life table used a shrinking window, which manufactured a decline. The fit statistics for Models 1 and 2 were scored against the wrong population. Two convergence diagnoses were also wrong, and both were float32.

For a retention problem, I would rather hand a team a model that says *here is what the evidence supports, here is where uncertainty remains, and here is the experiment I would run next* than one that says *here is the prediction*.

---

*Full series: [Part 1 — the estimand](/posts/vrchat-retention-1-a-defensible-question/) · [Part 2 — what the data said](/posts/vrchat-retention-2-what-the-data-said/) · [Part 3 — when simple models fail](/posts/vrchat-retention-3-when-simple-models-fail/) · [Part 4 — beyond the average user](/posts/vrchat-retention-4-beyond-the-average-user/) · Part 5*

*Fit in NumPyro (Python 3.12 / JAX) in float64, 4 chains, seeded for bit-level reproducibility. Sampler settings vary by model: 1,000 warmup / 1,000 draws at `target_accept` 0.90 for M1, M2 and M4; 1,000/2,000 at 0.95 for M3 (the independent-prior variant, which is the one kept and used downstream — the discarded random-walk variant ran 3,000/3,000); 6,000/8,000 at 0.99 for M5. Data: public Steam review corpus for app 438100, 267,903 reviewers, collected 2026-08-28. No user identifiers and no review text are reproduced anywhere in this series.*
