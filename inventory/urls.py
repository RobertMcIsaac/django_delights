from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home_view, name="home"),
    path('login/', views.InventoryLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUpView.as_view(),name="signup"),
    path('menu/', views.MenuItemList.as_view(), name="menu"),
    path('menu-item/add/', views.MenuItemCreate.as_view(), name="menuitem_new"),
    path('menu-item/<int:pk>/', views.MenuItemDetail.as_view(), name="menuitem_detail"),
    path('menu-item/edit/<int:pk>/', views.MenuItemUpdate.as_view(), name="menuitem_edit"),
    path('menu-item/delete/<int:pk>/', views.MenuItemDelete.as_view(), name="menuitem_delete"),
    path('inventory/', views.IngredientList.as_view(), name="inventory"),
    path('inventory/add/', views.IngredientCreate.as_view(), name="ingredient_new"),
    path('ingredient/edit/<int:pk>/', views.IngredientUpdate.as_view(), name="ingredient_edit"),
    path('ingredient/delete/<int:pk>/', views.IngredientDelete.as_view(), name="ingredient_delete"),
    path('recipes/', views.RecipeRequirementList.as_view(), name="recipes"),
    path('<int:pk>/add-recipe/', views.RecipeRequirementCreate.as_view(), name="recipe_new"),
    path('<int:pk>/edit-recipe-reqirement/', views.RecipeRequirementUpdate.as_view(), name="recipe_edit"),
    path('<int:pk>/delete-recipe-requirement/', views.RecipeRequirementDelete.as_view(), name="reciperequirement_delete"),
    path('purchase-log/', views.PurchaseList.as_view(), name="purchase_log"),
    path('purchase-log/add/', views.PurchaseCreate.as_view(), name="purchase_new"),
    path('purchase/edit/<int:pk>/', views.PurchaseUpdate.as_view(), name="purchase_edit"),
    path('purchase/delete/<int:pk>/', views.PurchaseDelete.as_view(), name="purchase_delete"),
    path('revenue/', views.RevenueView.as_view(), name="revenue"),
]