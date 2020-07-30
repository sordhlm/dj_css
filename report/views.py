import datetime
import json
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import Http404, JsonResponse
from common.models import Product
from contacts.models import Contact
from accounts.models import Account
from bills.models import Bill
from spend.models import Spend

# Create your views here.
def report(request):
    contact_detail = []
    spend_detail = []
    summary = {'total': 0, 'paid': 0, 'remain': 0, 'spend':0, 'paid_percent':0, 'remain_percent':0}
    if request.method == "GET":
        step = 1
        
        contacts = Contact.objects.all().order_by("created_on")
        for contact in contacts:
            aclist = Account.objects.filter(contacts=contact).values_list('total', flat=True)
            blist = Bill.objects.filter(contact=contact).values_list('amount', flat=True)
            total = sum(aclist)
            paid = sum(blist)
            if total != 0:
                contact_detail.append({'name':contact.name, 'total': total, 'remain':round((total-paid)/total*100,2), 'paid':round((paid)/total*100,2)})
            else:
                contact_detail.append({'name':contact.name, 'total': 0, 'remain':0, 'paid':0})
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
    if len(bills):
        sdate = bills[0].created_on.date()
    if len(spends):
        if sdate:
            sdate = sdate if sdate < spends[0].created_on.date() else spends[0].created_on.date()
        else:
            sdate = spends[0].created_on.date()
    if len(accounts):
        if sdate:
            sdate = sdate if sdate < accounts[0].created_on.date() else accounts[0].created_on.date()
        else:
            sdate = accounts[0].created_on.date()

    if sdate:
        now = datetime.datetime.now().date()
        date = sdate
        while date <= now:
            total = 0
            amount = 0
            idx = 0
            cost = 0
            for i in range(len(accounts)):
                if accounts[i].created_on.date() > date:
                    break
                total += accounts[i].total
                idx = i+1
                #idx = accounts.index(account)
            del accounts[0:idx]
            #print(accounts)
            idx = 0
            for i in range(len(bills)):
                if bills[i].created_on.date() > date:
                    break
                amount += bills[i].amount
                idx = i+1
            del bills[0:idx]
            idx = 0
            print(date)
            print(spends)
            for i in range(len(spends)):
                if spends[i].created_on.date() > date:
                    break
                cost += spends[i].amount
                idx = i+1
            del spends[0:idx]
            data_trend.append({'date':date.strftime("%Y-%m-%d"), 'total':total, 'paid':amount, 'spend':cost})
            summary['total'] += total
            summary['paid'] += amount
            summary['spend'] += cost
            #summary['remain'] += total-amount
            date = date + datetime.timedelta(days=step)
        #contact_detail = []
        #total = sum(total_trend)
        #paid = sum(amount_trend)
        #remain = total - paid
        if summary['total']:
            summary['remain'] = summary['total'] - summary['paid']
            summary['paid_percent'] = round(summary['paid']/summary['total'], 2)
            summary['remain_percent'] = 1- summary['paid_percent']
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