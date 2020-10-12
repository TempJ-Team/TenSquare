from utils.celery_tasks.main import celery_app
from utils.yuntongxun.ccp_sms import CCP


@celery_app.task(name='ccp_send_sms_code')
def ccp_send_sms_code(mobile, sms_code):
    # 参数：　电话＋验证码＋提示有效期＋模板
    result = CCP().send_template_sms(mobile, [sms_code, 5], 1)
    return result


