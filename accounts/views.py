'''from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rooms.models import Room  # Import Room model for dashboard

# ===== Register View =====
# ===== Login View =====
def login_view(request):
    # Remove context that preserves username
    context = {}

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # user = authenticate and login
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            context['error'] = "Invalid credentials"
            return render(request, 'login.html', context)  # do NOT pass username here

    return render(request, 'login.html', context)


# ===== Register View =====
def register_view(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            context['error'] = "Passwords do not match"
            return render(request, 'register.html', context)

        if User.objects.filter(username=username).exists():
            context['error'] = "Username already exists"
            return render(request, 'register.html', context)

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect('accounts:login')

    return render(request, 'register.html', context)  # do NOT pass username/email here


# ===== Dashboard View =====


@login_required(login_url='accounts:login')
def dashboard_view(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'dashboard.html', {'rooms': rooms})

# ===== Logout View =====
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('accounts:login')  # <-- add namespace
'''

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rooms.models import Room  # Import Room model for dashboard

# ===== Login View =====
def login_view(request):
    context = {}

    if request.method == "POST":
        username_or_email = request.POST.get('username')  # Can be username or email
        password = request.POST.get('password')

        user = None
        # Try to authenticate by username
        if User.objects.filter(username=username_or_email).exists():
            user = authenticate(request, username=username_or_email, password=password)
        # Try to authenticate by email
        elif User.objects.filter(email=username_or_email).exists():
            user_obj = User.objects.get(email=username_or_email)
            user = authenticate(request, username=user_obj.username, password=password)

        if user:
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            context['error'] = "Invalid credentials"
            return render(request, 'login.html', context)

    return render(request, 'login.html', context)


# ===== Register View =====
def register_view(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            context['error'] = "Passwords do not match"
            return render(request, 'register.html', context)

        if User.objects.filter(username=username).exists():
            context['error'] = "Username already exists"
            return render(request, 'register.html', context)

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect('accounts:login')

    return render(request, 'register.html', context)


# ===== Dashboard View =====
@login_required(login_url='accounts:login')
def dashboard_view(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'dashboard.html', {'rooms': rooms})


# ===== Logout View =====
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('accounts:login')

def home_view(request):
    return render(request, 'home.html')
