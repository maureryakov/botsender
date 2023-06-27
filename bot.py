import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Устанавливаем уровень логов на DEBUG
logging.basicConfig(level=logging.DEBUG)

# Создаем объект бота
bot = Bot(token='YOUR_TOKEN')

# Создаем объект диспетчера
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Отправляем приветственное сообщение
    await message.reply("Привет! Отправь мне сообщение, и я перешлю его в личный чат.")


# Обработчик всех входящих сообщений
@dp.message_handler(content_types=types.ContentType.ANY)
async def forward_message(message: types.Message):
    # Получаем ID чата, из которого пришло сообщение
    chat_id = message.chat.id

    # Получаем ID пользователя, отправившего сообщение
    user_id = message.from_user.id

    # Формируем никнейм пользователя в виде @name
    username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name

    # Формируем текст сообщения с указанием никнейма пользователя
    text = f"{username}: {message.text}" if message.text else f"{username}"

    # Пересылаем сообщение в личный чат
    forward_message = await bot.forward_message(chat_id=YOUR_PRIVATE_CHAT_ID, from_chat_id=chat_id, message_id=message.message_id)

    # Пересылаем все файлы, фотографии, голосовые и видео в личный чат
    if forward_message.content_type != 'text':
        await bot.send_chat_action(chat_id=YOUR_PRIVATE_CHAT_ID, action='upload_document')
        await bot.send_document(chat_id=YOUR_PRIVATE_CHAT_ID, document=forward_message.document.file_id)

    # Отправляем благодарность за отправку сообщения
    await message.reply("Спасибо! Я отправил твое сообщение.")


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
