import requests
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

FEISHU_APP_ID          = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET      = os.getenv("FEISHU_APP_SECRET")
FEISHU_WIKI_PARENT_TOKEN = os.getenv("FEISHU_WIKI_PARENT_TOKEN")

def get_token():
    res = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    )
    return res.json().get("tenant_access_token")

def get_space_id(token, node_token):
    res = requests.get(
        f"https://open.feishu.cn/open-apis/wiki/v2/nodes",
        headers={"Authorization": f"Bearer {token}"},
        params={"token": node_token}
    )
    data = res.json()
    if data.get("code") != 0:
        print(f"❌ 获取Wiki节点失败: {data.get('msg')}")
        return None
    return data["data"]["node"]["space_id"]

def create_wiki_subpage(token, space_id, parent_token, title):
    res = requests.post(
        f"https://open.feishu.cn/open-apis/wiki/v2/spaces/{space_id}/nodes",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "obj_type": "docx",
            "parent_node_token": parent_token,
            "node_type": "origin",
            "title": title
        }
    )
    data = res.json()
    if data.get("code") != 0:
        print(f"❌ 创建子页面失败: {data.get('msg')}")
        return None
    node = data["data"]["node"]
    return node["obj_token"], node["url"]

def write_content_to_doc(token, doc_token, content):
    # Get document blocks to find the first block
    res = requests.get(
        f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks",
        headers={"Authorization": f"Bearer {token}"},
        params={"page_size": 1}
    )
    data = res.json()
    if data.get("code") != 0:
        print(f"❌ 获取文档块失败: {data.get('msg')}")
        return

    page_block_id = data["data"]["items"][0]["block_id"]

    # Write content as a text block
    res = requests.patch(
        f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{page_block_id}/children",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "children": [{
                "block_type": 2,  # text block
                "text": {
                    "elements": [{"text_run": {"content": content}}],
                    "style": {}
                }
            }],
            "index": 0
        }
    )
    result = res.json()
    if result.get("code") != 0:
        print(f"❌ 写入内容失败: {result.get('msg')}")
    else:
        print("✅ 内容写入成功")

def main():
    if len(sys.argv) < 3:
        print("用法: python create_wiki_doc.py <brand_name> <report_content>")
        sys.exit(1)

    brand = sys.argv[1]
    content = sys.argv[2]
    date = datetime.now().strftime("%Y-%m-%d")
    title = f"{brand}_{date}"

    print(f"🔗 获取Token...")
    token = get_token()

    print(f"📖 获取Wiki空间信息...")
    space_id = get_space_id(token, FEISHU_WIKI_PARENT_TOKEN)
    if not space_id:
        return

    print(f"📄 创建子页面: {title}")
    result = create_wiki_subpage(token, space_id, FEISHU_WIKI_PARENT_TOKEN, title)
    if not result:
        return

    doc_token, url = result
    print(f"✅ 子页面创建成功: {url}")

    print(f"✏️ 写入报告内容...")
    write_content_to_doc(token, doc_token, content)
    print(f"🎉 完成！查看报告: {url}")

if __name__ == "__main__":
    main()
