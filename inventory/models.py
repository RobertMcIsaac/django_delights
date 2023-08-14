from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Ingredient MODEL
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cost_per_unit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity_available = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    # Define constants at class level for MEASUREMENT_UNIT_CHOICES
    GRAMS = "GR"
    KILOGRAMS = "KG"
    MILILITRES = "ML"
    LITRES = "LI"
    NUMBER = "NU"
    
    # Define MEASUREMENT_UNIT_CHOICES for measurement_unit field
    MEASUREMENT_UNIT_CHOICES = [
        (GRAMS, "g"),
        (KILOGRAMS, "kg"),
        (MILILITRES, "ml"),
        (LITRES, "l"),
        (NUMBER, "count"),
    ]

    # Define measurement_unit field with choices option
    measurement_unit = models.CharField(
        max_length=2,
        choices=MEASUREMENT_UNIT_CHOICES,
        help_text="Choose the measurement unit that will be used in recipes"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Ingredient"


# MenuItem MODEL
class MenuItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    description = models.CharField(max_length=200, blank=True)
    recipe_instructions = models.TextField(help_text="Instructions for preparing this menu item", blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Menu item"

    def get_total_cost(self):
        total_cost = 0
        for requirement in self.reciperequirement_set.all():
            total_cost += requirement.ingredient_quantity * requirement.ingredient.cost_per_unit
        return round(total_cost, 2)


# RecipeRequirement MODEL
class RecipeRequirement(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True)
    ingredient_quantity = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return str(self.menuitem) + " Recipe"
    
    class Meta:
        ordering = ["menuitem"]
        verbose_name = "Recipe requirement"


# Purchase MODEL
class Purchase(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    purchase_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        formatted_time = self.purchase_time.strftime("%Y-%m-%d %I:%M%p")
        return str(self.menuitem.name) + " purchased " + formatted_time

    class Meta:
        ordering = ["purchase_time"]
        verbose_name = "Purchase"