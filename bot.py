import telebot
from telebot import types
import const
import exchange_rates
from wording import wording
from calculations import *
import math
from commission import commissions_rate

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
    markup.add('Алексей Уваров(Affliction#6369)', 'kikoX', 'КитДо USA', 'Назад к выбору площадки')
    bot.send_message(message.chat.id, "Выбери посредника:", reply_markup=markup)
    bot.register_next_step_handler(message, stockx_handler)


def stockx_handler(message):
    if message.text == 'Алексей Уваров(Affliction#6369)':
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
            if float(message.text) > 950:
                bot.send_message(message.chat.id,
                                 f"Для расчета выплаты через kikoX при продаже товара на сумму свыше 950$ обратись в сообщество kikoX Вконтакте! Воспользуйся кнопками для дальнейших расчетов")
                bot.register_next_step_handler(message, kikox_calc)
            else:
                bot.send_message(message.chat.id,
                                 f'Сумма выплаты {kikox_calculation(message)}$ = {round(kikox_calculation(message) * const.usdkikox, 2)} руб. по курсу Paypal указанному в сообществе kikoX, {wording["retryandback"]}')
                bot.register_next_step_handler(message, stockx_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, kikox_calc)


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
    markup.add('НеКит', 'Quasar Logistic', 'КитДо', 'Индивидуальные условия', 'Назад к выбору площадки')
    bot.send_message(message.chat.id, "Выбери посредника:", reply_markup=markup)
    bot.register_next_step_handler(message, nice_handler)


def nice_handler(message):
    if message.text == 'НеКит':
        nekit_nice(message)
    elif message.text == 'Quasar Logistic':
        quasar_nice(message)
    elif message.text == 'КитДо':
        kitdo_nice(message)
    elif message.text == 'Индивидуальные условия':
        individual_terms(message)
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


def individual_terms(message):
    if commissions_rate["exchange_rate"] != '':
        markup = types.ReplyKeyboardMarkup(row_width=1)
        markup.add('Рассчитать', 'Изменить')
        bot.send_message(message.chat.id,
                         f'Последние заданные значения:\nКомиссия в рублях: {commissions_rate["comm_value"]}\nКомиссия в процентах: {commissions_rate["comm_percent"]}\nКурс: {commissions_rate["exchange_rate"]}',
                         reply_markup=markup)
        bot.register_next_step_handler(message, individual_terms_handler)
    else:
        bot.send_message(message.chat.id, 'Индивидуальные значение не были заданы, требуется их задать!')
        individual_terms_price(message)


def individual_terms_handler(message):
    if message.text == 'Рассчитать':
        individual_terms_price(message)
    elif message.text == 'Изменить':
        commissions_rate["comm_value"] = ''
        commissions_rate["comm_percent"] = ''
        commissions_rate["exchange_rate"] = ''
        bot.send_message(message.chat.id, 'Значения сброшены, требуется задать новые')
        individual_terms_price(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, f'Выбери из предложенных вариантов!')
        bot.register_next_step_handler(message, individual_terms_handler)


def individual_terms_price(message):
    bot.send_message(message.chat.id, f'{wording["nice"]}')
    bot.register_next_step_handler(message, commission_handler)


def commission_handler(message):
    if message.text.isdigit() and commissions_rate["exchange_rate"] == '':
        commissions_rate['price'] = f'{message.text}'
        markup = types.ReplyKeyboardMarkup(row_width=3)
        markup.add('НеКит', 'Quasar Logistic', 'КитДо', 'Собственное значение')
        bot.send_message(message.chat.id, f'{wording["commission"]}', reply_markup=markup)
        bot.register_next_step_handler(message, commission_check)
    elif message.text.isdigit() and commissions_rate["exchange_rate"] != '':
        commissions_rate['price'] = f'{message.text}'
        individual_terms_calc(message)
    else:
        bot.send_message(message.chat.id, "Введи корректное значение!")
        bot.register_next_step_handler(message, commission_handler)


