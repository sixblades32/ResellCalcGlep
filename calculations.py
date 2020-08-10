import const
from exchange_rates import *
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

def stockx_bestoffer_calculation(price):
    if max(uvarov_calculation(price), kikox_calculation(price),kitdousa_calculation(price)) == uvarov_calculation(price):
        return f'Лучшее предложение на StockX - Алексей Уваров. Сумма выплаты: {round(max(uvarov_calculation(price), kikox_calculation(price),kitdousa_calculation(price)), 2)}$ = {round(max(uvarov_calculation(price), kikox_calculation(price),kitdousa_calculation(price)) * USD, 2)} руб. по курсу ЦБ РФ'
    if max(uvarov_calculation(price), kikox_calculation(price),kitdousa_calculation(price)) == kikox_calculation(price):
        return f'Лучшее предложение на StockX - kikoX. Сумма выплаты: {round(max(uvarov_calculation(price), kikox_calculation(price),kitdousa_calculation(price)), 2)}$ = {round(max(uvarov_calculation(price), kikox_calculation(price),kitdousa_calculation(price)) * const.usdkikox, 2)} руб. по курсу Paypal указанному в сообществе kikoX'
    if max(uvarov_calculation(price), kikox_calculation(price),kitdousa_calculation(price)) == kitdousa_calculation(price):
        return f'Лучшее предложение на StockX - КитДо USA. Сумма выплаты: {round(max(uvarov_calculation(price), kikox_calculation(price),kitdousa_calculation(price)), 2)}$ = {round(max(uvarov_calculation(price), kikox_calculation(price),kitdousa_calculation(price)) * USD, 2)}, руб. по курсу ЦБ РФ'

def china_bestoffer_calculation(price):
    prices = price.text.split(",")
    price_n = price
    #price_n.json["text"] = f'{prices[0]}'
    price_n.text = f'{prices[0]}'
    price_p = price
    price_p.text = f'{prices[1]}'
    #price_p.json["text"] = f'{prices[1]}'
    print(price_n.text, price_p.text)
    max_nice = max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n),kitdo_nice_calculation(price_n))
    max_poison = max(nekit_poison_calculation(price_p), quasar_poison_calculation(price_p),kitdo_poison_calculation(price_p))
    if max_nice > max_poison:
        if max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n), kitdo_nice_calculation(price_n)) == nekit_nice_calculation(price_n):
            return f'Лучшее предложение в Китае - НеКит.Nice. Сумма выплаты: {round(max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n), kitdo_nice_calculation(price_n)), 2)}¥ = {round(max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n), kitdo_nice_calculation(price_n)) * CNY, 2)}'
        if max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n), kitdo_nice_calculation(price_n)) == quasar_nice_calculation(price_n):
            return f'Лучшее предложение в Китае - Quasar Logistic.Nice. Сумма выплаты: {round(max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n), kitdo_nice_calculation(price_n)), 2)}¥ = {round(max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n), kitdo_nice_calculation(price_n)) * CNY, 2)}'
        if max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n), kitdo_nice_calculation(price_n)) == kitdo_nice_calculation(price_n):
            return f'Лучшее предложение в Китае - КитДо.Nice. Сумма выплаты: {round(max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n), kitdo_nice_calculation(price_n)), 2)}¥ = {round(max(nekit_nice_calculation(price_n), quasar_nice_calculation(price_n), kitdo_nice_calculation(price_n)) * CNY, 2)}'
    else:
        if max(nekit_poison_calculation(price_p), quasar_poison_calculation(price_p), kitdo_poison_calculation(price_p)) == nekit_poison_calculation(price_p):
            return f'Лучшее предложение в Китае - НеКит.Poison. Сумма выплаты: {round(max(nekit_poison_calculation(price_p), quasar_poison_calculation(price_p), kitdo_poison_calculation(price_p)), 2)}¥ = {round(max(nekit_poison_calculation(price_p), quasar_poison_calculation(price_p), kitdo_poison_calculation(price_p)) * CNY, 2)}'
        if max(nekit_poison_calculation(price_p), quasar_poison_calculation(price_p), kitdo_poison_calculation(price_p)) == quasar_poison_calculation(price_p):
            return f'Лучшее предложение в Китае - Quasar Logistic.Poison. Сумма выплаты: {round(max(nekit_poison_calculation(price_p), quasar_poison_calculation(price_p), kitdo_poison_calculation(price_p)), 2)}¥ = {round(max(nekit_poison_calculation(price_p), quasar_poison_calculation(price_p), kitdo_poison_calculation(price_p)) * CNY, 2)}'
        if max(nekit_poison_calculation(price_p), quasar_poison_calculation(price_p), kitdo_poison_calculation(price_p)) == kitdo_poison_calculation(price_p):
            return f'Лучшее предложение в Китае - КитДо.Poison. Сумма выплаты: {round(max(nekit_poison_calculation(price_p), quasar_poison_calculation(price_p), kitdo_poison_calculation(price_p)), 2)}¥ = {round(max(nekit_poison_calculation(price_p), quasar_poison_calculation(price_p), kitdo_poison_calculation(price_p)) * CNY, 2)}'

