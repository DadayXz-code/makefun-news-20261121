# The World Today — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/DadayXz-code/makefun-news-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/DadayXz-code/makefun-news-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page newspaper front page summing up the world's news of Saturday
21 November 2026: 21 stories across 9 regions, drawn as original
illustrations (no photographs, no copied artwork).

## What the program does

`main.ts` (Node 22, standard library only) copies the front page image
shipped beside it (`entry.png`, 1024×1024, ~155 KB) to `/output/entry.png`.
No network, no clock, no randomness: two runs write byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## How the image was made

`generate.py` (Python 3 + Pillow, build-time only) draws the whole page:
masthead, ticker strip, lead story, two secondary stories, three story
cards, and a "Day in Brief" column. Every picture is drawn with code —
flat vector-style scenes (a climate-summit globe and thermometer, Riyadh's
skyline under interceptor fire, the Andes with a seismograph trace, a
Dnipro bridge, server racks, the UK and EU flags). Story facts were
checked against same-day reporting.

## Stories on the page (21)

- **Lead — Climate:** COP31 goes into overtime as the fossil-fuel row
  deadlocks talks (nearly 200 nations, draft omits fossil fuels).
- **Middle East:** Coalition intercepts three Houthi missiles aimed at Riyadh.
- **Peru:** Magnitude 6.7 quake shakes the Peruvian Andes (near Carhuamayo,
  Junín, 108 km deep).
- **Ukraine:** Fresh Russian strikes — 148 drones hit 19 sites.
- **United States:** FBI and Agriculture Department hit by hackers.
- **Britain/Europe:** London and Brussels sign biggest deal since Brexit.
- **In brief (15):** Kryvyi Rih strike; Zaporizhzhia kindergarten attacked;
  six Houthi workshops destroyed; COP31 extra day; youth climate strikes;
  Pakistan internet outage; cost-of-living protests; Poland calls missile
  fall "intentional"; Roundup settlement; BepiColombo reaches Mercury;
  displacement in Ethiopia; Iran drone claim; AI stock rout; UK–EU youth
  scheme; COP31 still split over fossil fuels.

## Entry

Built for make.fun's "Sum up 21 November's world news in one image"
bounty ($100). Payout wallet (see `.makefun/owner.json`):
`GMzu3QobBGo4sYP24deDowGocc47kQeU46eKv619eTcz`.

## License

MIT — see `LICENSE`.
