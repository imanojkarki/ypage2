from django import forms

# ypages import models
from ypages.models import (Group, Contact,
                           Phone, GroupM2M)


class FormGroup(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['slug', 'group', 'details', 'is_deleted']


class FormContact(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'address', 'is_deleted']


class FormPhone(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ["contact_fk", "phone", 'is_deleted']


class FormGroupM2M(forms.ModelForm):
    class Meta:
        model = GroupM2M
        fields = ["contact_fk", "group_fk", 'is_deleted']
