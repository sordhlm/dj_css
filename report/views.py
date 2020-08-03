import datetime
import json
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from common.models import Product
from contacts.models import Contact
from accounts.models import Account
from bills.models import Bill
from spend.models import Spend

# Create your views here.
def get_early_date(dates):
    print("get_early_data#######")
    print(dates)
    return min(dates)

def gen_trend_data(data, sdate, step):
    now = datetime.datetime.now().date()
    date = sdate
    summary = {}
    data_trend = []
    while date <= now:
        element = {'date':date.strftime("%Y-%m-%d")}
        for key in data.keys():
            dlist = data[key]
            idx = 0
            amount = 0        
            for i in range(len(dlist)):
                if dlist[i].created_on.date() > date:
                    break
                amount += dlist[i].amount
                idx = i+1
                #idx = accounts.index(account)
            del dlist[0:idx]
            element[key] = amount

            if key in summary.keys():
                summary[key] += amount
            else:
                summary[key] = amount
        data_trend.append(element)
        date = date + datetime.timedelta(days=step)
    return data_trend, summary

@login_required
def report(request):
    contact_detail = []
    spend_detail = []
    summary = {'total': 0, 'paid': 0, 'remain': 0, 'spend':0, 'paid_percent':0, 'remain_percent':0}
    if request.method == "GET":
        step = 1
        
        contacts = Contact.objects.all().order_by("created_on")
        for contact in contacts:
            aclist = Account.objects.filter(contacts=contact).values_list('amount', flat=True)
            blist = Bill.objects.filter(contact=contact).values_list('amount', flat=True)
            total = sum(aclist)
            paid = sum(blist)
            if total != 0:
                contact_detail.append({'id':contact.id, 'name':contact.name, 'total': total, 'remain':round((total-paid)/total*100,2), 'paid':round((paid)/total*100,2)})
            else:
                contact_detail.append({'id':contact.id, 'name':contact.name, 'total': 0, 'remain':0, 'paid':0})
        products = Product.objects.all()
        for product in products:
            spend_list = Spend.objects.filter(product=product).values_list('amount', flat=True)
            spend_detail.append({'name':product.name, 'total':sum(spend_list)})
    else:
        sdict = {'1':1, '2':7,'3':30,'4':360}
        key = request.POST.get('step')
        if key in sdict.keys():
            step = sdict[key]
        else:
            raise Http404("Not support step")



    data_trend = []   
    total = 0
    cost = 0
    amount = 0
    
    accounts = Account.objects.all().order_by("created_on")
    bills = Bill.objects.all().order_by("created_on")  
    spends = Spend.objects.all().order_by("created_on")    
    accounts = list(accounts)
    bills = list(bills)
    spends = list(spends)
    print(spends)
    sdate = None
    dates = []
    if len(bills):
        dates.append(bills[0].created_on.date())
    if len(spends):
        #if sdate:
        #    sdate = sdate if sdate < spends[0].created_on.date() else spends[0].created_on.date()
        #else:
        #    sdate = spends[0].created_on.date()
        dates.append(spends[0].created_on.date())
    if len(accounts):
        #if sdate:
        #    sdate = sdate if sdate < accounts[0].created_on.date() else accounts[0].created_on.date()
        #else:
        #    sdate = accounts[0].created_on.date()
        dates.append(accounts[0].created_on.date())
    sdate = min(dates)

    if sdate:
        data = {'total': accounts, 'paid': bills, 'spend':spends}
        data_trend, summary = gen_trend_data(data, sdate, step)
        summary['remain'] = summary['total'] - summary['paid']

        context_data = {
            'summary':summary,
            'data_trend': json.dumps(data_trend),
            'contacts': contact_detail,
            'spends': json.dumps(spend_detail)
        }
    else:
        context_data = {
            'summary':summary,
            'data_trend': [],
            'contacts': contact_detail,
            'spends': spend_detail
        }

    print(context_data)
    if request.method == "GET":
        return render(request, 'report.html', context_data)
    else:
        print("return POST data")
        print(data_trend)
        return JsonResponse({'result': data_trend, 'ok':1})

@require_POST
def get_contact_trend(request):
    id = request.POST.get('id')
    step = int(request.POST.get('step'))
    if id:
        contact = Contact.objects.get(pk=id)
        print(contact)
        accounts = Account.objects.filter(contacts=contact).order_by("created_on")
        bills = Bill.objects.filter(contact=contact).order_by("created_on")
        print(accounts)
        print(bills)
        accounts = list(accounts)
        bills = list(bills)
        dates = []
        dates.append(datetime.datetime.now().date())
        if len(bills):
            dates.append(bills[0].created_on.date())
        if len(accounts):
            dates.append(accounts[0].created_on.date())
        print(model_to_dict(accounts[0]))
        sdate = get_early_date(dates)
        data = {'total': accounts, 'paid': bills}
        data_trend, summary = gen_trend_data(data, sdate, step)
        #summary['remain'] = summary['total'] - summary['paid']
        return JsonResponse({'result': data_trend, 'ok':1})
    else:
        return JsonResponse({'ok':0})