from django.shortcuts import HttpResponse, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import Login, SignUp, ProfileForm
from .models import Profile, Friends, Chat, Message
from .tools import getFriendsList, getUserId, getChatName
from django.http import JsonResponse


def search(request):
    query = request.GET.get('query')
    if query:
        users = User.objects.filter(username__icontains=query)
        profiles = Profile.objects.filter(user__in=users)
        data = [
            {
                'username': profile.user.username,
                'pp': profile.avatar.url  # Add the fields you need from the Profile model
            }
            for profile in profiles
        ]
    else:
        data = []

    return JsonResponse(data, safe=False)


@login_required(login_url="/user")
def index(request):
    if Profile.objects.filter(user=request.user).exists():
        user_profile = Profile.objects.get(user=request.user)
        id = user_profile.id
        friends = getFriendsList(id)
        friends_chat = Friends.objects.filter(user=request.user.profile)
        chats = Chat.objects.filter(chat_between__in=friends_chat)
        context = {
            'profile': user_profile,
            'friends': friends,
            'chats': chats,
        }
        return render(request, "index.html", context)
    else:
        return redirect('/profile')


def authentication(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        context = {
            'form': Login(),
            'form2': SignUp()
        }
        return render(request, "authentication.html", context)


def handleSignup(request):
    if request.method == "POST":
        form2 = SignUp(request.POST)
        form = Login()
        if form2.is_valid():
            myusername = form2.cleaned_data['username']
            myemail = form2.cleaned_data['email']
            mypassword = form2.cleaned_data['password']
            myUser = User.objects.create_user(username=myusername, email=myemail, password=mypassword)
            myUser.save()
            loginaftersignup = authenticate(request, username=myusername, password=mypassword)
            if loginaftersignup is not None:
                login(request, loginaftersignup)
                return redirect('/')
        else:
            # Add form errors to messages for display
            for field, errors in form2.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            return redirect('/user')
    else:
        return redirect('/user')


def handlelogin(request):
    if request.method == "POST":
        form = Login(request.POST)
        form2 = SignUp()
        if form.is_valid():
            myusername = form.cleaned_data['username']
            mypassword = form.cleaned_data['password']
            myUser = authenticate(request, username=myusername, password=mypassword)
            if myUser is not None:
                login(request, myUser)
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('/user')  # Redirect to /user to show error


def handleLogout(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url="/user")
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated!")
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profile.html', context)


def addPeople(request, username):
    friend = User.objects.get(username=username)
    user_id = getUserId(request.user.username)
    friend_id = getUserId(friend.username)

    user_profile = Profile.objects.get(id=user_id)
    friend_profile = Profile.objects.get(id=friend_id)

    # Check if the friendship already exists
    if Friends.objects.filter(user=user_profile, friend=friend_profile).exists():
        messages.error(request, "You are already friends with this user.")
    else:
        # Add the friendship in both directions
        Friends.objects.create(user=user_profile, friend=friend_profile)
        Friends.objects.create(user=friend_profile, friend=user_profile)
        messages.success(request, "Friend added successfully!")

    return redirect('/')


@login_required(login_url="/user")
def addChat(request, username):
    friend = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=request.user)
    friend_profile = Profile.objects.get(user=friend)

    if Chat.objects.filter(chat_between=Friends.objects.get(user=user_profile, friend=friend_profile)).exists() and Chat.objects.filter(chat_between=Friends.objects.get(user=friend_profile, friend=user_profile)).exists():
        messages.error("You are already chatting!")
    else:
        Chat.objects.create(chat_name=f"{request.user.username}and{friend.username}", chat_between=Friends.objects.get(user=user_profile, friend=friend_profile))
        Chat.objects.create(chat_name=f"{request.user.username}and{friend.username}", chat_between=Friends.objects.get(user=friend_profile, friend=user_profile))
        messages.success(request, "Chat started successfully!")

    return redirect('/')

@login_required(login_url="/user")
def chats(request, chat_name):
    user_id = getUserId(request.user.username)
    user_chats = getChatName(user_id)
    chat = Chat.objects.filter(chat_name=chat_name)

    # Initialize chat_messages to avoid UnboundLocalError
    chat_messages = []

    if chat.exists():
        for chats in chat:
            chat_messages.extend(Message.objects.filter(chat=chats))
    
    msg = [{'text': messages.content, 'username': messages.sender.username, 'timestamp':messages.timestamp} for messages in chat_messages]

    if chat_name in user_chats:
        chats = Chat.objects.filter(chat_name=chat_name)
        if chats.exists():
            userchat = None
            for chat in chats:
                if chat.chat_between.user.user.username == request.user.username:
                    userchat = chat
                    break
            context = {
                "userchats": userchat,
                "room_name": chat_name,
                "msg": msg,
            }
            return render(request, "chats.html", context)
        else:
            return HttpResponse("404 Access Denied")
    else:
        return HttpResponse("404 Access Denied")
