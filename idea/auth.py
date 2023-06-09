from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from .models import User

def login_user(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "idea/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "idea/login.html")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "idea/register.html", {
                "message": "Passwords do not match"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "idea/register.html", {
                "message": "Username already exsists"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "idea/register.html")