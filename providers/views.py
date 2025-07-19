from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_providers(request):
    return HttpResponse("Hello, world. You're at the providers index.")
#     