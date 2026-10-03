---
layout: post
title: "VRChat Part 1: How long do VRChat reviewers keep playing, and who stays?"
date: 2026-10-03 06:20:00 +0000
categories: [Data Science]
tags: [Survival Analysis, Product Analytics, VRChat, Case Study]
description: "A case study on public Steam reviews: how long VRChat reviewers keep playing, the three decisions that make it measurable, and who stays."
---

VRChat retention case study \| Part 1: Who stays \| [Part 2: Who leaves sooner]({% post_url 2026-10-03-vrchat-retention-2-who-leaves-sooner %}) \| [Part 3: A fair test]({% post_url 2026-10-03-vrchat-retention-3-designing-a-test %})

After someone reviews VRChat on Steam, how long do they keep playing? Most keep going for years: 82.1% are still playing 90 days after their review, and the median time to their last session is about three years, though newer reviewers leave sooner. What best predicts who stays is how many hours they had played when they wrote the review, far more than whether the review was positive or what language it was in.

VRChat doesn't publish how long players stick around, but Steam publishes every review, and each one tells you two things about its author: how many hours they had played, and when Steam last saw them play. That's enough to measure retention.

_267,904 Steam reviews \| Feb 2017 to Aug 2026 \| Kaplan Meier in Python \| [notebook](https://github.com/t3chw/VRCHAT_analysis/blob/main/VRChat_1_who_stays.ipynb)_

## 1. The data

- I downloaded every public Steam review of VRChat on 28 August 2026: 267,904 reviews in 30 languages, going back to launch day, 1 February 2017.
- Steam allows one review per account per game, so each review is one person.
- Two thirds are in English and three quarters are thumbs up.
- The typical reviewer had about 30 hours of play when they wrote it.
- I removed Steam IDs, names and profile links, and I don't use the review text.
- Scope: this measures Steam reviewers, not all VRChat players. People who never write a review, or who play only on a standalone headset or phone, aren't in it, and "stopped playing" means stopped playing on Steam.

![Column chart of reviews written each year from 2017 to 2026, peaking at 63,171 in 2022](/assets/img/vrchat/p1_reviews_per_year.png){: .light style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
![Column chart of reviews written each year from 2017 to 2026, peaking at 63,171 in 2022](/assets/img/vrchat/p1_reviews_per_year_dark.png){: .dark style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
_Reviews per year. 2022 was the busiest: one week in July, after VRChat announced new anti cheat software, produced 21,699 reviews. 2026 runs to 28 August._

## 2. Three fixes before any model

Used as is, the raw data would give wrong answers in three ways. Each one needs a fix.

### Fix 1: only use what was known when the review was written

- Most columns describe the player on the download day, often years after the review. Total playtime, for example, is bigger than playtime at review for 90.7% of people, so it already contains the future. I dropped these columns.
- That leaves three inputs: **playtime at review**, **thumbs up or down**, and **language** (English or not).
- There was also a hidden leak. 18% of reviews were edited, and since 29 August 2024 an edit seems to reset "playtime at review" to the playtime on the day of the edit. That affects 19,655 reviews, about 7%. I couldn't confirm this in Steam's documentation; it shows up in the data.

![Column chart by month of edit in 2024: the share of matching playtimes jumps from between 8% and 26% to 100% in September 2024](/assets/img/vrchat/p1_edit_reset.png){: .light style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
![Column chart by month of edit in 2024: the share of matching playtimes jumps from between 8% and 26% to 100% in September 2024](/assets/img/vrchat/p1_edit_reset_dark.png){: .dark style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
_People who played after posting and stopped before editing. Their two playtimes can only match if Steam reset the first one at the edit. From 29 August 2024 on, 96% of them match._

### Fix 2: only count someone as gone after a year without play

- Nobody tells Steam they quit, so you need a rule.
- The obvious rule, "no play in the last 14 days", doesn't work with a single snapshot. Someone on a break at the download looks exactly like someone who quit.
- With that rule, 2026 looks six times worse than 2018 to 2024.

![Column chart of stops per 1,000 players per day by calendar year under a two week rule: 0.35 to 0.56 from 2018 to 2024, 0.67 in 2025 and 2.70 in 2026](/assets/img/vrchat/p1_two_week_rule.png){: .light style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
![Column chart of stops per 1,000 players per day by calendar year under a two week rule: 0.35 to 0.56 from 2018 to 2024, 0.67 in 2025 and 2.70 in 2026](/assets/img/vrchat/p1_two_week_rule_dark.png){: .dark style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
_Stops per 1,000 players per day under the two week rule: 0.35 to 0.56 from 2018 to 2024, then 0.67 in 2025 and 2.70 in 2026. One snapshot can't tell people on a break apart from a real change, so the 2026 jump stays unconfirmed. Part 2 checks 2025 with the stricter rule._

- My fix: end the analysis on 28 August 2025, a year before the download, and use the last year only to confirm. Someone counts as gone only if a full year without play follows their last session.
- The cost: 37,983 reviews from that final year can't be measured yet.

### Fix 3: start the clock at the last edit

- The thumbs (and, since August 2024, the playtime) belong to the latest version of the review, which can come more than a year after the first post.
- So each person's clock starts at the last edit. For the 82% of reviews never edited, that's simply the day it was posted.

> These choices matter more than random noise. Changing the silence rule moves the median across 128 days, and changing the start point moves it by about 120. The statistical uncertainty is much smaller: 1,157 to 1,173 days.

## 3. The retention curve

After the fixes I can follow 229,920 reviewers. They fall into three groups:

- **50.1%** still playing: seen playing after 28 Aug 2025 (115,113)
- **41.3%** left: stopped after the review, then a year without play (94,968)
- **8.6%** already gone: last played before they wrote the review (19,839)

The already gone group wrote their review after they had stopped. Their reviews are more negative: 57% thumbs up, against 78% for everyone else.

**Why not just count who's gone?** Because people had different amounts of time to leave. A simple count says 77.1% of 2017 reviewers are gone, against 22.3% of 2025 reviewers. But 2017 reviewers had 7.7 years to leave and 2025 reviewers had 0.3. Compare them at the same point, day 90, and both years have 79.2% still playing. The Kaplan Meier method avoids this trap by using each person only for as long as I could watch them.

![Survival curve falling from 91.4% at the review to 82.1% at day 90, 72.5% after a year, 50% at day 1,165 and 33.3% after five years](/assets/img/vrchat/p1_survival_curve.png){: .light style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
![Survival curve falling from 91.4% at the review to 82.1% at day 90, 72.5% after a year, 50% at day 1,165 and 33.3% after five years](/assets/img/vrchat/p1_survival_curve_dark.png){: .dark style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
_Share still playing over time, for all 229,920 reviewers. It starts at 91.4% because 8.6% had already stopped. 82.1% at day 90, 72.5% at one year, 33.3% at five years. Past three years the curve rests only on older reviewers, and Part 2 finds that newer reviewers leave sooner._

- Leaving happens early. Of the 9.3 points lost between the review and day 90, 4.5 go in the first week.
- After that the curve drops slowly for years.

## 4. Who keeps playing

These are simple comparisons, one input at a time. Part 2 looks at all of them together.

### Playtime matters most

I split players into five groups by playtime at review: under 1 hour, 1 to 20, 20 to 100, 100 to 1,000 and over 1,000 hours.

![Five survival curves by playtime band, in order: the more hours at the review, the higher the curve](/assets/img/vrchat/p1_playtime_bands.png){: .light style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
![Five survival curves by playtime band, in order: the more hours at the review, the higher the curve](/assets/img/vrchat/p1_playtime_bands_dark.png){: .dark style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
_A year after the review, 32.9% of the under 1 hour group are still playing, against 96.9% of the over 1,000 hour group._

- The lines never cross. More hours at the review means longer play, at every point in time.
- The two lightest groups are 46% of reviewers but 67% of everyone who stops.

### Thumbs down: often written after the player had already stopped

- At first glance the thumbs barely matter: 73.1% of thumbs up and 70.5% of thumbs down reviewers are still playing a year later.
- That's misleading. Thumbs down reviewers are more often heavy players (17.7% have over 1,000 hours, against 8.5%), and heavy players stay either way.
- Among new players, 1 to 20 hours, the gap is 14 points, the biggest of any group. Most of it comes from people who had already stopped when they wrote the review.

![Paired bars for new players: a year later 61.5% against 47.3%; already stopped at the review 8.5% against 28.7%; a year later if playing at the review 67.2% against 66.3%](/assets/img/vrchat/p1_thumbs_new_players.png){: .light style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
![Paired bars for new players: a year later 61.5% against 47.3%; already stopped at the review 8.5% against 28.7%; a year later if playing at the review 67.2% against 66.3%](/assets/img/vrchat/p1_thumbs_new_players_dark.png){: .dark style="border: 1px solid rgba(128, 128, 128, 0.55); border-radius: 6px;" }
_New players, 1 to 20 hours. 28.7% of thumbs down reviewers had already stopped when they wrote it, against 8.5% of thumbs up reviewers. Among those still playing at the review, the gap a year later is under a point._

- That last gap is small partly because of the July 2022 protest, when many players left a thumbs down and kept playing. Leave that week out and the gap is about 4 points: 67.2% against 62.8%.

### Language: mostly explained by playtime

- Reviews in other languages look worse: 66.5% still playing a year later, against 75.5% for English.
- But light players write in English less often. Compare people with the same playtime and the gap is about 7 points under 20 hours, about 1 point at 20 to 100 hours, and none from 100 hours up.

### The July 2022 protest: not more loyal after all

- 19,959 reviewers started their clock in the protest week, 25 to 31 July 2022, against about 528 in a typical week. 91% were thumbs down.
- 26% of them had over 1,000 hours, against 9% of everyone else.
- They look more loyal: 83.6% still playing a year later, against 73.8% for the other summer weeks of 2022.
- Compare people with the same playtime and the difference disappears: never more than 0.6 points worse, and up to 2.3 points better. They looked loyal mostly because so many were veterans.

## 5. What I can and can't say

**I can say**

- About 82% of reviewers are still playing 90 days after their review, and 72.5% after a year.
- About half of the drop by day 90 happens in the first week.
- More playtime at the review goes with much longer play: 33% of the under 1 hour group are still playing a year later, against 97% over 1,000 hours.
- New players with a thumbs down leave more, mostly because many had already stopped when they wrote it.

**I can't say**

- That playing more makes people stay. Heavy players may just be people who already love the game.
- That a negative review makes people leave. Both can come from the same bad experience.
- Whether someone quit VRChat or just stopped playing through Steam.
- Anything about players who never wrote a review.

**Next:** [Part 2]({% post_url 2026-10-03-vrchat-retention-2-who-leaves-sooner %}) models the daily risk of leaving: when it peaks, whether it changed in recent years, and what playtime, thumbs and language add when you look at them together.

---

_Data: Steam's public review feed for VRChat (app 438100), downloaded on 28 Aug 2026. Analysis in Python with pandas, lifelines and SciPy. [The notebook for this part](https://github.com/t3chw/VRCHAT_analysis/blob/main/VRChat_1_who_stays.ipynb) reproduces every result on this page._
