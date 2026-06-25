import requests
import subprocess
import json
import os
import time
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

FEISHU_APP_ID     = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")

# Shopify → Feishu
FEISHU_BASE_ID    = os.getenv("FEISHU_BASE_ID")
FEISHU_TABLE_ID   = os.getenv("FEISHU_TABLE_ID")

# Amazon → Feishu
FEISHU_AMAZON_BASE_ID  = os.getenv("FEISHU_AMAZON_BASE_ID")
FEISHU_AMAZON_TABLE_ID = os.getenv("FEISHU_AMAZON_TABLE_ID")

# TikTok → Feishu
FEISHU_TIKTOK_BASE_ID  = os.getenv("FEISHU_TIKTOK_BASE_ID")
FEISHU_TIKTOK_TABLE_ID = os.getenv("FEISHU_TIKTOK_TABLE_ID")

APIFY_API_TOKEN              = os.getenv("APIFY_API_TOKEN")
APIFY_AMAZON_ACTOR_ID        = "JyRjxUswjrRheOdmh"
APIFY_AMAZON_DETAIL_ACTOR_ID = "junglee~amazon-crawler"
APIFY_TIKTOK_ACTOR_ID        = "ukNOBkY1TUxHNE8os"


# ── Shared helpers ─────────────────────────────────────────────────────────────

def get_feishu_token():
    res = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    )
    return res.json().get("tenant_access_token")

def write_to_feishu(token, records, base_id, table_id):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{base_id}/tables/{table_id}/records/batch_create"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"records": [{"fields": r} for r in records]}
    res = requests.post(url, headers=headers, json=payload)
    return res.json()

def run_apify_actor(actor_id, run_input):
    run_res = requests.post(
        f"https://api.apify.com/v2/acts/{actor_id}/runs",
        params={"token": APIFY_API_TOKEN},
        json=run_input
    )
    run_data = run_res.json().get("data", {})
    run_id = run_data.get("id")
    if not run_id:
        raise RuntimeError(f"Failed to start Apify run: {run_res.text}")

    print(f"⏳ Apify run started ({run_id}), waiting...")
    while True:
        status = requests.get(
            f"https://api.apify.com/v2/actor-runs/{run_id}",
            params={"token": APIFY_API_TOKEN}
        ).json()["data"]["status"]
        print(f"   {status}")
        if status == "SUCCEEDED":
            break
        if status in ("FAILED", "ABORTED", "TIMED-OUT"):
            raise RuntimeError(f"Apify run ended with status: {status}")
        time.sleep(5)

    return requests.get(
        f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items",
        params={"token": APIFY_API_TOKEN}
    ).json()

def to_float(val):
    try:
        return float(str(val).replace("$", "").replace(",", ""))
    except Exception:
        return 0.0

def to_int(val):
    try:
        return int(val) if val is not None else 0
    except Exception:
        return 0

def today_ms():
    return int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)


# ── Shopify ────────────────────────────────────────────────────────────────────

