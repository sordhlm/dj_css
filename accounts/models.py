import arrow
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from common.models import User, Product
from common.utils import INDCHOICES, COUNTRIES
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from contacts.models import Contact
from teams.models import Teams


class Tags(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tags, self).save(*args, **kwargs)

class Account(models.Model):

    ACCOUNT_STATUS_CHOICE = (
        ("open", "Open"),
        ('close', 'Close')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(pgettext_lazy(
        "Name of Account", "Name"), max_length=64)
    product = models.ForeignKey('common.Product', related_name='account_product',
                                 on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='account_created_by',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Created on"))
    is_active = models.BooleanField(default=False)
    #cost = models.FloatField(null=True)
    price = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
    amount = models.FloatField(null=True)
    tags = models.ManyToManyField(Tags, blank=True)
    status = models.CharField(
        choices=ACCOUNT_STATUS_CHOICE, max_length=64, default='open')
    lead = models.ForeignKey(
        'leads.Lead', related_name="account_leads",
        on_delete=models.SET_NULL, null=True)
    #contact_name = models.CharField(pgettext_lazy(
    #    "Name of Contact", "Contact Name"), max_length=120)
    #contacts = models.ManyToManyField(
    #    'contacts.Contact', related_name="account_contacts")
    contacts = models.ForeignKey('contacts.Contact', related_name='account_contacts',
                                 on_delete=models.CASCADE, null=True)
    assigned_to = models.ManyToManyField(
        User, related_name='account_assigned_users')
    teams = models.ManyToManyField(Teams, related_name='account_teams')

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
            ret = Product.objects.get_or_create(name = values['product'], cost = values.get('cost'))
            product = ret[0]
        else:
            raise ValueError('Product not specify')

        suite = cls.objects.create(
            name=values['account'],
            product=product,
            created_by=values['user'],
            price=values['price'],
            contacts=values['contacts']
        )
        return suite

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def contact_values(self):
        contacts = list(self.contacts.values_list('id', flat=True))
        return ','.join(str(contact) for contact in contacts)

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        return User.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.assigned_to.values_list('id', flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return User.objects.filter(id__in=user_ids)

    @property
    def get_assigned_users_not_in_teams(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.assigned_to.values_list('id', flat=True))
        user_ids = set(assigned_user_ids) - set(team_user_ids)
        return User.objects.filter(id__in=list(user_ids))


class Email(models.Model):
    from_account = models.ForeignKey(
        Account, related_name='sent_email', on_delete=models.SET_NULL, null=True)
    recipients = models.ManyToManyField(Contact, related_name='recieved_email')
    message_subject = models.TextField(null=True)
    message_body = models.TextField(null=True)
    timezone = models.CharField(max_length=100, default='UTC')
    scheduled_date_time = models.DateTimeField(null=True)
    scheduled_later = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    from_email = models.EmailField()
    rendered_message_body = models.TextField(null=True)


    def __str__(self):
        return self.message_subject



class EmailLog(models.Model):
    """ this model is used to track if the email is sent or not """

    email = models.ForeignKey(Email, related_name='email_log', on_delete=models.SET_NULL, null=True)
    contact = models.ForeignKey(Contact, related_name='contact_email_log', on_delete=models.SET_NULL, null=True)
    is_sent = models.BooleanField(default=False)
