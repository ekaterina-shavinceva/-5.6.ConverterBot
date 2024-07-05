import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', ])
def repeat(message: telebot.types.Message):
    bot.reply_to(message, f'Привет, {message.chat.username}! Для вызова справки введите /help')

@bot.message_handler(commands=['help', ])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу с конвертором валют введите комманду в следующем формате: '
            '\n<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты> в нижнем регистре\n'
            'Пример: доллар рубль 3. Для просмотра достурных валют введите /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values', ])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException(f'Неверное количество параметров')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except Exception as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в валюте {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop = True)
