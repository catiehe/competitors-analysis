import requests
import subprocess
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

FEISHU_APP_ID     = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
FEISHU_TABLE_ID   = os.getenv("FEISHU_TABLE_ID")
FEISHU_BASE_ID    = os.getenv("FEISHU_BASE_ID")

def get_feishu_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    res = requests.post(url, json={
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    })
    return res.json().get("tenant_access_token")

def write_to_feishu(token, records):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_TABLE_ID}/tables/{FEISHU_BASE_ID}/records/batch_create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"records": [{"fields": r} for r in records]}
    res = requests.post(url, headers=headers, json=payload)
    return res.json()

def fetch_json(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        data = res.json()
        if "products" in data:
            return data
    except Exception:
        pass
    # 被拦截时回退到 curl
    result = subprocess.run(["curl", "-s", "--max-time", "15", url], capture_output=True, text=True)
    return json.loads(result.stdout)

def scrape_shopify(base_url, brand_name):
    products = []
    today = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)
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

            # 找出哪个option是颜色、哪个是尺码
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
                compare_price = float(v.get("compare_at_price") or 0)
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
                    "Competitor Source": brand_name,
                    "Brand": brand_name,
                    "Date Collected": today
                })

            print(f"✅ {name} | 共{len(p.get('variants',[]))}个SKU | 价格从${p['variants'][0]['price'] if p.get('variants') else 0}起")

        page += 1
        if len(items) < 250:
            break

    return products

def main():
    import sys
    if len(sys.argv) >= 3:
        url, brand = sys.argv[1], sys.argv[2]
        keyword = sys.argv[3].lower() if len(sys.argv) >= 4 else None
    else:
        print("用法: python scraper.py <品牌URL> <品牌名> [关键词过滤]")
        print("示例: python scraper.py https://wooland.com Wooland")
        print("示例: python scraper.py https://sheepinc.com SheepInc merino")
        sys.exit(1)

    print(f"🚀 开始抓取 {brand} ({url})...\n")
    if keyword:
        print(f"🔍 仅保留产品名包含 [{keyword}] 的记录\n")

    products = scrape_shopify(url, brand)

    if keyword:
        before = len(products)
        keywords = [k.strip().lower() for k in keyword.split("|")]
        products = [p for p in products if any(k in p["Product Name"].lower() for k in keywords)]
        print(f"\n🔍 过滤后保留 {len(products)} 条（原 {before} 条）")
    print(f"\n📦 共抓取 {len(products)} 个SKU记录")

    if not products:
        print("没有抓到数据")
        return

    print("\n🔗 正在连接飞书...")
    token = get_feishu_token()
    if not token:
        print("❌ 飞书Token获取失败")
        return

    print("✅ 飞书连接成功！")
    print("📝 正在写入数据...")

    batch_size = 50
    for i in range(0, len(products), batch_size):
        batch = products[i:i+batch_size]
        result = write_to_feishu(token, batch)
        if result.get("code") == 0:
            print(f"✅ 写入 {len(batch)} 条")
        else:
            print(f"❌ 写入失败 (batch {i//batch_size + 1}): {result.get('msg')}")

    print("\n🎉 完成！请打开飞书多维表格查看数据")

if __name__ == "__main__":
    main()