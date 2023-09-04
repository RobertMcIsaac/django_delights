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
import datetime
from dateutil.relativedelta import relativedelta

# HELPER METHODS
def calculate_daily_revenue(target_date):
    daily_revenue = Purchase.objects.filter(purchase_time__date=target_date)\
        .aggregate(income=Sum("sale_price"), costs=Sum("total_cost"))
    daily_revenue["income"] = daily_revenue["income"] or 0
    daily_revenue["costs"] = daily_revenue["costs"] or 0
    daily_revenue["profit"] = (daily_revenue["income"] or 0) - (daily_revenue["costs"] or 0)
    return daily_revenue

def calculate_monthly_revenue(target_month):
    monthly_revenue = Purchase.objects.filter(purchase_time__month=target_month.month, purchase_time__year=target_month.year)\
        .aggregate(income=Sum("sale_price"), costs=Sum("total_cost"))
    monthly_revenue["income"] = monthly_revenue["income"] or 0
    monthly_revenue["costs"] = monthly_revenue["costs"] or 0
    monthly_revenue["profit"] = (monthly_revenue["income"] or 0) - (monthly_revenue["costs"] or 0)
    return monthly_revenue

def calculate_total_revenue():
    total_sales = Purchase.objects.aggregate(income=Sum("sale_price"))["income"] or 0
    total_costs = Purchase.objects.aggregate(costs=Sum("total_cost"))["costs"] or 0
    total_profit = total_sales - total_costs
    return {"total_sales": total_sales, "total_costs": total_costs, "total_profit": total_profit}

def get_previous_month_dates(today):
    first_day_this_month = today.replace(day=1)
    last_day_previous_month = first_day_this_month - datetime.timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)
    return first_day_previous_month, last_day_previous_month

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
        # Get total number of menu items
        num_menuitems = MenuItem.objects.all().count()
        context["num_menuitems"] = num_menuitems
        # Get most recent menu item added
        try:
            latest_menuitem = MenuItem.objects.latest("created_at")
        except MenuItem.DoesNotExist:
            latest_menuitem = None
        context["latest_menuitem"] = latest_menuitem
        # Get total number of ingredients
        num_ingredients = Ingredient.objects.all().count()
        context["num_ingredients"] = num_ingredients
        # Get most recent ingredient added
        try:
            latest_ingredient = Ingredient.objects.latest("created_at")
        except Ingredient.DoesNotExist:
            latest_ingredient = None
        context["latest_ingredient"] = latest_ingredient
        # Get total number of purchases
        num_purchases = Purchase.objects.all().count()
        context["num_purchases"] = num_purchases
        # Get most recent purchase logged
        try: 
            latest_purchase = Purchase.objects.latest("purchase_time")
        except Purchase.DoesNotExist:
            latest_purchase = None
        context["latest_purchase"] = latest_purchase
        # Calculate previous day's revenue
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_revenue = calculate_daily_revenue(yesterday)
        context["yesterday_revenue"] = yesterday_revenue
        # Calculate previous month's revenue
        today = datetime.date.today()
        first_day_previous_month, _ = get_previous_month_dates(today)
        previous_month_revenue = calculate_monthly_revenue(first_day_previous_month)
        context["previous_month_revenue"] = previous_month_revenue

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
                restock_cost = defecit * ingredient.cost_per_unit
                restock_dict[ingredient] = {"restock_quantity": defecit, "restock_cost": restock_cost}
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

    def get_queryset(self) -> QuerySet[Any]:
        return MenuItem.objects.annotate(lower_name=Lower("name")).order_by("lower_name")

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

class PurchaseUpdate(LoginRequiredMixin, UpdateView):
    model = Purchase
    template_name = "inventory/purchase_update.html"
    fields = ["menuitem"]
    success_url = reverse_lazy("purchase_log")

class PurchaseDelete(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = "inventory/purchase_delete.html"
    success_url = reverse_lazy("purchase_log")



# REVENUE VIEWS
class RevenueView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/revenue.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Daily revenue using helper method
        daily_revenue_dates = Purchase.objects.annotate(date=TruncDate("purchase_time")).values("date").order_by("-date").distinct()
        daily_revenue = {date["date"]: calculate_daily_revenue(date["date"]) for date in daily_revenue_dates}
        context["daily_revenue"] = daily_revenue
        # Monthly revenue using helper method
        monthly_revenue_months = Purchase.objects.annotate(month=TruncMonth("purchase_time")).values("month").order_by("-month").distinct()
        monthly_revenue = {month["month"]: calculate_monthly_revenue(month["month"]) for month in monthly_revenue_months}
        context["monthly_revenue"] = monthly_revenue
        # Total revenue using helper method 
        total_revenue = calculate_total_revenue()
        context["total_revenue"] = total_revenue
        return context