from django.urls import path
from .views import (
    FriendsList,
    FriendshipDetail,
    FriendRequestList,
    FriendRequestDetail,
    FriendRequestAccepter
)


urlpatterns = [
    path("", FriendsList.as_view(), name='friend list'),
    path('<int:pk>/', FriendshipDetail.as_view(), name='friendship'),
    path('friend_requests/',
         FriendRequestList.as_view(),
         name='friend request list'),
    path('friend_requests/<int:user_to>/',
         FriendRequestDetail.as_view(),
         name='friend requests'),
    path('friend_requests/accepter/<int:user_from>/',
         FriendRequestAccepter.as_view(),
         name='friend requests')
]
