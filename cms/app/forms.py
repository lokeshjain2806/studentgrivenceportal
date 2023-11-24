from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django import forms
from .models import Student, Complain


class GrievanceSignupform(forms.Form):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='ReEnter Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    is_staff = forms.BooleanField(initial=False, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['is_staff']  # Set is_staff based on the form input
        if commit:
            user.save()
        return user


class GrievanceSignupform(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='ReEnter Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    is_staff = forms.BooleanField(initial=False, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['is_staff']  # Set is_staff based on the form input
        if commit:
            user.save()
        return user

phone_regex = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be 10 digits without spaces or special characters.",
)


class StudentSignupform(forms.ModelForm):
    user_username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    roll_number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    school = forms.ChoiceField(label='School', choices=Student.SCHOOL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    branch = forms.ChoiceField(label='Branch', choices=Student.COURSE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    contact_number = forms.IntegerField(label='Contact Number', widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[phone_regex])
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='ReEnter Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['user_username' ,'first_name', 'last_name', 'email', 'roll_number', 'school', 'branch', 'contact_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            self.fields['user_username'].initial = instance.username
            self.fields['first_name'].initial = instance.username.first_name
            self.fields['last_name'].initial = instance.username.last_name
            self.fields['email'].initial = instance.username.email
            self.fields['school'].initial = instance.School
            self.fields['branch'].initial = instance.Branch

    # def clean_user_username(self):
    #     user_username = self.cleaned_data.get('user_username')
    #     if not user_username:
    #         raise forms.ValidationError("Username field cannot be empty.")
    #     return user_username
    #
    # def clean_first_name(self):
    #     first_name = self.cleaned_data.get('first_name')
    #     if not first_name:
    #         raise forms.ValidationError("First Name field cannot be empty.")
    #     return first_name
    #
    # def clean_last_name(self):
    #     last_name = self.cleaned_data.get('last_name')
    #     if not last_name:
    #         raise forms.ValidationError("Last Name field cannot be empty.")
    #     return last_name

from django.contrib.auth import authenticate
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control my3'}))

    class Meta:
        model = User
        fields = ['username', 'password']



class CreateGrievanceForm(forms.Form):
    complain_type = forms.ChoiceField(label='Complain Category', choices=Complain.COMPLAIN_CATEGORY, widget=forms.Select(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Complain
        fields = ['complain_type', 'subject', 'description']


class UpdateGrievanceStatusForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    student = forms.CharField(label='Student Name', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    complain_type = forms.CharField(label='Complain Type', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    subject = forms.CharField(label='Subject',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    description = forms.CharField(label='Description',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    status = forms.ChoiceField(label='Update Status', choices=Complain.STATUS_CHOICES,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    remarks = forms.CharField(label='Remarks',
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Complain
        fields = ['username', 'student', 'complain_type', 'subject', 'description', 'status']


class OtpVerificationForm(forms.Form):
    otp = forms.IntegerField(label='Enter Your Otp', widget=forms.TextInput(attrs={'class': 'form-control'}))


class DateFilterForm(forms.Form):
    start_date = forms.DateTimeField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateTimeField(label='End Date', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

class LoginOtpForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
