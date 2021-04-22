import nsetools
from nsetools import Nse
from bsedata.bse import BSE
import csv
import pandas as pd
import yfinance as yf
import datetime
from datetime import date

"""b = BSE()
n = Nse()

b.updateScripCodes()

fieldnames = ['BSECode','Company Name']

data = b.getScripCodes()

print(len(data))

nata = n.get_stock_codes()
print("n",len(nata))

diction1 = {
    "Company Name":list(data.values()),
    "BSECode":list(data.keys()),
}

df1 = pd.DataFrame(diction1)

print(df1)

diction2 = {
    "NSECode":list(nata.keys())
}

df2 = pd.DataFrame(diction2)

#rt = pd.concat([df1,df2])

#print(rt)



#rt = pd.DataFrame(diction)

#rt.index = rt.index + 1

#rt.to_csv("stock_data.csv")

with open("stock_data.csv","w", encoding = "utf-8") as g:
    w = csv.DictWriter(g,fieldnames=fieldnames)
    w.writeheader()
    w.writerow(diction)
    print("done")

b.updateScripCodes()

data = b.getQuote('500290')

print(data)"""

today = date.today()

#data = yf.Ticker("MRF").history(start = date(today.year - 8,today.month, today.day ), end = today)

data = yf.download("SBIN",period = "1d", start = date(today.year - 8,today.month, today.day ), end = today)

df = pd.DataFrame(data)
print(df)
df.plot()