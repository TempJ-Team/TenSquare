import qiniu
import io
import uuid
from PIL import Image
from django.conf import settings
import imghdr


def image_file(value):
    """
    检查是否是图片文件
    # 防止上传其他文件
    :param value:
    :return:
    """
    try:
        file_type = imghdr.what(value)
        return file_type if file_type else None
    except:
        return None


_kodo = qiniu.Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)


# 封装一个吊炸天的狐狸函数
def imAge_upload(img):
    _img = img.read()
    _size = len(_img) / (1024 * 1024)

    image = Image.open(io.BytesIO(_img))

    _key = str(uuid.uuid1()).replace('-', '')

    _name = 'upfile.{0}'.format(image.format)

    if _size > 1:
        x, y = image.size
        im = image.resize((int(x / 1.73), int(y / 1.73)), Image.ANTIALIAS)
    else:
        im = image

    im.save('./media/' + _name)
    path = './media/' + _name

    token = _kodo.upload_token(settings.QINIU_BUCKET_NAME, _key, 3600, )
    try:
        qiniu.put_file(token, _key, path)
    except Exception as e:
        raise e

    url = settings.QINIU_ROOT_URL + _key

    return url
