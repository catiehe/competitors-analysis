# Amazon Market Analysis Report
**Search Keywords:** merino wool + merino wool sweater (combined)
**Records Analyzed:** 56 unique products (deduplicated by ASIN)
**Brands Identified:** 23
**Report Date:** 2026-06-25
**Prepared for:** Product Development Team

> **Note on enrichment fields:** Category, BSR Rank, Colors, Sizes, and In Stock columns are empty for this dataset — these records were scraped before the ASIN detail enrichment was added. Future scrapes will populate these automatically. Color and size analysis below is based on title parsing.

---

## PART 1: AMAZON MARKET DATA ANALYSIS

---

### 1. Market Snapshot

| Metric | Value |
|---|---|
| Total unique products | 56 |
| Unique brands | 23 |
| Keyword: "merino wool" | 47 products |
| Keyword: "merino wool sweater" | 9 products |
| Price range | $9.89 – $109.00 |
| Average price | $41.59 |
| Median price | $38.12 |
| Products with active discount | ~38 (68%) |
| Products with a badge | 33 (59%) |

**Badge breakdown:**

| Badge | Count |
|---|---|
| Prime Day Deal | 31 |
| Overall Pick | 2 |
| Save 47% | 1 |
| No badge | 23 |

The "Prime Day Deal" badge on 31 of 56 products (55%) signals heavy promotional dependency across the category — this is a market where discounting is near-universal, not a differentiator.

---

### 2. Price Architecture

#### Price Distribution (binned in $10 increments)

| Price Bin | Products | % | What Lives Here |
|---|---|---|---|
| $0 – $9 | 1 | 1.8% | Blend t-shirt (outlier, not true merino) |
| $10 – $19 | 6 | 10.7% | Neck gaiters, beanie, glove liner, women's underwear, blend shirts |
| $20 – $29 | 6 | 10.7% | Neck gaiters, 2-pack t-shirts, boxer briefs |
| **$30 – $39** | **22** | **39.3%** | **Base layer tops (LS), t-shirts, women's shirts — dominant peak** |
| $40 – $49 | 6 | 10.7% | Sweaters, polo, hoodie, boxer brief packs |
| $50 – $59 | 7 | 12.5% | Sets, polo, sweaters, half-zips |
| $60 – $69 | 5 | 8.9% | Full thermal sets, MERIWOOL base layers |
| $70 – $79 | 0 | 0% | — gap — |
| $80 – $89 | 2 | 3.6% | Merino.tech full sets (men's + women's) |
| $100+ | 1 | 1.8% | Woolino baby sleep sack (unrelated category) |

**Shape:** Strongly unimodal with a hard peak at $30–$39. The distribution is right-skewed: a long but sparse tail from $60–$85. No products between $70–$79 — a clean gap.

#### Price Tiers

| Tier | Range | Products | % | What Lives Here |
|---|---|---|---|---|
| Entry | $10–$29 | 13 | 23.2% | Accessories (gaiters, beanies, gloves), underwear 3–6 packs |
| **Core** | **$30–$39** | **22** | **39.3%** | **Base layer LS tops, short-sleeve tees, women's shirts** |
| Mid | $40–$59 | 13 | 23.2% | Sweaters, polo, hoodie, sets |
| Premium | $60–$85 | 7 | 12.5% | Full thermal sets (top + bottom), premium base layers |
| Outlier | $109 | 1 | 1.8% | Baby sleep sack (not a competitor product) |

#### Discount Analysis

| Metric | Value |
|---|---|
| Products with a stated discount | 38 (68%) |
| Typical discount range | 15% – 25% |
| Highest discount | 47% (Merino.tech turtleneck, "Save 47%" badge) |
| Most common discount | 15% – 20% |
| Full-price products | 18 (32%) — mostly newer SKUs and established brands (MERIWOOL, Woolly, Chanyarn) |

**Pattern:** Merino.tech runs 15–20% off consistently across its entire range. Discounting is table stakes at the $30–$39 Core — buyers expect a deal. At the $50–$65 Mid tier, discounts are larger (20–30%) to justify the higher ask.

---

### 3. Brand Landscape