def commission_check(message):
    if message.text == "Собственное значение":
        markup = types.ReplyKeyboardMarkup(row_width=1)
        markup.add('В рублях', 'В процентах')
        bot.send_message(message.chat.id, f'{wording["commission_choose"]}', reply_markup=markup)
        bot.register_next_step_handler(message, commission_format)
    elif message.text == 'НеКит':
        commission_value(message)
    elif message.text == 'КитДо':
        commission_value(message)
    elif message.text == 'Quasar Logistic':
        commission_value(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, f'Выбери из предложенных вариантов!')
        bot.register_next_step_handler(message, commission_check)


def commission_format(message):
    if message.text == 'В рублях':
        bot.send_message(message.chat.id, f'{wording["commission_rub"]}')
        bot.register_next_step_handler(message, commission_value)
    elif message.text == 'В процентах':
        bot.send_message(message.chat.id, f'{wording["commission_percent"]}')
        bot.register_next_step_handler(message, commission_value)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, f'Выбери из предложенных вариантов')
        bot.register_next_step_handler(message, commission_format)


def commission_value(message):
    if message.text[-1].isdigit() and message.text[-1] != "%":
        commissions_rate['comm_value'] = f'{message.text}'
        commissions_rate['comm_percent'] = '0'
        bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
        bot.register_next_step_handler(message, comm_exchange_rates)
    elif message.text[-1] == '%':
        bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
        commissions_rate['comm_percent'] = f'{message.text[:-1]}'
        commissions_rate['comm_value'] = '0'
        bot.register_next_step_handler(message, comm_exchange_rates)
    elif message.text == 'НеКит':
        bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
        commissions_rate['comm_percent'] = '0'
        commissions_rate['comm_value'] = '0'
        bot.register_next_step_handler(message, comm_exchange_rates)
    elif message.text == 'КитДо':
        if float(commissions_rate['price']) < 5000:
            commissions_rate['comm_value'] = f'{1500 / CNY}'
            commissions_rate['comm_percent'] = '0'
            bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
            bot.register_next_step_handler(message, comm_exchange_rates)
        else:
            commissions_rate['comm_value'] = '0'
            commissions_rate['comm_percent'] = '6'
            bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
            bot.register_next_step_handler(message, comm_exchange_rates)
    elif message.text == 'Quasar Logistic':
        commissions_rate['comm_percent'] = '0'
        commissions_rate['comm_value'] = '0'
        bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
        bot.register_next_step_handler(message, comm_exchange_rates)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, f'Неверный формат ввода!')
        bot.register_next_step_handler(message, commission_value)


def comm_exchange_rates(message):
    if message.text.split(".")[0].isdigit() and message.text.split(".")[1].isdigit():
        if message.text[2] == '.' or message.text[3] == '.':
            commissions_rate['exchange_rate'] = f'{message.text}'
            individual_terms_calc(message)
    elif message.text == 'ЦБ':
        commissions_rate['exchange_rate'] = f'{CNY}'
        individual_terms_calc(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, f'Неверный формат ввода!')
        bot.register_next_step_handler(message, comm_exchange_rates)
    print(commissions_rate)


def individual_terms_calc(message):
    price = copy.deepcopy(message)
    price.text = f'{commissions_rate["price"]}'
    if nice_backandchange(message):
        nice_handler(message)
    else:
        markup = types.ReplyKeyboardMarkup(row_width=3)
        markup.add('НеКит', 'Quasar Logistic', 'КитДо', 'Индивидуальные условия', 'Назад к выбору площадки')
        if f'{price.text}'.isdigit():
            bot.send_message(price.chat.id,
                             f'Сумма выплаты {round(individual_calculation_nice(price.text), 2)}¥ = {round(individual_calculation_nice(price.text) * float(commissions_rate["exchange_rate"]), 2)} руб. по заданному курсу, {wording["retryandback"]}',
                             reply_markup=markup)
            bot.register_next_step_handler(message, nice_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, individual_terms_calc)


