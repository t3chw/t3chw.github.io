---
layout: post
title: "VRChat Part 3: From patterns to a fair test"
date: 2026-10-03 06:20:00 +0000
categories: [Data Science]
tags: [Experimentation, Product Analytics, VRChat, Case Study]
description: "A case study on public Steam reviews: turning retention patterns into a fair, well sized experiment for new players at the moment of a negative review."
---

VRChat retention case study \| [Part 1: Who stays]({% post_url 2026-10-03-vrchat-retention-1-data-and-question %}) \| [Part 2: Who leaves sooner]({% post_url 2026-10-03-vrchat-retention-2-who-leaves-sooner %}) \| Part 3: A fair test

Parts 1 and 2 show who leaves and when, but not what would make anyone stay. For that you need an experiment. This part designs one, works out how big it has to be, and says what I would actually run.

_12,629 new players with a negative review \| power analysis and simulation \| SciPy and lifelines \| [notebook](https://github.com/t3chw/VRCHAT_analysis/blob/main/VRChat_3_designing_a_test.ipynb)_

## 1. Why we need an experiment

- Everything in Parts 1 and 2 is a correlation.
- If you give help only to the players you expect to recover, it will look like it works even if it does nothing.
- Random assignment fixes this. The two groups are alike on average, so a difference in outcome comes from the help, not from who got it.

**What to test:** for new players who leave a negative review and played in the 7 days before it, does help at that moment raise the share who play again between day 76 and day 90?

## 2. Who to test

- In: new players, 1 to 20 hours at the review, with a thumbs down.
- Out: players under 1 hour. About half of their negative reviews came after they had already stopped, and helping someone who has barely played is really an onboarding problem.
- Out: the July 2022 protest week, where negative reviews came with no extra risk of leaving.

| New players with a thumbs down, outside the protest week | Value |
| --- | ---: |
| Reviewers | 12,629 |
| Already stopped when they wrote the review | 27.3% |
| Still playing at day 90, everyone | 58.0% |
| Still playing at day 90, if playing at the review | 79.8% |

Two things shape the whole design:

- More than a quarter had already stopped. No help can reach them, and they water down any effect.
- The rest leave fast. About half of the leaving by day 90 happens within 3 days, and 364 of the 1,831 who leave, about 20%, had their last session within an hour of the review. So the help has to be ready at the review itself: shown at once if the player is online, or else at their next login.

You only know someone has quit in hindsight, so the test needs a rule to guess who is still playing. VRChat's login data could use "at least one session in the 7 days before the review". That drops most of the already gone, but about 3 in 10 of them, 1,006 of 3,450, would still pass.

## 3. What to measure

- Main measure: did the player play at all between day 76 and day 90 after the review? It's the login data version of "still playing at day 90", used all through this series.
- Compare everyone assigned to help with everyone assigned to no help, whether or not they actually saw it. This is called intention to treat (ITT). Comparing only the players who saw the help would break the randomisation, because seeing it depends on coming back.
- Also track play between day 166 and 180, and retained days in the first 180. These show whether help keeps players or only delays them leaving.

## 4. How big the test has to be

I describe the effect as the share of would be leavers that the help keeps. 20.2% of players still playing at the review leave by day 90, so help that keeps 1 in 5 of them lifts the day 90 share by 4.0 points.

The size depends a lot on who you let in:

| Who is let in | only those still playing (best case) | the plan's 7 day rule | already gone included |
| --- | ---: | ---: | ---: |
| Already gone | 0% | 9.9% | 27.3% |
| Day 90 share without help | 79.8% | 71.9% | 58.0% |
| Lift for 1 in 5, points | 4.0 | 3.6 | 2.9 |
| Players per group | 1,429 | 2,293 | 4,393 |

![Line chart on a log scale of people per group against the share of leavers the help keeps: with the already gone included from 17,683 at 10% to 686 at 50%, players still playing from 5,970 to 194, and the plan's 7 day rule between them at 2,293 for 20%](/assets/img/vrchat/p3_sample_size.png){: .light style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
![Line chart on a log scale of people per group against the share of leavers the help keeps: with the already gone included from 17,683 at 10% to 686 at 50%, players still playing from 5,970 to 194, and the plan's 7 day rule between them at 2,293 for 20%](/assets/img/vrchat/p3_sample_size_dark.png){: .dark style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
_Players per group needed for 80% power, by the share of leavers the help keeps. Letting in the already gone multiplies the size 3.0 to 3.5 times. The plan's 7 day rule sits between, at 2,293 per group for 1 in 5._

What drives the size:

- How well the help works. Halve the effect and you need about four times the players. Help that keeps 1 in 10 leavers would need 5,970 per group even in the best case, about 7 years of reviews.
- Players already gone. Letting all of them in triples the size.
- Timing. On the 7 day rule you need 2,293 per group if the help lands at the review, about 3,600 if it lands an hour later, and 5,900 a day later.
- Who sees it. If only half the players see the help, you need about four times as many.

> Keeping 1 in 5 leavers is a lot. Among new players still playing at the review, 82.6% of thumbs up and 79.8% of thumbs down reviewers are still playing at day 90. Closing that whole 2.8 point gap would only take keeping about 1 in 7.

## 5. How long it would take

- About 200 new players a month leave a negative review. About 161 of them would pass the 7 day rule.
- About 830 new players a month write any review.

![Paired bars of months needed: 43.9 and 19.4 with the already gone included, 28.4 and 12.3 for the plan's 7 day rule, 19.7 and 8.3 for players still playing at the review, 4.5 and 1.9 for new players with any review](/assets/img/vrchat/p3_months.png){: .light style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
![Paired bars of months needed: 43.9 and 19.4 with the already gone included, 28.4 and 12.3 for the plan's 7 day rule, 19.7 and 8.3 for players still playing at the review, 4.5 and 1.9 for new players with any review](/assets/img/vrchat/p3_months_dark.png){: .dark style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
_Months of reviews needed if the help keeps 1 in 5 or 3 in 10 leavers. A: already gone included. Plan: the 7 day rule. B: best case, only players still playing. C: new players with any review. D, a login based test on every new player, can't be sized from reviews._

- The plan, if help keeps 1 in 5 leavers: 2,293 per group, about 28 months of reviews, then 3 more months for the day 90 answer.
- The plan, if help keeps 3 in 10: about 12.3 months, then 3 more.
- C, every new player who writes any review: about 4.5 months in the best case, if that help also keeps 1 in 5 leavers. But it answers a wider question.
- Recent players leave a bit sooner than the 2017 to 2025 average, and arrive faster than the rate used here, so the real test may be quicker. The final sizing should use VRChat's current numbers.

## 6. Checking the maths by simulation

- I simulated 2,000 experiments per size, drawing real players at random from those still playing at the review, with help that keeps 3 in 10 leavers.
- At 600 per group the test found the effect 79% of the time; the formula promised 80% at 605. At 300 per group, only 49%.
- Even a well sized test misses a real effect one time in five, so a single "no effect" from a small test says little.

## 7. What success would be worth

- Help that keeps 3 in 10 leavers would add about 4 to 19 retained days per player over the next year, depending on how long the kept players stay.
- In people it's small. About 145 new players still playing at a negative review arrive each month, and about 29 of them leave by day 90. Keeping 3 in 10 means about 9 extra players a month; keeping 1 in 5, about 6.
- That's the bar the cost of the help has to clear.
- A test sized to find an effect can tell you the help works, but not whether it pays. In one simulated run, a 6.3 point lift came with a 95% interval of 2.1 to 10.6 points. If the decision needs that answer, size the test for the smallest lift that pays.

## 8. The plan

| Part | Decision |
| --- | --- |
| Who | new players with 1 to 20 hours at a negative review, with at least one session in the 7 days before it |
| Trigger | the player's first eligible negative review, new or edited to negative. Each player enters once |
| Assignment | random, 50/50, in small blocks within each calendar week |
| Help | one clear action, shown at once in game if the player is online, or else at their next login. Private, and the same for everyone |
| Main measure | any play from day 76 to day 90 after the review, compared as assigned (ITT) |
| Secondary | play from day 166 to 180, retained days in the first 180, survival curves |
| Guardrails | complaints, reports and refunds. The help never asks the player to change their review |
| Protest waves | flagged by a fixed rule and reported apart from the main result |
| Size | redone with VRChat's own data before launch, with interim checks fixed in advance |

Two rules protect the result:

- Check the split. If the two groups split in a way chance would produce less than once in 1,000 runs, check the assignment and logging.
- Only look at the times fixed in advance. Checking every week and stopping at the first good result gives false wins.

## 9. What I would run first

Negative reviews were the right place to find and size this idea, but they're too slow for a first test. On them alone, the test collects its players in about a year only if the help works twice as well as closing the whole thumbs gap, and the prize is a few players a month.

So I would start wider: help for every new player who writes any review (C above), about 4.5 months in the best case, and look at the negative reviewers inside it. The plan above is still the right design for the narrower question: does help work for the players who complained?

## 10. What I can and can't say

**I can say**

- Among new players with a negative review outside the protest week, 58% are still playing at day 90, and 27% had already stopped when they wrote it.
- About 20% of those who leave by day 90 had their last session within an hour of the review.
- The planned test needs about 28 months of reviews for help that keeps 1 in 5 leavers, and about 12 for 3 in 10, plus 3 months to the answer.

**I can't say**

- Whether any help works. That's what the test is for.
- What VRChat's own numbers are. The sizing should be redone with their login data.
- How well this carries over to players who never write a review.
- How public replies on Steam would spill over to other players. That's why the plan uses private help.

**Where this leaves things.** Public reviews got a long way: a clear definition of leaving and a picture of who stays ([Part 1]({% post_url 2026-10-03-vrchat-retention-1-data-and-question %})), a model of the risk that holds up on held out reviewers ([Part 2]({% post_url 2026-10-03-vrchat-retention-2-who-leaves-sooner %})), and a test that's designed and sized. The next step needs VRChat's own data, and a coin.

---

_Data: Steam's public review feed for VRChat (app 438100), downloaded on 28 Aug 2026. Analysis in Python with pandas, lifelines and SciPy. [The notebook for this part](https://github.com/t3chw/VRCHAT_analysis/blob/main/VRChat_3_designing_a_test.ipynb) reproduces every result on this page._
