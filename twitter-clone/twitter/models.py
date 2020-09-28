from django.db import models

# Create your models here.
class Tweet(models.Model):
    author = models.CharField(max_length=50)
    timeStamp = models.DateTimeField(auto_now=True)
    content = models.TextField()