from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home_view, name="home"),
    path('login/', views.InventoryLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUpView.as_view(),name="signup"),
    path('menu/', views.MenuList.as_view(), name="menu"),
    path('menuitem/add/', views.MenuCreate.as_view(), name="menuitem_new"),
    path('inventory/', views.IngredientList.as_view(), name="inventory"),
    path('inventory/add/', views.IngredientCreate.as_view(), name="ingredient_new"),
    path('recipes/', views.RecipeRequirementList.as_view(), name="recipes"),
    path('recipes/add/<int:pk>/', views.RecipeRequirementCreate.as_view(), name="recipe_new"),
    path('menuitem-recipe/<int:pk>/', views.RecipeDetail.as_view(), name="menuitem_recipe"),
    # path('recipe/<int:pk>/', views.RecipeRequirementDetail.as_view(), name="recipe"),
]