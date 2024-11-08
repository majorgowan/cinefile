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
                    return HttpResponseRedirect(reverse("profile"))
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
                return HttpResponseRedirect(reverse("profile"))
        else:
            form = SettingsForm(instance=request.user)
        return render(request, "accounts/settings.html",
                      {"form": form})
    else:
        return HttpResponseRedirect(reverse("profile"))


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
                      {"form": form})
    else:
        return HttpResponseRedirect(reverse("profile"))


def delete_account(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = DeleteAccountForm(request.POST)
            if form.is_valid():
                # delete user
                request.user.delete()
                return HttpResponseRedirect(reverse("profile"))
        else:
            form = DeleteAccountForm()
        return render(request, "accounts/delete_account.html",
                      {"form": form})
    else:
        return HttpResponseRedirect(reverse("profile"))
