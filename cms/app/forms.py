from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
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


class StudentSignupform(forms.ModelForm):
    user_username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    roll_number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    school = forms.ChoiceField(label='School', choices=Student.SCHOOL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    branch = forms.ChoiceField(label='Branch', choices=Student.COURSE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    contact_number = forms.IntegerField(label='Contact Number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='ReEnter Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['user_username' ,'first_name', 'last_name', 'email', 'roll_number', 'school', 'branch', 'contact_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if instance is provided (editing mode)
        instance = kwargs.get('instance')
        if instance:
            self.fields['user_username'].initial = instance.username
            self.fields['first_name'].initial = instance.username.first_name
            self.fields['last_name'].initial = instance.username.last_name
            self.fields['email'].initial = instance.username.email
            self.fields['school'].initial = instance.School
            self.fields['branch'].initial = instance.Branch


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control my3'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class CreateGrievanceFrom(forms.ModelForm):
    student = forms.CharField(label='Student', widget=forms.TextInput(attrs={'class': 'form-control'}))
    complain_type = forms.ChoiceField(label='Complain Category', choices=Complain.COMPLAIN_CATEGORY, widget=forms.Select(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={'class': 'form-control'}))
    decription = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Complain
        fields = ['student', 'complain_type', 'subject', 'decription']
