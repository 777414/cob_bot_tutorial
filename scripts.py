import Bot, Dispatcher, executor, types
API_TOKEN = '6297686341:AAEdPRUcB7UgYg8PBEVxSpIe6i0KYAQ_Zik'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['stop'])
async def send_welcome(message: types.message):
   await message.reply("Для вас рассылка преостоновлена")
@dp.message_handler()
async def echo(message: types.message):
   await message.answer(message.text) 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)