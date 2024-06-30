from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from Accounts.models import *
from management.models import *
from django.contrib import messages


from django.views import View


# Create your views here.

def sent_notification(recever, senter, subject, messagediscription):
    note = Notification.objects.create(
        recever = recever,
        subject = subject,
        discription = messagediscription,
        sent_by = senter

    )
    note.save()





class ManagerDeshboard(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        if user.manager_status:


            return render(request, "management/index.html")
        else:
            return redirect('/deshboard/')

class AccountRecharge(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user

        if user.manager_status:
            hostelmanager =  HoltelManager.objects.filter(users = user)[0]
            hotel_admin = hostelmanager.admin
            bankaccountlist = BankAccount.objects.filter(Hostel_account = hotel_admin)

            cp = {
                'bankaccountlist':bankaccountlist
            }
            return render(request,'management/recharge.html', context=cp)
        else:
            return redirect('/login/')

    @method_decorator(login_required)   
    def post(self, request):
        user = request.user
        data = request.POST
        if user.manager_status:        
            manager = HoltelManager.objects.filter(users = user)[0]
            admin = manager.admin
            bank = BankAccount.objects.get(id = data.get('account_id'))
            bankadmin = bank.Hostel_account
            if bankadmin == admin:
                payment_details = PaymentDetail.objects.create(
                    BankAccountNo = bank,
                    ammount = data.get('Rechargeamount'),
                    ammountchal = data.get('Rechargeamount2'),
                )

                bank.balance = bank.balance + float(data.get('Rechargeamount'))
                bank.balance_chal = bank.balance_chal + float(data.get('Rechargeamount2'))
                sent_notification(bank.user, manager, subject='Account Recharge Successfully !', messagediscription = f"Your Accounrt Successfully Fulfill! tk : {data.get('Rechargeamount')} tk and Rice : {data.get('Rechargeamount2')} pot. your Current balance is tk: {bank.balance} tk ,  Rice : {bank.balance_chal} pot.  Thankyou Dear User !" )
                bank.save()
                payment_details.save()
                messages.info(request,'Recharge Succcessfull!')
                return redirect('/management/recharge/')

        else:
            messages.info(request, 'Login with a manager Account !')
            return redirect('/login/')
        

class MymealToday(View):
    @method_decorator(login_required)
    def get(self, request):
        User = request.user
        if User.user_type == "3":
            student = HoltelBorder.objects.filter(users = User)[0]
            hostel_admin = student.admin
            meal_List = Meal.objects.filter(admin = hostel_admin, meal_date=timezone.now().date())

            S = 0
            D = 0
            N = 0
            for x in meal_List:
                if x.S:
                    S = S+1
                if x.D:
                    D = D+1
                if x.R:
                    N = N+1
            
            
            cp = {
                'student_list':meal_List,
                'today':timezone.now().date(),
                'S':S,
                'D':D,
                'N':N,
                }
            return render(request, 'management/mymealtoday.html', context=cp)
        else:
            return redirect('/login/')
        
        
    @method_decorator(login_required)
    def post(self,request):
        user = request.user
        if user.user_type == "3":
            data = request.POST
            try:
                value = data.get('checked')
            except:
                value = None

    #Meal time settings
            try:
                morning = data.get('morning')
            except:
                morning = None

            try:
                day = data.get('day')
            except:
                day = None

            try:
                night = data.get('night')
            except:
                night = None
    # End Meal time settings
            
            if value is not None:
                user.active_status = True
            else:
                user.active_status = False


    # Meal time sattings

            if morning is not None:
                user.S = True
            else:
                user.S = False

            if day is not None:
                user.D = True
            else:
                user.D = False

            if night is not None:
                user.R = True
            else:
                user.R = False

            user.save()

            return redirect('/management/today/')
        else:
            return redirect('/login/')
    




class ManageMeal(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        if user.manager_status:
           
            

            return render(request,'management/managetodaysmeal.html',)
        else:
            return redirect('/login/')
    
    @method_decorator(login_required)
    def post(self,request):
        user = request.user
        data = request.POST
        mealcharge = data.get('meal_charge')
        mealdate = data.get('meal_date')
        if user.manager_status:
            hostelmanager = HoltelManager.objects.filter(users = user)[0]
            hostel_admin = hostelmanager.admin
            hostel_border = HoltelBorder.objects.filter(admin = hostel_admin)
            if Meal.objects.filter(admin=hostel_admin, meal_date=mealdate ).exists():
                messages.info(request,"Already created !")
                return redirect('/management/mealmanagement/')
            elif str(mealdate) != str(timezone.now().date()):
                messages.info(request,"Pleace created today's meal!")
                return redirect('/management/mealmanagement/')
            
            for hb in hostel_border:
                users = hb.users
                bankaccount = BankAccount.objects.filter(user = users )[0]
                if bankaccount.balance > float(mealcharge) and bankaccount.balance_chal>3:
                    if users.active_status:

                        meal = Meal.objects.create(
                            user = users,
                            meal_chrge = float(mealcharge),
                            meal_date = mealdate,
                            admin = hostel_admin,
                            S =  users.S,
                            D =  users.D,
                            R =  users.R,
                            
                        )
                        meal.save()
                        bankaccount.balance = bankaccount.balance - float(mealcharge)
                        if users.S:
                            bankaccount.balance_chal = bankaccount.balance_chal - 1
                        if users.D:
                            bankaccount.balance_chal = bankaccount.balance_chal - 1
                        if users.R:
                            bankaccount.balance_chal = bankaccount.balance_chal - 1
                        bankaccount.save()
                        sent_notification(recever=users, senter=hostelmanager, subject = f"Today's({mealdate}) Meal is Successfully Created !", messagediscription=f'Your Current Balance is tk: {bankaccount.balance} tk and chal: {bankaccount.balance_chal} pot')
                    else:
                        continue
                else:
                    sent_notification(recever=users, senter=hostelmanager, subject = "Your Meal is Off", messagediscription=f'Dear User Your Account Quality Hasbeen Low. Pleace Recharge your Account First. Your Current Balance is tk: {bankaccount.balance} tk and chal: {bankaccount.balance_chal} pot')
            messages.info(request,"Successfully Manage todays Meal !")
            return redirect('/management/mealmanagement/')                      

        else:
            return redirect('/login/')
        




class CreateBills(View):
    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        if user.manager_status:
        
            return render(request,'management/createbills.html')
        else:
            return redirect('/login/')
    
    @method_decorator(login_required)
    def post(self, request):
        data = request.POST
        user = request.user
        if user.manager_status:
            hostel_manager = HoltelManager.objects.filter(users = user)[0]
            hoste_admin = hostel_manager.admin
            student_list = HoltelBorder.objects.filter(admin = hoste_admin)

            new_bill = Bills.objects.create(
                bill_creator = hostel_manager,
                hostel_admin = hoste_admin,
                title = data.get('title'),
                discription = data.get('billdiscriptions'),
                bill_amount = data.get('ammount'),
                rice_ammount = data.get('riceamount'),
                last_date_of_payment = data.get('lastdate'),
                jorimana = data.get('jorimana'),            
            )
            
            messages.info(request,"bills created Succesfully")
            new_bill.save()

            for x in student_list:
                reciver = x.users
                subject = f'{new_bill.title}'
                disc = f'New bill was created at {new_bill.created_at.date()} and last date of payment at {new_bill.last_date_of_payment} pay the bill. if last date is passed you have to pay the bill with extras :{new_bill.jorimana} thank you. for more information pleace contuct with manager.'
                sent_notification(recever = reciver , senter = hostel_manager, subject=subject, messagediscription = disc)
            return redirect('/management/billcreate/')
        else:
            return redirect('/login/')
                




class BillsandPayments(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        if user.manager_status:
            hostel_manger = HoltelManager.objects.filter(users = user)[0]
            hoste_admin = hostel_manger.admin
            bills = Bills.objects.filter(bill_creator = hostel_manger, active_status = True).order_by('-created_at')
            student_list = HoltelBorder.objects.filter(admin = hoste_admin)


            cp = {
                'bills':bills,
                'student_list':student_list,
                }
            return render(request,'management/billsandpayements.html',context=cp)
        else:
            return redirect('/login/')
        
    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        if user.manager_status:
            data = request.POST
            bill = Bills.objects.get(id = data.get('bill_id'))
            print(bill)        
            payment_user = data.getlist('payment_user_set')       
            
            for userss in payment_user:
                user = CustomUser.objects.get(id = userss)
                if user in bill.payment_user.all():
                    continue
                else:
                    bill.payment_user.add(user)        
            bill.save()

            return redirect('/management/billsandpayements/')
        else:
            return redirect('/login/')





        








