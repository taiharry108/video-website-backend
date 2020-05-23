from django.shortcuts import render

def index(request):
    """Render the index page of the app"""
    return render(request, 'frontend/index.html')
