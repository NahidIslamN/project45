from django import forms
from Accounts.models import HoltelBorder


class HostelBorderform(forms.ModelForm):
    class Meta:
        model = HoltelBorder
        fields = ['users', 'admin', 'location', 'phone_number','site_no']