from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import User
import datetime

start_time = datetime.datetime.now()

@api_view(['GET'])
@permission_classes([AllowAny])
def root_view(request):
    message = request.GET.get('message', None)
    return render(request, 'my_demo_app/index.html', {'message': message})

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == 'POST':
        account = request.data.get('account')
        password = request.data.get('password')
        if not account or not password:
            return render(request, 'my_demo_app/register.html', {'message': 'Account and password are required.', 'status': 'error'})
        if User.objects.filter(account=account).exists():
            return render(request, 'my_demo_app/register.html', {'message': 'Account already exists.', 'status': 'error'})
        User.objects.create(account=account, password=password)
        return redirect(f'/?message=Registration successful.')
    return render(request, 'my_demo_app/register.html')

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        account = request.data.get('account')
        password = request.data.get('password')
        try:
            user = User.objects.get(account=account, password=password)
            return redirect(f'/?message=Login successful.')
        except User.DoesNotExist:
            return render(request, 'my_demo_app/login.html', {'message': 'Invalid account or password.', 'status': 'error'})
    return render(request, 'my_demo_app/login.html')

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def forgot_password_view(request):
    if request.method == 'POST':
        account = request.data.get('account')
        try:
            user = User.objects.get(account=account)
            # Here you would typically send an email with a password reset link
            return render(request, 'my_demo_app/forgot_password.html', {'message': 'Password reset instructions have been sent to your email.', 'status': 'success'})
        except User.DoesNotExist:
            return render(request, 'my_demo_app/forgot_password.html', {'message': 'Account does not exist.', 'status': 'error'})
    return render(request, 'my_demo_app/forgot_password.html')

@api_view(['GET'])
@permission_classes([AllowAny])
def demo_view(request):
    return JsonResponse({'message': 'Hello, world!'})

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def nerds_view(request):
    if request.method == 'POST':
        User.objects.all().delete()
        return redirect('nerds')
    current_time = datetime.datetime.now()
    running_time = current_time - start_time
    users = User.objects.all()
    user_data = [{'account': user.account, 'password': user.password} for user in users]
    context = {
        'running_time': running_time,
        'user_data': user_data
    }
    return render(request, 'my_demo_app/nerds.html', context)

@api_view(['GET'])
@permission_classes([AllowAny])
def oauth_success_view(request):
    return JsonResponse({'message': 'OAuth login successful.'})