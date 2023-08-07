from django.contrib import admin
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase

class RecipeRequirementInline(admin.TabularInline):
    model = RecipeRequirement
    extra = 10

class MenuItemAdmin(admin.ModelAdmin):
    inlines = [RecipeRequirementInline]


# Register your models here.
admin.site.register(Ingredient)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(RecipeRequirement)
admin.site.register(Purchase)