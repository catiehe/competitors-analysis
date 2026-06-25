---
name: scrape-amazon
description: Search Amazon by keyword using Apify and write the top 10 best-selling products to Feishu Bitable. Use this skill whenever the user wants to search Amazon for products, find best sellers on Amazon, scrape Amazon data, do a keyword search on Amazon, or see what's popular on Amazon. Trigger on phrases like "scrape amazon", "search amazon", "amazon best sellers", "amazon keyword search", "what's selling on amazon", or any time the user names a product category and asks about Amazon.
---

# Scrape Amazon

Searches Amazon by keyword via Apify, filters out sponsored listings and unwanted product types, ranks by review count (popularity proxy), and writes the top 10 results into the Feishu Amazon Bitable table.

## Parameters

- **keyword** (required): The search term, e.g. `merino wool sweater`
- **exclude** (optional): Comma-separated words to filter out from product titles. Default: none

## Steps

1. If keyword not provided, ask: "What keyword do you want to search on Amazon?"
2. Run the scraper:
   ```bash
   cd /workspaces/competitors-analysis && source venv/bin/activate && python scraper.py amazon "<keyword>" "<exclude>"
   ```
   If no exclude words, omit the second argument.
3. Once complete, print a summary table: rank, product title (truncated), review count, price.
4. Confirm how many records were written to Feishu.

## Notes

- **Step 1 — Search scraper:** Apify actor `JyRjxUswjrRheOdmh` — fetches up to 50 results, filters sponsored + excluded words, sorts by review count, takes top 10
- **Step 2 — Detail enrichment:** Apify actor `junglee~amazon-crawler` — runs on the top 10 ASINs to pull category path, BSR rank, bullet points, color variants, sizes, and stock status
- Data goes to `FEISHU_AMAZON_BASE_ID` / `FEISHU_AMAZON_TABLE_ID`
- **Fields captured:**

| Field | Source |
|---|---|
| Title, Brand, ASIN | Search actor |
| Price, Original Price, Discount % | Search actor |
| Rating, Reviews, Badge | Search actor |
| Product URL, Image, Search Keyword, Date Collected | Search actor |
| Category | Detail actor (Amazon breadcrumb path) |
| BSR Rank | Detail actor (e.g. "#1 in Women's Thermal Underwear") |
| Bullet Points | Detail actor (first 5 feature bullets) |
| Colors | Detail actor (all color variants) |
| Sizes | Detail actor (all size variants) |
| In Stock | Detail actor (availability) |

- Total run time: ~2–4 minutes (search ~30s + detail ~1–3min for 10 products)
- **Feishu table must have the new columns added before running** — add text columns named: Category, BSR Rank, Bullet Points, Colors, Sizes, In Stock
