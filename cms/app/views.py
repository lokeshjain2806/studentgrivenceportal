import random
from django.utils import timezone
import csv
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, FormView
from .forms import GrievanceSignupform, LoginForm, StudentSignupform, \
    CreateGrievanceForm, UpdateGrievanceStatusForm, OtpVerificationForm, DateFilterForm, LoginOtpForm
from .models import Student, Complain
from django.contrib.auth.models import Permission


class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('LoginHome')
        else:
            form = LoginForm()
            return render(request, 'base.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # print(username)
            password = form.cleaned_data['password']
            # print(password)
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('Analytics')
                else:
                    return redirect('LoginHome')
                # num_numbers = 4
                # random_numbers = []
                # for i in range(num_numbers):
                #     random_1_digit = random.randint(1, 9)
                #     random_numbers.append(str(random_1_digit))
                # otp = int(''.join(random_numbers))
                # # print(otp)
                # request.session['user'] = user.id
                # # print('3')
                # request.session['expected_otp'] = otp
                # # print('4')
                # request.session.save()
                # # print('5')
                # subject = 'Login Verification'
                # message = f'Otp For Login: {otp}. Otp is valid for 10 minutes only.'
                # from_email = 'reset9546@gmail.com'
                # recipient_list = [user.email]
                # fail_silently = False
                # send_mail(subject, message, from_email, recipient_list, fail_silently)
                # return redirect('OtpVerification')
            else:
                messages.error(request, 'Username Or Password Are Not Correct')
                return redirect('Home')


@login_required(login_url="/")
def Home(request):
    return render(request, 'home.html')


@method_decorator(login_required(login_url="/"), name='dispatch')
class CreateGrievanceUserView(PermissionRequiredMixin, View):
    permission_required = "student.can_view_superuser"

    def get(self, request):
        form = GrievanceSignupform
        return render(request, 'creategrievanceuser.html', {'form': form})

    def post(self, request):
        form = GrievanceSignupform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 != password2:
                error_message = "Please Enter Same Password"
                return render(request, 'creategrievanceuser.html', {'form': form, 'error_message': error_message})
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=password1,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_staff=form.cleaned_data['is_staff']
            )
            permission = Permission.objects.get(codename='can_view_staff')
            user.user_permissions.add(permission)
            return redirect('ShowTeachers')
        else:
            form = GrievanceSignupform
            messages.error(request, 'user is already Exist')
            return render(request, 'creategrievanceuser.html', {'form': form})


