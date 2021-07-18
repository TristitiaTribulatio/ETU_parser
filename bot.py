from mirea_parser import Parser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

API_TOKEN = ""
updater = Updater(token=API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def welcome(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text='''
Привет, этот бот может отобразить ваше место в списке абитуриентов!
Просто введите /rate и ваш номер СНИЛСа в формате 123-456-789-00
''')

def rate(update, context):
    try:
        info = Parser(update.message.text).info['info']
        basic_info = list(info.values())[0]
        marks = basic_info[4].split()
        context.bot.send_message(chat_id=update.effective_chat.id,
        text=f'''
Оценки:
    * Физика или Информатика — {marks[0]}
    * Математика — {marks[1]}
    * Русский язык — {marks[2]}
Сумма баллов за ВИ:  {basic_info[5]}
Балл за ИД:  {basic_info[6]}
Сумма баллов:  {basic_info[7]}
Потребность в общежитии:  {basic_info[3]}
        ''')
        for competetion, info in info.items():
            context.bot.send_message(chat_id=update.effective_chat.id,
            text=f'''
{competetion}

Номер в списке:  {info[0]}
Согласие на зачисление:  {info[2]}
Согласий выше:  {info[9]}
            ''')
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id, text='К сожалению вас не оказалось в списках!')

def init():
    dispatcher.add_handler(CommandHandler('start', welcome))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'(\d{3}-){3}\d{2}'), rate))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    init()