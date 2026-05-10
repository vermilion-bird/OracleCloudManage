import json
import logging
import requests
from conf.config import DATABASE_ID, NOTION_TOKEN

logger = logging.getLogger(__name__)

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
base_url = "https://api.notion.com/v1"


def query_row(filter: dict) -> str:
    """
    查询 Notion 数据库中的行

    Args:
        filter: 查询过滤器，格式如:
            {"filter": {"property": "col_name", "title": {"equals": "value"}}}

    Returns:
        str: 匹配行的 page ID

    Raises:
        Exception: 查询失败或无结果时抛出异常
    """
    url = f"{base_url}/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers, data=json.dumps(filter))
    response.raise_for_status()
    data = response.json()

    if not data.get("results"):
        raise ValueError("查询无结果")

    return data["results"][0]["id"]


def insert_row(properties: dict) -> dict:
    """
    在 Notion 数据库中插入新行

    Args:
        properties: 行属性，格式如:
            {"properties": {"display_name": {"title": [{"text": {"content": "value"}}]}}}

    Returns:
        dict: API 响应结果
    """
    url = f"{base_url}/pages/"
    payload = {
        "parent": {"database_id": DATABASE_ID}
    }
    payload.update(properties)

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()


def update_row(page_id: str, properties: dict) -> dict:
    """
    更新 Notion 数据库中的行

    Args:
        page_id: 要更新的页面 ID
        properties: 更新的属性，格式如:
            {"properties": {"display_name": {"title": [{"text": {"content": "value"}}]}}}

    Returns:
        dict: API 响应结果
    """
    url = f"{base_url}/pages/{page_id}"
    response = requests.patch(url, headers=headers, data=json.dumps(properties))
    response.raise_for_status()
    return response.json()