import const
from exchange_rates import *
import copy
from telebot import types

def uvarov_calculation(price):
    x = float(price.text)
    return round(x * 0.84 - 11.5, 2)


def kikox_calculation(price):
    x = float(price.text)
    if x > 0 and x <= 300:
        return round(x * 0.89 - 11.5 - 700 / const.usdkikox, 2)
    if x > 300 and x <= 500:
        return round(x * 0.89 - 11.5 - 1100 / const.usdkikox, 2)
    if x > 500 and x <= 950:
        return round(x * 0.89 - 11.5 - 1600 / const.usdkikox, 2)


def kitdousa_calculation(price):
    x = float(price.text)
    return round(x * 0.875 - 23)


def nekit_nice_calculation(price):
    x = float(price.text)
    return round(x * 0.97 - 40)


def quasar_nice_calculation(price):
    x = float(price.text)
    return round(x * 0.97 - 40)


def kitdo_nice_calculation(price):
    x = float(price.text)
    if x < 5000:
        return round(x * 0.97 - 40 - 1500/CNY)
    else:
        return round(x * 0.91 - 40)

def nekit_poison_calculation(price):
    x = float(price.text)
    return round(x * 0.955 - 40)

def quasar_poison_calculation(price):
    x = float(price.text)
    return round(x * 0.94 - 40)

def kitdo_poison_calculation(price):
    x = float(price.text)
    if x < 5000:
        return round(x * 0.94 - 40 - 1500 / CNY)
    else:
        return round(x * 0.88 - 40)

def max_nice(price):
    return max(nekit_nice_calculation(price), quasar_nice_calculation(price), kitdo_nice_calculation(price))

def max_poison(price):
    return max(nekit_poison_calculation(price), quasar_poison_calculation(price), kitdo_poison_calculation(price))

def max_stockx(price):
    if int(price.text) > 950:
        return max(uvarov_calculation(price), kitdousa_calculation(price))
    else:
        return max(uvarov_calculation(price), kikox_calculation(price), kitdousa_calculation(price))


def stockx_bestoffer_calculation(price):
    if max_stockx(price) == uvarov_calculation(price):
        return f'Лучшее предложение на StockX - Алексей Уваров. Сумма выплаты: {round(max_stockx(price), 2)}$ = {round(max_stockx(price) * USD, 2)} руб. по курсу ЦБ РФ'
    if max_stockx(price) == kikox_calculation(price):
        return f'Лучшее предложение на StockX - kikoX. Сумма выплаты: {round(max_stockx(price), 2)}$ = {round(max_stockx(price) * const.usdkikox, 2)} руб. по курсу Paypal указанному в сообществе kikoX'
    if max_stockx(price) == kitdousa_calculation(price):
        return f'Лучшее предложение на StockX - КитДо USA. Сумма выплаты: {round(max_stockx(price), 2)}$ = {round(max_stockx(price) * USD, 2)}, руб. по курсу ЦБ РФ'


def china_bestoffer_calculation(price):
    prices = price.text.split(",")
    price_n = copy.deepcopy(price)
    #price_n.json["text"] = f'{prices[0]}'
    price_n.text = f'{prices[0]}'
    price_p = copy.deepcopy(price)
    price_p.text = f'{prices[1]}'
    print(price_p.text.isdigit())
    #price_p.json["text"] = f'{prices[1]}'
    print(price_n.text, price_p.text)
    max_n = max_nice(price_n)
    max_p = max_poison(price_p)
    if max_n > max_p:
        if max_nice(price_n) == nekit_nice_calculation(price_n):
            return f'Лучшее предложение в Китае - НеКит.Nice. Сумма выплаты: {round(max_nice(price_n), 2)}¥ = {round(max_nice(price_n) * CNY, 2)}, руб. по курсу ЦБ РФ'
        if max_nice(price_n) == quasar_nice_calculation(price_n):
            return f'Лучшее предложение в Китае - Quasar Logistic.Nice. Сумма выплаты: {round(max_nice(price_n), 2)}¥ = {round(max_nice(price_n) * CNY, 2)}, руб. по курсу ЦБ РФ'
        if max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n), kitdo_nice_calculation(price_n)) == kitdo_nice_calculation(price_n):
            return f'Лучшее предложение в Китае - КитДо.Nice. Сумма выплаты: {round(max_nice(price_n), 2)}¥ = {round(max_nice(price_n) * CNY, 2)}, руб. по курсу ЦБ РФ'
    else:
        if max_poison(price_p) == nekit_poison_calculation(price_p):
            return f'Лучшее предложение в Китае - НеКит.Poison. Сумма выплаты: {round(max_poison(price_p), 2)}¥ = {round(max_poison(price_p) * CNY, 2)}, руб. по курсу ЦБ РФ'
        if max_poison(price_p) == quasar_poison_calculation(price_p):
            return f'Лучшее предложение в Китае - Quasar Logistic.Poison. Сумма выплаты: {round(max_poison(price_p), 2)}¥ = {round(max_poison(price_p) * CNY, 2)}, руб. по курсу ЦБ РФ'
        if max_poison(price_p) == kitdo_poison_calculation(price_p):
            return f'Лучшее предложение в Китае - КитДо.Poison. Сумма выплаты: {round(max_poison(price_p), 2)}¥ = {round(max_poison(price_p) * CNY, 2)}, руб. по курсу ЦБ РФ'

def all_bestoffer_calculation(price):
    prices = price.text.split(",")
    price_s = copy.deepcopy(price)
    price_s.text = f'{prices[0]}'
    price_n = copy.deepcopy(price)
    price_n.text = f'{prices[1]}'
    price_p = copy.deepcopy(price)
    price_p.text = f'{prices[2]}'
    price_c = copy.deepcopy(price)
    price_c.text = f'{prices[1]},{prices[2]}'
    max_s = max_stockx(price_s)*USD
    max_n = max_nice(price_n)*CNY
    max_p = max_poison(price_p)*CNY
    if max(max_s, max_n, max_p) == max_s:
        return stockx_bestoffer_calculation(price_s)
    else:
        return china_bestoffer_calculation(price_c)


