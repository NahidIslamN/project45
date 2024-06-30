from django.shortcuts import render , redirect
from django.views import View
from Accounts.models import *
from django.core.paginator import Paginator
from management.models import BankAccount,Notification
# Create your views here.


class PublicBase(View):
    def get(self, request):
        
        return render(request, 'domain_index.html')
    

class SearchHostel(View):
    def get(self, request):

        Hosteles = HoltelUser.objects.all()
        sdlist = []

        for x in Hosteles:
            if x.hostel_name not in sdlist:
                sdlist.append(x.hostel_name)

            if x.cuntry not in sdlist:
                sdlist.append(x.cuntry)

            if x.district not in sdlist:
                sdlist.append(x.district)
            if x.upozilla not in sdlist:
                sdlist.append(x.upozilla)


        paginator = Paginator(Hosteles, 30)  
        pagenumber = request.GET.get("page")
        Hostels = paginator.get_page(pagenumber)
        last_page = Hostels.paginator.num_pages 

        cp = {
            "sdlist":sdlist,
            'Hostels':Hostels,
            "last_page":last_page,
            "totalpage_list":[n+1 for n in range(last_page)],
        }

        return render(request, 'Public/find_hostel.html', context=cp)

    def post(self, request):
        data = request.POST
        scarchkey = data.get('scarchkey')
        

        Hostels = HoltelUser.objects.all()
        Hostels = Hostels.filter(search_key__icontains = scarchkey)
        sdlist = []

        for x in Hostels:
            if x.hostel_name not in sdlist:
                sdlist.append(x.hostel_name)

            if x.cuntry not in sdlist:
                sdlist.append(x.cuntry)

            if x.district not in sdlist:
                sdlist.append(x.district)
            if x.upozilla not in sdlist:
                sdlist.append(x.upozilla)
    

             
        cp = {
            "sdlist":sdlist,
            'Hostels':Hostels
        }      
        return render(request, 'Public/find_hostel.html', context=cp)




class LearnMore(View):
    def get(self, request):

        id = request.GET.get("id")

        hostel = HoltelUser.objects.get(id = id)

        sits = HostelSits.objects.filter(admin = hostel)

        cp = {
            "hostel":hostel, 
            'sits':sits,         
        }
        return render (request, 'Public/learnmore.html', context=cp)


class MyAccounts(View):
    def get(self, request):
        user = request.user

        try:
            bankaccount = BankAccount.objects.filter(user = user)[0]
        except:
            bankaccount = None
        
        

        cp = {
            'bankaccount':bankaccount

        }

        return render(request,'Public/myaccount.html',context=cp)
    



class ViewmyNotification(View):
    def get(self, request):
        user = request.user
        notificationslist = Notification.objects.filter(recever = user).order_by('-created_at')
        count = notificationslist.count()
        if count>50:
            notificationslist = notificationslist[0:50]
        
        cp = {
            "notificationslist":notificationslist

        }
        return render(request,'Public/notification.html', context=cp)
    
    def post(self, request):
        user = request.user
        data = request.POST
        Note = Notification.objects.get(id = data.get("pk"))

        
        if Note.recever == user:
            Note.seen_status = True
            Note.save()
        
        return redirect('/notifications/')