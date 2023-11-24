"""
URL configuration for cms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import LoginPage, UserLogout, CreateGrievanceUserView, CreateStudent, AllShowUsers, DeleteAllUser, \
    search, UpdateUserDetails, CreateGrievanceView, ShowStudents, SearchStudents, ShowTeachers, SearchTeachers, \
    Student_Show_Grievance, ShowAllGrivances, UpdateGrivanceStatus, Home, analytics_view, DeleteTeachersUser, \
    DeleteStudentUser, Profile, CustomPasswordResetView, otpfun, AnalysisSheetView, OtpLogin
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', LoginPage.as_view(), name='Home'),
    path('loginviaotp/', OtpLogin.as_view(), name= 'OtpLogin'),
    path('otpverification/', otpfun.as_view(), name= 'OtpVerification'),
    path('password-reset/', CustomPasswordResetView.as_view(template_name='resetpassword.html'),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('home/', Home, name='LoginHome'),
    path('home/analytics/', analytics_view.as_view(), name='Analytics'),
    path('home/analytics/downloadsheet/', AnalysisSheetView.as_view(), name='AnalysisSheet'),
    path('home/allusers/', AllShowUsers.as_view(), name='ShowUsers'),
    path('home/showstudents/', ShowStudents.as_view(), name='ShowStudents'),
    path('home/showteachers/', ShowTeachers, name='ShowTeachers'),
    path('home/studentshowgrivances/', Student_Show_Grievance, name='StudentShowGrievance'),
    path('home/showallgrivances/', ShowAllGrivances.as_view(), name='ShowAllGrivances'),
    path('home/updategrivance/<int:pk>/', UpdateGrivanceStatus.as_view(), name='UpdateGrivanceStatus'),
    path('home/search/', search, name='Search'),
    path('home/searchstudents/', SearchStudents, name='SearchStudents'),
    path('home/searchteachers/', SearchTeachers, name='SearchTeachers'),
    path('home/updateuserdetails/<int:pk>/', UpdateUserDetails.as_view(), name='updateuserdetails'),
    path('home/deleteuser/<int:pk>/', DeleteAllUser, name='DeleteAllUsers'),
    path('home/deleteteacheruser/<int:pk>/', DeleteTeachersUser, name='DeleteTeachersUser'),
    path('home/deletestudentuser/<int:pk>/', DeleteStudentUser, name='DeleteStudentUser'),
    path('home/creategrievanceview/', CreateGrievanceView.as_view(), name='CreateGrievance'),
    path('home/createstudentview/', CreateStudent.as_view(), name='CreateStudent'),
    path('home/creategrievanceuser/', CreateGrievanceUserView.as_view(), name='CreateGrievanceUser'),
    path('home/profile/<int:pk>', Profile.as_view(), name='Profile'),
    path('logout/', UserLogout.as_view(), name='Logout'),

]


