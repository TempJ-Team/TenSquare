'''
Descripition: 
Version: 
Author: SmartFox97
Date: 2020-10-12 20:12:55
LastEditors: SmartFox97
LastEditTime: 2020-10-13 23:34:27
'''
from celery import Celery


# 指定使用django工程默认的配置文件
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ihome.settings')

# 注册异步任务app
celery_app = Celery('tensquare')

# 加载配置文件
celery_app.config_from_object('utils.celery_tasks.config')
celery_app.autodiscover_tasks([
    'utils.celery_tasks.sms',
])



