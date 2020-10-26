from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Tweet(models.Model):
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now=True)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    profilePic = models.ImageField(upload_to='pics', null=True, blank=True)
    backgroundPic = models.ImageField(upload_to='banners', null=True, blank=True)
    
    LIGHT_MODE = 'L'
    DARK_MODE = 'D'
    MODES = [
        (DARK_MODE, 'Darkmode'),
        (LIGHT_MODE, 'Lightmode'),
    ]
    mode = models.CharField(max_length=1, choices=MODES, default=DARK_MODE)
 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
        
    
class Follow(models.Model):
    user_id = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)


class Notification(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='your_notifications', on_delete=models.CASCADE)
    target = models.ForeignKey(Tweet, related_name='target', on_delete=models.CASCADE)

    LIKED = 'L'
    POSTED = 'P'
    COMMENTED = 'C'
    FOLLOWED = 'F'
    TYPES = [
        (LIKED, 'liked'),
        (POSTED, 'posted'),
        (COMMENTED, 'commented'),
        (FOLLOWED, 'followed')
    ]
    type = models.CharField(max_length=1, choices=TYPES)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.seen)

    def Notify(self):
        switcher = {
            'L': f'{self.sender} liked your tweet!',
            'P': f'{self.sender} posted a new tweet!',
            'C': f'{self.sender} commented on your tweet!',
            'F': f'{self.sender} is now following you!',
        }
        
        return switcher.get(self.type)

class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comment_author', on_delete=models.CASCADE)
    main_tweet = models.ForeignKey(Tweet, related_name='main_tweet', on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now=True)
    content = models.TextField()