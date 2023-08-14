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
from .forms import MenuItemCreateForm, IngredientCreateForm, RecipeRequirementCreateForm, PurchaseCreateForm

# LOGIN VIEW (built-in)
class InventoryLoginView(auth_views.LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

# SIGNUP VIEW
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# HOME VIEW
def home_view(request):
    context = {}
    return render(request, "inventory/home.html", context)

# MENU VIEWS
class MenuItemList(LoginRequiredMixin ,ListView):
    model = MenuItem
    template_name = "inventory/menu.html"
    context_object_name = "menuitem_list"

class MenuItemCreate(LoginRequiredMixin ,CreateView):
    model= MenuItem
    template_name = "inventory/menuitem_create_form.html"
    form_class = MenuItemCreateForm
    success_url = reverse_lazy("recipe_new")

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('recipe_new', pk=self.object.pk)
    
    def get_success_url(self):
        return reverse_lazy('recipe_new', kwargs={'pk': self.object.pk})
    
class MenuItemUpdate(UpdateView):
    model = MenuItem
    template_name = "inventory/menuitem_update.html"
    fields = "__all__"
    success_url = reverse_lazy("menu")

class MenuItemDelete(DeleteView):
    model = MenuItem
    template_name = "inventory/menuitem_delete.html"
    success_url = reverse_lazy("menu")


# INVENTORY VIEWS
class IngredientList(LoginRequiredMixin ,ListView):
    model = Ingredient
    template_name = "inventory/inventory.html"
    context_object_name = "ingredient_list"

class IngredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/ingredient_create_form.html"
    form_class = IngredientCreateForm
    success_url = reverse_lazy("inventory")

class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient_update.html"
    fields = ["cost_per_unit", "quantity_available", "measurement_unit"]
    success_url = reverse_lazy("inventory")

class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient_delete.html"
    success_url = reverse_lazy("inventory")


# RECIPE VIEWS
class RecipeRequirementList(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/recipes.html"
    context_object_name = "menuitem_list"

class RecipeRequirementCreate(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = "inventory/recipe_create_form.html"
    form_class = RecipeRequirementCreateForm
    success_url = reverse_lazy("menu")
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["menuitem"] = MenuItem.objects.get(pk=self.kwargs["pk"])
        context["recipe_requirement"] = RecipeRequirement.objects.filter(menuitem=context["menuitem"]).exists()
        return context
    
    def form_valid(self, form):
        form.instance.menuitem = MenuItem.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("recipe_new", kwargs={"pk": self.object.menuitem.pk})
    
class RecipeDetail(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = "inventory/recipe_detail.html"


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["reciperequirement_list"] = RecipeRequirement.objects.filter(menuitem=self.object)
        context["menuitem"] = self.object
        return context


# PURCHASE VIEWS
class PurchaseList(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchase_log.html"
    context_object_name = "purchase_list"

class PurchaseCreate(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = "inventory/purchase_create_form.html"
    form_class = PurchaseCreateForm
    success_url = reverse_lazy("purchase_log")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        menu_item_id = self.request.POST.get("menu_item", None)
        if menu_item_id:
            menu_item = MenuItem.objects.get(id="menu_item_id")
            context["total_costs"] = menu_item.get_total_cost()
            context["sale_price"] = menu_item.price
        return context


# REVENUE VIEWS
