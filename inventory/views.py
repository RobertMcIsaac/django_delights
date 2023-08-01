from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import MenuCreateForm, RecipeRequirementForm, RecipeRequirementFormSet

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
    return render(request, "inventory/home.html", context)

# MENU VIEWS
class MenuList(LoginRequiredMixin ,ListView):
    model = MenuItem
    template_name = "inventory/menu.html"
    context_object_name = "menuitem_list"

class MenuCreate(LoginRequiredMixin ,CreateView):
    model= MenuItem
    template_name = "inventory/menu_create_form.html"
    form_class = MenuCreateForm
    success_url = reverse_lazy("menu")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["requirements"] = RecipeRequirementFormSet(self.request.POST)
        else:
            context["requirements"] = RecipeRequirementFormSet()
            return context
    
    def form_valid(self, form):
        context = super().form_valid(form)
        requirements = context["requirements"]
        self.object = form.save()
        if requirements.is_valid():
            requirements.instance = self.object
            requirements.save()
            return super().form_valid(form)

# INVENTORY VIEWS
class IngredientList(LoginRequiredMixin ,ListView):
    model = Ingredient
    template_name = "inventory/inventory.html"
    context_object_name = "ingredient_list"


# RECIPE VIEWS



# PURCHASE VIEWS