def poison(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add('НеКит', 'Quasar Logistic', 'КитДо', 'Индивидуальные условия', 'Назад к выбору площадки')
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
    elif message.text == 'Индивидуальные условия':
        individual_terms_p(message)
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


def individual_terms_p(message):
    if commissions_rate_p["exchange_rate"] != '':
        markup = types.ReplyKeyboardMarkup(row_width=1)
        markup.add('Рассчитать', 'Изменить')
        bot.send_message(message.chat.id,
                         f'Последние заданные значения:\nКомиссия в рублях: {commissions_rate_p["comm_value"]}\nКомиссия в процентах: {commissions_rate_p["comm_percent"]}\nКурс: {commissions_rate_p["exchange_rate"]}',
                         reply_markup=markup)
        bot.register_next_step_handler(message, individual_terms_handler_p)
    else:
        bot.send_message(message.chat.id, 'Индивидуальные значение не были заданы, требуется их задать!')
        individual_terms_price_p(message)


def individual_terms_handler_p(message):
    if message.text == 'Рассчитать':
        individual_terms_price(message)
    elif message.text == 'Изменить':
        commissions_rate_p["comm_value"] = ''
        commissions_rate_p["comm_percent"] = ''
        commissions_rate_p["exchange_rate"] = ''
        bot.send_message(message.chat.id, 'Значения сброшены, требуется задать новые')
        individual_terms_price_p(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, f'Выбери из предложенных вариантов!')
        bot.register_next_step_handler(message, individual_terms_handler_p)


def individual_terms_price_p(message):
    bot.send_message(message.chat.id, f'{wording["poison"]}')
    bot.register_next_step_handler(message, commission_handler_p)


def commission_handler_p(message):
    if message.text.isdigit() and commissions_rate_p["exchange_rate"] == '':
        commissions_rate_p['price'] = f'{message.text}'
        markup = types.ReplyKeyboardMarkup(row_width=3)
        markup.add('НеКит', 'Quasar Logistic', 'КитДо', 'Собственное значение')
        bot.send_message(message.chat.id, f'{wording["commission"]}', reply_markup=markup)
        bot.register_next_step_handler(message, commission_check_p)
        print(commissions_rate_p['price'],message.text)
    elif message.text.isdigit() and commissions_rate_p["exchange_rate"] != '':
        commissions_rate_p['price'] = f'{message.text}'
        individual_terms_calc_p(message)
    else:
        bot.send_message(message.chat.id, "Введи корректное значение!")
        bot.register_next_step_handler(message, commission_handler_p)


def commission_check_p(message):
    if message.text == "Собственное значение":
        markup = types.ReplyKeyboardMarkup(row_width=1)
        markup.add('В рублях', 'В процентах')
        bot.send_message(message.chat.id, f'{wording["commission_choose"]}', reply_markup=markup)
        bot.register_next_step_handler(message, commission_format_p)
    elif message.text == 'НеКит':
        commission_value(message)
    elif message.text == 'КитДо':
        commission_value(message)
    elif message.text == 'Quasar Logistic':
        commission_value(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, f'Выбери из предложенных вариантов!')
        bot.register_next_step_handler(message, commission_check_p)


def commission_format_p(message):
    if message.text == 'В рублях':
        bot.send_message(message.chat.id, f'{wording["commission_rub"]}')
        bot.register_next_step_handler(message, commission_value_p)
    elif message.text == 'В процентах':
        bot.send_message(message.chat.id, f'{wording["commission_percent"]}')
        bot.register_next_step_handler(message, commission_value_p)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, f'Выбери из предложенных вариантов')
        bot.register_next_step_handler(message, commission_format_p)


def commission_value_p(message):
    if message.text[-1].isdigit() and message.text[-1] != "%":
        commissions_rate_p['comm_value'] = f'{message.text}'
        commissions_rate_p['comm_percent'] = '0'
        bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
        bot.register_next_step_handler(message, comm_exchange_rates_p)
    elif message.text[-1] == '%':
        bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
        commissions_rate_p['comm_percent'] = f'{message.text[:-1]}'
        commissions_rate_p['comm_value'] = '0'
        bot.register_next_step_handler(message, comm_exchange_rates_p)
    elif message.text == 'НеКит':
        bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
        commissions_rate_p['comm_percent'] = '0'
        commissions_rate_p['comm_value'] = '0'
        bot.register_next_step_handler(message, comm_exchange_rates_p)
    elif message.text == 'КитДо':
        if float(commissions_rate['price']) < 5000:
            commissions_rate_p['comm_value'] = f'{1500 / CNY}'
            commissions_rate_p['comm_percent'] = '0'
            bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
            bot.register_next_step_handler(message, comm_exchange_rates_p)
        else:
            commissions_rate_p['comm_value'] = '0'
            commissions_rate_p['comm_percent'] = '6'
            bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
            bot.register_next_step_handler(message, comm_exchange_rates_p)
    elif message.text == 'Quasar Logistic':
        commissions_rate_p['comm_percent'] = '0'
        commissions_rate_p['comm_value'] = '0'
        bot.send_message(message.chat.id, f'{wording["exchange_rate"]}')
        bot.register_next_step_handler(message, comm_exchange_rates_p)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, f'Неверный формат ввода!')
        bot.register_next_step_handler(message, commission_value_p)
    print(commissions_rate_p)


