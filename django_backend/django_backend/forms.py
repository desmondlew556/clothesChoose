from django import forms
from django.utils.translation import gettext_lazy as _
from .models import female_Clothes

class getform(forms.ModelForm):
    class Meta:
        model = female_Clothes
        fields = ['name','company','phone_num','email','message_type','message']
        widgets = {
            'phone_num': forms.TextInput(attrs={'placeholder': '97123452'})
        }
        labels = {
            'name': _('Name'),
            'company': _('Company'),
            'phone_num': _('Phone number'),
            'email': _('Email'),
            'message_type': _('Type of message'),
            'message': _('Message'),
        }