from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.

# El index
def index (request):
    return render(request, 'index.html')

# Admin