---
name: analyze-amazon
description: >
  Amazon market analysis for merino wool product development, using data collected
  in Feishu Bitable. Use this skill whenever the user wants to analyze Amazon search
  results, understand the merino wool market on Amazon, identify pricing opportunities,
  find product gaps, or generate a strategic report from Amazon data. Triggers on phrases
  like "analyze amazon data", "amazon market analysis", "what's selling on amazon",
  "analyze amazon results", "amazon competitor report", or "what should we develop based
  on amazon".
---

# Analyze Amazon Skill
## For Product Development Teams

This skill produces a two-part professional report based on Amazon product data
collected via the scrape-amazon skill and stored in Feishu Bitable.

- **Part 1** → Objective market data analysis (what Amazon shows us)
- **Part 2** → Strategic product development takeaways (what we do with it)

---

## Data Structure (Feishu Amazon Table Columns)

| Column | Source | Description |
|--------|--------|-------------|
| Text | Search | Full product title |
| Brand | Search | Brand name |
| ASIN | Search | Amazon product ID |
| Price | Search | Current selling price (USD) |
| Original Price | Search | Pre-discount price |
| Discount % | Search | Discount percentage |
| Rating | Search | Star rating (0–5) |
| Reviews | Search | Total review count |
| Badge | Search | Best Seller / Amazon's Choice / etc. |
| Product URL | Search | Link to Amazon listing |
| Image | Search | Product image URL |
| Search Keyword | Search | The keyword used when scraping |
| Date Collected | Search | Date the record was scraped |
| Category | Detail | Amazon breadcrumb path (e.g. Clothing > Women's > Thermal Underwear) |
| BSR Rank | Detail | Best Seller Rank in category (e.g. #1 in Women's Thermal Underwear) |
| Bullet Points | Detail | First 5 product feature bullets (pipe-separated) |
| Colors | Detail | All available color variants (comma-separated) |
| Sizes | Detail | All available size variants (comma-separated) |
| In Stock | Detail | Availability (Yes/No) |

---

## Workflow

### Step 1: Ask for Keyword
If the user has not specified which product category or keyword to analyze, ask:

> "Which search keyword would you like to analyze? (e.g. 'merino wool sweater', 'merino wool base layer', 'merino wool t-shirt')"

If they say "all" or don't specify, fetch all records regardless of keyword.

### Step 2: Fetch Records from Feishu

Use the Feishu API to pull all records from the Amazon table, then filter to only those where `Search Keyword` matches the user's selection.

```python
import requests, os
from dotenv import load_dotenv
load_dotenv("/workspaces/competitors-analysis/.env")

APP_ID     = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")
BASE_ID    = os.getenv("FEISHU_AMAZON_BASE_ID")
TABLE_ID   = os.getenv("FEISHU_AMAZON_TABLE_ID")

token = requests.post(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={"app_id": APP_ID, "app_secret": APP_SECRET}
).json().get("tenant_access_token")

records = []
page_token = None
while True:
    params = {"page_size": 100}
    if page_token:
        params["page_token"] = page_token
    res = requests.get(
        f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BASE_ID}/tables/{TABLE_ID}/records",
        headers={"Authorization": f"Bearer {token}"},
        params=params
    ).json()
    items = res.get("data", {}).get("items", [])
    records.extend(items)
    page_token = res.get("data", {}).get("page_token")
    if not res.get("data", {}).get("has_more"):
        break

# Filter by keyword (case-insensitive match)
keyword_filter = "<user's keyword>"
filtered = [
    r for r in records
    if keyword_filter.lower() in r.get("fields", {}).get("Search Keyword", "").lower()
] if keyword_filter else records
```

Tell the user how many records were found before proceeding.

### Step 3: Run Part 1 Analysis

Work through each dimension systematically using the fetched data.

### Step 4: Generate Part 2

Based on Part 1, produce actionable product development recommendations.

### Step 5: Save Report

Save as markdown to `reports/amazon/` using the format below.

---

## PART 1: Amazon Market Data Analysis

### 1. Market Snapshot
- Total products analyzed, search keyword, date collected
- Number of unique brands
- Badge summary: how many Best Seller, Amazon's Choice, or other badges
- In Stock vs out of stock split

### 2. Price Architecture

**Step 1 — Run a price distribution analysis first:**
Bin all products into $10 increments and count per bin. Read the actual shape — do NOT assume evenly distributed tiers.

Look for:
- **Peak(s):** Where product density is highest → this is the market's "sweet spot" price
- **Valleys:** Natural breaks in density → tier boundaries
- **Long tail:** Sparse high-price zone → premium segment
- **Bimodal vs unimodal:** Multiple peaks often mean different product types (e.g. accessories cheap, base layers mid, sweaters premium)

**Step 2 — Define price tiers based on what you find:**
- **Entry:** Below the main cluster (accessories, basics)
- **Core:** The dominant peak — where most products compete
- **Mid:** Between peaks or slope from peak
- **Premium:** Sparse high-price zone — $100+

For each tier: price range, product count, % of total, which product types live there.

**Step 3 — Discount analysis:**
- How many products are discounted vs. full price?
- Average discount % across discounted products
- Do higher-priced products discount more or less?

### 3. Brand Landscape
- List all unique brands with: product count, avg price, avg rating, total reviews
- Sort by total reviews (market share proxy)
- Identify dominant brands (top 3 by review count)
- Identify premium vs. budget brand positioning

### 4. Product Category Mix
Parse from product titles:

**Product Type breakdown:**
Identify and count: base layers / thermal underwear, sweaters / crewneck / V-neck, t-shirts, underwear / boxer briefs, accessories (beanies, gaiters, gloves), sets (top+bottom), other

For each type: count, %, avg price, avg reviews

**Gender split:**
- Men's vs Women's vs Unisex — count and % for each
- Average price per gender
- Which gender has higher avg reviews?

**Weight tier mentions:**
- Lightweight / Midweight / Heavyweight — how many products explicitly mention weight?
- Avg price per weight tier

### 5. Demand & Popularity Signals

**Review distribution:**
- Top 3 products by review count (title, brand, reviews, price, rating)
- Median review count
- % of products with 500+ reviews (established demand) vs under 100 (newer/niche)

**Rating quality:**
- % with 4.5+ stars, 4.0–4.5, below 4.0
- Does higher price correlate with better rating? (compare avg rating across price tiers)
- Any brand with consistently high rating across multiple products?

**Badge breakdown:**
- List all badged products: title, badge type, price, reviews
- What do badged products have in common (price point, product type)?

**BSR Rank analysis (from BSR Rank column):**
- List the BSR rank and category for each product that has one
- Which Amazon subcategories appear most often? (reveals where the market is classified)
- Is there a pattern between BSR rank and review count — or are some products punching above/below their review weight?

**Category path breakdown (from Category column):**
- List all unique Amazon category paths
- Which subcategories appear most? (e.g. "Women's Thermal Underwear" vs "Men's Base Layers")
- Do any products appear in unexpected categories?

### 6. Gender Analysis
Parse gender signals from product titles (keywords: "men's", "mens", "women's", "womens", "ladies", "unisex", "kids", "baby").

**Gender split table:**
| Gender | Products | % | Avg Price | Avg Rating | Total Reviews |
|---|---|---|---|---|---|
| Men's | | | | | |
| Women's | | | | | |
| Unisex | | | | | |
| Other (kids/baby) | | | | | |

**Gender depth analysis:**
- Which gender has more products listed? Does review volume match?
- Price gap between men's and women's equivalents (same product type, different gender)
- Are any product types gender-exclusive vs. sold in both?
- Which gender has the strongest demand signal (highest avg reviews per product)?

**Gender white space:**
- Is one gender clearly underserved (fewer products, lower review depth)?
- Which product types exist for one gender but not the other?

---

### 7. Color Analysis
Use the **Colors** column (real variant data from the detail scraper). Fall back to title parsing only for records where Colors is empty.

**Color inventory:**
List all unique colors across all products. Group into families:
| Color Family | Colors | Product Count | % of Products Offering This Family |
|---|---|---|---|
| Neutral (black, white, gray, charcoal, heather) | | | |
| Earth (tan, camel, olive, brown, oatmeal, natural) | | | |
| Classic (navy, burgundy, forest green, blue) | | | |
| Seasonal / Statement (bright, bold, seasonal) | | | |

**Color depth per product:**
- Average number of color options per product
- Which products offer the widest color range? (list top 3 with color count)
- Which products are single-color only?

**Key observations:**
- Which colors appear across the most products (market "safe bets")?
- Is the market neutral-heavy or varied?
- Do higher-reviewed products offer more or fewer colors?
- Any colors appearing in only 1–2 products (potential differentiation opportunity)?

---

### 8. Size & Fit Analysis
Use the **Sizes** column (real variant data from the detail scraper). Fall back to title parsing for records where Sizes is empty.

**Size range coverage:**
List all unique sizes appearing across products, then assess:
| Size Signal | Products Offering It | % |
|---|---|---|
| XS | | |
| S / M / L / XL | | |
| XXL / 2XL | | |
| 3XL / Plus | | |
| Big & Tall | | |
| One size | | |
| Numeric (waist/inseam) | | |

**Size depth per product:**
- Average number of size options per product
- Which products offer the fullest size run? (list top 3)
- Which products are limited to S–XL only?

**Fit language (from Bullet Points column):**
- How many products mention fit type: "slim", "regular", "relaxed", "athletic"?
- Any mention of "seamless", "tagless", or "4-way stretch"?

**Size strategy observations:**
- Is inclusive sizing (3XL+) a crowded or underserved space?
- Do men's and women's offerings differ in size depth?
- Where does the market draw the size ceiling — is there a clear cutoff?

---

### 9. Positioning & Title Language
Analyze the titles of the top 10 products by review count:

**Frequent claims and keywords:** (count how often each appears)
- "100%" / "pure"
- "merino wool" vs just "wool"
- "base layer" / "thermal" / "underwear"
- "odor resistance" / "anti-odor"
- "RWS certified" / "ethically sourced"
- "machine washable"
- "lightweight" / "midweight" / "heavyweight"
- Weight in grams (150g, 200g, 250g)
- Pack deals ("2 pack", "6 pack")

**Title structure patterns:**
- Do top sellers lead with the use case or the material?
- Do they mention gender first, material second?
- Any naming conventions that repeat across top sellers?

---

## PART 2: Strategic Takeaways & Product Development

### A. Key Market Insights
For each dimension from Part 1, extract 2–3 concrete insights. Format as:
> **[Dimension]:** [What the data shows] → [What this means for us]

Example:
> **Price:** The market clusters at $40–60 for base layer tops with 100+ reviews → This is where the trust is established; launching below $40 signals cheap, above $80 needs strong brand story.

### B. Competitive White Space
Identify specific gaps:
- **Price gaps:** Are there price ranges with almost no competition?
- **Product type gaps:** Any product types underrepresented in top results?
- **Gender gaps:** Does one gender have weaker competition?
- **Positioning gaps:** Claims or features no one is owning in titles?

### C. Suggested Product Development Priorities
Based on demand signals and white space, recommend which products to develop first. Format as a table:

| Priority | Product Type | Target Gender | Price Point | Why |
|---|---|---|---|---|
| 1 | [e.g. Midweight Base Layer Top] | Women's | $X–$X | [Reason: high reviews, gap at this price, etc.] |
| 2 | ... | | | |
| 3 | ... | | | |

Cap at 5–6 priorities. Be specific — "merino base layer" is too broad; "women's midweight long sleeve crew, $55–70" is actionable.

### D. Price Positioning Recommendation
- Where to price vs. the market (above / below / alongside which competitors)
- Which price tier to enter first and why
- Specific price points to target per product type
- Any anchor pricing strategy (if offering sets or multipacks)

### E. Marketing Language & Positioning
Based on what works in top-seller titles:
- 3–5 key phrases or claims to always include in our product titles and copy
- 1–2 positioning angles that are underused and we could own
- What NOT to lead with (overcrowded territory)

### F. Combined Learnings with Shopify Competitor Data
If Shopify competitor reports exist in `reports/` (e.g. Wooland, Unbound Merino, Minus33, Duckworth), cross-reference:
- Do Amazon price sweet spots align with what competitors charge on their own stores?
- Are the dominant Amazon product types the same ones competitors invest most SKU depth in?
- Any contradictions between what Amazon buyers buy vs. what brands offer on D2C?
- Synthesize into 3 final strategic bullets combining both data sources.

---

## Saving the Report

Save the completed report as a markdown file:

- **Folder:** `reports/amazon/` (create if it doesn't exist)
- **File name:** `Amazon_{keyword_slug}_{YYYY-MM-DD}.md`
  - Replace spaces with underscores in keyword
  - Example: `reports/amazon/Amazon_merino_wool_sweater_2026-06-25.md`

Use the Write tool to create the file.

---

## Output Format

Always produce in **English** as a clean markdown document:

```
# Amazon Market Analysis Report
**Search Keyword:** [keyword]
**Records Analyzed:** [N]
**Report Date:** [Today]
**Prepared for:** Product Development Team

---

## PART 1: AMAZON MARKET DATA ANALYSIS

### 1. Market Snapshot
...

### 2. Price Architecture
#### Price Distribution
...
#### Price Tiers
...
#### Discount Analysis
...

### 3. Brand Landscape
| Brand | Products | Avg Price | Avg Rating | Total Reviews |
...

### 4. Product Category Mix
#### Product Types
| Type | Count | % | Avg Price | Avg Reviews |
...
#### Gender Split
...
#### Weight Tier Mentions
...

### 5. Demand & Popularity Signals
#### Top Products by Reviews
...
#### Rating Quality
...
#### Badge Breakdown
...

### 6. Gender Analysis
#### Gender Split Table
...
#### Gender Depth Analysis
...
#### Gender White Space
...

### 7. Color Analysis
#### Color Family Breakdown
| Color Family | Colors Mentioned | Product Count | % |
...
#### Key Observations
...

### 8. Size & Fit Analysis
#### Size Inclusivity Signals
| Signal | Products Mentioning It | % |
...
#### Fit Language
...
#### Size Strategy Observations
...

### 9. Positioning & Title Language
...

---

## PART 2: STRATEGIC TAKEAWAYS & PRODUCT DEVELOPMENT

### A. Key Market Insights
...

### B. Competitive White Space
...

### C. Suggested Product Development Priorities
| Priority | Product Type | Target Gender | Price Point | Why |
...

### D. Price Positioning Recommendation
...

### E. Marketing Language & Positioning
...

### F. Combined Learnings with Shopify Competitor Data
...
```

---

## Important Notes
- Always output in **English**
- Part 1 must be purely objective — numbers and patterns only, no recommendations
- Part 2 must be specific and actionable — avoid vague statements like "consider offering more products"
- The product development priority table in Part 2C is the most important deliverable
- Section F (combined learnings) is only included if Shopify reports exist in `reports/` — check first
- If fewer than 5 records match the keyword filter, warn the user and suggest re-scraping with `/scrape-amazon`
