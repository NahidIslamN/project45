from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class MyaccountSettings(View):
    @method_decorator(login_required)
    def get(self, request):

        return render(request,'account_settings.html')



class MypersonalInfo(View):
    @method_decorator(login_required)
    def get(self, request):
        
        return render(request, "Accounts/personal_info.html")


    def post(self, request):
        data = request.POST
       
        image = request.FILES.get('profile_pic')
        user = request.user
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.workd_place = data.get('workd_place')
        user.study_at = data.get('study_at')
        user.adress = data.get('adress')
        user.phone_number = data.get('phone_number')
        if image:
            user.profile_pic = image
        
        user.save()

        return redirect ('/personalinfo/')