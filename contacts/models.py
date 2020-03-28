import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.forms import BillingAddressForm
from common.models import Address, User
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams


class Contact(models.Model):
    name = models.CharField(_("name"), max_length=255, null=True, unique=True)
    phone = PhoneNumberField(null=True, unique=True)
    address = models.ForeignKey(
        Address, related_name='adress_contacts',
        on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(
        User, related_name='contact_assigned_users')
    created_by = models.ForeignKey(
        User, related_name='contact_created_by',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=False)
    teams = models.ManyToManyField(Teams, related_name='contact_teams')
    consumption = models.FloatField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, values):
        """
        Create the suite element based on models/forms.
        """
        address_form = BillingAddressForm(values)
        if address_form.is_valid():
            address_obj = address_form.save()

        suite = cls.objects.create(
            name=values['name'],
            phone=values['phone'],
            address=address_obj,
            created_by=values['user'],
            consumption=round(values['price'], 2),
            score=values['price']//10
        )
        return suite

    def update(self, values):
        self.score += values['price']//10
        self.consumption += round(values['price'], 2)
        self.save()
        return self

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    class Meta:
        ordering = ['-created_on']

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
