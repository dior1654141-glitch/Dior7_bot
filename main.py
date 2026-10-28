import asyncio
from aiogram import Bot, Dispatcher, executor, types

# Bot tokeningiz muvaffaqiyatli kiritildi
API_TOKEN = '9212516343:AAFmh7yjsWSqlG'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Albomlarni xotirada tekshirish uchun lug'at
album_storage = {}

@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def check_album_limit(message: types.Message):
    if message.chat.type not in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]:
        return

    # Agar rasm albom (media guruh) tarkibida bo'lsa
    if message.media_group_id:
        media_id = message.media_group_id
        
        if media_id not in album_storage:
            album_storage[media_id] = []
        
        album_storage[media_id].append(message.message_id)
        
        # Telegram rasmlarni yuklashi uchun 0.7 soniya kutamiz
        await asyncio.sleep(0.7)
        
        # Agar guruhda albomdagi rasmlar soni 2 tadan oshsa
        if media_id in album_storage and len(album_storage[media_id]) > 2:
            try:
                # Barcha rasmlarni o'chirish
                for msg_id in album_storage[media_id]:
                    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
                
                # Ogohlantirish
                warn = await message.answer(f"⚠️ @{message.from_user.username} guruhda bitta xabarda 2 tadan ortiq rasm yuborish taqiqlangan!")
                
                await asyncio.sleep(5)
                await bot.delete_message(chat_id=message.chat.id, message_id=warn.message_id)
                
            except Exception as e:
                print(f"Xatolik: {e}")
            finally:
                if media_id in album_storage:
                    del album_storage[media_id]

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
