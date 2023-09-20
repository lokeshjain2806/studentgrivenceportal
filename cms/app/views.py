from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import GrievanceSignupform, LoginForm, StudentSignupform
from .models import Student


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
                return redirect('Home')  # Redirect to the home page upon successful login
            else:
                return redirect('LoginPage')


def Dashboard(request):
    return render(request, 'home.html')


class CreateGrievanceView(View):
    def get(self, request):
        form = GrievanceSignupform
        return render(request, 'creategrievanceuser.html', {'form': form})

    def post(self, request):
        form = GrievanceSignupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CreateGrievance')
        else:
            form = GrievanceSignupform
            return render(request, 'creategrievanceuser.html', {'form': form})


class CreateStudent(View):
    def get(self, request):
        form = StudentSignupform
        return render(request, 'createstudentuser.html', {'form': form})

    def post(self, request):
        form = StudentSignupform(request.POST)
        if form.is_valid():
            # Create a new User instance
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # Now create a Student instance associated with the user
            student = Student(
                username=user,
                name=form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name'],
                roll_number=form.cleaned_data['roll_number'],
                School=form.cleaned_data['school'],
                Branch=form.cleaned_data['branch'],
                contact_number=form.cleaned_data['contact_number'],
                email_id=form.cleaned_data['email']
            )
            student.save()

            return render(request, 'createstudentuser.html', {'form': form})
        else:
            form = StudentSignupform
            return redirect('CreateStudent')


@login_required(login_url='/login')
def ShowUsers(request):
    all_users = User.objects.filter(is_superuser=False)
    return render(request, 'showallusers.html', {'users': all_users})


def DeleteUser(request, pk):
    user = User.objects.get(pk=pk).delete()
    return redirect('ShowUsers')


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('LoginPage')

