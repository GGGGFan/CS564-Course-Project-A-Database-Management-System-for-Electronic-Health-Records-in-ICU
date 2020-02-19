from django.shortcuts import render

# This is the function for django to guide the page to home.html.
def home(request):
    return render(request, 'home/home.html')
