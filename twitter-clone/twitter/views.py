from django.dispatch.dispatcher import receiver
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.db.models import Count
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse


from twitter.models import Tweet, Follow, Notification, Comment
from twitter.myDecor import check_if_user_logged
from twitter.forms import SignUpForm

# Create your views here.
@check_if_user_logged
def index(request):
    return render(request, 'index.html')

@check_if_user_logged
def login(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            mail = request.POST['email']
            pwd = request.POST['password']
            user = authenticate(request, username=mail, password=pwd)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
                return render(request, 'login.html') 
        elif 'cancel' in request.POST:
            return redirect('index')
    else:
        return render(request, 'login.html')

def logout(reqeuest):
    auth_logout(reqeuest)
    return redirect('index')

@check_if_user_logged
def register(request):
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('index')
        elif 'register' in request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password')
                user.set_password(raw_password)
                user.save()
                user = authenticate(request, username=email, password = raw_password)
                auth_login(request, user)
                return redirect('home')
            else:
                form = SignUpForm()
                messages.error(request, 'Invalid form fill')
                return render(request, 'register.html', {'form':form})            
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

@login_required(redirect_field_name=None)
def home(request):
    if request.method == 'POST':
        author = request.user
        content = request.POST['tweet']
        tweet = Tweet(author=author, content=content)
        tweet.save()

        for follower in request.user.following.all().values_list('following_user_id', flat=True):
            Notification.objects.create(sender = request.user, receiver = User.objects.get(id=follower), target = tweet, type = 'L')

        return redirect('home')
    else:
        followedUsers = [request.user]
        for followed in request.user.followers.all():
            followedUsers.append(User.objects.get(id=followed.user_id_id))
        
        tweets = Tweet.objects.filter(author__in=followedUsers).order_by('-timeStamp')
        
        rec_profiles = User.objects.annotate(count=Count('followers')).order_by('followers').exclude(username=request.user.username).exclude(id__in=request.user.followers.all().values_list('user_id', flat=True))[:5]

        return render(request, 'home.html', {'tweets':tweets, 'rec_profiles':rec_profiles})

def profile(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)

        user.profile.bio = request.POST['bio']
        user.profile.profilePic = request.FILES['pic'] if 'pic' in request.FILES else user.profile.profilePic
        user.profile.backgroundPic = request.FILES['banner'] if 'banner' in request.FILES else user.profile.backgroundPic

        user.save()
        return redirect('profile', username=username)
    else:
        try:
            userProfile = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('User Not Found')

        tweets = Tweet.objects.filter(author__exact=userProfile).order_by('-timeStamp')

        is_following = False
        for follow in request.user.followers.all():
            if userProfile.id == follow.user_id_id:
                is_following=True

        rec_profiles = User.objects.annotate(count=Count('followers')).order_by('followers').exclude(username=request.user.username).exclude(username=username).exclude(id__in=request.user.followers.all().values_list('user_id', flat=True))[:5]

        return render(request, 'profile.html', {'userProfile':userProfile, 'tweets':tweets, 'is_following':is_following, 'rec_profiles':rec_profiles})

@login_required(redirect_field_name=None)
def delete_post(request, tweetID):
    if request.method == 'POST':
        tweet = Tweet.objects.get(id=tweetID)
        if tweet.author == request.user:
            tweet.delete()
        return redirect('profile', username=request.user.username)
    else:
        return redirect('home')

@login_required(redirect_field_name=None)
def like_post(request):
    tweet = get_object_or_404(Tweet, id=request.POST.get('id'))
    
    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
        is_liked = False
    else:
        tweet.likes.add(request.user)
        is_liked = True

        if(request.user != tweet.author):
            Notification.objects.create(sender = request.user, receiver = User.objects.get(username = tweet.author), target = tweet, type = 'L')
            
    context = {
        'tweet': tweet,
        'is_liked': is_liked,
    }

    if request.is_ajax():
        html = render_to_string('tweet.html', context, request=request)
        return JsonResponse({'form':html})

@login_required(redirect_field_name=None)
def change_mode(request):
    if request.method == 'POST':
        usr = User.objects.get(id=request.user.id)
        usr.profile.mode = request.POST['mode']
        usr.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(redirect_field_name=None)
def follow_profile(request):
    followed_user = get_object_or_404(User, id=request.POST.get('id'))

    if Follow.objects.filter(user_id=followed_user.id, following_user_id = request.user.id).exists():
        Follow.objects.filter(user_id=followed_user.id, following_user_id = request.user.id).delete()
        is_following = False
    else:
        Follow.objects.create(user_id=followed_user, following_user_id = request.user)
        Notification.objects.create(sender = request.user, receiver = followed_user, target = None, type = 'F')
        is_following = True

    context = {
        'profile':followed_user,
        'userProfile':followed_user,
        'is_following':is_following
    }

    if request.is_ajax():
        html = render_to_string('follow_button.html', context, request=request)
        return JsonResponse({'form':html})


def notifications(request):
    notifics = request.user.your_notifications.all()
    for notific in notifics:
        notific.seen = True
        notific.save()
    notifics = request.user.your_notifications.all().order_by('-id')[:10]
    return render(request, 'notifications.html', {'notifics':notifics})


def tweet_details(request, tweetID):
    tweet = Tweet.objects.get(id=tweetID)
    comments = tweet.main_tweet.all().order_by('-timeStamp')
    
    return render(request, 'tweet_details.html', {'tweet':tweet, 'comments':comments})


def comment(request, tweetID):
    if request.method == 'POST':
        author = request.user
        content = request.POST['comment']
        tweet = Tweet.objects.get(id=tweetID)
        Comment.objects.create(author=author, main_tweet=tweet, content=content)

        if(request.user != tweet.author):
            Notification.objects.create(sender = request.user, receiver = tweet.author, target = tweet, type = 'C')
        return redirect(tweet_details, tweetID=tweetID)
    else:
        return redirect(home)

#Notification on post comment