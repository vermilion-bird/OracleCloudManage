import logging
from notion_sdk.databases import query_row, insert_row, update_row

logger = logging.getLogger(__name__)


def construct_properties_body(label: str, type_x: str, data) -> dict:
    """构建 Notion API properties body"""
    body = {'properties': {}}

    property_builders = {
        'checkbox': lambda: {label: {'type': 'checkbox', 'checkbox': data}},
        'date': lambda: {label: {'type': 'date', 'date': {'start': data, 'end': None}}},
        'select': lambda: {label: {'type': 'select', 'select': {'name': data}}},
        'rich_text': lambda: {label: {'type': 'rich_text', 'rich_text': [
            {'type': 'text', 'text': {'content': data}, 'plain_text': data}]}},
        'title': lambda: {label: {'id': 'title', 'type': 'title', 'title': [
            {'type': 'text', 'text': {'content': data}, 'plain_text': data}]}},
        'number': lambda: {label: {'type': 'number', 'number': data}},
    }

    if type_x in property_builders:
        body['properties'].update(property_builders[type_x]())

    return body


def write_instance2notion(instances: list):
    """将实例列表写入 Notion 数据库"""
    for instance in instances:
        update_or_insert(instance)


def construct_instance(instance) -> dict:
    """构建实例的 Notion properties 结构"""
    return {
        "properties": {
            "display_name": {
                "title": [{"text": {"content": instance.display_name}}]
            },
            "region": {
                'rich_text': [{
                    'type': 'text',
                    'text': {'content': instance.region},
                    'plain_text': instance.region
                }]
            },
            'lifecycle_state': {
                'type': 'select',
                'select': {'name': instance.lifecycle_state}
            },
            'time_created': {
                'rich_text': [{
                    'type': 'text',
                    'text': {'content': instance.time_created},
                    'plain_text': instance.time_created
                }]
            },
            'ip': {
                'rich_text': [{
                    'type': 'text',
                    'text': {'content': instance.ip},
                    'plain_text': instance.ip
                }]
            },
            'processor_description': {
                'rich_text': [{
                    'type': 'text',
                    'text': {'content': instance.processor_description},
                    'plain_text': instance.processor_description
                }]
            },
        }
    }


def update_or_insert(instance):
    """更新或插入实例到 Notion"""
    filters = {
        "filter": {
            "property": "display_name",
            "title": {"equals": instance.display_name}
        }
    }

    page_id = None
    try:
        page_id = query_row(filters)
    except Exception as e:
        logger.debug(f"查询实例 {instance.display_name} 时发生错误 (可能不存在): {e}")

    properties = construct_instance(instance)

    if page_id:
        logger.info(f"更新数据: {page_id}")
        update_row(page_id, properties)
    else:
        logger.info(f"插入数据: {instance.display_name}")
        insert_row(properties)