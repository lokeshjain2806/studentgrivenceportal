from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
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


class ShowUsers(View):
    def get(self, request):
        all_users = User.objects.filter(is_superuser=False)
        students = Student.objects.all()
        grievanceform = GrievanceSignupform
        studentform = StudentSignupform
        return render(request, 'showallusers.html', {'users': all_users, 'students': students, 'grievanceform': grievanceform, 'studentform': studentform})

    def post(self, request):
        all_users = User.objects.filter(is_superuser=False)
        students = Student.objects.all()
        grievanceform = GrievanceSignupform(request.POST)
        studentform = StudentSignupform(request.POST)
        if studentform.is_valid():
            if studentform.is_valid():
                try:
                    user = User.objects.get(username=studentform.cleaned_data['username'])
                except User.DoesNotExist:
                    return HttpResponse("User does not exist")
                user.set_password(studentform.cleaned_data['password1'])
                user.save()
                username = studentform.cleaned_data['username']
            student = Student.objects.get(username=username)(
                username=user,
                name=studentform.cleaned_data['first_name'] + ' ' + studentform.cleaned_data['last_name'],
                roll_number=studentform.cleaned_data['roll_number'],
                School=studentform.cleaned_data['school'],
                Branch=studentform.cleaned_data['branch'],
                contact_number=studentform.cleaned_data['contact_number'],
                email_id=studentform.cleaned_data['email'],
            )
            student.save()
            username = studentform.cleaned_data['username']
            password = studentform.cleaned_data['password1']
            email = studentform.cleaned_data['email']
            first_name = studentform.cleaned_data['first_name']
            last_name = studentform.cleaned_data['last_name']

            user = User.objects.get(username=username)
            user.set_password(password)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        if grievanceform.is_valid():
            if grievanceform.is_valid():
                try:
                    user = User.objects.get(username=grievanceform.cleaned_data['username'])
                except User.DoesNotExist:
                    return HttpResponse("User does not exist")
                user.set_password(grievanceform.cleaned_data['password1'])
                user.save()
            username = grievanceform.cleaned_data['username']
            password = grievanceform.cleaned_data['password1']
            email = grievanceform.cleaned_data['email']
            first_name = grievanceform.cleaned_data['first_name']
            last_name = grievanceform.cleaned_data['last_name']

            user = User.objects.get(username=username)
            user.set_password(password)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        return render(request, 'showallusers.html',
                      {'users': all_users, 'students': students, 'grievanceform': grievanceform,
                       'studentform': studentform})



# class UserDetails(View):
#     def get(self, request, pk):
#         data = User.objects.get(pk=pk)
#         grievanceform = GrievanceSignupform(instance=data)
#         studentform = StudentSignupform(instance=data)
#         return render(request, 'showallusers.html', {'grievanceform': grievanceform, 'studentform': studentform})



def DeleteUser(request, pk):
    user = User.objects.get(pk=pk).delete()
    return redirect('ShowUsers')


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('LoginPage')
