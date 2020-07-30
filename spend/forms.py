from django import forms
from common.models import User, Product
from spend.models import Spend
from django.db.models import Q

class SpendForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        bill_view = kwargs.pop('spend', False)
        request_user = kwargs.pop('request_user', None)
        super(SpendForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({'rows': '8'})

        if request_user:
            self.fields["product"].queryset = Product.objects.filter() 
        self.fields["amount"].required = True

    class Meta:
        model = Spend
        fields = ('name', 'description', 'amount', 'product', 'created_on')
