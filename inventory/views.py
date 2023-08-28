from typing import Any, Dict, Sequence
from django.db.models.query import QuerySet
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
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import MenuItemCreateForm, IngredientCreateForm, RecipeRequirementCreateForm, PurchaseCreateForm
from django.db.models import Sum, DateField, F
from django.db.models.functions import TruncDate, TruncMonth, Lower
from django.db import transaction
from django.contrib import messages


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
    if request.user.is_authenticated:

        num_menuitems = MenuItem.objects.all().count
        context["num_menuitems"] = num_menuitems
        try:
            latest_menuitem = MenuItem.objects.latest("created_at")
        except MenuItem.DoesNotExist:
            latest_menuitem = None
        context["latest_menuitem"] = latest_menuitem

        num_ingredients = Ingredient.objects.all().count
        context["num_ingredients"] = num_ingredients
        try:
            latest_ingredient = Ingredient.objects.latest("created_at")
        except Ingredient.DoesNotExist:
            latest_ingredient = None
        context["latest_ingredient"] = latest_ingredient

        num_purchases = Purchase.objects.all().count
        context["num_purchases"] = num_purchases
        latest_purchase = Purchase.objects.latest("purchase_time")
        context["latest_purchase"] = latest_purchase

        return render(request, "inventory/home_authenticated.html", context)
    else:
        return render(request, "inventory/home_unauthenticated.html", context)

# MENU VIEWS
class MenuItemList(LoginRequiredMixin ,ListView):
    model = MenuItem
    template_name = "inventory/menu.html"
    context_object_name = "menuitem_list"

    # order list by 'name' field, treating all characters as lowercase in annotated field
    def get_queryset(self) -> QuerySet[Any]:
        return MenuItem.objects.annotate(lower_name=Lower("name")).order_by("lower_name")


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
    
    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     measurement_unit = RecipeRequirement.objects.annotate(measurement_unit=Ingredient.measurement_unit)
    #     context["measurement_unit"] = measurement_unit

class MenuItemDetail(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = "inventory/menuitem_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["reciperequirement_list"] = RecipeRequirement.objects.filter(menuitem=self.object)
        return context
    
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

    # order list by 'name' field, treating all characters as lowercase in annotated field.
    def get_queryset(self) -> QuerySet[Any]:
        return Ingredient.objects.annotate(lower_name=Lower("name")).order_by("lower_name")
    
    # Calculate which ingredients need to be restocked and how much restocking each will cost.
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ingredient_list = context["ingredient_list"]
        restock_dict = {}
        for ingredient in ingredient_list:
            requirements = ingredient.reciperequirement_set.all()
            total_requirements = sum([requirement.ingredient_quantity for requirement in requirements])
            defecit = total_requirements - ingredient.quantity_available
            if defecit > 0:
                restock_dict[ingredient] = defecit * ingredient.cost_per_unit
        context["restock_dict"] = restock_dict
        return context

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
    
    # Fetch the MenuItem instance, check if it has an existing RecipeRequirement instance, get a list of it's RecipeRequirement instances. 
    # Purpose: allow different templates to be displayed if the MenuItem already has a RecipeRequirement
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["menuitem"] = MenuItem.objects.get(pk=self.kwargs["pk"])
        context["recipe_requirement"] = RecipeRequirement.objects.filter(menuitem=context["menuitem"]).exists()
        context["reciperequirement_list"] = RecipeRequirement.objects.filter(menuitem=self.object)
        return context
    
    # Associate the RecipeRequirement with the specific MenuItem
    def form_valid(self, form):
        form.instance.menuitem = MenuItem.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
    # Redirect user back to the recipe_create page specific to the associated MenuItem
    def get_success_url(self):
        return reverse_lazy("recipe_new", kwargs={"pk": self.object.menuitem.pk})
    
class RecipeRequirementDelete(LoginRequiredMixin, DeleteView):
    model = RecipeRequirement
    template_name = "inventory/recipe_requirement_delete.html"

    # Allow access to MenuItem instance
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["menuitem"] = self.object.menuitem
        return context
    
    def get_success_url(self):
        return reverse_lazy("menuitem_detail", kwargs={"pk": self.object.menuitem.pk})


# PURCHASE VIEWS
class PurchaseList(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchase_log.html"
    context_object_name = "purchase_list"
    ordering = ["-purchase_time"]

class PurchaseCreate(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = "inventory/purchase_create_form.html"
    form_class = PurchaseCreateForm
    success_url = reverse_lazy("purchase_log")

    # Prevent users from logging purchases of Menuitems when it's RecipeRequirements cannot be met by Ingredient stock level
    # Adjust Ingredient stock level when MenuItem is logged
    @transaction.atomic
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        menuitem = form.cleaned_data.get("menuitem")
        form.instance.total_cost = menuitem.get_total_cost()
        form.instance.sale_price = menuitem.price
        form.instance.user = self.request.user
        recipe_requirements = RecipeRequirement.objects.filter(menuitem=menuitem)
        for requirement in recipe_requirements:
            ingredient = requirement.ingredient
            if ingredient.quantity_available < requirement.ingredient_quantity:
                messages.error(self.request, f"Not enough {ingredient.name} to make this menu item.")
                return super().form_invalid(form)
            else:
                ingredient.quantity_available = F("quantity_available") - requirement.ingredient_quantity
                ingredient.save()
        return super().form_valid(form)

    # Allow access to MenuItem instance and associated attributes 
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        form = context.get("form")
        if form.is_bound and form.is_valid():
            menuitem = form.cleaned_data.get("menuitem")
            if menuitem:
                context["menuitem"] = menuitem
                context["total_cost"] = menuitem.get_total_cost()
                context["sale_price"] = menuitem.price
        return context




# REVENUE VIEWS
class RevenueView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/revenue.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Calculate and allow access to income, costs and profit. Order by date.
        daily_revenues = Purchase.objects.annotate(date=TruncDate("purchase_time"))\
            .values("date")\
            .annotate(income=Sum("sale_price"), costs=Sum("total_cost")) \
            .order_by("-date")
        for revenue in daily_revenues:
            revenue["profit"] = revenue["income"] - revenue["costs"]
        context["daily_revenues"] = daily_revenues
        # Calculate and allow access to income, costs and profit. Order by month.
        monthly_revenues = Purchase.objects.annotate(month=TruncMonth("purchase_time"))\
            .values("month")\
            .annotate(income=Sum("sale_price"), costs=Sum("total_cost")) \
            .order_by("-month")
        for revenue in monthly_revenues:
            revenue["profit"] = revenue["income"] - revenue["costs"]
        context["monthly_revenues"] = monthly_revenues
        # Calculate and allow access to totals for income, costs and profit. Order by date.
        total_sales = Purchase.objects.aggregate(income=Sum("sale_price"))["income"]
        total_costs = Purchase.objects.aggregate(costs=Sum("total_cost"))["costs"]
        total_profit = total_sales - total_costs
        context["total_sales"] = total_sales
        context["total_costs"] = total_costs
        context["total_profit"] = total_profit

        return context
    