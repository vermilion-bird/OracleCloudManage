from oracle_sdk.oracle_cloud import get_instance_from_account
from notion_sdk.notion_api import write_instance2notion

if __name__ == '__main__':
    instances = get_instance_from_account()
    write_instance2notion(instances)
