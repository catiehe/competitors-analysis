---
name: scrape-tiktok
description: Search TikTok Shop by keyword using Apify and write the top 10 best-selling products to Feishu Bitable. Use this skill whenever the user wants to search TikTok Shop for products, find best sellers on TikTok Shop, scrape TikTok Shop data, do a keyword search on TikTok Shop, or analyze what's selling on TikTok Shop. Trigger on phrases like "scrape tiktok", "search tiktok shop", "tiktok best sellers", "tiktok keyword search", "what's selling on tiktok", or any time the user names a product category and asks about TikTok Shop.
---

# Scrape TikTok Shop

Searches TikTok Shop for a keyword via Apify, filters out unwanted product types, ranks by 30-day sales volume, and writes the top 10 best sellers into the Feishu TikTok Bitable table.

## Parameters

- **keyword** (required): The search term, e.g. `merino wool`
- **exclude** (optional): Comma-separated words to exclude from product names. Default: `sock`

## Steps

1. If keyword not provided, ask: "What keyword do you want to search on TikTok Shop?"
2. If exclude not specified, default to `sock` and mention this to the user.
3. Run the scraper:
   ```bash
   cd /workspaces/competitors-analysis && source venv/bin/activate && python scraper.py tiktok "<keyword>" "<exclude>"
   ```
4. Once complete, print a summary table of the top 10 results: rank, product name (truncated), 30D sales, and price.
5. Confirm how many records were written to Feishu.

## Notes

- Uses Apify actor `ukNOBkY1TUxHNE8os` (TikTok Shop Search Scraper, US region)
- Fetches up to 50 products from Apify, filters excluded words, sorts by 30-day sales, takes top 10
- Data goes to `FEISHU_TIKTOK_BASE_ID` / `FEISHU_TIKTOK_TABLE_ID` — a separate table from the Shopify scraper
- The Apify run takes roughly 30–90 seconds
- Cost: ~$0.012 per result (about $0.60 for 50 results)
- To pass multiple exclude words: `python scraper.py tiktok "merino wool" "sock,glove,hat"`
