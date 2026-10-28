import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatType

# Tokeningizni joylashtiring
API_TOKEN = 9212516343:AAFMh7yjswSqlGM0ihfCmS2W_LV2dlgkRWk

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Albomlarni xotirada tekshirish uchun lug'at
album_storage = {}

@dp.message(lambda message: message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP] and message.photo)
async def check_album_limit(message: types.Message):
    # Agar rasm albom (media guruh) tarkibida bo'lsa
    if message.media_group_id:
        media_id = message.media_group_id
        
        if media_id not in album_storage:
            album_storage[media_id] = []
        
        album_storage[media_id].append(message.message_id)
        
        # Telegram barcha rasmlarni yuklab olishi uchun 0.7 soniya kutamiz
        await asyncio.sleep(0.7)
        
        # Agar guruhda ushbu albomdagi rasmlar soni 2 tadan oshib ketgan bo'lsa
        if media_id in album_storage and len(album_storage[media_id]) > 2:
            try:
                # Albomdagi barcha rasmlarni guruhdan butunlay o'chirish
                for msg_id in album_storage[media_id]:
                    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
                
                # Foydalanuvchini ogohlantirish
                warn = await message.answer(f"⚠️ @{message.from_user.username} guruhda bitta xabarda 2 tadan ortiq rasm yuborish taqiqlangan!")
                
                # Ogohlantirish xabarini 5 soniyadan keyin o'chirish
                await asyncio.sleep(5)
                await bot.delete_message(chat_id=message.chat.id, message_id=warn.message_id)
                
            except Exception as e:
                print(f"Xatolik: {e}")
            finally:
                # Xotirani tozalash
                if media_id in album_storage:
                    del album_storage[media_id]

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
