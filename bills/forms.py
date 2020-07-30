from django import forms
from common.models import User
from contacts.models import Contact
from bills.models import Bill
from django.db.models import Q

class BillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        bill_view = kwargs.pop('bill', False)
        request_user = kwargs.pop('request_user', None)
        super(BillForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({'rows': '8'})

        if request_user:
            if request_user.role == 'ADMIN':
                self.fields["contact"].queryset = Contact.objects.filter() 
            else:
                self.fields["contact"].queryset = Contact.objects.filter(
                    Q(created_by=request_user))
        self.fields["amount"].required = True

    class Meta:
        model = Bill
        fields = ('name', 'description', 'amount', 'contact', 'created_on')
