from django.urls import path
from .views import TaskView, UserPasswordResetView, PassResetEmailView, RegisterView, LoginView, UserView,ChangePassView, ProjectView, ClientView
from .views import TaskView, UserPasswordResetView, PassResetEmailView, RegisterView, LoginView, UserView,ChangePassView, ProjectView, AllDataView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('',UserView.as_view(),name='user'),
    path('change-password/',ChangePassView.as_view(),name='change password'),
    path('projects/',ProjectView.as_view(),name='projects'),
    path('reset-pass-email/',PassResetEmailView.as_view(),name='reset-pass-email'),
    path('reset-pass/<uid>/<token>',UserPasswordResetView.as_view(),name='reset-pass'),
    path('task/',TaskView.as_view(),name='task'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('client/', ClientView.as_view(), name='client'),
    path('all/', AllDataView.as_view(), name='token_refresh'),
]