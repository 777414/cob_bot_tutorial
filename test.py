import logging
import telegram
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
import random
import pandas as pd

df = pd.read_csv('users.csv', sep=';')
df.insert(2, "          ", "          ")
df.to_string(index=False)
TOKEN = '6297686341:AAEdPRUcB7UgYg8PBEVxSpIe6i0KYAQ_Zik'
df.sort_values(["rating"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
df_leaders = df.head(3)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)

async def leaders(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=df_leaders[['user_name', 'rating']].to_string(index=False))

async def echo(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Не понимаю')

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('leaders', leaders))
    application.add_handler(MessageHandler(filters.TEXT or (~filters.COMMAND), echo))
    application.run_polling()