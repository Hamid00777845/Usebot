import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8358302547:AAF1UhD-TuNGozH2zOTzUC-SMg02Wal_uH0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! YouTube yoki Instagram linkini yuboring!")

async def download_video(url: str):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    def extract():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return 'video.' + info['ext'], info.get('title', 'Video')
    return await asyncio.to_thread(extract)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not any(domain in url for domain in ["youtube.com", "youtu.be", "instagram.com"]):
        return
    status_message = await update.message.reply_text("⏳ Yuklab olinmoqda...")
    try:
        file_path, title = await download_video(url)
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video, caption=f"🎬 {title}")
        if os.path.exists(file_path):
            os.remove(file_path)
        await status_message.delete()
    except Exception as e:
        print(f"Xatolik: {e}")
        await status_message.edit_text("❌ Xatolik, linkni tekshiring")

if __name__ == '__main__':
    print("✅ Bot ishlamoqda")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
