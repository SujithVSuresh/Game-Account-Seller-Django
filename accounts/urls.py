from os import name
from django.urls import path
from .views import UserSignupView, UserLoginView, UserLogoutView, password_reset_request, acc_activate
from django.contrib.auth import views as auth_views


app_name='accounts'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path("password_reset", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('activate/<uidb64>/<token>/', acc_activate, name='activate'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]