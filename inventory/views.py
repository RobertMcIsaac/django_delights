from django.shortcuts import render

# Create your views here.

# HOME VIEW
def home_view(request):
    context = {}
    return render(request, "home.html", context)