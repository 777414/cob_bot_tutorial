import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import random
from scripts import *


secrets = read_secrets()
users = read_users()
questions_data = read_questions()
TOKEN = secrets['secrets']['api_key']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_user(secrets, update.effective_chat.id):
        secrets['secrets']['chat_ids'].append(update.effective_chat.id)
        add_user(users, update.effective_chat.full_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Поздравляю вас, вы зарегистрированы!')
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Теперь вы будете получать ежедневные задания')
    elif check_user(secrets, update.effective_chat.id) and not check_user_is_malling(users, secrets, update.effective_chat.id):
        update_user_mailng(users, secrets, update.effective_chat.id, True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Вы снова будете получать задания')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_user(secrets, update.effective_chat.id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не зарегистрированы, команда для регистрации /start')
    elif check_user(secrets, update.effective_chat.id) and check_user_is_malling(users, secrets, update.effective_chat.id):
        update_user_mailng(users, secrets, update.effective_chat.id, False)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Рассылка заданий приостановлена')

async def leaders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    df_leaders = get_leaders(users)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=df_leaders[['user_name', 'rating']].to_string(index=False))

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.id, text='Такой команды я не знаю')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mes_text = query.message.text
    await query.edit_message_text(text=mes_text)
    result_text = 'Правильно!' if query.data == '1' else 'Неправильно!'
    if query.data == '1':
        update_user_score(users, secrets, query.message.chat_id)
    await context.bot.send_message(chat_id=query.message.chat_id, text=result_text, reply_to_message_id=query.message.id)

async def callback_everyday(context: ContextTypes.DEFAULT_TYPE):
    question = get_random_question(questions_data)
    text = question['q_text']
    keyboard = []
    for answer in question['q_answers']:
        keyboard.append([InlineKeyboardButton(answer, callback_data='0')])
    keyboard.append([InlineKeyboardButton(question['correct_answer'], callback_data='1')])
    random.shuffle(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)
    users = secrets['secrets']['chat_ids']
    for user in users:
        await context.bot.send_message(chat_id=user, text=text, reply_markup=reply_markup)

async def callback_five_minute(context: ContextTypes.DEFAULT_TYPE):
    save_users(users)
    save_secrets(secrets)

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    job = application.job_queue
    job_minute = job.run_repeating(callback_five_minute, interval=300)
    job_everyday = job.run_repeating(callback_everyday, interval=43200)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(CommandHandler('leaders', leaders))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT or (~filters.COMMAND), echo))
    application.run_polling()
