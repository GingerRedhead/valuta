import telebot
import extensions
import config

TOKEN = config.TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    instructions = "Привет! Я - валютный конвертер бот.\n"\
                   "Чтобы узнать цену валюты, отправь мне сообщение в формате:\n"\
                   "<валюта1> <валюта2> <количество валюты1>\n\n"\
                   "Например, для перевода 10 долларов в евро, отправь:\n"\
                   "USD EUR 10\n\n"\
                   "Используй команду /values для получения списка доступных валют."
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['values'])
def handle_values(message):
    available_currencies = "Доступные валюты:\n"\
                           "USD - Доллар США\n"\
                           "EUR - Евро\n"\
                           "RUB - Российский рубль"
    bot.reply_to(message, available_currencies)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        base, quote, amount = message.text.split()
        result = extensions.CurrencyConverter.get_price(base, quote, amount)
        response = f"{amount} {base} = {result} {quote}"
        bot.reply_to(message, response)
    except ValueError:
        bot.reply_to(message, "Неправильный формат сообщения. Введите валюты и количество числами, разделенными пробелами.")
    except extensions.APIException as e:
        bot.reply_to(message, f"Ошибка: {type(e).__name__} - {str(e)}")

bot.polling()