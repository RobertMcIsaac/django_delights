from django import forms
from .models import MenuItem, Ingredient, RecipeRequirement, Purchase
from django.forms import inlineformset_factory

class MenuCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "price"]

class RecipeRequirementForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ["ingredient", "ingredient_quantity_required"]


RecipeRequirementFormSet = inlineformset_factory(MenuItem, RecipeRequirement, form=RecipeRequirementForm, extra=10, can_delete=False)
