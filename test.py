import logging
import telegram
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
import random
from scripts import *

TOKEN = get_TOKEN()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)

async def start(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    res = add_user([int(chek_user(-1)[0]) + 1, check_name_user(update.effective_chat.effective_name), 0, False, False], check_chat_id(update.effective_chat.id), update.effective_chat.id)
    if res:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Поздравляю вас, вы зарегестрированы!!!')
    else:
        key = check_user_is_malling(update.effective_chat.effective_name, check_is_malling(update.effective_chat.effective_name))
        if key:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='вы вернулись!')
        else: 
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Зачем тыкать на кнопку старт, если ты уже зарегестрирован?')

async def echo(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Не понимаб')

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT or (~filters.COMMAND), echo))
    application.run_polling()










