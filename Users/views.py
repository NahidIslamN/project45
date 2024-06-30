from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Accounts.models import *
from django.contrib import messages
from Accounts.forms import HostelBorderform
from django.http import HttpResponseNotAllowed
from management.models import BankAccount
import random

# Create your views here.


class HomePage(View):
    @method_decorator(login_required)
    def get(self,request):

        return render(request,'index.html')


class HostelsitCreate(View):
    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        if user.user_type == "1":            

            return render(request,'Users/add_hostelsits.html')
        else:
            return redirect('/login/')
    
    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        if user.user_type == "1":
            admin = HoltelUser.objects.get(users = user)
            
            data = request.POST
            image = request.FILES.get('bed_photo')

            sits = HostelSits.objects.create(
                admin = admin,
                photo_of_bed = image,
                sit_range = data.get('sit_range'),
            )
            sits.save()
            messages.info(request,"Sit Created Successfully!")
        else:
            messages.info(request, 'You are not able to created a sits!')

        return redirect("/createsits/")
    


    




# admit a hostel student admit a hostel student admit a hostel student admit a hostel sutdent


def generate_AC_no():
    return str(random.randint(100000000000000, 999999999999999))

class AdmithostelStudent(View):

    @method_decorator(login_required)
    def get(self,request):     
        user = request.user

        if user.user_type == "1":
            hosteladmin = HoltelUser.objects.get(users = user)
            sits = HostelSits.objects.filter(admin=hosteladmin, if_blank = True )
            forms = HostelBorderform()
            cp = {
                "forms":forms,
                "sits":sits

            }
            return render(request,'Users/admit_a_student.html', context=cp)
        else:
            messages.info(request,"login in your admin account!")

            return redirect('/login/')
    
    @method_decorator(login_required)
    def post(self, request):
        user = request.user

        if user.user_type == "1":
            hosteladmin = HoltelUser.objects.get(users = user)
            data = request.POST
            image = request.FILES.get('Profilepic') 
            sit = HostelSits.objects.get(id = data.get('sit'))

            if CustomUser.objects.filter(username = data.get('username')).exists():
                messages.info(request,'username  already exist!')
                return redirect('/admitasutdent/')
            elif CustomUser.objects.filter(email = data.get('email')).exists():
                messages.info(request,'email address already exist!')
                return redirect('/admitasutdent/')

            userse = CustomUser.objects.create(
                first_name = data.get("first_name"),
                last_name = data.get("last_name"),
                username = data.get('username'),
                email = data.get('email'),
                user_type = '3',
                profile_pic = image,
                phone_number = data.get('phone'),
                is_staff = False,
          
            ) 
            userse.set_password(data.get('password')) 

            userse.save()

            hostelborder = HoltelBorder.objects.create(
                users = userse,
                admin = hosteladmin,          
                site_no = sit,
                phone_number = data.get('phone'),
            
            ) 

            
            
            bankaccount = BankAccount.objects.create(
                account_nmber = generate_AC_no(),
                user = userse,
                Hostel_account = hosteladmin,
                
                )
            
            hostelborder.save()
            sit.if_blank = False
            sit.save()
            bankaccount.save()
            messages.info(request,"Student Admid Successfully!")

            return redirect('/admitasutdent/')
        
        else:
            messages.info(request,"You are not able to admit sutdent!")
            return redirect('/admitasutdent/')



