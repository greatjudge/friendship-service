from django.urls import path
from .views import RegisterView, UserDetail, UserList


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('', UserList.as_view(), name='user_list'),
    path('<int:pk>/', UserDetail.as_view(), name='user_detail'),
]
