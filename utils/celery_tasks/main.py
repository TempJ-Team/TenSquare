from celery import Celery
import os


# 指定使用django工程默认的配置文件
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ihome.settings')

# 注册异步任务app
celery_app = Celery('ihome')

# 加载配置文件
celery_app.config_from_object('utils.celery_tasks.config')

# 新建了任务以后，要在这里报备，然后 celery_app就可以自动监测制定路径中的任务了
celery_app.autodiscover_tasks([
    'utils.celery_tasks.sms',
])




