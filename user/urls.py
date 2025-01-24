from django.urls import path
from .views import UserPasswordResetView, PassResetEmailView, RegisterView, LoginView, UserView,ChangePassView, ProjectView

urlpatterns = [
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('',UserView.as_view(),name='user'),
    path('change-password/',ChangePassView.as_view(),name='change password'),
    path('projects/',ProjectView.as_view(),name='projects'),
    path('reset-pass-email/',PassResetEmailView.as_view(),name='reset-pass-email'),
    path('reset-pass/<uid>/<token>',UserPasswordResetView.as_view(),name='reset-pass'),
]