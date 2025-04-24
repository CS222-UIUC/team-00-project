from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import LoggedInUser, UserTextData
from django.shortcuts import get_object_or_404, render, redirect

# from .forms import UserTextDataForm
# from django.views.decorators.csrf import csrf_exempt
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
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            doc, created = UserTextData.objects.get_or_create(
                user=request.user, name=name
            )
            if created:
                doc.text_data = DEFAULT_LATEX
                doc.save()
            return redirect("latex_editor", doc_id=doc.id)

    docs = UserTextData.objects.filter(user=user)
    return render(
        request,
        "my_demo_app/document_list.html",
        {
            "username": user.username,
            "documents": docs,
        },
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


DEFAULT_LATEX = r"""\documentclass{article}
\usepackage{amsmath}
\begin{document}
Developed by Team 00.

Getting started:

1. Direct text input

2. Upload your image

3. Describe math formula you want in natural language to the chatbot

\end{document}"""


@login_required
def latex_editor_view(request, doc_id):
    user = request.user

    try:
        document = UserTextData.objects.get(id=doc_id, user=user)
    except UserTextData.DoesNotExist:
        return redirect("logged_in")

    if request.method == "POST":
        content = request.POST.get("content")
        new_name = request.POST.get("name", document.name)

        if new_name != document.name:
            if (
                UserTextData.objects.filter(user=user, name=new_name)
                .exclude(id=document.id)
                .exists()
            ):
                return JsonResponse({"error": "Name already in use"}, status=400)
            document.name = new_name

        document.text_data = content
        document.save()
        return JsonResponse(
            {"status": "updated", "doc_name": document.name, "doc_id": document.id}
        )

    return render(
        request,
        "my_demo_app/latex_editor.html",
        {
            "username": user.username,
            "document": document,
        },
    )

@login_required
def delete_document(request, doc_id):
    """
    Delete a UserTextData if it belongs to the current user.
    Shows a simple browser confirm, or deletes on POST.
    """
    doc = get_object_or_404(UserTextData, id=doc_id, user=request.user)
    if request.method == "POST":
        doc.delete()
        return redirect("document_list")
    # If you ever wanted a custom confirmation page, render it here:
    return render(
        request,
        "my_demo_app/document_confirm_delete.html",
        {"document": doc},
    )