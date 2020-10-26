from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('like', views.like_post, name='like_post'),
    path('notifications', views.notifications, name='notifications'),
    path('comment/<int:tweetID>', views.comment, name='comment' ),
    path('tweet_details/<int:tweetID>', views.tweet_details, name='tweet_details'),
    path('delete/<int:tweetID>', views.delete_post, name='delete_post'),
    path('follow_profile', views.follow_profile, name='follow_profile'),
    path('change_mode', views.change_mode, name='change_mode'),
    path('<str:username>', views.profile, name='profile'),    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)