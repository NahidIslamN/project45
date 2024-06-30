from django.contrib import admin
from Accounts.models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.


# Register your models here.
class userModels(UserAdmin):
    list_display = ["username","user_type"]


admin.site.register(CustomUser,userModels)


admin.site.register(HoltelUser)
admin.site.register(HostelSits)
admin.site.register(HoltelManager)