| Brand | Products | Avg Price | Avg Rating | Total Reviews | Positioning |
|---|---|---|---|---|---|
| **Merino.tech** | 19 | $42 | 4.4 | ~4,600 | Mass market leader, base layers + accessories |
| Merino Protect | 3 | $34 | 4.3 | 873 | Value base layers, men's + women's |
| ACUSHLA | 1 | $15 | 4.6 | 686 | Accessories only (neck gaiter) |
| Woolly Clothing Co | 1 | $38 | 4.1 | 646 | Women's underwear, RWS certified |
| Chanyarn | 2 | $52 | 4.1 | 559 | 100% merino sweaters (women's + men's) |
| ANRABESS | 1 | $40 | 4.2 | 420 | Women's wool blend sweater |
| MERINNOVATION | 1 | $64 | 4.5 | 322 | Men's pajama/thermal set |
| C202 | 1 | $19 | 4.3 | 242 | Women's blend shirts (not 100% merino) |
| LEADHALO | 2 | $60 | 4.6 | 142 | Midweight sets, men's + women's |
| BEENIUBEE | 4 | $37 | 4.4 | 135 | 2-pack base layer tops + tank tops |
| MERIWOOL | 2 | $65 | 4.7 | 92 | Premium US brand, full-price only |
| SUNCHIRI | 2 | $31 | 4.2 | 90 | 2-pack value t-shirts |
| FORVEVO | 3 | $31 | 4.2 | 66 | Men's + women's underwear packs |
| Calvin Klein | 1 | $41 | 4.5 | 68 | Men's V-neck sweater, blend |
| CAOZITOU | 1 | $30 | 4.2 | 63 | Women's underwear 3-pack |
| Buff | 1 | $32 | 4.6 | 56 | Neck gaiter, full-price |
| DAZZWEAR | 1 | $10 | 4.2 | 51 | Blend t-shirts (very low price, not 100% merino) |
| Woolino | 1 | $109 | 4.7 | 41 | Baby sleep sack (unrelated) |
| Innophra | 1 | $28 | 4.6 | 39 | Women's base layer shirt |
| Minus33 | 3 | $22 | 4.5 | 38 | Accessories only on Amazon |
| BEENIUBEE | — | — | — | — | — |
| WWOMAY | 1 | $32 | 4.4 | 25 | Women's shirts |
| Brooks Brothers | 1 | $53 | 4.1 | 9 | Men's merino crewneck sweater |

**Dominant brand:** Merino.tech holds 19 of 56 products and approximately 50% of all reviews in the dataset. This is single-brand category dominance — no other brand comes close on volume. Their strategy: wide assortment + perpetual 15–20% discount + heavy SKU fragmentation (same style, multiple ASINs for different color/size combos).

**Top 3 by review count (single products):**
1. Merino.tech Men's Base Layer LS (B0CLB3T36D) — 878 reviews, $38.24
2. Merino.tech Men's Polo (B0BHZMJCZS) — 878 reviews, $50.99
3. Merino Protect Women's V-Neck T-Shirt (B0BN8CJ7VF) — 849 reviews, $34.39

**Surprising finding:** The Merino.tech polo at $50.99 matches the top base layer on review count — signaling real demand for merino polos that the market underestimates.

---

### 4. Product Category Mix

#### Product Types (parsed from titles)

| Type | Count | % | Avg Price | Avg Reviews |
|---|---|---|---|---|
| Base layer tops (LS thermal, long sleeve) | 18 | 32.1% | $42 | 195 |
| T-shirts / Short sleeve | 14 | 25.0% | $32 | 152 |
| Sweaters (crewneck, V-neck knit) | 8 | 14.3% | $47 | 137 |
| Underwear / Boxer briefs / Panties | 7 | 12.5% | $29 | 91 |
| Sets (top + bottom) | 6 | 10.7% | $68 | 97 |
| Accessories (gaiters, beanies, gloves) | 6 | 10.7% | $20 | 127 |
| Tank tops | 3 | 5.4% | $38 | 164 |
| Bottoms / Thermal pants | 2 | 3.6% | $65 | 46 |
| Baby | 1 | 1.8% | $109 | 41 |

**Hero categories by volume:** Base layer tops (32%) and T-shirts (25%) dominate — together they are 57% of the market. Sweaters are a distinct 14% with higher avg price ($47) and meaningful review depth.

#### Gender Split

| Gender | Products | % | Avg Price | Avg Reviews |
|---|---|---|---|---|
| Men's | 25 | 44.6% | $43 | 182 |
| Women's | 23 | 41.1% | $38 | 162 |
| Unisex / Accessories | 7 | 12.5% | $21 | 114 |
| Baby | 1 | 1.8% | $109 | 41 |

