from datetime import datetime
from django.db import models
from django.contrib.auth.backends import get_user_model

# 吐槽和吐槽的评论数据都存储在mongodb中,不是存储在mysql中
# 吐槽和吐槽的评论都属于吐槽的这张表
# 吐槽的parent_id为None,评论则有parent_id

User = get_user_model()
class Spit(models.Model):
    content = models.CharField(max_length=255)  # 吐槽内容
    publishtime = models.DateTimeField(default=datetime.utcnow)  # 发布日期
    userid = models.CharField(max_length=255)  # 发布人ID
    nickname = models.CharField(max_length=255)  # 发布人昵称
    visits = models.IntegerField(default=0)  # 浏览量
    thumbup = models.IntegerField(default=0)  # 点赞数
    comment = models.IntegerField(default=0)  # 回复数
    avatar = models.CharField(max_length=255, null=True)  # 用户的头像
    parent = models.ForeignKey("Spit", on_delete=models.CASCADE, null=True)  # 上级ID
    collected = models.BooleanField(default=False)  # 是否收藏
    hasthumbup = models.BooleanField(default=False)  # 是否点赞
    collected_users = models.ManyToManyField(User, symmetrical=False, related_name='collected_users', verbose_name="收藏者")
    hasthumbup_users = models.ManyToManyField(User, symmetrical=False, related_name='hasthumbup_users', verbose_name="点赞者")

    meta = {'collection': 'spit'}

    def __unicode__(self):
        return self.content
