from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import LoggedInUser, UserTextData
from .forms import UserTextDataForm
import datetime

User = get_user_model()

start_time = datetime.datetime.now()


@api_view(["GET"])
@permission_classes([AllowAny])
def root_view(request):
    if LoggedInUser.objects.exists():
        # Redirect logged-in users to /logged_in/
        return redirect("logged_in")
    else:
        message = request.GET.get("message", None)
        return render(request, "my_demo_app/index.html", {"message": message})


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/?message=Registration successful.")
        else:
            return render(
                request,
                "my_demo_app/register.html",
                {"form": form, "message": "Registration failed.", "status": "error"},
            )
    else:
        form = UserCreationForm()
    return render(request, "my_demo_app/register.html", {"form": form})


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log out the currently logged-in user if there is one
            try:
                current_logged_in_user = LoggedInUser.objects.get()
                logout(request)
                current_logged_in_user.delete()
            except LoggedInUser.DoesNotExist:
                pass

            # Log in the new user and update the LoggedInUser model
            login(request, user)
            LoggedInUser.objects.create(user=user)
            return redirect("/")
        else:
            return render(
                request,
                "my_demo_app/login.html",
                {"message": "Invalid username or password.", "status": "error"},
            )
    return render(request, "my_demo_app/login.html")


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def forgot_password_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            _ = User.objects.get(username=username)
            # Here you would typically send an email with a password reset link
            return render(
                request,
                "my_demo_app/forgot_password.html",
                {
                    "message": "Password reset instructions have been sent to your email.",
                    "status": "success",
                },
            )
        except User.DoesNotExist:
            return render(
                request,
                "my_demo_app/forgot_password.html",
                {"message": "Account does not exist.", "status": "error"},
            )
    return render(request, "my_demo_app/forgot_password.html")


@api_view(["GET"])
@permission_classes([AllowAny])
def demo_view(request):
    return JsonResponse({"message": "Hello, world!"})


@api_view(["GET"])
@permission_classes([AllowAny])
def oauth_success_view(request):
    return redirect("/")


@login_required
def logged_in_view(request):
    user = request.user
    try:
        user_text_data = UserTextData.objects.get(user=user)
    except UserTextData.DoesNotExist:
        user_text_data = None

    if request.method == "POST":
        form = UserTextDataForm(request.POST, instance=user_text_data)
        if form.is_valid():
            user_text_data = form.save(commit=False)
            user_text_data.user = user
            user_text_data.save()
            return redirect("logged_in")
    else:
        form = UserTextDataForm(instance=user_text_data)

    return render(
        request,
        "my_demo_app/logged_in_main.html",
        {"username": user.username, "form": form},
    )


@login_required
def logout_view(request):
    # Delete the LoggedInUser entry when the user logs out
    try:
        current_logged_in_user = LoggedInUser.objects.get(user=request.user)
        current_logged_in_user.delete()
    except LoggedInUser.DoesNotExist:
        pass
    logout(request)
    return redirect("/")
