from django.urls import path
from .views import RegisterView, LoginView, UserView,ChangePassView

urlpatterns = [
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('',UserView.as_view(),name='user'),
    path('change-password/',ChangePassView.as_view(),name='change password'),
]