def comm_exchange_rates_p(message):
    if message.text.split(".")[0].isdigit() and message.text.split(".")[1].isdigit():
        if message.text[2] == '.' or message.text[3] == '.':
            commissions_rate_p['exchange_rate'] = f'{message.text}'
            individual_terms_calc_p(message)
    elif message.text == 'ЦБ':
        commissions_rate_p['exchange_rate'] = f'{CNY}'
        individual_terms_calc_p(message)
    elif message.text == '/start':
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, f'Неверный формат ввода!')
        bot.register_next_step_handler(message, comm_exchange_rates_p)
    print(commissions_rate_p)


def individual_terms_calc_p(message):
    price = copy.deepcopy(message)
    price.text = f'{commissions_rate_p["price"]}'
    print(price.text)
    if nice_backandchange(message):
        nice_handler(message)
    else:
        markup = types.ReplyKeyboardMarkup(row_width=3)
        markup.add('НеКит', 'Quasar Logistic', 'КитДо', 'Индивидуальные условия', 'Назад к выбору площадки')
        if f'{price.text}'.isdigit():
            bot.send_message(price.chat.id,
                             f'Сумма выплаты {round(individual_calculation_poison(price.text), 2)}¥ = {round(individual_calculation_poison(price.text) * float(commissions_rate_p["exchange_rate"]), 2)} руб. по заданному курсу, {wording["retryandback"]}',
                             reply_markup=markup)
            bot.register_next_step_handler(message, poison_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, individual_terms_calc_p)


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
        if len(message.text.split(",")) == 2:
            bot.send_message(message.chat.id,
                             f'{china_bestoffer_calculation(message)}, {wording["retryandback"]}')
            bot.register_next_step_handler(message, bestoffer_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Неверный формат ввода!')
            bot.register_next_step_handler(message, china_bestoffer_calc)


def all_bestoffer(message):
    bot.send_message(message.chat.id, f'{wording["all"]}')
    bot.register_next_step_handler(message, all_bestoffer_calc)


def all_bestoffer_calc(message):
    if bestoffer_backandchange(message):
        bestoffer_handler(message)
    else:
        if len(message.text.split(",")) == 3:
            bot.send_message(message.chat.id, f'{all_bestoffer_calculation(message)}, {wording["retryandback"]}')
            bot.register_next_step_handler(message, bestoffer_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Неверный формат ввода!')
            bot.register_next_step_handler(message, all_bestoffer_calc)


def stockx_backandchange(message):
    if message.text == 'Алексей Уваров(Affliction#6369)' or message.text == 'kikoX' or message.text == 'КитДо USA' or message.text == 'Назад к выбору площадки':
        return True


def nice_backandchange(message):
    if message.text == 'НеКит' or message.text == 'Quasar Logistic' or message.text == 'КитДо' or message.text == 'Индивидуальные условия' or message.text == 'Назад к выбору площадки':
        return True


def poison_backandchange(message):
    if message.text == 'НеКит' or message.text == 'Quasar Logistic' or message.text == 'КитДо' or message.text == 'Назад к выбору площадки':
        return True


def bestoffer_backandchange(message):
    if message.text == 'StockX' or message.text == 'Китай' or message.text == 'На всех площадках' or message.text == 'Назад к выбору площадки':
        return True


bot.infinity_polling(True)
