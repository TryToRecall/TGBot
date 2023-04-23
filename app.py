import telebot

from extensions import CurrencyConverter,  APIException
from config import TOKEN


bot = telebot.TeleBot(TOKEN)

keys = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}


@bot.message_handler(commands=['help', 'start'])
def help_(message: telebot.types.Message):
    text = "Для начала работы введите запрос в следующем формате: \n <Валюту, цена которой интересует>\n " \
           "<Валюта, в которой надо узнать цену первой валюты> \n " \
           "<Кол-во валюты, по которой делаем расчёт> \n" \
           "Доступные валюты для расчёта: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = "\n".join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values_ = message.text.split()
    try:
        if len(values_) != 3:
            raise APIException('Неверное количество параметров.')

        answer = CurrencyConverter.get_price(*values_)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")

    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling(none_stop=True)
