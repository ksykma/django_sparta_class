from django.db import models
from user.models import UserModel
from taggit.managers import TaggableManager  # 우리가 우리 글에 태그를 추가해 줄 수 있게 만들어주는 매니저


# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    tags = TaggableManager(blank=True)  # 이게 비어있어도 작동하겠다.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TweetComment(models.Model):
    class Meta:
        db_table = "comment"
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)