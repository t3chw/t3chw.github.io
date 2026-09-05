---
title: VRChat Retention
icon: fas fa-chart-line
order: 4
---

A Bayesian survival analysis of **267,903 VRChat reviewers on Steam**, built entirely from public data, written up as a five-part case study.

> **These are reviewers, not players.** Steam does not publish how many accounts have played VRChat, so the ratio of reviewers to players is unmeasured — and Steam itself sees only about half of VRChat's concurrent users. Every number below describes this population, and the gap to the whole player base is unknown rather than small.
{: .prompt-warning }

Everything is fit in NumPyro (Python 3.12 / JAX) in float64, with convergence gates on every model, PSIS-LOO for model comparison, and credible intervals on every published quantity. Data collected 2026-08-28 from the public Steam review corpus for app 438100.

---

## The business answer, first

The 267,903 reviewers in this dataset carry roughly **702,000 user-years** of expected retained time over five years. **18.5% of them are inactive by day 90** — though 8.5 of those 18.5 points had already stopped playing before they wrote the review, so the true post-review 90-day loss is about 10%. After that, churn settles to a flat ~1.5% a month and stays there for three years.

That sets the strategy for *timed* effort: **the first 90 days, on the light-playtime bands** — that is where risk is concentrated enough for an intervention to have something to aim at. It does not mean the later loss is small. Nearly twice as many people are lost between day 90 and year three as in the first 90 days; that loss is spread evenly, so it needs an always-on product mechanism rather than a campaign.

| Finding | Number | So what |
|---|---|---|
| Risk is front-loaded in *rate*, not in headcount | 212× collapse over 90 days; but 18.5% of the base lost in those 90 days against 35.4% over the three years after | Time interventions to the first 90 days; treat the later loss as a continuous product problem |
| The weakest band front-loads its losses | Among those still playing when they reviewed, 34.6% of its 5-year churn happens by day 90, against 2.5% for the strongest | Segment-specific review windows — day 7/30/90 for light bands, annual for heavy |
| Value tracks headcount, not user quality | The heaviest 12.1% of reviewers hold 19.6% of expected retained time — 1.63× over-represented, against a structural ceiling of 1.91× | Do not build a whale strategy on this. It is why the biggest prize sits in the biggest band, not the richest one. Separately: average a band over *everyone* in it, not just the still-active — that inflates the weakest band by 72% |
| The biggest prize is in the middle, not the top | ~7,700 user-years for a 10% conversion of the 1–20h band, against ~5,000 at the top of the ladder | The per-user prize is roughly flat across bands, so band size is the whole story — run the first onboarding experiment on the 1–20h band |
| Segments are on different clocks | 59% of the lightest band is inactive by day 90, against 1.4% of the heaviest | One shared retention KPI moves mostly when the user mix moves |
| Tenure makes weak users more valuable, not less | +28.8% expected remaining life by day 90 for the weakest band; +0.1% for the strongest | An LTV model that depreciates new users has the sign backwards |

## And the methodological answer

- **Flexibility in *time* beat flexibility in *people*.** A model with five covariates lost to a model with none, by 2,840 elpd, because it had the wrong hazard shape. That is a resourcing lesson, not a curiosity.
- **The hierarchy earned almost none of its margin.** Five independent per-segment fits with no pooling and no sampler tie with the 91-parameter hierarchical model (log predictive density −144,138.3 against −144,138.5). Stratifying is what mattered; the hierarchy was insurance that turned out not to be needed at this sample size.
- **Several published numbers in this project were wrong and are corrected in place,** including one that reversed a business recommendation, and one "validation check" that turned out to be an algebraic identity.

---

## The five parts

**[Part 1 — Turning a Product Question Into a Defensible Statistical One](/posts/vrchat-retention-1-a-defensible-question/)**
Where the clock starts, what counts as churn, why 8.5% of the sample needed a two-part model, and which feature would have leaked. The estimand is post-review retention, not account lifetime, and the distinction is load-bearing.

