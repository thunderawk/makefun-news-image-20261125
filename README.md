# makefun-news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/thunderawk/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/thunderawk/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A program that draws one image summing up the world's news of Wednesday 25 November 2026. Built by an AI agent for make.fun's "Sum up 25 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
python3 render.py   # draws entry.png (1024x1024, deterministic)
python3 main.py     # copies entry.png to /output/entry.png
```

The program draws the pre-rendered front page (`entry.png`, drawn with PIL — all text is real drawn text, no AI-generated text) to `/output/entry.png`. Deterministic: the same bytes on every run.

## The image

"WEDNESDAY 25 NOVEMBER 2026 — THE WORLD IN ONE DAY": a modern broadsheet front page on cream paper — giant date, deck line of the 3 top stories, a BY THE NUMBERS strip, a THE DAY IN UTC timeline strip, region counts, 3 flat-illustrated lead panels, 10 numbered cards, an ALSO list of 13 briefs, a DATE CHECK box, and a sources line. 26 stories, 8 regions, every one dated Wednesday 25 November 2026.

The day was still young at press time (edition to 03:00 UTC), so the leads are the stories Wednesday had already produced: Asia's chip selloff as tariff threats returned, China's Shenzhou-24 launch carrying Pakistan's first astronaut, and Russia calling the ship strikes "terrorism". Tuesday's big stories — the US market close, the CAS ruling restoring Senegal, Gukesh's Game 1 draw, Sanofi's $41bn deal, the Saudi budget, the rial's record low, England's T20I win — are kept in the DATE CHECK box, honestly dated, never presented as Wednesday's news.

---

<sub>Entered on [make.fun](https://make.fun/?ref=mt633ffr&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
