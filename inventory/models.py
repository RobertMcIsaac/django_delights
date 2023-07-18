from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Ingredient MODEL
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cost_per_unit = models.DecimalField(max_digits=5, decimal_places=2)
    quantity_available = models.DecimalField(max_digits=5, decimal_places=2)
# Define constants at class level for MEASUREMENT_UNIT_CHOICES
    GRAMS = "GR"
    MILILITRES = "ML"
    NUMBER = "NU"
    TEASPOON = "TS"
    TABLESPOON = "TB"
# Define MEASUREMENT_UNIT_CHOICES for measurement_unit field
    MEASUREMENT_UNIT_CHOICES = [
        (GRAMS, "Grams"),
        (MILILITRES, "Mililitres"),
        (NUMBER, "Number"),
        (TEASPOON, "Teaspoon"),
        (TABLESPOON, "Tablespoon")
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


# MenuItem MODEL
class MenuItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    recipe_requirement = models.ManyToManyField(Ingredient, through="RecipeRequirement")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]


# RecipeRequirement MODEL
class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    ingredient_quantity_required = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.menu_item) + " Recipe"
    
    class Meta:
        ordering = ["menu_item"]


# Purchase MODEL
class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    purchase_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        formatted_time = self.purchase_time.strftime("%Y-%m-%d %I:%M%p")
        return str(self.menu_item.name) + " purchased " + formatted_time

    class Meta:
        ordering = ["purchase_time"]