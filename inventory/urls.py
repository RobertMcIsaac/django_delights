from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home_view, name="home"),
    path('login/', views.InventoryLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUpView.as_view(),name="signup"),
    path('menu/', views.MenuList.as_view(), name="menu"),
    path('inventory/', views.IngredientList.as_view(), name="inventory"),
]