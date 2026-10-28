from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from rest_framework import generics
from .serializers import RegisterSerializer


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
               
    return render(request, 'login.html')

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer