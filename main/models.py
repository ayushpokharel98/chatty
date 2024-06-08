from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Profile(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fn = models.CharField(max_length=155)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(default='default_avatar.png', upload_to='profile_picture')
    def __str__(self):
        return f'{self.user.username}'

class Friends(models.Model):

    id = models.AutoField(primary_key=True, unique=True, editable=False, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friend")

    def __str__(self):
        return f"{self.user} - {self.friend}' Friends"

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True, unique=True, editable=False, blank=True)
    chat_name = models.CharField(max_length=255, editable=False, blank=True)
    chat_between = models.ForeignKey(Friends, on_delete=models.CASCADE, related_name="chats_as_user")

    def __str__(self):
        return f"{self.chat_id}. Chat between {self.chat_between}"

class Message(models.Model):
    MESSAGE_STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    ]
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=MESSAGE_STATUS_CHOICES, default='sent')

    def __str__(self):
        return f"{self.chat.chat_id} - {self.sender.username}: {self.content[:20]}"