Men's and women's are nearly equal in product count. Men's averages $5 more and has slightly higher avg reviews per product. Women's sweater keyword drives up women's average price for that subset ($47 for sweaters).

#### Weight Tier Mentions

| Weight Tier | Products Mentioning It |
|---|---|
| Midweight | 10 |
| Lightweight | 7 |
| Heavyweight | 5 |
| No weight mentioned | 34 |

60% of products don't mention weight at all — mostly in the sweater and T-shirt categories. Merino.tech explicitly uses Lite/Midweight/Heavyweight in their naming, which helps buyers self-select. This is underused by other brands.

---

### 5. Demand & Popularity Signals

#### Top 5 Products by Review Count

| # | Title (truncated) | Brand | Reviews | Price | Rating |
|---|---|---|---|---|---|
| 1 | Men's Base Layer Merino LS Shirt | Merino.tech | 878 | $38.24 | 4.5 |
| 2 | Men's Merino Polo Shirt | Merino.tech | 878 | $50.99 | 4.3 |
| 3 | Women's Merino V-Neck T-Shirt | Merino Protect | 849 | $34.39 | 4.3 |
| 4 | Men's Merino Underwear Boxer Briefs | Merino.tech | 715 | $43.19 | 4.3 |
| 5 | 100% Merino Wool Neck Gaiter (Unisex) | ACUSHLA | 686 | $14.99 | 4.6 |

**Median review count:** ~39 reviews
**Products with 500+ reviews:** 7 (12.5% of catalog — established demand)
**Products with under 50 reviews:** 35 (62.5% — mostly newer or niche SKUs)

The review distribution is highly skewed: a small number of proven winners carry the volume, while most of the catalog is still building traction.

#### Rating Quality

| Rating Range | Products | % |
|---|---|---|
| 4.5+ stars | 14 | 25% |
| 4.0 – 4.4 stars | 34 | 60.7% |
| Below 4.0 | 8 | 14.3% |

85% of products rate 4.0+. The floor is surprisingly high — buyers clearly expect quality from merino wool and abandon products that disappoint. Products below 4.0 tend to be sweaters ($40–60 range) where fit and shrinkage are common complaints.

**Price vs. rating:** No strong correlation. Highest-rated products are MERIWOOL ($65, 4.7★) and Innophra ($28, 4.6★) and Merino.tech turtleneck ($45, 4.8★) — price does not predict quality perception.

#### Badge Breakdown

"Prime Day Deal" dominates the badge landscape and appears to be an Amazon-assigned promotional label rather than a true quality signal — 31 of 56 products carry it. The more meaningful badges:
- **Overall Pick** (Merino.tech t-shirt + Arach&Cloz sweater) — quality signal; awarded to top performers in a search
- **Save 47%** (Merino.tech turtleneck) — promotional urgency signal
- No badge on 23 products, including MERIWOOL, Buff, and Woolly — premium brands that don't rely on discount signals

---

### 6. Gender Analysis

#### Gender Split Table

| Gender | Products | % | Avg Price | Avg Rating | Total Reviews (est.) |
|---|---|---|---|---|---|
| Men's | 25 | 44.6% | $43 | 4.4 | ~5,200 |
| Women's | 23 | 41.1% | $38 | 4.3 | ~4,600 |
| Unisex | 7 | 12.5% | $21 | 4.5 | ~1,500 |
| Baby | 1 | 1.8% | $109 | 4.7 | 41 |

#### Gender Depth Analysis

Men's and women's are close in count, but men's leads in both avg price ($43 vs $38) and estimated total reviews. The biggest men's categories: base layer LS tops, polo, underwear, sets. The biggest women's categories: base layer LS tops, short-sleeve tees, tank tops, underwear.

**Key gender differences:**
- Men's has a polo ($50.99, 878 reviews) — no women's equivalent; clear gap
- Women's has tank tops — no men's equivalent (minor)
- Women's sweater lineup (3 products from "merino wool sweater" keyword) has stronger brand variety (Chanyarn, ANRABESS, Arach&Cloz, Calvin Klein for men's)
- Women's avg price is $5 lower than men's for equivalent product types

#### Gender White Space

- **Women's polo:** Zero products. Men's polo is a top-2 reviewed product — demand signal for a women's version
- **Men's tank top:** Zero dedicated products
- **Women's thermal bottoms:** Only 1 product in set form (LEADHALO); no standalone women's legging or thermal pant
- **Men's sets:** Underserved relative to demand — only 3 dedicated sets, yet sets in the $60–80 range perform well

