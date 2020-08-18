from wording import *
from calculations import *
import telebot

def commission_handler(message):
    if message.text.isdigit():
        commissions_rate['price'] = f'{message.text}'
        markup = types.ReplyKeyboardMarkup(row_width=3)
        markup.add('НеКит', 'Quasar Logistic', 'КитДо','Собственное значение')
        bot.send_message(message.chat.id, f'{wording["commission"]}',reply_markup=markup)
        bot.register_next_step_handler(message, commission_check)
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
def commission_value(message):
    if message.text[-1] == '₽':
        commissions_rate['comm_value'] = f'{message.text[:-1]}'
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
            commissions_rate['comm_value'] = f'{1500/CNY}'
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
                             f'Сумма выплаты {round(individual_calculation_nice(price.text),2)}¥ = {round(individual_calculation_nice(price.text) * float(commissions_rate["exchange_rate"]), 2)} руб. по заданному курсу, {wording["retryandback"]}',reply_markup=markup)
            bot.register_next_step_handler(message, nice_handler)
        elif message.text == '/start':
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, f'Введи корректное значение!')
            bot.register_next_step_handler(message, individual_terms_calc)