from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.db.models import Count

from twitter.models import Tweet, Profile, Follow
from twitter.myDecor import check_if_user_logged
from twitter.forms import SignUpForm
from django.http import HttpResponseRedirect

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
        author = request.user.username
        content = request.POST['tweet']
        tweet = Tweet(author=author, content=content)
        tweet.save()

        return redirect('home')
    else:
        followedUsers = [request.user.username]
        followedQuery = request.user.followers.all()
        for followed in followedQuery:
            followedUsers.append(User.objects.get(id=followed.user_id_id).username)
        tweets = Tweet.objects.filter(author__in=followedUsers)
        
        rec_profiles = User.objects.annotate(count=Count('followers')).order_by('followers').exclude(username=request.user.username)[:5]

        return render(request, 'home.html', {'tweets':tweets[::-1], 'rec_profiles':rec_profiles})

def profile(request, username, tweetID=None):
    if request.method == 'POST':
        if 'follow' in request.POST:
            Follow.objects.create(user_id=User.objects.get(username=username), following_user_id=request.user)
            return redirect('profile', username=username)
        elif 'unfollow' in request.POST:
            Follow.objects.filter(user_id=User.objects.get(username=username), following_user_id=request.user).delete()
            return redirect('profile', username=username)
        elif 'delete' in request.POST:
            Tweet.objects.get(id=tweetID).delete()
            return redirect('profile', username=username)
        else:
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

        tweets = Tweet.objects.filter(author__exact=username)

        following = False
        for follow in request.user.followers.all():
            if userProfile.id == follow.user_id_id:
                following=True

        followersNum = request.user.following.all().count()
        followedNum = request.user.followers.all().count()
        rec_profiles = User.objects.annotate(count=Count('followers')).order_by('followers').exclude(username=request.user.username).exclude(username=username)[:5]

        return render(request, 'profile.html', {'userProfile':userProfile, 'tweets':tweets[::-1], 'following':following, 'followersNum':followersNum, 'followedNum':followedNum, 'rec_profiles':rec_profiles})

def like_post(request, tweetID):
    post = get_object_or_404(Tweet, id=tweetID)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return redirect('home')