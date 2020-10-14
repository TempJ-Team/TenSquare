"""
WSGI config for TenSquare project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from multiprocessing import Process
from django.core.wsgi import get_wsgi_application
from config.config import ENV

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TenSquare.settings')

application = get_wsgi_application()


def check_migrate() -> None:
    # cmd = 'cd .. && /root/.virtualenvs/MyMeiduoMall/bin/python manage.py makemigration'
    # os.system(cmd)
    # cmd = '/root/.virtualenvs/MyMeiduoMall/bin/python manage.py migrate'
    # os.system(cmd)
    pass


def redis_server() -> None:
    cmd = 'redis-server'
    os.system(cmd)


def sms_server() -> None:
    # cmd = 'bash workon MyMeiduoMall'
    # os.system(cmd)
    # cmd = 'cd .. && /root/.virtualenvs/MyMeiduoMall/bin/celery -A utils.celery_tasks.main worker -l info'
    cmd = "bash -c 'source /root/.bashrc && source /usr/local/bin/virtualenvwrapper.sh && workon " + ENV +" && cd .. && celery -A utils.celery_tasks.main worker -l info'"
    os.system(cmd)
    pass


def run_task() -> None:
    print('正在检查数据库迁移情况')
    check_migrate()

    print('正在启动Redis')
    t = Process(target=redis_server, args=())
    t.start()

    # print('正在启动前端静态服务')
    # t = Process(target=frontend_server, args=())
    # t.start()

    print('正在启动短信服务')
    t = Process(target=sms_server, args=())
    t.start()


#run_task()
