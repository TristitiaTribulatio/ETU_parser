from config import API_TOKEN
from ETU_parser import get_pages
from re import match
from telebot import TeleBot, types

bot = TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def add_button(message):
    bot.send_message(message.chat.id,
                     text=
                     """
Привет, этот бот может отобразить ваше место в списке абитуриентов ЛЭТИ!
Поиск производится по спискам очной формы обучения и источником финансирования — бюджет
Введите ваш номер СНИЛСа в формате 123-456-789 00
                     """
                     )

@bot.message_handler(content_types='text')
def rate_reply(message):
    if match(r'\d{3}-\d{3}-\d{3} \d{2}', message.text):
        mess = [
                f"{info.speciality}\nСогласий выше: {info.count_agreements}\n\n"
                for info in get_pages(message.text)
                if type(info.count_agreements) == int
               ]
        if mess: bot.send_message(message.chat.id, "".join([line for line in mess]))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton(message.text)
        markup.add(item)
        bot.send_message(message.chat.id, "Если вашей специальности нет в списке, то это значит, что вас нет в этом списке", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Формат введённых данных некорректен (Пример: 123-456-789 00)")

bot.infinity_polling()