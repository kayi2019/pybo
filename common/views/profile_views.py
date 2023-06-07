from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, resolve_url
from common.forms import UserForm
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordChangeView, PasswordResetCompleteView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.urls import reverse_lazy
