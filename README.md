# The World in One Day — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Rifat7600/news-image-20261118-5/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard)
[![reward](https://make.fun/badge/news-image-20261118/Rifat7600/news-image-20261118-5/reward.svg)](https://make.fun/bounty/news-image-20261118)

A newspaper front page summing up Wednesday 18 November 2026 in one image:
a four-panel split screen under the banner "THE WORLD IN ONE DAY —
18 NOVEMBER 2026".

- **SUMMIT** — Trump, Xi and Putin meet in Shenzhen at APEC
- **WAR** — Iran war: US base in Kuwait hit
- **STORM** — Cyclone Akvan heads for India
- **GAZA** — Israel opens a new Gaza operation

Plus a ticker with three more stories of the day: the Quad meets in Manila,
GTA VI launches at midnight, and the US loses measles-free status.

## Run it

```sh
python3 generate.py   # draws entry.png (1024x1024) with Pillow
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` is standard library only: it copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`.
