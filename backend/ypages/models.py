from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CHOICES_PERSONALOFFICE = (
    (0, 'Office'),
    (1, 'Personal')
)


class Group(models.Model):
    slug = models.SlugField(unique=True, default="123456789", max_length=45)
    group = models.CharField(unique=True, max_length=15)
    details = models.CharField(max_length=25, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    updated_user = models.ForeignKey(
        User, default=None, on_delete=models.SET(0), related_name="group_user")
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.group

    class Meta:
        ordering = ["group", "details"]


class Contact(models.Model):
    slug = models.SlugField(unique=True, default="123456789", max_length=45)
    name = models.CharField(max_length=50, blank=False, null=False)
    address = models.CharField(max_length=50, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    updated_user = models.ForeignKey(User, default=None, on_delete=models.SET(0), related_name="contact_user")
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f'{self.name} {self.address}'

    class Meta:
        ordering = ["name", "address"]


class Phone(models.Model):
    contact_fk = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.SET(0),
                                   related_name="contact_phone", verbose_name="Phone Number")
    phone = models.CharField(max_length=10, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.phone

    class Meta:
        ordering = ["contact_fk", "phone"]


class GroupM2M(models.Model):
    contact_fk = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.SET(0),
                                   related_name="groupm2m_contact", verbose_name="Contact Name")
    group_fk = models.ForeignKey(Group, blank=True, null=True, on_delete=models.SET(0),
                                 related_name="group_contact", verbose_name="Group Name")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.group_fk} > {self.contact_fk}'

    class Meta:
        ordering = ["contact_fk", "group_fk"]
