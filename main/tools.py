from .models import Profile
from django.contrib.auth.models import User

from .models import Friends, Chat

def getFriendsList(id):
    try:
        user = Profile.objects.get(id=id)
        friends = Friends.objects.filter(user=user)
        friend_list = []
        for i in friends:
            friend_list.append(i)
        return friend_list
    except:
        return []

def getUserId(username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user = user)
    id = user_profile.id
    return id

def getChatName(id):
    try:
        # Retrieve the user's Profile instance
        user = Profile.objects.get(id=id)
        # Retrieve all Friends instances where the user is involved
        friends = Friends.objects.filter(user=user)
        # Retrieve Chat instances involving the user's friends
        chats = Chat.objects.filter(chat_between__in=friends)
        # Extract chat_id values from the Chat instances
        chat_ids = [chat.chat_name for chat in chats]
        return chat_ids
    except:
        # Handle the case where the Profile does not exist
        return []
