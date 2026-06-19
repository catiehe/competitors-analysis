---
name: competitor-analysis
description: >
  Professional product development competitor analysis using Feishu Bitable data.
  Use this skill whenever the user wants to analyze a competitor brand, review 
  collected SKU/price/color/size data, or generate a professional product development 
  report with strategic recommendations. Triggers on phrases like "analyze competitor", 
  "analyze brand", "give me a report on [brand]", "竞品分析", "product development report",
  "what should we develop next", or "gap analysis".
---

# Competitor Analysis Skill
## For Product Development Teams

This skill produces a two-part professional report based on competitor data 
collected in Feishu Bitable (多维表格).

- **Part 1** → Objective data analysis (what the data shows)
- **Part 2** → What we can learn and how to apply it to our own brand

---

## Data Structure (Feishu Table Columns)

| Column | Description |
|--------|-------------|
| Brand | Competitor brand name |
| Product Name | Full product title |
| SKU | Unique SKU code |
| Category | Product category/type |
| Color | Color variant (multiselect) |
| Size | Size variant (multiselect) |
| Price | Current selling price (USD) |
| Product URL | Link to product page |
| Competitor Source | Brand/website source |
| Date Collected | Date data was scraped |

---

## Workflow

### Step 1: Identify Brand
Ask user which brand to analyze if not specified.

### Step 2: Pull & Filter Data
Fetch all records from Feishu matching the selected brand via the API.

### Step 3: Run Part 1 Analysis
Go through each dimension systematically using the data.

### Step 4: Generate Part 2
Based on Part 1, produce learning takeaways and a suggested classification for the user's own brand.

### Step 5: Save Report
Save as markdown file in `reports/` folder.

---

## PART 1: Data Analysis Dimensions

### 1. Assortment Overview
- Total styles, total SKUs, avg SKUs per style
- Total categories
- Men's vs Women's split (SKU count and %)

### 2. Price Architecture
Analyze in full, then split by Men's and Women's.

**Step 1 — Run a price distribution analysis first:**
Bin all SKU prices into $25 increments and count SKUs per bin. This reveals the actual shape of the distribution — do NOT assume a normal curve or use mechanical thirds.

Look for:
- **Peak(s):** Where SKU density is highest — this is the true Core price point
- **Valleys:** Natural breaks in density — these define tier boundaries
- **Long tail:** Sparse high-price zone — Premium
- **Bimodal vs unimodal:** Many brands have two peaks (e.g. one for tops, one for bottoms) — call this out explicitly

**Step 2 — Define tiers based on what you find:**
Name tiers based on volume logic, not arbitrary divisions:
- **OPP (Opening Price Point):** Below the main cluster — accessories, entry basics
- **Core:** The dominant peak — where most SKUs and likely most revenue sits
- **Mid / Transitional:** Between peaks (if bimodal) or the slope down from the peak
- **Elevated:** A secondary peak or zone with meaningful SKU density
- **Premium:** The sparse long tail — $250+ or whatever is clearly outlier

For each tier, list: price range, % of SKUs, which categories live there.

**Step 3 — Split by Men's and Women's:**
Run the same distribution logic separately for each gender.
- Do the peaks shift between genders?
- Does men's or women's skew higher/lower?
- Where is each gender's Core?

### 3. Category Breakdown
Analyze overall first, then split:

**Overall:**
- SKU count and % per category, avg price per category
- Identify core categories (top 3 by SKU count) vs secondary

**Women's categories:**
- List all women's categories with SKU count, %, avg price
- Which is the hero category?

**Men's categories:**
- List all men's categories with SKU count, %, avg price
- Which is the hero category?

### 4. Color Strategy
Analyze overall first, then split by gender:

**Overall:**
- Total unique colors
- Color family breakdown: Neutral / Earth / Seasonal / Statement (% of SKUs)
- Top 8 most used colors with SKU counts
- Avg colors offered per style

**Women's colors:**
- Top colors, dominant color family

**Men's colors:**
- Top colors, dominant color family, any difference from women's

### 5. Size Curve
Split by gender. For each gender, run a size distribution analysis first — count SKUs per size — then read the shape.

**Step 1 — Identify the distribution shape:**
- **Flat/Uniform:** All sizes have roughly equal SKU counts → brand invests equally across all sizes
- **Bell curve:** Middle sizes (M/L) have more SKUs, extremes (XS/XXL) have fewer → brand prioritizes core sizes
- **Skewed:** Distribution peaks at one end → brand skews toward smaller or larger customers
- **Cliff:** A sudden drop at a specific size (e.g. XL→XXL) → hard size ceiling, deliberate cutoff

**Step 2 — Find the cliff:**
Where does SKU count drop significantly? That's where the brand stops investing. Call this out explicitly — it often signals who the brand is NOT designing for.

