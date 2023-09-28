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
from .views import LoginPage, Dashboard, UserLogout, CreateGrievanceUserView, CreateStudent, AllShowUsers, DeleteUser, \
    search, UpdateUserDetails, CreateGrievanceView, ShowStudents, SearchStudents, ShowTeachers, SearchTeachers, \
    Student_Show_Grievance, ShowAllGrivances, UpdateGrivanceStatus, Home

urlpatterns = [
    path('', Dashboard, name='Home'),
    path('home/', Home, name='LoginHome'),
    path('login/', LoginPage.as_view(), name='LoginPage'),
    path('home/allusers/', AllShowUsers.as_view(), name='ShowUsers'),
    path('home/showstudents/', ShowStudents.as_view(), name='ShowStudents'),
    path('home/showteachers/', ShowTeachers, name='ShowTeachers'),
    path('home/studentshowgrivances/', Student_Show_Grievance, name='StudentShowGrievance'),
    path('home/showallgrivances/', ShowAllGrivances.as_view(), name='ShowAllGrivances'),
    path('home/updategrivance/<int:pk>/', UpdateGrivanceStatus.as_view(), name='UpdateGrivanceStatus'),
    path('home/search/', search, name='Search'),
    path('home/searchstudents/', SearchStudents, name='SearchStudents'),
    path('home/searchteachers/', SearchTeachers, name='SearchTeachers'),
    # path('home/allusers/userdetails/<int:pk>', UserDetails.as_view(), name='UserDetails'),
    path('home/updateuserdetails/<int:pk>/', UpdateUserDetails.as_view(), name='updateuserdetails'),
    path('home/deleteuser/<int:pk>/', DeleteUser, name='DeleteUsers'),
    path('home/creategrievanceview/', CreateGrievanceView.as_view(), name='CreateGrievance'),
    path('home/createstudentview/', CreateStudent.as_view(), name='CreateStudent'),
    path('home/creategrievanceuser/', CreateGrievanceUserView.as_view(), name='CreateGrievanceUser'),
    path('logout/', UserLogout.as_view(), name='Logout'),

]
