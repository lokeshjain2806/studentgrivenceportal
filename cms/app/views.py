from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import GrievanceSignupform, LoginForm, StudentSignupform, CreateGrievanceFrom
from .models import Student, Complain


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


def search(request):
    query = request.GET.get('username')
    data = User.objects.filter(username__icontains=query)
    return render(request, 'search.html', {'data': data, 'query': query})


class ShowUsers(View):
    def get(self, request):
        all_users = User.objects.filter(is_superuser=False)
        students = Student.objects.all()
        grievanceform = GrievanceSignupform
        # drop_down = StudentUpdateform(initial={'update_details': 'Select'})
        return render(request, 'showallusers.html', {
                                                     'users': all_users,
                                                     'students': students,
                                                     'grievanceform': grievanceform})


class UpdateUserDetails(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_staff:
            form = GrievanceSignupform(instance=user)
        else:
            student = get_object_or_404(Student, pk=pk)
            form = StudentSignupform(instance=student)
        return render(request, 'updatedetails.html', {'form': form, 'id': pk})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_staff:
            form = GrievanceSignupform(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('Home')
        elif not user.is_staff:
            form = StudentSignupform(request.POST)
            if form.is_valid():
                username = form.cleaned_data['user_username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']

                try:
                    # Check if a Student with the same username already exists
                    student = Student.objects.get(username=user)

                    # Update the existing Student object
                    student.name = f"{first_name} {last_name}"
                    student.roll_number = form.cleaned_data['roll_number']
                    student.School = form.cleaned_data['school']
                    student.Branch = form.cleaned_data['branch']
                    student.contact_number = form.cleaned_data['contact_number']
                    student.email_id = email
                    student.save()

                    # Update the associated User object
                    user.set_password(password)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    return redirect('Home')
                except Student.DoesNotExist:
                    # If Student doesn't exist, create a new one
                    student = Student.objects.create(
                        username=user,
                        name=f"{first_name} {last_name}",
                        roll_number=form.cleaned_data['roll_number'],
                        School=form.cleaned_data['school'],
                        Branch=form.cleaned_data['branch'],
                        contact_number=form.cleaned_data['contact_number'],
                        email_id=email,
                    )
                    student.save()

                    # Update the associated User object
                    user.set_password(password)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    return redirect('Home')
                except User.DoesNotExist:
                    return HttpResponse("User does not exist")

        # Handle errors here or return an appropriate response
        return HttpResponse("Form submission failed or encountered an error")


def DeleteUser(request, pk):
    user = User.objects.get(pk=pk).delete()
    return redirect('ShowUsers')


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('LoginPage')


class CreateGrievanceView(View):
    def get(self,request):
        form = CreateGrievanceFrom
        return render(request, 'creategrievance.html', {'form': form})

    # def post(self,request):
    #     student = Student.objects.get(name=Student.username)
    #     form = CreateGrievanceFrom(request.POST, instance=student)
    #
    #     if form.is_valid():
    #         complaint = Complain(
    #             student=student,
    #             complain_type=form.cleaned_data['complain_type'],
    #             subject=form.cleaned_data['subject'],
    #             description=form.cleaned_data['description']
    #         )
    #         complaint.save()
    #         return redirect("Home")