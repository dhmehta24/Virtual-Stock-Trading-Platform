from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse,JsonResponse
# from .models import User
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
from Major_Project.Celery import app
from Accounts.models import User,Investor
from .models import Company_Names_BSE, Company_Names_NSE, Daily_Realtime_Price, Watchlist, Holdings,Investor_Staus,History
from datetime import date
from datetime import datetime
from nsetools import Nse
from bsedata.bse import BSE
#from celery.task import periodic_task
import yfinance as yf
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from celery import shared_task
from celery.decorators import periodic_task
import requests
import json
from django.db.models import Q


# import dummy_predi
# Create your views here.
@login_required
def home(request):
    add_to_db()
    data = Holdings.objects.filter(investor=request.user)
    profile = Investor_Staus.objects.get(investor=request.user)
    return render(request, "Dashboard.html", {"data": data, "profile":profile})


def refresh(request):
    add_to_db()
    data = Holdings.objects.filter(investor=request.user)

@login_required
def profile(request):
    data = Investor_Staus.objects.get(investor=request.user)
    return render(request, "profile.html",{"data":data})

def hello(request):
    add_to_db()
    return render(request, "hello.html")

@login_required
def watchlist(request):
    data_bse = Company_Names_BSE.objects.all()
    data_nse = Company_Names_NSE.objects.all()

    stock = Watchlist.objects.filter(user=request.user)

    for i in stock:
        update_data(i.stock.company_ticker,i.stock.market)

    return render(request, "watchlist.html", {"companies_bse": data_bse,"companies_nse":data_nse, "stocks": stock})


@login_required
def share_info(request, slug=None):
    return render(request, "shares_info.html")


def login(request):
    return render(request, "login-signup.html")

def edit_profile(request):
    return render(request,"edit_profile.html")

