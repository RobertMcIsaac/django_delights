from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

# LOGIN VIEW (built-in)
class InventoryLoginView(auth_views.LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

# SIGNUP VIEW
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# # LOGIN VIEW (custom)
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("home")
#         else:
#             return render(request, "registration/login.html")


# HOME VIEW
def home_view(request):
    context = {}
    return render(request, "home.html", context)