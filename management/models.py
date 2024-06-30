from django.db import models
from Accounts.models import CustomUser, HoltelUser, HoltelManager

# Create your models here.

class BankAccount(models.Model):
    account_nmber = models.CharField(max_length=15, unique= True)
    is_veryfied = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Hostel_account = models.ForeignKey(HoltelUser, on_delete=models.DO_NOTHING)
    balance = models.FloatField(default=0.00)
    balance_chal = models.FloatField(default=0.00)
    if_manager = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateField(auto_now = True)
    def __str__(self):
        return f'{self.account_nmber}'



class Notification(models.Model):
    recever = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    subject = models.CharField(max_length=250)
    discription = models.TextField(null=True, blank= True)
    sent_by = models.ForeignKey(HoltelManager, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateField(auto_now = True)
    seen_status = models.BooleanField(default=False)


class Meal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    meal_chrge = models.FloatField()
    meal_date = models.DateField(null=True, blank=True)
    admin = models.ForeignKey(HoltelUser, on_delete = models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateField(auto_now = True)
    paid_status = models.BooleanField(default=True)
    S =  models.BooleanField(default=True)
    D =  models.BooleanField(default=True)
    R =  models.BooleanField(default=True)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'



class Bills(models.Model):
    bill_creator = models.ForeignKey(HoltelManager, on_delete= models.DO_NOTHING)
    hostel_admin = models.ForeignKey(HoltelUser, on_delete= models.DO_NOTHING,null=True, blank=True)
    title = models.CharField(max_length=250)
    discription = models.TextField()
    bill_amount = models.FloatField()
    rice_ammount = models.FloatField(null=True, blank=True)
    last_date_of_payment = models.DateField()
    jorimana = models.FloatField(default=100.00)
    created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateField(auto_now = True)
    payment_user = models.ManyToManyField(CustomUser, related_name='paymentof_bills')
    active_status = models.BooleanField(default=True)
    


class PaymentDetail(models.Model):
    BankAccountNo = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    Bills_Account = models.ForeignKey(Bills, on_delete=models.CASCADE, null=True, blank=True)
    ammount = models.FloatField()
    ammountchal = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateField(auto_now = True)




   




