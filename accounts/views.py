from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout

from .forms import SignupForm, LoginForm


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
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