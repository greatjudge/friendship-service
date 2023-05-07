from django.urls import path
from .views import RegisterView, UserDetail


urlpatterns = [
    path("register/", RegisterView.as_view(), name='register_user'),
    path('<int:pk>/', UserDetail.as_view(), name='user_detail'),
]
