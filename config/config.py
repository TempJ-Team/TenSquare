# DEBUG
DEBUG = True

# 运行虚拟环境名
if DEBUG:
    ENV = 'MyMeiduoMall'
else:
    ENV = 'django_env'

eXt_List = ['jpg', 'png', 'PNG', 'GIF', 'JPG', 'gif']

# 密钥
SECRET_KEY = '*x@4+k$_3qd%55+=nvuv&w*%$u=j2l!)#*&x5)3+1vsm(*_0b^'

# 允许访问的域名
URL = '192.168.203.153:8080'
Storage_URL = ''
ALLOWED_HOSTS = ['*']

# 语言设置项
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

# 数据库配置
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_USER = 'root'
DB_PASS = 'mysql'
DB_NAME = 'tensquare'

# Redis数据库配置
Redis_HOST = '127.0.0.1'
Redis_PORT = '6379'

# 日志相关
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/ihome.log'

# 短信服务秘钥
sms_key = ''
sms_token = ''

# 邮箱服务
SMTP_HOST = 'smtp.163.com'
SMTP_PORT = 25
SMTP_USER = 'itcast_weiwei@163.com'
SMTP_PASSWORD = 'MQOCURBQWCSZIJTT'
SMTP_FROM = '爱家租房<itcast_weiwei@163.com>'

# 七牛云相关配置
Qiniu_access_kEy = 'D7XBhwuX2Iw7RERpodL0H6obFg9EcLzD3hLalDcb'
Qiniu_secret_kEy = 'lmwsIUKEHRckQJFKkIpZtZxzP3sy33AcfSIqvcZh'
Qiniu_bucket_nAme = 'smartfox'
Qiniu_rOOt_URL = 'http://kodo.smartfox.cc/'

# ElasticsearchSearch
ES_URL = 'http://192.168.203.153:9200/'
ES_INDEX = 'tensquare'
ES_PER_PAGE = 5
