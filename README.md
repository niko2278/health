# RxSavings Guide

Free prescription discount card site operated by DELABARRE INC.

- `index.html` — homepage (US map + GoodRx / National Drug Card)
- `drugs.html` and `*-coupon.html` — one savings page per drug (generated)
- `legal.html` — terms, privacy, affiliate disclosure
- `cards.js` — affiliate links used on every page: edit `CARD_LINKS` here

To add or change a drug page, edit `DRUGS` in `tools/build_drug_pages.py`, then run
`python3 tools/build_drug_pages.py` (also rebuilds `sitemap.xml` and `robots.txt`).
When the custom domain is connected, change `SITE` in that script and run it again.

The previous site is kept on the `ancien-site` branch.
