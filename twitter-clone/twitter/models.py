from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Tweet(models.Model):
    author = models.CharField(max_length=50)
    timeStamp = models.DateTimeField(auto_now=True)
    content = models.TextField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    profilePic = models.ImageField(upload_to='pics', null=True, blank=True)
    backgroundPic = models.ImageField(upload_to='banners', null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
        
    
        
    