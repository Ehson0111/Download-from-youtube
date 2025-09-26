import yt_dlp
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = 'Token '

ydl_opts = {
    "continuedl": True,
    "retries": 10,  
    "outtmpl": "downloads/%(title)s.%(ext)s",  # Сохраняем видео в папке downloads
}

# Команда старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Отправь мне ссылку на YouTube-видео, и я загружу его для тебя."
    )

# Обработка ссылок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text
    await update.message.reply_text("🔄 Загружаю видео, пожалуйста, подождите...")
    try:
        # Загрузка видео
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            video_title = info.get("title", "video")
            video_filename = ydl.prepare_filename(info)
        
        # Отправка видео пользователю
        await update.message.reply_video(video=open(video_filename, "rb"), caption=f"✅ Видео: {video_title}")
        
        # Удаление файла после отправки
        os.remove(video_filename)
        print(f"Файл {video_filename} успешно удален.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при загрузке видео:\n{e}")

# Главная функция для запуска бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Обработчики команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()