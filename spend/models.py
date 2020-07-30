from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
import django.utils.timezone as timezone
from common.models import User, Product
# Create your models here.

class Spend(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(pgettext_lazy(
        "Name of Spend", "Name"), max_length=64)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='spend_created_by',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Created on"), default=timezone.now)
    amount = models.FloatField(null=True)
    product = models.ForeignKey('common.Product', related_name='spend_product',
                                 on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']

    @classmethod
    def create(cls, values):
        """
        Create the suite element based on models/forms.
        """
        if values.get('product'):
            ret = Product.objects.get_or_create(name = values['product'])
            product = ret[0]
        else:
            product = None

        suite = cls.objects.create(
            name=values['spend'],
            created_by=values['user'],
            amount=values['amount'],
            product=product
        )
        return suite

# Create your models here.
