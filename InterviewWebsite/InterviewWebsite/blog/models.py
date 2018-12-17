import datetime
from django.db import models
from django.utils import timezone


class Author(models.Model):
    author_id = models.CharField(max_length=32)
    small_avatar_url = models.TextField()
    username = models.CharField(max_length=32)


class Comment(models.Model):
    comment_text = models.TextField(max_length=400)
    article_id = models.CharField(max_length=36)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')

    def is_recent_comment(self, num_days=0):
        now = timezone.now()
        return now - datetime.timedelta(days=num_days) <= self.pub_date <= now
