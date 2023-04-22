import json
from conf.config import DATABASE_ID, NOTION_TOKEN
import requests
import os
import sys
sys.path.append(os.getcwd())

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
base_url = "https://api.notion.com/v1"


def query_row(filter):
    """_summary_
    Args:
        filter (_type_):
        {"filter": 
            {
            "property": col_name,
            "title": {"equals": value}
            }
        }
    Returns:
        _type_: _description_
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers, data=json.dumps(filter))
    response = response.json()
    row_id = response["results"][0]["id"]
    return row_id


def insert_row(properties):
    """_summary_
    Args:
        properties (_type_): 
        {
        "display_name":{ "title": [
        {"text": {"content": "instance.display_name"}}] 
            }
        }
    Returns:
        _type_: _description_
    """
    url = base_url+'/pages/'
    payload = {
        "parent": {"database_id": DATABASE_ID}
    }
    payload.update(properties)
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    return r.json()


def update_row(page_id, properties):
    """_summary_

    Args:
        page_id (_type_): _description_
        properties (_type_): {
        "display_name":{ "title": [
        {"text": {"content": "instance.display_name"}}] 
            }
        }

    Returns:
        _type_: _description_
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    r = requests.patch(url, headers=headers, data=json.dumps(properties))
    return r.json()
