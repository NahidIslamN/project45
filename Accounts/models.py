from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



# Create your models here.


class CustomUser(AbstractUser):
    USER = (
        (1,"H-Controler"),
        (2,"H-Manager"),
        (3,"H-Border"),        
    )

    is_email_varified = models.BooleanField(default=False)
    otp = models.CharField(max_length=8)
    otp_created_expired = models.DateTimeField(null=True, blank=True)     
    user_type = models.CharField(choices = USER,max_length=50)
    profile_pic = models.ImageField(upload_to="profile_picture")
    able_change_pass = models.BooleanField(default=False)

    tow_factor_authentication = models.BooleanField(default=False)

    active_status = models.BooleanField(default=True)
    S =  models.BooleanField(default=True)
    D =  models.BooleanField(default=True)
    R =  models.BooleanField(default=True)

    manager_status = models.BooleanField(default=False) ### Manager Status     

    workd_place = models.CharField(max_length=250, null=True, blank=True)
    study_at = models.CharField(max_length=250, null=True, blank=True)
    adress = models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)


    
    def __str__(self):
        return self.first_name + " " + self.last_name
   

class HoltelUser(models.Model):
    users = models.OneToOneField(CustomUser, on_delete=models.Model)
    hostel_name = models.CharField(max_length=100,null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    holtel_cover_photo = models.ImageField(upload_to="coverphoto")

    cuntry = models.CharField(max_length=100,null=True, blank=True)
    district = models.CharField(max_length=100,null=True, blank=True)
    upozilla = models.CharField(max_length=100,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True,null=True, blank=True)

    search_key = models.TextField(default="bangladesh")

    def save(self, *args, **kwargs):
        # Perform operation on the search_key field before saving
        if self.district and self.upozilla and self.cuntry:
            self.search_key = f"{self.hostel_name} {self.district} {self.upozilla} {self.cuntry}"
        super(HoltelUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.hostel_name


class HostelSits(models.Model):
    admin = models.ForeignKey(HoltelUser, on_delete = models.CASCADE)
    photo_of_bed = models.ImageField('sitspic')
    sit_range = models.FloatField()
    if_blank = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True,null=True, blank=True)

class HoltelManager(models.Model):
    users = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    admin = models.ForeignKey(HoltelUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True,null=True, blank=True)

    

class HoltelBorder(models.Model):
    users = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    admin = models.ForeignKey(HoltelUser, on_delete=models.DO_NOTHING)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    site_no = models.ForeignKey(HostelSits, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.users.first_name} {self.users.last_name}'
    
  







