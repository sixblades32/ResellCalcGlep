import datetime
from pycbrf.toolbox import ExchangeRates
now = datetime.datetime.now()
day = now.day
month = now.month
year = now.year

rates = ExchangeRates(f'{year}-{month}-{day}')
USD = round(float(rates['USD'][4]), 2)
CNY = round(float(rates['CNY'][6]), 2)
