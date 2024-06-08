from django.urls import path
from . import views
urlpatterns = [
   path("", views.index, name="index"),
   path("user", views.authentication, name="authentication"),
   path("handlelogin", views.handlelogin, name="login"),
   path("handleLogout", views.handleLogout, name="login"),
   path("handleSignup", views.handleSignup, name="signup"),
   path("profile", views.profile, name="profile"),
   path('search/', views.search, name='search'),
   path('add/<str:username>', views.addPeople, name='add'),
   path('addchat/<str:username>', views.addChat, name='add'),
   path('chat/<str:chat_name>', views.chats, name='chats'),
]

