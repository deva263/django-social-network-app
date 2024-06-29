from django.urls import path
from .views import signup, password_reset, login, search_users, send_friend_request,accept_friend_request,reject_friend_request, list_friends, list_pending_friend_requests

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('password-reset/', password_reset, name='password_reset'),
    path('login/', login, name='login'),
    path('search/<str:search_keyword>/', search_users, name='user-search'),
    path('send-friend-request/', send_friend_request, name='send-friend-request'),
    path('accept-friend-request/', accept_friend_request, name='accept-friend-request'),
    path('reject-friend-request/', reject_friend_request, name='reject-friend-request'),
    path('list-friends/', list_friends, name='list_friends'),
    path('list-pending-friend-requests/', list_pending_friend_requests, name='list_pending_friend_requests'),
]