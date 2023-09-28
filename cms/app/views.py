from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, FormView

from .forms import GrievanceSignupform, LoginForm, StudentSignupform, CreateGrievanceForm, UpdateGrievanceStatusForm
from .models import Student, Complain
from django.contrib.auth.models import Permission


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
                return redirect('LoginHome')  # Redirect to the home page upon successful login
            else:
                return redirect('LoginPage')


def Dashboard(request):
    return render(request, 'base.html')


def Home(request):
    return render(request, 'home.html')


class CreateGrievanceUserView(View):
    def get(self, request):
        form = GrievanceSignupform
        return render(request, 'creategrievanceuser.html', {'form': form})

    def post(self, request):
        form = GrievanceSignupform(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_staff=form.cleaned_data['is_staff']
            )
            permission = Permission.objects.get(codename='can_view_staff')
            user.user_permissions.add(permission)
            return redirect('Home')
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
                username=form.cleaned_data['user_username'],
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
            return redirect('Home')
        else:
            form = StudentSignupform
            return redirect('CreateStudent')


def search(request):
    query = request.GET.get('username')
    data = User.objects.filter(username__icontains=query)
    return render(request, 'searchallusers.html', {'data': data, 'query': query})


def SearchStudents(request):
    query = request.GET.get('username')
    data = Student.objects.filter(username__username__icontains=query)
    return render(request, 'searchstudent.html', {'data': data, 'query': query})


def SearchTeachers(request):
    query = request.GET.get('username')
    data = User.objects.filter(Q(is_superuser=False) & Q(is_staff=True) & Q(username__icontains=query))
    return render(request, 'searchteachers.html', {'data': data, 'query': query})


class AllShowUsers(View):
    def get(self, request):
        all_users = User.objects.filter(is_superuser=False)
        students = Student.objects.all()
        grievanceform = GrievanceSignupform
        return render(request, 'showallusers.html', {
                                                     'users': all_users,
                                                     'students': students,
                                                     'grievanceform': grievanceform})


class ShowStudents(View):
    def get(self, request):
        students = Student.objects.all()
        return render(request, 'showallstudents.html', {'students': students})


def ShowTeachers(request):
    data = User.objects.filter(Q(is_superuser=False) & Q(is_staff=True))
    return render(request, 'showallteachers.html', {'data': data})


class UpdateUserDetails(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_staff:
            form = GrievanceSignupform(instance=user)
            form.fields['username'].widget.attrs['readonly'] = 'readonly'
        else:
            student = get_object_or_404(Student, pk=pk)
            form = StudentSignupform(instance=student)
            form.fields['user_username'].widget.attrs['readonly'] = 'readonly'
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
        form = CreateGrievanceForm
        return render(request, 'creategrievance.html', {'form': form})

    def post(self, request):
        form = CreateGrievanceForm(request.POST)
        if form.is_valid():
            student_instance = request.user.student
            complain = Complain.objects.create(
                username = request.user,
                student=student_instance,
                complain_type=form.cleaned_data['complain_type'],
                subject=form.cleaned_data['subject'],
                description=form.cleaned_data['description'],
            )
            return redirect("Home")


def Student_Show_Grievance(request):
    if request.user.is_authenticated:
        user = request.user.id
        complain = Complain.objects.filter(student=user)
        if complain:
            return render(request, 'showgrivance.html', {'complains': complain})
        else:
            return HttpResponse("You have no complaints.")


class ShowAllGrivances(ListView):
    template_name = 'showallgrivances.html'
    context_object_name = 'grivances'

    def get_queryset(self):
        queryset = Complain.objects.all()
        return queryset


class UpdateGrivanceStatus(View):

    def get(self, request, pk):
        grievance = get_object_or_404(Complain, pk=pk)
        initial_data = {
            'username': grievance.username,
            'student': grievance.student,
            'complain': grievance.complain_type,
            'complain_type': grievance.complain_type,
            'subject': grievance.subject,
            'description': grievance.description,
            'status': grievance.status,
        }
        print(f"grievance.status: {grievance.status}")
        form = UpdateGrievanceStatusForm(initial=initial_data)
        return render(request, 'updategrievancestatus.html', {'form': form})

    def post(self, request, pk):
        grievance = get_object_or_404(Complain, pk=pk)
        updateform = UpdateGrievanceStatusForm
        form = updateform(request.POST)
        if form.is_valid():
            grievance.status = form.cleaned_data['update_status']
            grievance.save()
            return redirect('ShowAllGrivances')
