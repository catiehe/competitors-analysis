# Competitor Analysis Toolkit

An AI-assisted competitive intelligence tool for wool/merino apparel brands. Scrapes product data from Shopify competitor stores, Amazon, and TikTok Shop, stores it in Feishu Bitable, and generates structured product development reports.

---

## What It Does

1. **Scrape competitor data** — pull SKU-level product, price, color, and size data from Shopify stores; keyword search results from Amazon and TikTok Shop
2. **Store in Feishu Bitable** — all records land in shared tables for team review
3. **Generate analysis reports** — AI-assisted reports covering pricing, color range, sizing, category mix, and strategic recommendations

---

## Scraper

All scraping is handled by a single entry point:

```bash
source venv/bin/activate

# Shopify brand — scrape all SKUs
python scraper.py shopify <url> <brand> [keyword_filter]

# Amazon — top sellers by keyword
python scraper.py amazon <keyword> [exclude1,exclude2] [top_n] [max_fetch]

# TikTok Shop — top sellers by keyword
python scraper.py tiktok <keyword> [exclude1,exclude2] [top_n]
```

**Examples:**

```bash
python scraper.py shopify https://wooland.com Wooland
python scraper.py shopify https://sheepinc.com SheepInc merino
python scraper.py amazon 'merino wool sweater' sock,yarn
python scraper.py tiktok 'merino wool' sock,glove
```

---

## Skills (AI Agent Commands)

The following slash commands are available inside Claude Code (and other agents after `sync-skills.sh`):

| Skill | What it does |
|---|---|
| `/scrape-brand` | Scrape a Shopify competitor into Feishu |
| `/scrape-amazon` | Search Amazon by keyword, write top 10 to Feishu |
| `/scrape-tiktok` | Search TikTok Shop by keyword, write top 10 to Feishu |
| `/competitor-analysis` | Generate a full product development report from Feishu data |

---

## Reports

Generated reports are saved to `reports/` as Markdown files:

- `Wooland_2026-06-19.md`
- `Unbound_Merino_2026-06-19.md`
- `Minus33_2026-06-20.md`
- `Duckworth_2026-06-20.md`

---

## Environment Variables

Create a `.env` file (or set in Codespaces secrets):

```
# Feishu app credentials
FEISHU_APP_ID=
FEISHU_APP_SECRET=

# Shopify scraper table
FEISHU_BASE_ID=
FEISHU_TABLE_ID=

# Amazon scraper table
FEISHU_AMAZON_BASE_ID=
FEISHU_AMAZON_TABLE_ID=

# TikTok scraper table
FEISHU_TIKTOK_BASE_ID=
FEISHU_TIKTOK_TABLE_ID=

# Apify (for Amazon + TikTok scrapers)
APIFY_API_TOKEN=
```

---

## Other Utilities

- `dedup.py` — remove duplicate records from Feishu tables
- `create_wiki_doc.py` — publish reports to Feishu wiki

---

## Dev Container

Built on [calvinw/ai-agentic-tools](https://github.com/calvinw/ai-agentic-tools). Includes Claude Code, OpenCode, Copilot, Crush, Gemini, and Codex pre-installed. See `CLAUDE.md` for the full container reference.
