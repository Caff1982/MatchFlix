from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('update_profile/', ProfileView.as_view(), name='update_profile'),
    path('accounts/login/', auth_views.LoginView.as_view(
                            template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
                            template_name='accounts/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
                            template_name='accounts/password_change_done.html'), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile/<pk>/', profile_view, name='profile_view'),
    path('friends-search/', friend_search, name='friend_search'),
]