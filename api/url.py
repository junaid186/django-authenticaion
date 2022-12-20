# from django.contrib import admin
import imp
from django.urls import path

# from .models import Custmer
from .views import UserChangePasswordView, UserRegistrationView
from .views import userLoginView
from .views import UserProfileView
from .views import UserChangePasswordView
from .views import SendPasswordEmailView
from .views import ResetPasswordView
# from .views import CustmerLogin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('regiser/',UserRegistrationView.as_view(),
    name='register'),
    path('login/',userLoginView.as_view(),
    name='Login'),
    path('profile/',UserProfileView.as_view(),
    name='Profile'),
    path('changepassword/',UserChangePasswordView.as_view(),
    name='changepassword'),
    path('send-reset-password-email/',SendPasswordEmailView.as_view(),
    name='send-reset-password-email'),
    path('reset-password/<uid>/<token>', ResetPasswordView.as_view(),
    name='reset-password')
]
