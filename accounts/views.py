from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm
from .models import Profile


# REGISTER
def register_view(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.first_name = form.cleaned_data.get("full_name")
            user.email = form.cleaned_data.get("email")

            user.save()

            

            login(request, user)

            return redirect("user_dashboard")

    else:
        form = CustomUserCreationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


# LOGIN
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("user_dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html"
    )


# LOGOUT
def logout_view(request):

    logout(request)

    return redirect("home")


# PROFILE
login_required
def profile(request):

    profile = request.user.profile

    if request.method == "POST":

        user = request.user

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")

        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")
        profile.county = request.POST.get("county")

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]

        user.save()
        profile.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile
        }
    )


# ABOUT
def about(request):

    return render(
        request,
        "accounts/about.html"
    )

def work(request):

    return render(
        request,
        "accounts/work.html"
    )

def contact(request):

    return render(
        request,
        "accounts/contact.html"
    )