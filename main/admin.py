from django.contrib import admin
from .models import Profile, Friends, Chat, Message
admin.site.register(Profile)
admin.site.register(Friends)
admin.site.register(Chat)
admin.site.register(Message)