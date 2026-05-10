import os
import yaml

_config_loaded = False
ACCOUNTS = []
NOTION_TOKEN = ""
DATABASE_ID = ""


def load_config():
    """加载配置文件"""
    global ACCOUNTS, NOTION_TOKEN, DATABASE_ID, _config_loaded

    if _config_loaded:
        return ACCOUNTS, NOTION_TOKEN, DATABASE_ID

    config_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(config_dir, 'config.yaml')

    with open(config_path) as f:
        data = yaml.safe_load(f)

    if data is None:
        raise ValueError(f"配置文件 {config_path} 为空或解析失败")

    accounts = data.get('accounts', [])
    # 处理 key_file 路径
    ACCOUNTS = [
        {k: os.path.join(config_dir, 'file', v) if k == 'key_file' else v
         for k, v in account.items()}
        for account in accounts
    ]

    notion_config = data.get('notion', {})
    NOTION_TOKEN = notion_config.get('token', '')
    DATABASE_ID = notion_config.get('database_id', '')

    _config_loaded = True
    return ACCOUNTS, NOTION_TOKEN, DATABASE_ID


# 在模块导入时加载配置
ACCOUNTS, NOTION_TOKEN, DATABASE_ID = load_config()