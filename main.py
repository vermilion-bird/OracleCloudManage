import logging
from oracle_sdk.oracle_cloud import get_instance_from_account
from notion_sdk.notion_api import write_instance2notion

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    instances = get_instance_from_account()
    write_instance2notion(instances)