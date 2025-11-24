from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.http import require_http_methods


# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard:home")
  # Login ke baad dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Register view
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login") # Register ke baad login page
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect("users:login")