**[Part 2 — Churn Risk Has Three Regimes, and Only One Is Addressable](/posts/vrchat-retention-2-what-the-data-said/)**
Four questions answered non-parametrically before any model was fitted. The hazard shape rules out every smooth survival family; proportional hazards is rejected on a measured 34× effect-size decay rather than a p-value; and the most interesting-looking finding in the tail turns out to be an artefact of who is left in the risk set.

**[Part 3 — When Simple Survival Models Are Not Enough](/posts/vrchat-retention-3-when-simple-models-fail/)**
Four models, each fitted because the previous one failed in a nameable way. Includes the project's most informative comparison — five covariates losing to none — and a correction I found while writing: two models had been scored against the wrong population.

**[Part 4 — Five Segments, Five Different Lifecycles](/posts/vrchat-retention-4-beyond-the-average-user/)**
The hierarchical stratified piecewise-exponential model, why it is not proportional hazards in disguise, and a convergence failure I diagnosed as structural non-identifiability that turned out to be float32 — reproduced here in a controlled re-run.

**[Part 5 — From a Survival Model to a Product Decision](/posts/vrchat-retention-5-from-model-to-decision/)**
What a user is worth, where the risk lives, the error in my own value table that changed a headline number by 72% and reversed an onboarding recommendation, a scenario sweep on the Steam-only blind spot — deliberately not a bound, and the line between what this evidence supports and what needs an experiment.

---

## The words, in plain English

Every technical term the series uses, in one line each. Nothing here is needed to follow the business answer above.

| Term | What it means |
|---|---|
| **survival analysis** | The maths for "how long until something happens", when some cases have not happened yet |
| **censored** | We know this person lasted *at least* this long, but not how long in total. 24.3% of this data |
| **hazard** | The chance of leaving today, among the people still here. Different from "how many are left" |
| **Kaplan–Meier** | A way to draw the retention curve that handles censored people correctly and assumes no shape |
| **estimand** | The exact quantity you are trying to measure. Get this wrong and everything after it is precise and useless |
| **prior / posterior** | What the model believed before seeing the data, and after. Here the prior barely matters — it moves the answers by 0.09% |
| **credible interval** | The range the model thinks the answer sits in. At this sample size they are very narrow, which is not the same as being right |
| **expected active days (RMST)** | Add up the retention curve over five years. Roughly, "how many days will this person still be around" |
| **elpd / PSIS-LOO** | A score for how well a model predicts data it was not fitted on. Used here only to rank models against each other |
| **piecewise-exponential** | Chop time into pieces and let the risk be a different constant inside each one. No overall shape is assumed |
| **partial pooling / hierarchical** | Let groups differ, but pull thin groups toward the average. It bought almost nothing here — see Part 4 |
| **proportional hazards vs AFT** | Proportional hazards says one group is always X times riskier. AFT says one group's clock simply runs slower. The first was rejected on the data |
| **per reviewer vs per still-active reviewer** | Two ways to average a band: over everybody in it, or only over those still playing when they reviewed. The difference is worth 72% on the weakest band |
| **R̂ / ESS / divergences** | Checks that the sampler explored the model properly. They say nothing about whether the model itself is right |
| **float32 / float64** | How many digits the computer keeps. Two failures in this project looked statistical and were really this |

## What was checked rather than assumed

192 automated checks, all re-run for this write-up: 30 likelihood checks against SciPy and internal identities, 30 estimator checks against `lifelines` and analytic values, 132 published-number checks against the saved posteriors — the last of those extended after the audit to cover the quantities the audit had disputed, which is what a verification gate is for. Proportional hazards, a cure fraction, the smoothing prior, the model parameterisation and the priors were each tested rather than argued for — the priors move the published numbers by 0.09%.

None of those checks found any of the errors reported in the series. Reproducibility is not the same thing as correctness, and the difference is most of what Parts 3 and 5 are about.
