from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)

from .forms import (SignupForm, LoginForm, SettingsForm,
                    ChangePasswordForm, DeleteAccountForm)


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("user_login"))
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html",
                  {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            user = authenticate(request,
                                username=cleaned["username"],
                                password=cleaned["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    error_message = "The account is disabled."
                    return render(request,
                                  "accounts/user_login.html",
                                  {
                                      "form": form,
                                      "error": error_message
                                  })
            else:
                error_message = "Your username and password do not match."
                return render(request,
                              "accounts/user_login.html",
                              {
                                  "form": form,
                                  "error": error_message
                               })
    else:
        if request.user.is_authenticated:
            logout(request)
        form = LoginForm()
    return render(request, "accounts/user_login.html",
                  {"form": form})


def settings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = SettingsForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save(commit=True)
                return HttpResponseRedirect(reverse("index"))
        else:
            form = SettingsForm(instance=request.user)
        return render(request, "accounts/settings.html",
                      {
                          "form": form,
                          "displayname": request.user.displayname
                      })
    else:
        return HttpResponseRedirect(reverse("index"))


def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangePasswordForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save(commit=True)
                # prevent logging out user on password change
                update_session_auth_hash(request, request.user)
                return HttpResponseRedirect(reverse("settings"))
        else:
            form = ChangePasswordForm(instance=request.user)
        return render(request, "accounts/change_password.html",
                      {
                          "form": form,
                          "displayname": request.user.displayname
                      })
    else:
        return HttpResponseRedirect(reverse("index"))


def delete_account(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = DeleteAccountForm(request.POST)
            if form.is_valid():
                # delete user
                request.user.delete()
                return HttpResponseRedirect(reverse("index"))
        else:
            form = DeleteAccountForm()
        return render(request, "accounts/delete_account.html",
                      {
                          "form": form,
                          "displayname": request.user.displayname
                      })
    else:
        return HttpResponseRedirect(reverse("index"))


# mobile views
def mobile_user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            user = authenticate(request,
                                username=cleaned["username"],
                                password=cleaned["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("mobile_index"))
                else:
                    error_message = "The account is disabled."
                    return render(request,
                                  "accounts/mobile_user_login.html",
                                  {
                                      "form": form,
                                      "error": error_message
                                  })
            else:
                error_message = "Your username and password do not match."
                return render(request,
                              "accounts/mobile_user_login.html",
                              {
                                  "form": form,
                                  "error": error_message
                              })
    else:
        if request.user.is_authenticated:
            logout(request)
        form = LoginForm()
    return render(request, "accounts/mobile_user_login.html",
                  {"form": form})


def mobile_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("mobile_user_login"))
    else:
        form = SignupForm()
    return render(request, "accounts/mobile_signup.html",
                  {"form": form})


def mobile_settings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = SettingsForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save(commit=True)
                return HttpResponseRedirect(reverse("mobile_index"))
        else:
            form = SettingsForm(instance=request.user)
        return render(request, "accounts/mobile_settings.html",
                      {
                          "form": form,
                          "displayname": request.user.displayname
                      })
    else:
        return HttpResponseRedirect(reverse("mobile_index"))


def mobile_change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangePasswordForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save(commit=True)
                # prevent logging out user on password change
                update_session_auth_hash(request, request.user)
                return HttpResponseRedirect(reverse("mobile_settings"))
        else:
            form = ChangePasswordForm(instance=request.user)
        return render(request, "accounts/mobile_change_password.html",
                      {
                          "form": form,
                          "displayname": request.user.displayname
                      })
    else:
        return HttpResponseRedirect(reverse("mobile_index"))


def mobile_delete_account(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = DeleteAccountForm(request.POST)
            if form.is_valid():
                # delete user
                request.user.delete()
                return HttpResponseRedirect(reverse("mobile_index"))
        else:
            form = DeleteAccountForm()
        return render(request, "accounts/mobile_delete_account.html",
                      {
                          "form": form,
                          "displayname": request.user.displayname
                       })
    else:
        return HttpResponseRedirect(reverse("mobile_index"))

