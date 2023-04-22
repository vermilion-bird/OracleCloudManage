import os
import yaml

config_basedir = os.getcwd() + '/conf/'
with open(f'{config_basedir}config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    ACCOUNTS = data.get('accounts')
    ACCOUNTS = [{k: os.getcwd()+'/conf/file/'+v if k ==
                 'key_file' else v for k, v in i.items()} for i in ACCOUNTS]
    NOTION_TOKEN = data.get('notion').get('token')
    DATABASE_ID = data.get('notion').get('database_id')
