import logging
import telegram
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
import random

TOKEN = '6297686341:AAEdPRUcB7UgYg8PBEVxSpIe6i0KYAQ_Zik'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)

async def stop(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Для вас рассылка преостоновлена')
def send_welcome(message):
  a = 0
  while True:
    print(a)
    a = a + 1
    (1)

async def echo(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Не понимаю')

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(MessageHandler(filters.TEXT or (~filters.COMMAND), echo))
    application.run_polling()
     

