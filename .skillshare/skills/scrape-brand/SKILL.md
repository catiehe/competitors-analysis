---
name: scrape-brand
description: Scrape competitor product data from a Shopify brand and write it to Feishu Bitable
---

# Scrape Brand

Scrapes all SKU-level product data from a Shopify competitor brand and writes it into the Feishu Bitable table.

## Usage

When invoked, this skill will:
1. Ask the user for the brand's Shopify URL and brand name (if not provided as args)
2. Verify the site is a valid Shopify store by checking `/products.json`
3. Run `scraper.py` with the provided URL and brand name
4. Report how many SKUs were scraped and written

## Parameters

- **url** (optional): The Shopify store base URL, e.g. `https://wooland.com`
- **brand** (optional): The brand display name to tag records with, e.g. `Wooland`

## Steps

1. If url or brand not provided, ask the user:
   - "What is the brand's website URL?"
   - "What should we call this brand in the table?"
2. Verify it's a Shopify store:
   ```bash
   curl -s "{url}/products.json?limit=1"
   ```
   If the response doesn't contain a `products` key, tell the user this site isn't supported (not Shopify).
3. Run the scraper:
   ```bash
   source venv/bin/activate && python scraper.py "{url}" "{brand}"
   ```
4. Report the result — how many SKUs were written, or what error occurred.

## Notes

- Only works with Shopify-based stores
- Each brand is tagged with its brand name in the `Brand` field, so it won't overwrite other brands' data
- If you re-scrape the same brand, use `dedup.py` afterwards to remove duplicates
