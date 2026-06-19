import requests
import os
from dotenv import load_dotenv

load_dotenv()

FEISHU_APP_ID     = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
FEISHU_TABLE_ID   = os.getenv("FEISHU_TABLE_ID")
FEISHU_BASE_ID    = os.getenv("FEISHU_BASE_ID")

BASE_URL = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_TABLE_ID}/tables/{FEISHU_BASE_ID}"

def get_token():
    res = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    )
    return res.json().get("tenant_access_token")

def fetch_all_records(token):
    headers = {"Authorization": f"Bearer {token}"}
    records = []
    page_token = None

    while True:
        params = {"page_size": 500}
        if page_token:
            params["page_token"] = page_token
        res = requests.get(f"{BASE_URL}/records", headers=headers, params=params)
        data = res.json()
        items = data.get("data", {}).get("items", [])
        records.extend(items)
        print(f"已读取 {len(records)} 条...")
        if not data.get("data", {}).get("has_more"):
            break
        page_token = data["data"]["page_token"]

    return records

def delete_records(token, record_ids):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    for i in range(0, len(record_ids), 100):
        batch = record_ids[i:i+100]
        res = requests.post(f"{BASE_URL}/records/batch_delete", headers=headers, json={"records": batch})
        result = res.json()
        if result.get("code") == 0:
            print(f"✅ 删除 {len(batch)} 条")
        else:
            print(f"❌ 删除失败: {result.get('msg')}")

def main():
    print("🔗 获取Token...")
    token = get_token()

    print("📖 读取所有记录...")
    records = fetch_all_records(token)
    print(f"共 {len(records)} 条记录")

    # 按SKU去重，保留第一条，删除其余
    seen = {}
    to_delete = []
    for r in records:
        sku = r.get("fields", {}).get("SKU", "")
        record_id = r.get("record_id")
        if sku in seen:
            to_delete.append(record_id)
        else:
            seen[sku] = record_id

    print(f"发现 {len(to_delete)} 条重复记录，{len(seen)} 条唯一记录")

    if not to_delete:
        print("没有重复，无需处理")
        return

    print("🗑️ 开始删除重复记录...")
    delete_records(token, to_delete)
    print("✅ 去重完成！")

if __name__ == "__main__":
    main()
