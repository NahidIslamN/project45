
from django.urls import path

from .views import *

urlpatterns = [
    path('', ManagerDeshboard.as_view(), name='management'),
    path('recharge/', AccountRecharge.as_view(), name='recharge'),
    path('today/', MymealToday.as_view() , name='today'),
    path('mealmanagement/', ManageMeal.as_view(), name='mealmanagement'),
    path('billcreate/', CreateBills.as_view(), name='billcreate'),
    path('billsandpayements/', BillsandPayments.as_view(), name='billsandpayements'),
    path('userbills/', UserBillPayments.as_view(), name='userbills'),
   
]