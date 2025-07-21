from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def landing_page(request):
    return render("landing_page.html")
def home(request):
    return HttpResponse("This is the home page")

def about(request):
    return HttpResponse("This is the about page")