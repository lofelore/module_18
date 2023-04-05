import telebot

from config import keys, TOKEN
from extensions import CustomConvertor, CustomException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_me(message: telebot.types.Message):
    text = 'Enter data separated by space: <currency_name> <conversion_name> <amount>:\n/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        user_values = message.text.split(' ')
        length_user_values = len(user_values)

        if length_user_values == 2 or length_user_values == 1:
            raise CustomException(f'Not enough params. Need 3. Got {length_user_values}')

        if length_user_values != 3:
            raise CustomException(f'Too much params. Need 3. Got {length_user_values}')

        quote, base, amount = user_values
        total_base = CustomConvertor.get_price(quote, base, amount)

    except CustomException as ex:
        bot.reply_to(message, f'User error.\n{ex}')
    except Exception as ex:
        bot.reply_to(message, f'Cannot run command\n{ex}')

    else:
        text = f'Cost {amount} {quote} in {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