**Step 3 — Separate apparel vs numeric sizing:**
Analyze standard sizes (XS–3XL) and numeric/waist sizes (24–40) separately. Numeric sizing depth tells you how seriously they take the fit of bottoms.

**Women's sizes:**
- Distribution shape + cliff location
- Are XS and XXL treated equally to S/M/L/XL or deprioritized?
- Numeric sizing coverage (pants)
- Inclusive sizing verdict

**Men's sizes:**
- Distribution shape + cliff location
- Numeric waist sizing range and coverage
- Comparison to women's — who gets better size investment?

### 6. SKU Depth & Variant Analysis

For every style mentioned, **decompose the variant count** — do not just report the total. Break it down into:
- How many unique colors does this style come in?
- How many sizes does each color offer?
- If numeric sizing: how many waist × inseam combinations?
- Formula: Colors × Sizes = Variants (verify against actual count, explain any discrepancy)

**Top 5 deepest styles:**
For each, show the full breakdown:
```
[Style Name] — X total variants
  Colors: X (list them or describe the range)
  Sizes: X (list the size run)
  Breakdown: X colors × X sizes = X variants
  What this means: [why this style gets this level of investment]
```

**Categories with deepest average SKU count:**
- Which category has the highest avg variants per style?
- What does that tell us about where the brand invests in depth?

**Styles with 1–2 variants:**
- How many styles have only 1–2 variants?
- What are they? (usually bundles, multipacks, one-color accessories)
- These are not real product investments — call that out

**What the depth pattern reveals:**
- Which styles did the brand clearly decide are heroes (deep color + size run)?
- Which styles are fillers (few colors, limited sizes)?
- What does the investment pattern tell us about the brand's strategy and core customer?

---

## PART 2: What We Can Learn & Our Classification

### A. Key Learnings from This Brand
For each dimension (price, category, color, size), extract 2–3 concrete things the user's brand can learn or borrow from the competitor. Focus on:
- What they do well that we should replicate
- What they do that we should do differently
- What their assortment reveals about their customer and strategy

### B. Suggested Classification for Our Brand
Based on the competitor's structure, mock up a suggested product classification for the user's own brand. Format as a table:

| Division | Category | Suggested SKU Depth | Price Range | Priority |
|---|---|---|---|---|
| Women's | [Category] | X styles / X SKUs | $X–$X | Hero / Core / Secondary |
| Men's | [Category] | X styles / X SKUs | $X–$X | Hero / Core / Secondary |

Base this on:
- What the competitor does well → mirror for our brand
- Where the competitor is weak → opportunity for us
- Realistic SKU depth for a new/smaller brand (scale down from competitor)

### C. Price Positioning Recommendation
Based on what the competitor charges, recommend:
- Where to price relative to them (above / below / alongside)
- Which price tiers to prioritize for launch
- Any specific price points to target

### D. Color & Size Recommendations
- Recommended starting color palette (based on what works for the competitor)
- Recommended size run for launch

---

## Saving the Report

After generating the report, always save it as a markdown file in the `reports/` folder:

- File name format: `{Brand_Name}_{YYYY-MM-DD}.md` (spaces replaced with underscores)
- Example: `reports/Unbound_Merino_2026-06-19.md`

Use the Write tool to create the file. The `reports/` folder already exists in the repo.

---

## Output Format

Always produce in **English** as a clean markdown document using this structure:

```
# Competitor Analysis Report
**Brand:** [Brand Name]
**Report Date:** [Today]
**Prepared for:** Product Development Team

---

## PART 1: MARKET DATA ANALYSIS

### 1. Assortment Overview
...

### 2. Price Architecture

#### Overall
...

#### Women's
...

#### Men's
...

### 3. Category Breakdown

#### Overall
...

#### Women's
| Category | SKUs | % | Avg Price |
...

#### Men's
| Category | SKUs | % | Avg Price |
...

### 4. Color Strategy

#### Overall
...

#### Women's
...

#### Men's
...

### 5. Size Curve

#### Women's
...

#### Men's
...

### 6. SKU Depth & Variant Analysis
...

---

## PART 2: WHAT WE CAN LEARN & OUR CLASSIFICATION

### A. Key Learnings
...

### B. Suggested Classification for Our Brand
| Division | Category | Suggested SKU Depth | Price Range | Priority |
...

### C. Price Positioning
...

### D. Color & Size Recommendations
...
```

---

## Important Notes
- Always output in **English**
- Part 1 must be purely objective — data only, no opinions
- Part 2 must be actionable and specific to the user's brand
- Always split Men's and Women's where data allows
- The classification table in Part 2B is the most important deliverable — make it realistic and usable
- If data is missing for any dimension, flag it clearly
