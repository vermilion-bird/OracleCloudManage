from notion_sdk.databases import query_row, insert_row, update_row
import os
import sys
sys.path.append(os.getcwd())


def body_propertie_input(label, type_x, data):
    body = {
        'properties': {}
    }

    if type_x == 'checkbox':
        body['properties'].update(
            {label: {'type': 'checkbox', 'checkbox': data}})

    if type_x == 'date':
        body['properties'].update(
            {label: {'type': 'date', 'date': {'start': data, 'end': None}}})

    if type_x == 'select':
        body['properties'].update(
            {label: {'type': 'select', 'select': {'name': data}}})

    if type_x == 'rich_text':
        body['properties'].update({label: {'type': 'rich_text', 'rich_text': [
                                  {'type': 'text', 'text': {'content': data},  'plain_text': data}]}})

    if type_x == 'title':
        body['properties'].update({label: {'id': 'title', 'type': 'title', 'title': [
                                  {'type': 'text', 'text': {'content': data}, 'plain_text': data}]}})

    if type_x == 'number':
        body['properties'].update({label: {'type': 'number', 'number': data}})

    return body


def write_instance2notion(instances):
    for instance in instances:
        update_or_insert(instance)


def construct_instance(instance):
    properties = {"properties": {
        "display_name": {"title": [
            {
                "text": {
                    "content": instance.display_name
                }
            }
        ]},
        "region": {
            'rich_text': [{'type': 'text',
                           'text': {'content': instance.region},
                           'plain_text': instance.region}]
        },
        'lifecycle_state': {
            'type': 'select',
            'select': {'name': instance.lifecycle_state}
        },
        'time_created': {
            'rich_text': [{
                'type': 'text',
                        'text': {'content': instance.time_created},
                        'plain_text': instance.time_created}]
        },
        'ip': {
            'rich_text': [{
                'type': 'text',
                        'text': {'content': instance.ip},
                        'plain_text': instance.ip}]
        },
    }}
    return properties


def update_or_insert(instance):
    filters = {"filter":
               {
                   "property": "display_name",
                   "title": {"equals": instance.display_name}
               }
               }
    try:
        page_id = query_row(filters)
    except Exception as e:
        page_id = None
    properties = construct_instance(instance)
    if page_id:
        print("更新数据", page_id)
        update_row(page_id, properties)
    else:
        print("插入数据")
        insert_row(properties)