@method_decorator(login_required(login_url="/"), name='dispatch')
class CreateStudent(PermissionRequiredMixin, View):
    permission_required = "app.can_view_staff"

    def get(self, request):
        form = StudentSignupform
        return render(request, 'createstudentuser.html', {'form': form})

    def post(self, request):
        form = StudentSignupform(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_username']
            a = User.objects.filter(username=user_name).exists()
            if a:
                messages.error(request, 'username is already exist')
                return render(request, 'createstudentuser.html', {'form': form})
            else:
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    error_message = "Please Enter Same Password"
                    return render(request, 'createstudentuser.html', {'form': form, 'error_message': error_message})
                user = User.objects.create_user(
                    username=form.cleaned_data['user_username'],
                    password=password1,
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
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
                return redirect('ShowStudents')
            return HttpResponseRedirect(reverse('CreateStudent'))
        else:
            form = StudentSignupform
            return redirect('CreateStudent')


@permission_required('student.can_view_superuser', raise_exception=True)
@login_required(login_url="/")
def search(request):
    query = request.GET.get('username')
    data = User.objects.filter(username__icontains=query)
    a = data.exclude(is_superuser=True)
    return render(request, 'searchallusers.html', {'data': a, 'query': query})


@permission_required('student.can_view_staff', raise_exception=True)
@login_required(login_url="/")
def SearchStudents(request):
    query = request.GET.get('username')
    data = Student.objects.filter(username__username__icontains=query)
    return render(request, 'searchstudent.html', {'data': data, 'query': query})


@permission_required('student.can_view_superuser', raise_exception=True)
@login_required(login_url="/")
def SearchTeachers(request):
    query = request.GET.get('username')
    data = User.objects.filter(Q(is_superuser=False) & Q(is_staff=True) & Q(username__icontains=query))
    return render(request, 'searchteachers.html', {'data': data, 'query': query})


@method_decorator(login_required(login_url="/"), name='dispatch')
class AllShowUsers(PermissionRequiredMixin, View):
    permission_required = 'student.can_view_superuser'

    def get(self, request):
        all_users = User.objects.filter(is_superuser=False).order_by('-pk')
        grievanceform = GrievanceSignupform
        return render(request, 'showallusers.html', {
                                                     'users': all_users,
                                                     'grievanceform': grievanceform})


@method_decorator(login_required(login_url="/"), name='dispatch')
class ShowStudents(PermissionRequiredMixin, View):
    permission_required = "app.can_view_staff"

    def get(self, request):
        students = Student.objects.all().order_by('-pk')
        return render(request, 'showallstudents.html', {'students': students})


@permission_required('student.can_view_superuser', raise_exception=True)
@login_required(login_url="/")
def ShowTeachers(request):
    data = User.objects.filter(Q(is_superuser=False) & Q(is_staff=True)).order_by('-id')
    return render(request, 'showallteachers.html', {'data': data})


@method_decorator(login_required(login_url="/"), name='dispatch')
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
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    messages.error(request,'Password Do Not Match')
                    return render(request, 'updatedetails.html', {'form': form, 'id': pk})
                user.set_password(password1)
                form.save()
                return redirect('ShowTeachers')
            else:
                messages.error(request, 'Password Is Not Match')
                return render(request, 'updatedetails.html', {'form': form, 'id': pk})
        elif not user.is_staff:
            form = StudentSignupform(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    messages.error(request, 'Password Do Not Match')
                    return render(request, 'updatedetails.html', {'form': form, 'id': pk})
                username = form.cleaned_data['user_username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']

                try:
                    student = Student.objects.get(username=user)
                    student.name = f"{first_name} {last_name}"
                    student.roll_number = form.cleaned_data['roll_number']
                    student.School = form.cleaned_data['school']
                    student.Branch = form.cleaned_data['branch']
                    student.contact_number = form.cleaned_data['contact_number']
                    student.email_id = email
                    student.save()

                    user.set_password(password)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    return redirect('ShowStudents')
                except Student.DoesNotExist:
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
                    user.set_password(password)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    return redirect('Home')
                except User.DoesNotExist:
                    return HttpResponse("User does not exist")
        return HttpResponse("Form submission failed or encountered an error")


@permission_required("can_view_staff", raise_exception=True)
@login_required(login_url="/")
def DeleteAllUser(request, pk):
    user = User.objects.get(pk=pk).delete()
    return redirect('ShowUsers')


def DeleteTeachersUser(request, pk):
    user = User.objects.get(pk=pk).delete()
    return redirect('ShowTeachers')


def DeleteStudentUser(request, pk):
    user = User.objects.get(pk=pk).delete()
    return redirect('ShowStudents')


@method_decorator(login_required(login_url="/"), name='dispatch')
class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('Home')


@method_decorator(login_required(login_url="/"), name='dispatch')
class CreateGrievanceView(View):

    def get(self,request):
        form = CreateGrievanceForm
        return render(request, 'creategrievance.html', {'form': form})

    def post(self, request):
        form = CreateGrievanceForm(request.POST)
        if form.is_valid():
            student_instance = request.user.student
            complain = Complain.objects.create(
                username=request.user,
                student=student_instance,
                complain_type=form.cleaned_data['complain_type'],
                subject=form.cleaned_data['subject'],
                description=form.cleaned_data['description'],
                complain_date=timezone.now(),
            )
            return redirect("StudentShowGrievance")


@login_required(login_url="/")
def Student_Show_Grievance(request):
    if request.user.is_authenticated:
        user = request.user.id
        complain = Complain.objects.filter(student=user).order_by('-pk')
        if complain:
            return render(request, 'showgrivance.html', {'complains': complain})
        else:
            return render(request,'nocomplain.html')


@method_decorator(login_required(login_url="/"), name='dispatch')
class ShowAllGrivances(PermissionRequiredMixin, ListView):
    permission_required = "app.can_view_staff"
    template_name = 'showallgrivances.html'
    context_object_name = 'grivances'

    def get_queryset(self):
        queryset = Complain.objects.all().order_by('-complain_date')
        return queryset


@method_decorator(login_required(login_url="/"), name='dispatch')
class UpdateGrivanceStatus(PermissionRequiredMixin, View):
    permission_required = "app.can_view_staff"
    try:
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
                'remarks': grievance.remarks,
            }
            form = UpdateGrievanceStatusForm(initial=initial_data)
            return render(request, 'updategrievancestatus.html', {'form': form})

        def post(self, request, pk):
            grievance = get_object_or_404(Complain, pk=pk)
            form = UpdateGrievanceStatusForm(request.POST, instance=grievance.username)
            if form.is_valid():
                grievance.username = grievance.username
                grievance.student = grievance.student
                grievance.complain_type = grievance.complain_type
                grievance.subject = grievance.subject
                grievance.description = grievance.description
                grievance.status = form.cleaned_data['status']
                grievance.remarks = form.cleaned_data['remarks']
                grievance.save()
                return redirect('ShowAllGrivances')
    except Exception as e:
        pass


@method_decorator(login_required(login_url="/"), name='dispatch')
class analytics_view(PermissionRequiredMixin, View):
    permission_required = "app.can_view_staff"

    def get(self,request):
        form = DateFilterForm
        complaint_counts = {}
        complaint_types = []
        complaint_percentages = []
        total_complaints = Complain.objects.count()
        for complaint_type, _ in Complain.COMPLAIN_CATEGORY:
            try:
                count = Complain.objects.filter(complain_type=complaint_type).count()
                percentage = (count / total_complaints) * 100
                complaint_percentages.append(percentage)
                complaint_types.append(complaint_type)
            except:
                return render(request, 'noanalytics.html')

        context = {
            'complaint_types': complaint_types,
            'complaint_percentages': complaint_percentages,
            'form': form,
        }

        return render(request, 'analytics.html', context)
    
    def post(self, request):
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999)
            complaints = Complain.objects.filter(complain_date__range=(start_date, end_date))
            if complaints:
                total_complaints = complaints.count()
                complaint_types = []
                complaint_percentages = []
                for complaint_type, _ in Complain.COMPLAIN_CATEGORY:
                    count = complaints.filter(complain_type=complaint_type).count()
                    percentage = (count / total_complaints) * 100
                    complaint_percentages.append(percentage)
                    complaint_types.append(complaint_type)
            else:
                return render(request, 'noanalytics.html')

        else:
            complaint_types = []
            complaint_percentages = []


        context = {
            'complaint_types': complaint_types,
            'complaint_percentages': complaint_percentages,
            'form': form,
        }

        return render(request, 'analytics.html', context)


class Profile(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_staff:
            form = GrievanceSignupform(instance=user)
            form.fields['username'].widget.attrs['readonly'] = 'readonly'
            form.fields['first_name'].widget.attrs['readonly'] = 'readonly'
            form.fields['last_name'].widget.attrs['readonly'] = 'readonly'
            form.fields['email'].widget.attrs['readonly'] = 'readonly'
        else:
            student = get_object_or_404(Student, pk=pk)
            form = StudentSignupform(instance=student)
            form.fields['user_username'].widget.attrs['readonly'] = 'readonly'
            form.fields['first_name'].widget.attrs['readonly'] = 'readonly'
            form.fields['last_name'].widget.attrs['readonly'] = 'readonly'
            form.fields['email'].widget.attrs['readonly'] = 'readonly'
            form.fields['roll_number'].widget.attrs['readonly'] = 'readonly'
            form.fields['school'].widget.attrs['readonly'] = 'readonly'
            form.fields['branch'].widget.attrs['readonly'] = 'readonly'
            form.fields['contact_number'].widget.attrs['readonly'] = 'readonly'
        return render(request, 'profile.html', {'form': form, 'id': pk})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_staff:
            form = GrievanceSignupform(request.POST, instance=user)
            if form.is_valid():
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    messages.error(request, 'Passwords Do Not Match')
                    return render(request, 'profile.html', {'form': form, 'id': pk})
                user.set_password(password1)
                user.save()
                updated_user = authenticate(username=user.username, password=password1)
                if updated_user is not None:
                    login(request, updated_user)
                return redirect('LoginHome')
            else:
                messages.error(request, 'Password Is Not Match')
                return render(request, 'profile.html', {'form': form, 'id': pk})
        elif not user.is_staff:
            form = StudentSignupform(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    messages.error(request, 'Passwords Do Not Match')
                    return render(request, 'profile.html', {'form': form, 'id': pk})
                username = form.cleaned_data['user_username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']

                try:
                    student = Student.objects.get(username=user)
                    student.name = f"{first_name} {last_name}"
                    student.roll_number = form.cleaned_data['roll_number']
                    student.School = form.cleaned_data['school']
                    student.Branch = form.cleaned_data['branch']
                    student.contact_number = form.cleaned_data['contact_number']
                    student.email_id = email
                    student.save()

                    user.set_password(password)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    updated_user = authenticate(username=username, password=password)
                    if updated_user is not None:
                        login(request, updated_user)

                    return redirect('LoginHome')
                except Student.DoesNotExist:
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
                    user.set_password(password)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    updated_user = authenticate(username=username, password=password)
                    if updated_user is not None:
                        login(request, updated_user)
                    return redirect('LoginHome')
                except User.DoesNotExist:
                    return HttpResponse("User does not exist")
        return HttpResponse("Form submission failed or encountered an error")


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        try:
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(self.request, 'User with this email does not exist.')
            return redirect('password-reset')
        return super().form_valid(form)


class OtpLogin(View):
    def get(self, request):
        form = LoginOtpForm
        return render(request, 'loginviaotp.html', {'form': form})

    def post(self, request):
        form = LoginOtpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            a = User.objects.filter(username=username).exists()
            if a:
                user = User.objects.get(username=username)
                num_numbers = 4
                random_numbers = []
                for i in range(num_numbers):
                    random_1_digit = random.randint(1, 9)
                    random_numbers.append(str(random_1_digit))
                otp = int(''.join(random_numbers))
                # print(otp)
                request.session['user'] = user.id
                # print('3')
                request.session['expected_otp'] = otp
                # print('4')
                request.session.save()
                # print('5')
                subject = 'Login Verification'
                message = f'Otp For Login: {otp}. Otp is valid for 10 minutes only.'
                from_email = 'reset9546@gmail.com'
                recipient_list = [user.email]
                fail_silently = False
                send_mail(subject, message, from_email, recipient_list, fail_silently)
                return redirect('OtpVerification')

class otpfun(View):
    def get(self, request):
        form = OtpVerificationForm
        return render(request, 'otpverification.html', {'form': form})

    def post(self, request):
        form = OtpVerificationForm(request.POST)
        entered_otp = request.POST.get('otp')
        expected_otp = request.session.get('expected_otp')
        user_id = request.session.get('user')
        user = User.objects.get(id=user_id)
        if str(entered_otp) == str(expected_otp):
            login(request, user)
            if request.user.is_superuser:
                return redirect('Analytics')
            else:
                return redirect('LoginHome')
        else:
            messages.error(request, 'OTP Not Valid')
            return render(request, 'otpverification.html', {'form': form})


@method_decorator(login_required(login_url="/"), name='dispatch')
class AnalysisSheetView(PermissionRequiredMixin, FormView):
    permission_required = "app.can_view_superuser"
    form_class = DateFilterForm
    template_name = 'analytics_sheet_download.html'
    success_url = reverse_lazy('AnalysisSheet')

    def form_valid(self, form):
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999)
        complaints = Complain.objects.filter(complain_date__range=[start_date, end_date])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="complaints.csv"'
        writer = csv.writer(response)
        writer.writerow(['Complain Type', 'Complain Subject', 'Complain Date', 'Description', 'Status'])
        for complaint in complaints:
            writer.writerow([complaint.complain_type, complaint.subject, complaint.complain_date, complaint.description, complaint.status])

        return response

