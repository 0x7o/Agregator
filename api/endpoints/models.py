from django.db import models


class Article(models.Model):
    url = models.URLField()
    title = models.TextField()
    text = models.TextField(default=None, null=True)
    image = models.URLField(default=None, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
