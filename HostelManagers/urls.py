"""
URL configuration for HostelManagers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from Users.views import *
from Authentications.views import *
from Accounts.views import *
from Publics.views import *

urlpatterns = [
    path('management/', include('management.urls')),
    #Users
    path('deshboard/',HomePage.as_view(), name = 'deshboard'),
    path('createsits/', HostelsitCreate.as_view(), name="createsits"),
    path('admitasutdent/', AdmithostelStudent.as_view(), name='admitasutdent'),
    path('allstudents/', AllstudentViews.as_view(), name="allstudents"),
    path('allstudents/<int:id>/', AllstudentViews.as_view(), name="allstudents"),
    path('createmanager/', ManagerCreate.as_view(), name='createmanager'),
    path('managerdetails/', ManagerDetails.as_view(), name="ManagerDetails" ),


    #authentication
    path('login/', LogoinView.as_view(), name = 'login'),
    path('logout/', LogoutUser.as_view(), name = "logout"),
    path('change_my_password/', ChangePassword.as_view(), name = 'change_my_password'),
    path('sent_otp_email/', SentOTP.as_view(), name='sent_otp_email'),





    #Accounts app
    path('settings/', MyaccountSettings.as_view(), name='settings'),
    path("personalinfo/", MypersonalInfo.as_view(), name='personalinfo'),


    #Publics App
    path('', PublicBase.as_view(), name="homepage"),
    path('hostels/', SearchHostel.as_view(), name='hostels'),
    path('learnmore/', LearnMore.as_view(), name="learnmore"),
    path('myaccounts/', MyAccounts.as_view(), name='myaccounts'),
    path('notifications/', ViewmyNotification.as_view(), name = "notifications" ),




    #Admin
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
       
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
