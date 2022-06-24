from ypages.models import (Group, Contact,
                           Phone, GroupM2M)
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Unregister the provided model admin
admin.site.unregister(User)


class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display = ['slug', 'group', 'details', 'is_deleted', ]


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ['slug', 'name', 'address', 'is_deleted']


class PhoneAdmin(admin.ModelAdmin):
    model = Phone
    list_display = ["contact_fk", "phone", 'is_deleted']


class GroupM2MAdmin(admin.ModelAdmin):
    model = GroupM2M
    list_display = ["contact_fk", "group_fk", 'is_deleted']


# Register your models here.
admin.site.register(Group, GroupAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(GroupM2M, GroupM2MAdmin)


# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
