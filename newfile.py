from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

# Replace this with your BotFather token
BOT_TOKEN = '7494957178:AAErLKc7lM2w7a0SxNl-bh4_1pZ_B09KciM'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a song name and I'll get it for you!")

async def download_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Usage: /song <song name>")
        return

    await update.message.reply_text(f"Searching for: {query}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            title = info['title']
            file_path = f"downloads/{title}.mp3"
            await update.message.reply_audio(audio=open(file_path, 'rb'), title=title)
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("song", download_song))

    print("Bot running...")
    app.run_polling()