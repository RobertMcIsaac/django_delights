from django import forms
from .models import MenuItem, Ingredient, RecipeRequirement, Purchase
from django.forms import inlineformset_factory

class MenuItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"

class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"

class RecipeRequirementCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ["ingredient", "ingredient_quantity"]

class PurchaseCreateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["menuitem", "purchase_time"]



