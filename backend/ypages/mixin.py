from datetime import (datetime, )
from django.template.defaultfilters import (slugify, )

class Mixin(object):
    def parse_2slug(self, any_string="random", any_width=45):
        slug = ' '.join(set(any_string)).replace(' ', '')
        slug = slugify(f'{datetime.now()}-{slug}')
        return slug[:any_width] if len(slug) > any_width else slug

    def get_formerror(self, any_form):
        errors = {}
        for j in any_form.errors:
            errors[j] = '.'.join(any_form.errors[j])

        print("error in form", errors)
        return errors
