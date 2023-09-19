from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import Signupform, LoginForm


class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Home')
        else:
            form = LoginForm()
            return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)  # Log the user in
                return redirect('Home') # Redirect to the home page upon successful login
            else:
                return redirect('LoginPage')


def Dashboard(request):
    return render(request, 'home.html')


class CreateGrievanceView(View):
    def get(self, request):
        form = Signupform
        return render(request, 'creategrievanceuser.html', {'form': form})

    def post(self, request):
        form = Signupform(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'creategrievanceuser.html', {'form': form})
        else:
            form = Signupform
            return render(request, 'creategrievanceuser.html', {'form': form})


# Create your views here.
# class Signup(View):
#     def get(self, request):
#         form = Signupform()
#         return render(request,'signup.html', {'form': form})
#
#     def post(self, request):
#         form = Signupform(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'signup.html', {'form': form})
#         else:
#             return HttpResponse("<h1>Something Went Wrong With Details</h1>")


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('LoginPage')