class AllstudentViews(View):
    @method_decorator(login_required)
    def get(self, request):
        User = request.user
        try:
            admin = HoltelUser.objects.get(users = User)
        except:
            return redirect('/login/')


        hostel_student = HoltelBorder.objects.filter(admin = admin)

        cp = {
            'hostel_student':hostel_student,
        }
        return render(request, 'Users/all_students.html', context=cp)

    @method_decorator(login_required)
    def delete(self, request, id):
        # Handle DELETE request logic here
        student = HoltelBorder.objects.get(id = id)

        usr = request.user
        try:
            admin = HoltelUser.objects.get(users = usr)
        except:
            return redirect('/')
        
        if usr.user_type == '1' and student.admin == admin:
            
            sits = student.site_no
            sits.if_blank = True
            sits.save()
            usr = CustomUser.objects.get(id = student.users.id)
            usr.delete()
            student.delete()
        
        return redirect('/allstudents/')
    
    
    @method_decorator(login_required)
    def put(self, request, id):
        student = HoltelBorder.objects.get(id = id)
        user = request.user
        try:
            admin = HoltelUser.objects.get(users = user)
        except:
            return redirect('/')
        sits = HostelSits.objects.filter(admin = admin, if_blank = True)

        cp = {
            'student':student,
            'sits':sits,
        }        
        return render(request,'Users/edite_hostel_sutdent.html', context=cp)

    @method_decorator(login_required)
    def save(self,request, id):
        usr = request.user
        try:
            student =  HoltelBorder.objects.get(id = id)
        except:
            return redirect('/')


        try:
            admin = HoltelUser.objects.get(users = usr)
        except:
            return redirect('/')
        
        if usr.user_type == '1' and student.admin == admin:             
            data = request.POST
            user = student.users
            user.username = data.get('username')
            user.email = data.get('email')
            user.phone_number = data.get('phone')
            student.phone_number = data.get('phone')
            if data.get("sit"):
                blsit = student.site_no
                blsit.if_blank = True
                blsit.save()
                sit = HostelSits.objects.get(id = data.get('sit'))
                sit.if_blank = False
                sit.save()
                student.site_no = sit
            
            user.save()
            student.save()
            messages.info(request,'Successfully Updated !')
            return redirect(f'/allstudents/')
        else:
            return redirect('/')

    

    @method_decorator(login_required)
    def post(self, request, id=None):
        method = request.POST.get('_method', '').upper()
        if method == 'DELETE':
            return self.delete(request, id)
        elif method == 'PUT':
            return self.put(request, id)
        elif method == "SAVE":
            return self.save(request, id)
        
        return HttpResponseNotAllowed(['DELETE', 'PUT','SAVE'])
    








class ManagerCreate(View):
    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        if user.user_type == "1":
            admin = HoltelUser.objects.get(users = user)
            students = HoltelBorder.objects.filter(admin = admin, is_active = True)
            
            cp = {
                'students':students
            }
            return render(request, "Users/Createmanager.html", context=cp)
        else:
            return redirect('/login/')
    
    @method_decorator(login_required)
    def post(self, request):
        usersss = request.user
        if usersss.user_type == "1":
            user = request.user
            admin = HoltelUser.objects.get(users = user)
            data = request.POST
            student = HoltelBorder.objects.get(id = data.get('user_pk'))
            location = student.users.adress
            phone_number = student.users.phone_number

            if HoltelManager.objects.filter(admin = admin).exists():
                Manager = HoltelManager.objects.filter(admin = admin)[0]
                old_student = Manager.users
                old_student.manager_status = False
                old_student.save()

                new_manager = student.users
                new_manager.manager_status = True
                new_manager.save()
                
                Manager.users = new_manager
                Manager.location = location
                Manager.phone_number = phone_number
                Manager.start_date = data.get('join_date')
                Manager.end_date = data.get('expire_date')
                Manager.save()
                messages.info(request,"Manager Successfully Updated!")
                return redirect('/createmanager/')

            else:
                manager = HoltelManager.objects.create(
                    users = student.users,
                    admin = admin,
                    location = location,
                    phone_number = phone_number,
                    start_date = data.get('join_date'),
                    end_date = data.get('expire_date'),

                )
                manager.save()
                usr = student.users
                usr.manager_status = True
                usr.save()
                messages.info(request,"Manager Successfully Crated!")
                return redirect('/createmanager/')

        else:
            return redirect('/login/')
    


class ManagerDetails(View):
    @method_decorator(login_required)
    def get(self, request):

        user = request.user
        if user.user_type == "1":
            admin = HoltelUser.objects.get(users = user)
            try:
                manager = HoltelManager.objects.filter(admin = admin)[0]
            except:
                return redirect('createmanager')

            cp = {
                "manager":manager
            }
            return render(request,"Users/details_manager.html", context=cp)
        else:
            return redirect('/login/')