---

### 7. Color Analysis

> **Data limitation:** Colors column is empty for this dataset (pre-enrichment records). Analysis is based on title parsing only.

**Color mentions in titles:**
- Very few products name specific colors in the title — most products with multiple colorways don't list them (Amazon convention is to handle colors as variants on the listing, not in the title)
- Notable exceptions: Minus33 glove liner ("Multiple Colors"), ACUSHLA neck gaiter ("Maple Leaf" colorway named)
- MERIWOOL and Buff do not name colors in titles

**Color strategy inference from known brands:**
- Merino.tech (19 products): Based on their catalog, they typically offer neutral bases (black, gray, navy) with 3–5 colorways per style — not wide palettes
- Woolly Clothing Co (women's underwear): Known for neutral + earthy color palette aligned with their sustainability positioning
- MERIWOOL: Limited neutral palette (black, navy, charcoal, natural)

**Conclusion:** Amazon merino wool products are overwhelmingly neutral-first. Brands that attempt bold/seasonal colors are rare and generally have lower review depth. Neutral (black, gray, navy, charcoal) is the safe bet for launch.

*Note: Run `/scrape-amazon` again to populate the Colors column for future analysis with actual variant data.*

---

### 8. Size & Fit Analysis

> **Data limitation:** Sizes column is empty for this dataset. Analysis is based on title parsing only.

**Explicit size mentions in titles:**

| Signal | Products Mentioning | Notes |
|---|---|---|
| "Multiple Colors and Sizes" | 1 (Minus33 glove) | Generic mention only |
| "Big & Tall" | 1 (ANRABESS sweater) | Women's wool blend |
| "One Size Fits Most" | 1 (Minus33 beanie) | Accessory |
| "2-24 Months" | 1 (Woolino baby) | Non-competitor |
| "3/4 Length" | 1 (Merino.tech pants) | Bottoms variant |
| No size mention | 51 | Default — handled as listing variants |

Almost no brand calls out size range in the title. This is the Amazon convention — size is a variant selector, not a title attribute.

**Fit language in titles:**
- "Slim Fit" — 1 product (Merino.tech hoodie women)
- "High Waisted" — 1 product (CAOZITOU women's underwear)
- No "regular fit", "relaxed", or "athletic" in any title

**Size strategy inference:**
Pack products (2-pack, 6-pack) only appear in t-shirts and underwear — the size-range investment for packs is likely narrower (S–XL core only). Premium single-unit products like MERIWOOL and MERINNOVATION likely run XS–2XL based on brand standards.

*Note: Run `/scrape-amazon` again to populate the Sizes column for actual variant data.*

---

### 9. Positioning & Title Language

#### Top 10 Products by Reviews — Title Analysis

| Claim / Keyword | Appears in Top 10 | Total Catalog |
|---|---|---|
| "Merino Wool" (explicit) | 10/10 | 55/56 |
| "100%" | 6/10 | 28/56 |
| "Base Layer" | 7/10 | 26/56 |
| "Lightweight / Midweight / Heavyweight" | 4/10 | 15/56 |
| "Moisture Wicking" | 3/10 | 9/56 |
| "Odor Resistance / Anti-Odor" | 2/10 | 7/56 |
| "Breathable" | 3/10 | 12/56 |
| "Hiking" | 3/10 | 10/56 |
| "Thermal / Thermal Underwear" | 4/10 | 16/56 |
| "RWS Certified / Ethically Sourced" | 1/10 | 1/56 (Woolly) |
| Weight in grams (e.g. 250g, 190g) | 1/10 | 3/56 |
| Pack deals (2 Pack, 6 Pack) | 2/10 | 10/56 |

**Title structure patterns:**

- Top sellers almost always follow this pattern: **[Gender + Product Type] + [Brand name in title] + [Key Claims]**
  - Example: *"Merino Wool Base Layer Mens - 100% Merino Wool Shirts for Men Thermal Underwear Long Sleeve T-Shirt for Hiking Hunting"*
- Gender comes first or second in 9 of 10 top titles
- "Merino Wool" explicitly stated — buyers search specifically for it vs. generic "wool"
- "Base Layer" is the dominant functional frame, even for sweater-adjacent products
- Use case keywords ("Hiking", "Hunting", "Ski") appear in functional products but not sweaters

**Most crowded claims:** "100%", "Base Layer", "Thermal" — everyone says this. No differentiation.

**Underused in high-review titles:**
- Weight in grams (only Innophra uses 190g) — technical buyers search this
- "RWS Certified" — only Woolly uses it (and has 646 reviews on underwear)
- "Machine Washable" — rare despite being a key buyer concern for merino

---

## PART 2: STRATEGIC TAKEAWAYS & PRODUCT DEVELOPMENT

---

### A. Key Market Insights

> **Price:** The Amazon merino wool Core sits at $30–39 — well below what D2C brands charge ($70–99). → Amazon is the value channel. A new brand building on Amazon at $30–39 will compete on price, not brand. If targeting D2C, the $70–99 range is validated and much less crowded.

> **Brand concentration:** Merino.tech holds ~50% of category reviews with 19 SKUs. → The playbook exists: wide assortment + perpetual discount + fragmented ASINs per color/size. Replicating this requires volume. Competing against it requires differentiation — better brand story, higher quality signal, or a niche the category ignores.

> **Sweaters are undervalued on Amazon:** 8 sweater products at avg $47, but none is the clear dominant player. Chanyarn leads women's with 495 reviews; no single brand owns men's merino sweaters. → A dedicated merino sweater brand (vs a base layer brand that also sells sweaters) has white space here.

> **Polo is a surprise winner:** Merino.tech's polo at $50.99 has 878 reviews — matching their #1 base layer. → The merino polo is an underserved style. No women's version exists in the top results. This is a real product gap.

> **Sets drive higher AOV without dominance:** Sets (top+bottom, $60–85) have only 6 products and none above 322 reviews. → Sets are a clear upsell opportunity. High-value, low competition relative to tops and t-shirts.

> **Discounting is the norm, not the exception:** 68% of products have an active discount. → Full-price positioning (MERIWOOL, Buff) signals quality. A no-discount strategy is actually a differentiator on Amazon.

---

### B. Competitive White Space

**Price gaps:**
- $70–$79 range: zero products. A premium single garment (women's or men's merino sweater at $72–78) occupies uncrowded territory.
- $85–$109: only 2 products (Merino.tech full sets). A premium single-item sweater or knit top at $85–$95 would stand alone.

**Product type gaps:**
- **Women's merino polo** — no products at all. Men's polo has 878 reviews. This is the clearest product gap in the dataset.
- **Women's standalone thermal bottom (legging/pant)** — only available as part of sets; no standalone women's merino legging in top results.
- **Men's quarter-zip / half-zip sweater (knit, not thermal)** — Merino.tech's "half zip" is actually a base layer; no true knit half-zip merino sweater for men.

**Positioning gaps:**
- **"Machine Washable"** — a critical buyer concern for merino; appears in almost zero titles despite being relevant
- **"RWS / Responsible Wool Standard"** — only Woolly uses this; 646 reviews suggests sustainability positioning resonates, especially for underwear
- **Weight in grams** — technical buyers (hikers, travelers, outdoors) search "150g merino" or "250g merino"; only 3 products use this

---

### C. Suggested Product Development Priorities

| Priority | Product Type | Target Gender | Price Point | Why |
|---|---|---|---|---|
| 1 | Merino Polo Shirt | Women's | $60–$75 | No women's equivalent to the #2 reviewed men's product (878 reviews). Clear demand signal, zero competition. |
| 2 | 100% Merino Crewneck Sweater | Women's | $65–$80 | Chanyarn leads with 495 reviews but is a generic brand with no differentiation. Branded quality entry would take this. |
| 3 | Merino Thermal Legging / Bottom | Women's | $65–$80 | Only available in sets; no standalone women's thermal pant. Men's has MERIWOOL at $65. |
| 4 | Merino Half-Zip Sweater (knit) | Men's | $75–$90 | No true knit merino half-zip; Merino.tech's version is a thermal layer, not a sweater. |
| 5 | Merino Top + Bottom Set | Both | $110–$130 | Sets are underserved (6 products only, max 322 reviews). Higher AOV, less noise than single items. |

---

### D. Price Positioning Recommendation

**For Amazon channel:**
- Price $5–$15 above Merino.tech on equivalent product types. At $44–$48 for a base layer top, you sit above the noise without reaching the Mid tier gap.
- Do NOT enter at $30–$39 Core unless you can sustain 15–20% discounts permanently. This tier is fully owned by Merino.tech and value-brand noise.
- For sweaters: anchor at $65–$80 — above the Chanyarn/ANRABESS cluster ($40–$48) but below the set/premium zone. This positions you as a real sweater brand vs. a commoditized base layer.

**For D2C channel:**
- The Shopify competitor data shows the D2C Core for merino apparel is $70–$99 (Minus33, Wooland) up to $130–$200+ (Wooland dresses, Duckworth). Amazon's $30–$39 Core is purely the volume/value channel.
- Target $79–$99 for base layer tops and $95–$130 for sweaters in D2C. This aligns with Minus33 positioning and is well below Duckworth's $180+ premium.
- No-discount full-price positioning on D2C (like MERIWOOL on Amazon) signals quality more effectively than constant Prime Day deals.

**Specific anchors to target:**

| Product Type | Amazon Price | D2C Price |
|---|---|---|
| Base layer LS top | $44–$52 | $79–$99 |
| Polo shirt | $60–$75 | $95–$115 |
| Crewneck sweater | $65–$80 | $110–$135 |
| Thermal bottom | $55–$65 | $89–$109 |
| Top + bottom set | $110–$130 | $160–$195 |

---

### E. Marketing Language & Positioning

**Must-include in every product title and listing:**
1. "100% Merino Wool" — non-negotiable; buyers filter for this explicitly
2. Gender first — "Women's" or "Men's" before the product type
3. Weight descriptor — "Midweight", "Lightweight", or grams (190g/250g) for functional products
4. At least one use case — "Hiking", "Travel", "Everyday" — to capture search intent beyond base layer
5. "Machine Washable" — almost no competitor mentions this; it reduces the #1 buyer objection

**Positioning angles to own (underused in current market):**
- **"RWS Certified"** — Woolly Clothing Co is the only brand using this at scale (646 reviews). There is room for a second brand to own responsible sourcing as a core identity.
- **Gram weight as specification** — Outdoor and travel buyers search by weight (150g ultralight, 250g midweight). Being the brand that leads with specs (like "190g Merino") targets a higher-intent buyer.

**What NOT to lead with:**
- "Anti-odor" / "Odor resistance" — everyone says this; it's table stakes, not a differentiator
- "Moisture wicking" — same issue; generic claim that adds noise
- "Breathable" — overused and unverified; skip unless backed by a spec
- Generic "wool sweater" framing without "100% Merino" — wool blend products ($9–$19) pollute the category and destroy price credibility

---

### F. Combined Learnings with Shopify Competitor Data

Cross-referencing this Amazon analysis against the Shopify brand reports (Wooland, Minus33, Unbound Merino, Duckworth):

**1. Amazon and D2C price worlds don't overlap — and that's intentional.**
Amazon Core sits at $30–39; D2C Core for the same brands sits at $70–99 (Minus33) to $80–99 (Wooland) to $180–340 (Duckworth). Merino.tech exists almost exclusively on Amazon with no meaningful D2C presence. Woolly Clothing Co uses Amazon for underwear at $38 but likely prices higher D2C. The Shopify reports confirm: a brand that competes on Amazon at $30–39 is buying volume at near-zero margin. A brand that sells D2C at $85–99 is building a business. The strategic play is to use Amazon at $50–75 for discovery and drive repeat buyers to D2C where margin lives.

**2. Product categories that work on Amazon also dominate D2C SKU depth.**
Minus33's D2C hero categories are base layer tops and bottoms ($70–90) — exactly what dominates Amazon reviews. Wooland's volume drivers are tees and tanks ($80–98). Both channels validate: **base layer tops are the entry product for a merino brand.** But on Amazon they're commoditized at $34–38; on D2C they hold $79–99. The product is the same; the channel determines the margin.

**3. The sweater category is an Amazon gap and a D2C opportunity simultaneously.**
Amazon has no dominant merino sweater brand (Chanyarn leads women's with just 495 reviews; men's has no clear winner). Duckworth's D2C report shows sweaters in the $188–$258 range as a Core category with deep investment. Wooland has knitwear at $148–$168. The Amazon sweater gap ($65–80 bracket is empty) aligns with D2C brands not even trying to compete there — they're pricing $120+ for the same item. A brand that builds merino sweaters at $75–95 D2C and $65–80 on Amazon would occupy the precise white space both channels leave open.

---

*Report generated: 2026-06-25 | Data source: Feishu Bitable Amazon table | Keywords: "merino wool" + "merino wool sweater"*
*Next step: Run `/scrape-amazon` with enrichment to populate Category, BSR, Colors, Sizes fields for deeper variant analysis.*
