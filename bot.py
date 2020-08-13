import telebot
from telebot import types
import const
import exchange_rates
from wording import wording
from calculations import *
import math

bot = telebot.TeleBot(const.api_token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = f"{message.from_user.first_name} {message.from_user.last_name}"
    bot.send_message(message.chat.id, f'Привет, {name}, я твой реселл-калькулятор!')
    marketplace_menu(message)


def marketplace_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add('StockX')
    markup.add('Nice')
    markup.add('Poison')
    markup.add('Лучшее предложение')
    if message.text == 'Назад к выбору площадки':
        bot.send_message(message.chat.id, 'Хорошо, выбери площадку:', reply_markup=markup)
        bot.register_next_step_handler(message, handler_menu)
    else:
        bot.send_message(message.chat.id, f'{wording["welcome"]}', reply_markup=markup)
        bot.register_next_step_handler(message, handler_menu)

def handler_menu(message):
    if message.text == 'StockX':
        stockx(message)
    elif message.text == 'Nice':
        nice(message)
    elif message.text == 'Poison':
        poison(message)
    elif message.text == 'Лучшее предложение':
        bestoffer(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, 'Выбери один из предложенных вариантов!')
        bot.register_next_step_handler(message, handler_menu)


def stockx(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add('Алексей Уваров', 'kikoX', 'КитДо USA', 'Назад к выбору площадки')
    bot.send_message(message.chat.id, "Выбери посредника:", reply_markup=markup)
    bot.register_next_step_handler(message, stockx_handler)


def stockx_handler(message):
    if message.text == 'Алексей Уваров':
        uvarov(message)
    elif message.text == 'kikoX':
        kikox(message)
    elif message.text == 'КитДо USA':
        kitdousa(message)
    elif message.text == 'Назад к выбору площадки':
        marketplace_menu(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, 'Выбери один из предложенных вариантов!')
        bot.register_next_step_handler(message, stockx_handler)



def uvarov(message):
    bot.send_message(message.chat.id, f'{wording["stockx"]}')
    bot.register_next_step_handler(message, uvarov_calc)


def uvarov_calc(message):
    if stockx_backandchange(message):
        stockx_handler(message)
    else:
        if f'{message.text}'.isdigit():
            bot.send_message(message.chat.id,
                             f'Сумма выплаты {uvarov_calculation(message)}$ = {round(uvarov_calculation(message) * exchange_rates.USD, 2)} руб. по курсу ЦБ РФ, {wording["retryandback"]}')
            bot.register_next_step_handler(message, stockx_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, uvarov_calc)


def kikox(message):
    bot.send_message(message.chat.id, f'{wording["stockx"]}')
    bot.register_next_step_handler(message, kikox_calc)


def kikox_calc(message):
    if stockx_backandchange(message):
        stockx_handler(message)
    else:
        if f'{message.text}'.isdigit():
            bot.send_message(message.chat.id,
                             f'Сумма выплаты {kikox_calculation(message)}$ = {round(kikox_calculation(message) * const.usdkikox, 2)} руб. по курсу Paypal указанному в сообществе kikoX, {wording["retryandback"]}')
            bot.register_next_step_handler(message, stockx_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, uvarov_calc)


def kitdousa(message):
    bot.send_message(message.chat.id, f'{wording["stockx"]}')
    bot.register_next_step_handler(message, kitdousa_calc)


def kitdousa_calc(message):
    if stockx_backandchange(message):
        stockx_handler(message)
    else:
        if f'{message.text}'.isdigit():
            bot.send_message(message.chat.id,
                             f'Сумма выплаты {kitdousa_calculation(message)}$ = {round(kitdousa_calculation(message) * exchange_rates.USD, 2)} руб. по курсу ЦБ РФ, {wording["retryandback"]}')
            bot.register_next_step_handler(message, stockx_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, kitdousa_calc)


def nice(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add('НеКит', 'Quasar Logistic', 'КитДо', 'Назад к выбору площадки')
    bot.send_message(message.chat.id, "Выбери посредника:", reply_markup=markup)
    bot.register_next_step_handler(message, nice_handler)


def nice_handler(message):
    if message.text == 'НеКит':
        nekit_nice(message)
    elif message.text == 'Quasar Logistic':
        quasar_nice(message)
    elif message.text == 'КитДо':
        kitdo_nice(message)
    elif message.text == 'Назад к выбору площадки':
        marketplace_menu(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, 'Выбери один из предложенных вариантов!')
        bot.register_next_step_handler(message, nice_handler)


def nekit_nice(message):
    bot.send_message(message.chat.id, f'{wording["nice"]}')
    bot.register_next_step_handler(message, nekit_nice_calc)


def nekit_nice_calc(message):
    if nice_backandchange(message):
        nice_handler(message)
    else:
        if f'{message.text}'.isdigit():
            bot.send_message(message.chat.id,
                             f'Сумма выплаты {nekit_nice_calculation(message)}¥ = {round(nekit_nice_calculation(message) * exchange_rates.CNY, 2)} руб. по курсу ЦБ РФ, {wording["retryandback"]} {wording["nekit"]}')
            bot.register_next_step_handler(message, nice_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, nekit_nice_calc)


def quasar_nice(message):
    bot.send_message(message.chat.id, f'{wording["nice"]}')
    bot.register_next_step_handler(message, quasar_nice_calc)


def quasar_nice_calc(message):
    if nice_backandchange(message):
        nice_handler(message)
    else:
        if f'{message.text}'.isdigit():
            bot.send_message(message.chat.id,
                             f'Сумма выплаты {quasar_nice_calculation(message)}¥ = {round(quasar_nice_calculation(message) * exchange_rates.CNY, 2)} руб. по курсу ЦБ РФ, {wording["retryandback"]} {wording["quasar"]}')
            bot.register_next_step_handler(message, nice_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, quasar_nice_calc)


def kitdo_nice(message):
    bot.send_message(message.chat.id, f'{wording["nice"]}')
    bot.register_next_step_handler(message, kitdo_nice_calc)


def kitdo_nice_calc(message):
    if nice_backandchange(message):
        nice_handler(message)
    else:
        if f'{message.text}'.isdigit():
            bot.send_message(message.chat.id,
                             f'Сумма выплаты {kitdo_nice_calculation(message)}¥ = {round(kitdo_nice_calculation(message) * exchange_rates.CNY, 2)} руб. по курсу ЦБ РФ, {wording["retryandback"]}')
            bot.register_next_step_handler(message, nice_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, kitdo_nice_calc)


def poison(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add('НеКит', 'Quasar Logistic', 'КитДо', 'Назад к выбору площадки')
    bot.send_message(message.chat.id, "Выбери посредника:", reply_markup=markup)
    bot.register_next_step_handler(message, poison_handler)


def poison_handler(message):
    if message.text == 'НеКит':
        nekit_poison(message)
    elif message.text == 'Quasar Logistic':
        quasar_poison(message)
    elif message.text == 'КитДо':
        kitdo_poison(message)
    elif message.text == 'Назад к выбору площадки':
        marketplace_menu(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, 'Выбери один из предложенных вариантов!')
        bot.register_next_step_handler(message, poison_handler)


def nekit_poison(message):
    bot.send_message(message.chat.id, f'{wording["poison"]}')
    bot.register_next_step_handler(message, nekit_poison_calc)


def nekit_poison_calc(message):
    if poison_backandchange(message):
        poison_handler(message)
    else:
        if f'{message.text}'.isdigit():
            bot.send_message(message.chat.id,
                             f'Сумма выплаты {nekit_poison_calculation(message)}¥ = {round(nekit_poison_calculation(message) * exchange_rates.CNY, 2)} руб. по курсу ЦБ РФ, {wording["retryandback"]} {wording["nekit"]}')
            bot.register_next_step_handler(message, poison_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, nekit_poison_calc)


def quasar_poison(message):
    bot.send_message(message.chat.id, f'{wording["poison"]}')
    bot.register_next_step_handler(message, quasar_poison_calc)


def quasar_poison_calc(message):
    if poison_backandchange(message):
        poison_handler(message)
    else:
        if f'{message.text}'.isdigit():
            bot.send_message(message.chat.id,
                             f'Сумма выплаты {quasar_poison_calculation(message)}¥ = {round(quasar_poison_calculation(message) * exchange_rates.CNY, 2)} руб. по курсу ЦБ РФ, {wording["retryandback"]} {wording["quasar"]}')
            bot.register_next_step_handler(message, poison_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, quasar_poison_calc)


def kitdo_poison(message):
    bot.send_message(message.chat.id, f'{wording["poison"]}')
    bot.register_next_step_handler(message, kitdo_poison_calc)


def kitdo_poison_calc(message):
    if poison_backandchange(message):
        poison_handler(message)
    else:
        if f'{message.text}'.isdigit():
            bot.send_message(message.chat.id,
                             f'Сумма выплаты {kitdo_poison_calculation(message)}¥ = {round(kitdo_poison_calculation(message) * exchange_rates.CNY, 2)} руб. по курсу ЦБ РФ, {wording["retryandback"]}')
            bot.register_next_step_handler(message, poison_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, kitdo_poison_calc)


def bestoffer(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add('StockX', 'Китай', 'На всех площадках', 'Назад к выбору площадки')
    bot.send_message(message.chat.id, "Выбери вариант:", reply_markup=markup)
    bot.register_next_step_handler(message, bestoffer_handler)


def bestoffer_handler(message):
    if message.text == 'StockX':
        stockx_bestoffer(message)
    elif message.text == 'Китай':
        china_bestoffer(message)
    elif message.text == 'На всех площадках':
        all_bestoffer(message)
    elif message.text == 'Назад к выбору площадки':
        marketplace_menu(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, 'Выбери один из предложенных вариантов!')
        bot.register_next_step_handler(message, bestoffer_handler)


def stockx_bestoffer(message):
    bot.send_message(message.chat.id, f'{wording["stockx"]}')
    bot.register_next_step_handler(message, stockx_bestoffer_calc)


def stockx_bestoffer_calc(message):
    if bestoffer_backandchange(message):
        bestoffer_handler(message)
    else:
        if f'{message.text}'.isdigit():
            bot.send_message(message.chat.id, f'{stockx_bestoffer_calculation(message)}, {wording["retryandback"]}')
            bot.register_next_step_handler(message, bestoffer_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, stockx_bestoffer_calc)

def china_bestoffer(message):
    bot.send_message(message.chat.id, f'{wording["china"]}')
    bot.register_next_step_handler(message, china_bestoffer_calc)


def china_bestoffer_calc(message):
    if bestoffer_backandchange(message):
        bestoffer_handler(message)
    else:
        if isinstance(message.text.split(","), list):
            bot.send_message(message.chat.id,
                             f'{china_bestoffer_calculation(message)} руб. по курсу ЦБ РФ, {wording["retryandback"]}')
            bot.register_next_step_handler(message, bestoffer_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, china_bestoffer_calc)

def all_bestoffer(message):
    bot.send_message(message.chat.id, f'{wording["all"]}')
    bot.register_next_step_handler(message, all_bestoffer_calc)
def all_bestoffer_calc(message):
    if bestoffer_backandchange(message):
        bestoffer_handler(message)
    else:
        if isinstance(message.text.split(","), list):
            bot.send_message(message.chat.id, f'{all_bestoffer_calculation(message)}, {wording["retryandback"]}')
            bot.register_next_step_handler(message, bestoffer_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, all_bestoffer_calc)


def stockx_backandchange(message):
    if message.text == 'Алексей Уваров' or message.text == 'kikoX' or message.text == 'КитДо USA' or message.text == 'Назад к выбору площадки':
        return True


def nice_backandchange(message):
    if message.text == 'НеКит' or message.text == 'Quasar Logistic' or message.text == 'КитДо' or message.text == 'Назад к выбору площадки':
        return True


def poison_backandchange(message):
    if message.text == 'НеКит' or message.text == 'Quasar Logistic' or message.text == 'КитДо' or message.text == 'Назад к выбору площадки':
        return True

def bestoffer_backandchange(message):
    if message.text == 'StockX' or message.text == 'Китай' or message.text == 'На всех площадках' or message.text == 'Назад к выбору площадки':
        return True


bot.infinity_polling(True)
