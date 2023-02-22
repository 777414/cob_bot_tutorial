import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import random
import yaml

TOKEN = '6297686341:AAEdPRUcB7UgYg8PBEVxSpIe6i0KYAQ_Zik'
with open("secrets.yaml", "r") as stream:
    try:
        secrets = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Не понимаб')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mes_text = query.message.text
    await query.edit_message_text(text=mes_text)
    result_text = 'Правильно!' if query.data == '1' else 'Неправильно!'
    await context.bot.send_message(chat_id=query.message.chat_id, text=result_text, reply_to_message_id=query.message.id)

async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    text = 'Сколько колес у машин?'
    keyboard = [[]]
    answers = ['5', '6', '7']
    right_ans = '4'
    for wrong_ans in answers:
        keyboard[0].append(InlineKeyboardButton(wrong_ans, callback_data='0'))
    keyboard[0].append(InlineKeyboardButton(right_ans, callback_data='1'))
    random.shuffle(keyboard[0])
    reply_markup = InlineKeyboardMarkup(keyboard)
    users = secrets['secrets']['chat_ids']
    for user in users:
        await context.bot.send_message(chat_id=user, text=text, reply_markup=reply_markup)

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    job = application.job_queue
    job_minute = job.run_repeating(callback_minute, interval=30)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT or (~filters.COMMAND), echo))
    application.run_polling()