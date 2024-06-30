from django.shortcuts import render, redirect
from django.views import View
from Accounts.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib import messages
from django.utils import timezone




from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import random


# Create your views here.

class LogoinView(View):
    def get(self,request):

        return render(request,"authentication/loginpage.html")
    
    def post(self, request):
        data = request.POST
        username = data.get('userName')
        password = data.get('password')
        if CustomUser.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/deshboard/")
            else:
                messages.info(request,"Incurrect Password !")
                return redirect('/login/')
        else:
            messages.info(request,"Wrong Candidate")
            return redirect('/login/')
        



class LogoutUser(View):
    def get(self,request):
        logout(request)
        return redirect("/")
    


class ChangePassword(View):
    @method_decorator(login_required)
    def get(self,request):       

        return render(request,"authentication/changepassword.html")
    
    @method_decorator(login_required)
    def post(self, request):
        data = request.POST
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
       

        users = request.user
        is_password_correct = check_password(old_password, users.password)
        if is_password_correct:
            if new_password == confirm_password:
                users.set_password(new_password)
                users.save()
                logout(request)
                return redirect('/')
            else:
                messages.info(request,"Password is not Matched!")
                return redirect('/change_my_password/')
        else:
            messages.info('Wrong Password !')
            return redirect('/change_my_password/')
            




def generate_otp():
    return str(random.randint(100000, 999999))



def send_otp_email(email, otp):
    subject = 'Your Hostel Manager OTP'
    html_message = render_to_string('authentication/email_template.html', {'otp': otp})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'from@example.com', [email], html_message=html_message)



class SentOTP(View):
    def get(self,request):

        return render(request,'authentication/generate_otp.html')
    
    def post(self, request):       
        email = request.POST.get('email')

        if CustomUser.objects.filter(email = email).exists():
            otp = generate_otp()
            send_otp_email(email, otp)
            otp_user = CustomUser.objects.filter(email = email)[0]
            otp_user.otp = otp
            otp_user.otp_created_expired = timezone.now()
            otp_user.save()
            
            return redirect('/')

        else:
            messages.info(request,'invaild email address !')
            return redirect('/sent_otp_email/')
        

# # def generate_and_send_otp(request):
# #     if request.method == 'POST':
# #         email = request.POST.get('email')
# #         if CustomUser.objects.filter(email = email).exists():
# #             otp = generate_otp()
# #             send_otp_email(email, otp)
# #             otp_instance, created = CustomUser.objects.get_or_create(email=email)
# #             otp_instance.otp = otp
# #             otp_instance.save()
# #             return redirect(f'/verify_otp/{email}/')
# #         else:
# #             messages.info(request,"Invailed Email Address !")
# #             return redirect("/generate_otp/")
# #     return render(request, 'generate_otp.html')


# def verify_otp(request , email):
#     if request.method == 'POST':
#         email_adress = email 
#         otp_entered = request.POST.get('otp')
#         try:
#             otp_instance = CustomUser.objects.get(email=email_adress)
#             if otp_instance.otp == otp_entered:
#                 # OTP matched, do something here
#                 messages.info(request,"Success Veryfied !")
#                 return redirect("/generate_otp/")
#             else:
#                 # OTP matched, do something here
#                 messages.info(request,"Failed Veryfied !")
#                 return redirect("/generate_otp/")
#         except CustomUser.DoesNotExist:
#             messages.info(request,"Failed Veryfied !")
#             return redirect("/generate_otp/")
#     return render(request,'verify_otp.html')

