from django.shortcuts import render

# Create your views here.

def home_view(request):
    code=request.GET.get('code')