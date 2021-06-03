from django.db import models
from Accounts.models import User, Investor
#from django.contrib.auth.models import User
from time import timezone
from django.utils.text import slugify
import datetime

# Create your models here.
"""class User(AbstractBaseUser):
    gender = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    name = models.CharField(max_length=75)
    email = models.EmailField()
    phone = models.IntegerField()
    gender = models.CharField(choices=gender, max_length=10)
    dob = models.DateField()
    passwd = models.CharField(max_length=12)
    c_pwd = models.CharField(max_length=12)"""

class Company_Names_BSE(models.Model):
    company_name = models.CharField(max_length=350)
    company_code_bse = models.CharField(max_length=50)
    #market = models.CharField(max_length=10,choices = markets, default='BSE')
    #company_code = models.CharField(max_length=50, default = '000000')

    def __str__(self):
        return self.company_name

    def get_absolute_url(self):
        return f"info/{ self.company_code_bse }/BSE"

class Company_Names_NSE(models.Model):
    company_name = models.CharField(max_length=350)
    company_code_nse = models.CharField(max_length=50)
    #market = models.CharField(max_length=10,choices = markets, default='BSE')
    #company_code = models.CharField(max_length=50, default = '000000')

    def __str__(self):
        return self.company_name

    def get_absolute_url(self):
        return f"info/{ self.company_code_nse }/NSE"

class Daily_Realtime_Price(models.Model):
    markets = [
        ('BSE','BSE'),
        ('NSE','NSE')
    ]
    company_name = models.CharField(max_length=350)
    company_ticker = models.CharField(max_length=70)
    market = models.CharField(choices=markets, max_length=5)
    open = models.FloatField(default=0)
    high = models.FloatField(default=0)
    low = models.FloatField(default=0)
    close = models.FloatField(null = True,default=0)
    price = models.FloatField(default=0)
    volume = models.FloatField(default=0)
    latest_trading_day = models.CharField(max_length=20,default=datetime.datetime.now(), null = True)
    prev_close = models.FloatField(default=0)
    change  = models.FloatField(null=True,default=0)
    change_percentage = models.TextField(null = True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_ticker

    def get_absolute_url(self):
        return f"/{self.company_ticker}/{self.market}"

    def add_to_wtl(self):
        return f"addw/{self.company_ticker}/{self.market}"

    def rm_frm_wtl(self):
        return f"rmw/{self.company_ticker}/{self.market}"


    def buy(self):
        return f"/buy/{ self.company_ticker }/{ self.market }"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Daily_Realtime_Price, on_delete= models.CASCADE)

    def __str__(self):
        return self.stock

    def get_absolute_url(self):
        return f"/info/{ self.stock.company_ticker }/{ self.stock.market }"

class Holdings(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Daily_Realtime_Price, on_delete=models.CASCADE)
    bought_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    ltp = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    #bought_time = models.SlugField(default = )

    def __str__(self):
        return self.stock

    def get_time(self):
        return str(self.time)

    def get_absolute_url(self):
        return f"info/{ self.stock.company_ticker }/{ self.stock.market }"

    def get_detailed_url(self):
        return f"info/{self.stock.company_ticker}/{self.stock.market}/{ self.get_time() }"

    def get_buy_price(self):
        return f"buy/{ self.stock.company_ticker }/{ self.stock.market }"

    def sell_stock(self):
        time_slug = self.get_time()
        return f"sell/{ self.stock.company_ticker }/{ self.stock.market }/{ self.get_time() }"

    def value(self):
        return self.ltp * self.quantity
    def gain(self):
        return self.ltp - self.bought_price

class Investor_Staus(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=500000)
    transactions = models.PositiveIntegerField(default=0)
    profit = models.FloatField(default=0)
    loss = models.FloatField(default=0)
    p_transactions = models.PositiveIntegerField(default=0)
    n_transactions = models.PositiveIntegerField(default=0)


class History(models.Model):
    transaction = [
        ('BUY','BUY'),
        ('SELL','SELL'),
    ]
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Daily_Realtime_Price, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    bought_price = models.FloatField(default=0)
    cost = models.PositiveIntegerField(default=0)
    sold_price = models.FloatField(default=0)
    t_type = models.CharField(choices=transaction,max_length=5)
    gain = models.FloatField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)







