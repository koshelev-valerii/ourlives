from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler
import asyncio
import os

# Настройки
BOT_TOKEN = os.getenv("BOT_TOKEN", "8022352224:AAHU4ZlNvSnpJ2AzVVDeSp0gH8PPnarETP0")
CHANNEL_URL = "https://t.me/+r7HwMfNFsSUxNDVi"
CHANNEL_ID = -1002878246565  # ID канала с уроками

async def new_member(update: Update, context):
    """Приветствие новых участников"""
    for user in update.message.new_chat_members:
        keyboard = [
            [InlineKeyboardButton("📚 Подписаться на канал с уроками", url=CHANNEL_URL)],
            [InlineKeyboardButton("✅ Я подписался", callback_data="check_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"Привет! Рады видеть тебя в чате 🧡\n\n"
            f"Это пространство для общения, обмена опытом и поддержки. "
            f"А все уроки и материалы интенсива живут в канале «Уроки и материалы».\n\n"
            f"Подпишись, чтобы открыть доступ к записям и файлам 🎬✨",
            reply_markup=reply_markup
        )

async def check_subscription(update: Update, context):
    """Проверка подписки на канал"""
    query = update.callback_query
    user_id = query.from_user.id
    
    try:
        # Проверяем статус пользователя в канале
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        
        if member.status in ['member', 'administrator', 'creator']:
            # Подписан — удаляем сообщение
            await query.answer("Спасибо! Сообщение удалится через 5 секунд ⏳")
            await asyncio.sleep(5)
            await query.message.delete()
        else:
            # Не подписан — меняем текст
            await query.answer("Подпишись на канал, чтобы продолжить 😊", show_alert=True)
            
            keyboard = [
                [InlineKeyboardButton("📚 Подписаться на канал с уроками", url=CHANNEL_URL)],
                [InlineKeyboardButton("✅ Я подписался", callback_data="check_sub")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.edit_text(
                "Кажется, ты ещё не подписался на канал 😊\n\n"
                "Подписка открывает доступ к урокам и материалам — "
                "они реально помогут тебе создавать классные видео 🎬\n\n"
                "Подпишись и возвращайся! 🧡",
                reply_markup=reply_markup
            )
    except Exception as e:
        await query.answer("Ошибка проверки. Попробуй ещё раз.", show_alert=True)
        print(f"❌ Ошибка проверки подписки: {e}")

# Запуск бота
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
app.add_handler(CallbackQueryHandler(check_subscription))

print("🤖 Бот запущен!")
app.run_polling()
```

## requirements.txt
```
python-telegram-bot==20.7