def fetch_json(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        data = res.json()
        if "products" in data:
            return data
    except Exception:
        pass
    result = subprocess.run(["curl", "-s", "--max-time", "15", url], capture_output=True, text=True)
    return json.loads(result.stdout)

def scrape_shopify(base_url, brand_name):
    products = []
    today = today_ms()
    page = 1

    while True:
        url = f"{base_url}/products.json?limit=250&page={page}"
        data = fetch_json(url)
        items = data.get("products", [])
        if not items:
            break

        for p in items:
            name = p.get("title", "")
            product_type = p.get("product_type", "")
            product_url = f"{base_url}/products/{p.get('handle', '')}"

            img_url = ""
            if p.get("images"):
                img_url = p["images"][0].get("src", "")

            color_idx, size_idx = None, None
            for i, opt in enumerate(p.get("options", []), 1):
                opt_name = opt.get("name", "").lower()
                if any(k in opt_name for k in ["color", "colour", "颜色"]):
                    color_idx = i
                elif any(k in opt_name for k in ["size", "尺", "型"]):
                    size_idx = i

            for v in p.get("variants", []):
                sku = v.get("sku", "") or v.get("id", "")
                price = float(v.get("price", 0))
                color = v.get(f"option{color_idx}", "") if color_idx else ""
                size = v.get(f"option{size_idx}", "") if size_idx else ""

                products.append({
                    "Product Name": name,
                    "SKU": str(sku),
                    "Color": [color] if color else [],
                    "Size": [size] if size else [],
                    "Category": [product_type] if product_type else [],
                    "Price": price,
                    "Product URL": {"link": product_url, "text": name},
                    **({"Image URL": {"link": img_url, "text": "View Image"}} if img_url else {}),
                    "Brand": brand_name,
                    "Date Collected": today
                })

            print(f"✅ {name} | {len(p.get('variants', []))} SKUs | from ${p['variants'][0]['price'] if p.get('variants') else 0}")

        page += 1
        if len(items) < 250:
            break

    return products


# ── Amazon ─────────────────────────────────────────────────────────────────────

def _extract_amazon_detail(d):
    """Parse enrichment fields from a junglee/amazon-crawler item."""
    # Category path from breadcrumbs
    crumbs = d.get("breadCrumbs") or d.get("breadcrumbs") or []
    if isinstance(crumbs, list):
        category = " > ".join(
            b.get("name", str(b)) if isinstance(b, dict) else str(b) for b in crumbs
        )
    else:
        category = str(crumbs)

    # Best Seller Rank — actor returns a list of {rank, category} dicts
    bsr_list = d.get("bestsellerRanks") or d.get("bestseller_ranks") or []
    if isinstance(bsr_list, list) and bsr_list:
        first = bsr_list[0]
        if isinstance(first, dict):
            bsr_str = f"#{first.get('rank','')} in {first.get('category','')}"
        else:
            bsr_str = str(first)
    else:
        bsr_str = str(bsr_list) if bsr_list else ""

    # Bullet points / features (keep first 5 to stay within Feishu text limit)
    features = d.get("features") or d.get("bullet_points") or []
    bullets = " | ".join(features[:5]) if isinstance(features, list) else str(features)

    # Colors and sizes from variant list
    colors, sizes = set(), set()
    for v in (d.get("variants") or []):
        if not isinstance(v, dict):
            continue
        for key in ("color", "Color", "colour"):
            if v.get(key):
                colors.add(str(v[key]).strip())
        for key in ("size", "Size"):
            if v.get(key):
                sizes.add(str(v[key]).strip())
    # Also grab top-level colorName if present
    if d.get("colorName"):
        colors.add(str(d["colorName"]).strip())

    # Availability
    avail = d.get("availability") or d.get("inStock", "")
    if isinstance(avail, bool):
        in_stock = "Yes" if avail else "No"
    else:
        avail_lower = str(avail).lower()
        if "in stock" in avail_lower or avail_lower == "true":
            in_stock = "Yes"
        elif avail_lower in ("false", "out of stock", "unavailable"):
            in_stock = "No"
        else:
            in_stock = str(avail)

    return {
        "Category":      category,
        "BSR Rank":      bsr_str,
        "Bullet Points": bullets,
        "Colors":        ", ".join(sorted(colors)),
        "Sizes":         ", ".join(sorted(sizes)),
        "In Stock":      in_stock,
    }


def scrape_amazon(keyword, exclude_words=None, top_n=10, max_fetch=None):
    if exclude_words is None:
        exclude_words = []
    if max_fetch is None:
        max_fetch = max(50, top_n * 5)

    print(f"🔍 Searching Amazon: '{keyword}'")
    if exclude_words:
        print(f"🚫 Excluding: {exclude_words}\n")

    raw = run_apify_actor(APIFY_AMAZON_ACTOR_ID, {
        "keyword": keyword, "maxProducts": max_fetch, "marketplace": "amazon.com"
    })
    print(f"\n📦 Got {len(raw)} raw results")

    keyword_terms = keyword.lower().split()
    filtered = [
        p for p in raw
        if not p.get("is_sponsored")
        and all(term in p.get("title", "").lower() for term in keyword_terms)
        and not any(ex.lower() in p.get("title", "").lower() for ex in exclude_words)
    ]
    print(f"✅ After filtering: {len(filtered)} products")

    filtered.sort(key=lambda p: to_int(p.get("reviews_count", 0)), reverse=True)
    top = filtered[:top_n]
    today = today_ms()

    # ── Step 2: Enrich top results with ASIN detail scraper ───────────────────
    print(f"\n🔬 Running ASIN detail scrape on top {len(top)} products...")
    product_urls = [p.get("product_url") or p.get("url", "") for p in top if p.get("product_url") or p.get("url")]
    detail_map = {}
    try:
        detail_items = run_apify_actor(APIFY_AMAZON_DETAIL_ACTOR_ID, {
            "startUrls": [{"url": u} for u in product_urls],
            "maxItems": len(product_urls),
            "proxyConfiguration": {"useApifyProxy": True},
        })
        for d in detail_items:
            asin = d.get("asin", "")
            if asin:
                detail_map[asin] = d
        print(f"✅ Got detail data for {len(detail_map)} products")
    except Exception as e:
        print(f"⚠️  Detail scrape failed ({e}), continuing without enrichment")

    # ── Step 3: Build records ─────────────────────────────────────────────────
    records = []
    for rank, p in enumerate(top, 1):
        asin = p.get("asin", "")
        record = {
            "Text":           p.get("title", ""),
            "Brand":          p.get("brand", ""),
            "ASIN":           asin,
            "Price":          to_float(p.get("price")),
            "Original Price": to_float(p.get("original_price")),
            "Discount %":     to_float(p.get("discount_percentage")),
            "Rating":         to_float(p.get("rating")),
            "Reviews":        to_int(p.get("reviews_count")),
            "Badge":          str(p.get("badge", "") or ""),
            "Product URL":    {"link": p.get("product_url") or p.get("url", ""), "text": p.get("title", "")},
            "Image":          {"link": p.get("image_url", ""), "text": "View Image"},
            "Search Keyword": keyword,
            "Date Collected": today,
        }
        if asin in detail_map:
            record.update(_extract_amazon_detail(detail_map[asin]))
        records.append(record)
        print(f"  #{rank} {p.get('title', '')[:60]} | {p.get('reviews_count', 0)} reviews | ${p.get('price', '')}")

    return records


# ── TikTok ─────────────────────────────────────────────────────────────────────

def get_prop_values(sale_props, prop_name):
    for prop in sale_props:
        if prop.get("prop_name", "").lower() == prop_name.lower():
            return ", ".join(v["prop_value"] for v in prop.get("sale_prop_values", []))
    return ""

def scrape_tiktok(keyword, exclude_words=None, top_n=10):
    if exclude_words is None:
        exclude_words = ["sock"]

    print(f"🔍 Searching TikTok Shop: '{keyword}'")
    if exclude_words:
        print(f"🚫 Excluding: {exclude_words}\n")

    raw = run_apify_actor(APIFY_TIKTOK_ACTOR_ID, {
        "keyword": keyword, "maxItems": max(50, top_n * 5), "country_code": "US"
    })
    print(f"\n📦 Got {len(raw)} raw results")

    filtered = [
        p for p in raw
        if not any(ex.lower() in p.get("product_title", "").lower() for ex in exclude_words)
    ]
    print(f"✅ After filtering: {len(filtered)} products")

    filtered.sort(key=lambda p: to_int(p.get("total_sale_30d_cnt", 0)), reverse=True)
    top = filtered[:top_n]
    today = today_ms()

    records = []
    for rank, p in enumerate(top, 1):
        product_id = p.get("product_id", "")
        product_url = f"https://www.tiktok.com/view/product/{product_id}"
        seller = p.get("seller", {})

        record = {
            "Product Name":   p.get("product_title", ""),
            "Seller":         seller.get("seller_name", ""),
            "Category":       p.get("categories", ""),
            "Min Price":      to_float(p.get("min_price", 0)),
            "Max Price":      to_float(p.get("max_price", 0)),
            "Original Price": to_float(p.get("original_price", 0)),
            "Commission":     str(p.get("commission", "")),
            "Total Sales":    str(p.get("total_sale_cnt", "")),
            "Sales 7D":       to_int(p.get("total_sale_7d_cnt", 0)),
            "Sales 30D":      to_int(p.get("total_sale_30d_cnt", 0)),
            "GMV Total":      str(p.get("total_sale_gmv_amt", "")),
            "GMV 7D":         str(p.get("total_sale_gmv_7d_amt", "")),
            "GMV 30D":        str(p.get("total_sale_gmv_30d_amt", "")),
            "Influencers":    to_int(p.get("influencers_count", 0)),
            "Videos":         to_int(p.get("videos_count", 0)),
            "Views":          str(p.get("view_count", "")),
            "Rating":         to_float(p.get("product_rating", 0)),
            "Reviews":        to_int(p.get("review_count", 0)),
            "Colors":         get_prop_values(p.get("sale_props", []), "Color"),
            "Sizes":          get_prop_values(p.get("sale_props", []), "Size"),
            "Free Shipping":  "Yes" if p.get("is_free_shipping") else "No",
            "Product URL":    {"link": product_url, "text": p.get("product_title", "")},
            "Image":          {"link": p.get("cover_url", ""), "text": "View Image"},
            "Search Keyword": keyword,
            "Date Collected": today,
        }
        records.append(record)
        print(f"  #{rank} {p.get('product_title', '')[:60]} | 30D: {p.get('total_sale_30d_cnt', 0)} sales | {p.get('min_price', '')}")

    return records


# ── Entry point ────────────────────────────────────────────────────────────────

USAGE = """Usage:
  python scraper.py shopify <url> <brand> [keyword_filter]
  python scraper.py amazon  <keyword> [exclude1,exclude2] [top_n] [max_fetch]
  python scraper.py tiktok  <keyword> [exclude1,exclude2] [top_n]

Examples:
  python scraper.py shopify https://wooland.com Wooland
  python scraper.py shopify https://sheepinc.com SheepInc merino
  python scraper.py amazon 'merino wool sweater' sock,yarn
  python scraper.py tiktok 'merino wool' sock,glove
"""

def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "shopify":
        if len(sys.argv) < 4:
            print("Usage: python scraper.py shopify <url> <brand> [keyword_filter]")
            sys.exit(1)
        url, brand = sys.argv[2], sys.argv[3]
        keyword_filter = sys.argv[4].lower() if len(sys.argv) >= 5 else None

        print(f"🚀 Scraping {brand} ({url})...\n")
        if keyword_filter:
            print(f"🔍 Keeping only products matching [{keyword_filter}]\n")

        products = scrape_shopify(url, brand)

        if keyword_filter:
            before = len(products)
            keywords = [k.strip().lower() for k in keyword_filter.split("|")]
            products = [p for p in products if any(k in p["Product Name"].lower() for k in keywords)]
            print(f"\n🔍 After filter: {len(products)} of {before} records kept")

        print(f"\n📦 Total: {len(products)} SKU records")
        if not products:
            print("No data scraped.")
            return

        print("\n🔗 Connecting to Feishu...")
        token = get_feishu_token()
        if not token:
            print("❌ Failed to get Feishu token")
            return

        print("✅ Connected! Writing records...")
        for i in range(0, len(products), 50):
            batch = products[i:i + 50]
            result = write_to_feishu(token, batch, FEISHU_BASE_ID, FEISHU_TABLE_ID)
            if result.get("code") == 0:
                print(f"✅ Wrote {len(batch)} records")
            else:
                print(f"❌ Write failed (batch {i // 50 + 1}): {result.get('msg')}")

    elif mode == "amazon":
        if len(sys.argv) < 3:
            print("Usage: python scraper.py amazon <keyword> [exclude1,exclude2] [top_n] [max_fetch]")
            sys.exit(1)
        keyword = sys.argv[2]
        exclude_words = [w.strip().lower() for w in sys.argv[3].split(",")] if len(sys.argv) >= 4 else []
        top_n     = int(sys.argv[4]) if len(sys.argv) >= 5 else 10
        max_fetch = int(sys.argv[5]) if len(sys.argv) >= 6 else None

        records = scrape_amazon(keyword, exclude_words, top_n=top_n, max_fetch=max_fetch)
        if not records:
            print("❌ No results after filtering")
            return

        print("\n🔗 Connecting to Feishu...")
        token = get_feishu_token()
        if not token:
            print("❌ Failed to get Feishu token")
            return

        print("✅ Connected! Writing records...")
        result = write_to_feishu(token, records, FEISHU_AMAZON_BASE_ID, FEISHU_AMAZON_TABLE_ID)
        if result.get("code") == 0:
            print(f"✅ Wrote {len(records)} records to Feishu Amazon table")
        else:
            print(f"❌ Write failed: {result.get('msg')}\n{result}")

    elif mode == "tiktok":
        if len(sys.argv) < 3:
            print("Usage: python scraper.py tiktok <keyword> [exclude1,exclude2] [top_n]")
            sys.exit(1)
        keyword = sys.argv[2]
        exclude_words = [w.strip().lower() for w in sys.argv[3].split(",")] if len(sys.argv) >= 4 else ["sock"]
        top_n = int(sys.argv[4]) if len(sys.argv) >= 5 else 10

        records = scrape_tiktok(keyword, exclude_words, top_n=top_n)
        if not records:
            print("❌ No results after filtering")
            return

        print("\n🔗 Connecting to Feishu...")
        token = get_feishu_token()
        if not token:
            print("❌ Failed to get Feishu token")
            return

        print("✅ Connected! Writing records...")
        result = write_to_feishu(token, records, FEISHU_TIKTOK_BASE_ID, FEISHU_TIKTOK_TABLE_ID)
        if result.get("code") == 0:
            print(f"✅ Wrote {len(records)} records to Feishu TikTok table")
        else:
            print(f"❌ Write failed: {result.get('msg')}\n{result}")

    else:
        print(f"Unknown mode: '{mode}'\n\n{USAGE}")
        sys.exit(1)

    print("\n🎉 Done! Check your Feishu table.")

if __name__ == "__main__":
    main()
