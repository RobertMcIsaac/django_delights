from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Ingredient MODEL
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cost_per_unit = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quantity_available = models.DecimalField(max_digits=5, decimal_places=2, default=0)
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
        (NUMBER, ""),
    ]

    # Define measurement_unit field with choices option
    measurement_unit = models.CharField(
        max_length=2,
        choices=MEASUREMENT_UNIT_CHOICES,
        help_text="Please choose a unit of measurement from the available options."
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Ingredient"


# MenuItem MODEL
class MenuItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Menu item"


# RecipeRequirement MODEL
class RecipeRequirement(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    ingredient_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.menuitem) + " Recipe"
    
    class Meta:
        ordering = ["menuitem"]
        verbose_name = "Recipe requirement"


# Purchase MODEL
class Purchase(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    purchase_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        formatted_time = self.purchase_time.strftime("%Y-%m-%d %I:%M%p")
        return str(self.menuitem.name) + " purchased " + formatted_time

    class Meta:
        ordering = ["purchase_time"]
        verbose_name = "Purchase"