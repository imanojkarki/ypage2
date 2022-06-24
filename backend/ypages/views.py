import json
from django.views import View
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

from ypages.choices import *
from ypages.mixin import (Mixin, )
from ypages.models import (Group, Contact, Phone, GroupM2M)
from ypages.forms import (FormGroup, FormContact, FormPhone, FormGroupM2M)


# Create your views here.
class YPages_Index(Mixin, View):
    has_error = False
    error_msg = {"contact": False, "phones": False, "groupm2ms": False}

    def onsave_group(self, icrud, slug, form_data):
        if icrud == ICRUD_CREATE:
            row = Group.objects.filter(is_deleted=True).order_by("created_on").first()
        else:
            row = Group.objects.filter(slug=slug).first()

        form = FormGroup(form_data)
        if row:
            form = FormGroup(form_data, instance=row)

        if form.is_valid():
            row = form.save(commit=False)
            if icrud == ICRUD_CREATE:
                row.is_deleted = False
                row.slug = self.parse_2slug(any_string=row.group.lower())

            elif icrud == ICRUD_DELETE:
                row.group = slug

            row.updated_user = self.request.user
            row.save()

            new_data = model_to_dict(row)
            data = {'error': False, 'new_data': new_data}
        else:
            data = {'error': True, 'new_data': self.get_formerror(form)}
        return data

    def onsave_phone(self, contact_fk, form_data):
        data = {"contact_fk": contact_fk, "phone": "", "is_deleted": False}
        for j in form_data:
            if j and len(j) > 0:
                data["phone"] = j
                form = FormPhone(data)
                row = Phone.objects.filter(is_deleted=True).first()
                if row:
                    form = FormPhone(data, instance=row)

                if form.is_valid():
                    form.save()
                else:
                    self.has_error = True
                    self.error_msg["phones"] = self.get_formerror(form)

                if self.has_error:
                    break

    def onsave_groupm2m(self, contact_fk, form_data):
        data = {"contact_fk": contact_fk, "group_fk": 0, "is_deleted": False}
        for j in form_data:
            # print("group", j)
            if j and int(j) > 0:
                group_fk = Group.objects.get(id=j)
                if group_fk:
                    data["group_fk"] = group_fk
                    form = FormGroupM2M(data)
                    row = GroupM2M.objects.filter(is_deleted=True).first()
                    if row:
                        form = FormGroupM2M(data, instance=row)

                    if form.is_valid():
                        form.save()
                    else:
                        self.has_error = True
                        self.error_msg["groupm2ms"] = self.get_formerror(form)

            if self.has_error:
                break

    def onsave_contact(self, icrud, slug, form_data):
        if icrud == ICRUD_CREATE:
            row = Contact.objects.filter(is_deleted=True).order_by("created_on").first()
        else:
            row = Contact.objects.filter(slug=slug).first()

        if icrud == ICRUD_DELETE:
            row.name = slug
            row.is_deleted = True
            row.save()

            Phone.objects.filter(contact_fk=row).update(is_deleted=True)
            GroupM2M.objects.filter(contact_fk=row).update(is_deleted=True)

        else:
            form = FormContact(form_data["contact"])
            if row:
                form = FormContact(form_data["contact"], instance=row)

            if form.is_valid():
                row = form.save(commit=False)
                if icrud == ICRUD_CREATE:
                    row.slug = self.parse_2slug(any_string=f'{row.name}{row.address}'.lower())

                row.updated_user = self.request.user
                row.save()

                Phone.objects.filter(contact_fk=row).update(is_deleted=True)
                GroupM2M.objects.filter(contact_fk=row).update(is_deleted=True)

                self.onsave_phone(row, form_data["phones"]), self.onsave_groupm2m(row, form_data["groupm2ms"])

            else:
                row = False
                self.has_error = True
                self.error_msg["contact"] = self.get_formerror(form)

        return row

    @method_decorator(login_required)
    def get(self, request, ypage=10, slug=SLUG_DEFAULT):
        rows = Group.objects.filter(is_deleted=False).order_by("group")
        fields = ("id", "slug", "group", "details")
        groups = list(rows.values(*fields))

        rows = Contact.objects.filter(is_deleted=False).order_by("name")
        fields = ("id", "slug", 'name', 'address', 'is_deleted')
        contacts = list(rows.values(*fields))

        rows = Phone.objects.filter(is_deleted=False).order_by("contact_fk", "phone")
        fields = ("id", "contact_fk", "phone", "is_deleted")
        phones = list(rows.values(*fields))

        rows = GroupM2M.objects.filter(is_deleted=False).order_by("group_fk")
        fields = ("id", "contact_fk", "group_fk")
        groupm2ms = list(rows.values(*fields))

        data = {"groups": groups, "contacts": contacts, "phones": phones,
                "groupm2ms": groupm2ms, "csrf": get_token(request), "slug": SLUG_DEFAULT}

        return JsonResponse(data=data, safe=False, status=200)

    @method_decorator(login_required)
    def post(self, request, ypage=30, slug=SLUG_DEFAULT):
        api_request, pcrud = ypage // 10, ypage % 10
        form_data = json.loads(request.body)
        if api_request == API_REQUEST_4GROUP:
            data = self.onsave_group(pcrud, slug, form_data)

        if api_request == API_REQUEST_4CONTACT:
            row = self.onsave_contact(pcrud, slug, form_data)
            if self.has_error:
                data = {'error': True, 'new_data': self.error_msg}
                print(data)
            else:
                phones = list(Phone.objects.filter(is_deleted=False, contact_fk=row).values_list('phone', flat=True))
                data = {'error': False, 'new_data': model_to_dict(row), 'phones': phones}

        return JsonResponse({**data, 'csrf': get_token(request)}, status=200)
