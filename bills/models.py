from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
import django.utils.timezone as timezone
from common.models import User
from contacts.models import Contact
# Create your models here.

class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(pgettext_lazy(
        "Name of Account", "Name"), max_length=64)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='bill_created_by',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Created on"), default=timezone.now)
    amount = models.FloatField(null=True)
    contact = models.ForeignKey('contacts.Contact', related_name='bill_contact',
                                 on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']

    @classmethod
    def create(cls, values):
        """
        Create the suite element based on models/forms.
        """
        if values.get('contact'):
            ret = Contact.objects.get_or_create(name = values['contact'])
            contact = ret[0]
        else:
            raise ValueError('Contact not specify')

        suite = cls.objects.create(
            name=values['bill'],
            product=product,
            created_by=values['user'],
            amount=values['amount'],
            contact=contact
        )
        return suite