def login_save(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        dob = request.POST.get('year') + "-" + request.POST.get('month') + "-" + request.POST.get('day')
        psswd = request.POST.get('password')
        cpwd = request.POST.get('cpassword')

        data = User(name=name, email=email, phone=phone, gender=gender, dob=dob, passwd=psswd, c_pwd=cpwd)
        data.save()

    return render(request, "Dashboard.html")


def display_data(request, ticker, market, time = None):
    update_data(ticker, market)

    if market == 'NSE':

        data = Daily_Realtime_Price.objects.filter(company_ticker=ticker, market=market).last()

        """if data is None:
            update_data(ticker, market)
            data = Daily_Realtime_Price.objects.get(company_ticker=ticker, market=market)"""

    elif market == 'BSE':

        data = Daily_Realtime_Price.objects.filter(company_ticker=ticker, market=market).last()
        """if data is None:
            update_data(ticker, market)
            data = Daily_Realtime_Price.objects.filter(company_ticker=ticker, market=market).last()"""

    else:
        data = None

    watch = Watchlist.objects.filter(user = request.user, stock__company_ticker=ticker, stock__market=market).last()
    if time:
        hold = Holdings.objects.get(investor=request.user, stock__company_ticker=ticker, stock__market=market, time=time)
    else:
        hold = None
    # data = Daily_Realtime_Price.objects.last()

    return render(request, "shares_info.html", {"data": data, "watch":watch, "hold":hold})


def add_to_watchlist(request, ticker, market):
    data = Daily_Realtime_Price.objects.filter(company_ticker=ticker, market=market).last()

    # q = Watchlist.objects.get(user = request.user, stock = data.company_ticker)

    watch = Watchlist.objects.get_or_create(user=request.user, stock=data)

    return redirect("/watchlist")

def remove_from_watchlist(request, ticker, market):
    data = Watchlist.objects.get(stock__company_ticker=ticker, stock__market=market)

    # q = Watchlist.objects.get(user = request.user, stock = data.company_ticker)

    data.delete()

    return redirect("/watchlist")


def buy_stock(request, ticker, market):

    if request.method == "POST":

        qty = request.POST.get('quantity')

    else:
        qty = 0

    data = Daily_Realtime_Price.objects.filter(company_ticker=ticker, market=market).last()

    status = Investor_Staus.objects.get(investor=request.user)

    if (data.price * int(qty)) > status.balance:
        messages.error(request,"You dont have enough money, you can buy {} shares instead".format(round(status.balance / data.price)))
        return redirect(reverse("stock_info", args=[ticker, market]))
    else:
        status.balance = status.balance - (data.price * int(qty))

        status.transactions += 1

        status.save()

        History.objects.create(investor=request.user, stock=data, bought_price=data.price,cost = (data.price * int(qty)), quantity=qty, t_type='BUY')

    """"if request.method == "POST":

        quantity = request.POST.get("quantity")"""

    Holdings.objects.create(investor=request.user, stock=data, bought_price=data.price,  quantity= qty, ltp=data.price)

    #Investor_S.ftaus.objects.create(investor=request.user )
    messages.success(request,"You Have successfully Bought {} shares of {}".format(qty, data.company_name))
    return redirect("/")


def sell_stock(request, ticker, market, time):

    data = Daily_Realtime_Price.objects.filter(company_ticker=ticker, market=market).last()

    if request.method == "POST":
        qty = request.POST.get('quantity')
    else:
        qty = 0
    hold = Holdings.objects.get(investor=request.user, stock__company_ticker=ticker, stock__market=market, time=time)

    status = Investor_Staus.objects.get(investor=request.user)

    if int(qty) <= hold.quantity:

        if int(qty) == hold.quantity:
            Holdings.objects.get(investor=request.user, stock__company_ticker= ticker , stock__market=market, quantity=int(qty), time = time).delete()

        else:
            hold.quantity = hold.quantity - int(qty)
            hold.save()

        """if hold.bought_price <= data.price:
    
            gain = data.price - hold.bought_price
    
        else:
    
            gain = hold.bought_price - data.price"""

        gain = (data.price * int(qty)) - (hold.bought_price * int(qty))
        status.balance = status.balance + (data.price * int(qty))
        status.transactions +=1
        if gain >= 0:
            status.profit += gain
            status.p_transactions +=1
        else:
            status.loss += gain
            status.n_transactions += 1

        status.save()

        History.objects.create(investor=request.user, stock=data, bought_price=hold.bought_price, quantity= qty, t_type='SELL', sold_price=data.price, gain = gain)

        messages.info(request, "Sold {} stocks of {}".format(qty, hold.stock.company_name))

        return redirect("/")

    else:
        messages.error(request, "You have only {} stocks to sell".format(hold.quantity))
        return  redirect("/")
        #return reverse('stock_info_sell',args=[ticker, market, time])
    # Investor_Staus.objects.create(investor=request.user )


def update_data(ticker, market):
    b = BSE()
    n = Nse()

    if market == 'NSE':
        data = n.get_quote(ticker)
        # format_date = '%d-%M-%Y'
        e = Daily_Realtime_Price.objects.filter(company_name=data['companyName'], company_ticker=data['symbol'],market='NSE').last()
    
        if e is not None:

            e.open = data['open']
            e.close = data['closePrice']
            e.high = data['dayHigh']
            e.low = data['dayLow']
            e.price = data['lastPrice']
            e.volume = data['totalTradedVolume']
            e.latest_trading_day = data['secDate']
            e.prev_close = data['previousClose']
            e.change =  data['change']
            e.change_percentage = data['pChange']

            e.save()

        else:

            e = Daily_Realtime_Price.objects.create(company_name=data['companyName'], company_ticker=data['symbol'],market='NSE', open=data['open'], high=data['dayHigh'],
                                                      low=data['dayLow'], close=data['closePrice'],
                                                      price=data['lastPrice'], volume=data['totalTradedVolume'],
                                                      latest_trading_day=data['secDate'],
                                                      prev_close=data['previousClose'], change=data['change'],
                                                      change_percentage=data['pChange'])

        up = Holdings.objects.filter(stock__company_ticker=ticker).last()

        if up is not None:
            up.ltp = data['lastPrice']
            # print("ltp", up.ltp)
            up.save()

    elif market == 'BSE':
        data = b.getQuote(ticker)
        e = Daily_Realtime_Price.objects.filter(company_name=data['companyName'],
                                                      company_ticker=data['scripCode'], market='BSE').last()
        
        if e is not None:

            e.open = data['previousOpen']
            e.close = data['previousClose']
            e.high = data['dayHigh']
            e.low = data['dayLow']
            e.price = data['currentValue']
            e.volume = 0
            e.latest_trading_day = data['updatedOn']
            e.prev_close = data['previousClose']
            e.change =  data['change']
            e.change_percentage = data['pChange']

            e.save()

        else:

            e = Daily_Realtime_Price.objects.create(company_name=data['companyName'], company_ticker=data['scripCode'],market='BSE', open=data['previousOpen'], high=data['dayHigh'],
                                                      low=data['dayLow'], close=data['previousClose'],
                                                      price=data['currentValue'], volume=0,
                                                      latest_trading_day=data['updatedOn'],
                                                      prev_close=data['previousClose'], change=data['change'],
                                                      change_percentage=data['pChange'])

        up = Holdings.objects.filter(stock__company_ticker=ticker).last()

        if up is not None:
            up.ltp = data['currentValue']

            # print("ltp",up.ltp)

            up.save()

# @periodic_task(run_every = crontab())

@shared_task
def add_to_db():
    nsed = Holdings.objects.all()
    for i in nsed:
        if i.stock.market == 'NSE':
            update_data(i.stock.company_ticker, 'NSE')
            # print("Added {}".format(i.stock.company_ticker))
        elif i.stock.market == 'BSE':
            update_data(i.stock.company_ticker, 'BSE')
            # print("Added {}".format(i.stock.company_ticker))

    print("updated all data")
    #time.sleep(30)


def update_real_time():
    add_to_db.delay()


def display_chart(request, ticker):
    pass


def search_stocks(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        market = request.POST.get('market')

        print(market)

        if market == 'NSE':
            result = Company_Names_NSE.objects.filter(Q(company_name__icontains=keyword) | Q(company_code_nse__icontains=keyword))
        else:
            result = Company_Names_BSE.objects.filter(Q(company_name__icontains=keyword) | Q(company_code_bse__icontains=keyword))

        return render(request,"search-results.html",{"data":result,"market":market})

def predict(request, ticker, market):
    if market == 'BSE':
        messages.info(request, "This Feature will appear in future, Only NSE Based Stock available for prediction")
        return redirect("/")

    else:
        res = requests.get('http://localhost:5900/predict/?ticker={}'.format(ticker))

        res  = res.json()

        res = {
            "Prediction":str(res)
        }

        return JsonResponse(res)


def show_history(request):
    h = History.objects.filter(investor=request.user).order_by('-datetime')

    return render(request,"history.html",{"data":h})

def reset_data(request):
    Holdings.objects.filter(investor=request.user).delete()
    Daily_Realtime_Price.objects.all().delete()
    History.objects.filter(investor=request.user).delete()
    Watchlist.objects.filter(user=request.user).delete()
    i = Investor_Staus.objects.get(investor=request.user)
    i.balance = 500000
    i.transactions = 0
    i.profit = 0
    i.loss = 0
    i.p_transactions = 0
    i.n_transactions = 0
    i.save()
    messages.info(request,"Account Has Been Reset. All Records Deleted.")

    return redirect("/")