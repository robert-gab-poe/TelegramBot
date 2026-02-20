import os
import sys
import glob
import signal
import shutil
import asyncio
import subprocess
from dotenv import load_dotenv
from colorama import init, Fore
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

def clean_env_for_ytdlp():
    env = os.environ.copy()

    # 1) Quitar variables típicas de PM2/Node IPC
    for k in list(env.keys()):
        if k.startswith("PM2_") or k.startswith("NODE_"):
            env.pop(k, None)

    # 2) Quitar opciones raras de Node (si existieran)
    env.pop("NODE_OPTIONS", None)

    # 3) Quitar deno del PATH (evita que yt-dlp lo intente)
    path = env.get("PATH", "")
    path = path.replace("/home/ubuntu/.deno/bin:", "")
    path = path.replace("/home/ubuntu/.deno/bin", "")
    env["PATH"] = path

    return env

load_dotenv()

current_process = None

init(autoreset=True)

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("Token not found in environment variables")



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
COOKIES_PATH = os.path.join(BASE_DIR, "cookies.txt")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def run_command_blocking(cmd):
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=clean_env_for_ytdlp()
    )
    out, err = p.communicate()
    return p.returncode, out, err

async def descargar_y_enviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "youtube.com" in url or "youtu.be" in url:
        pass
    else:
        await update.message.reply_text("Link not recognized.")
        return

    msg = await update.message.reply_text("Whait wile downloading...")

    try:
        comando = [
            "python3", "-m", "yt_dlp",
            "--cookies", COOKIES_PATH,
            "--js-runtimes", "node",
            "--extractor-args", "youtube:player-client=web,web_safari",

            "-f", "bestaudio/best",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "192K",

            "--write-thumbnail",
            "--convert-thumbnails", "jpg",
            "--add-metadata",
            "--embed-thumbnail",
            "--embed-metadata",

            # Limpiar título
            "--replace-in-metadata", "title", "(?i)\\(official video\\)", "",
            "--replace-in-metadata", "title", "(?i)\\(lyrics?\\)", "",
            "--replace-in-metadata", "title", "(?i)\\[4k\\]", "",
            "--replace-in-metadata", "title", "(?i)video oficial", "",

            # Output: mismo "basename" para mp3 y jpg
            "-o", os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),

            url
        ]

        # ejecutar sin bloquear el event loop
        returncode, stdout, stderr = await asyncio.to_thread(run_command_blocking, comando)

        if returncode != 0:
            print(stderr)
            await update.message.reply_text("Download error.")
            await msg.delete()
            return

        archivos = glob.glob(os.path.join(DOWNLOAD_DIR, "*.mp3"))
        if not archivos:
            await update.message.reply_text("MP3 not found.")
            await msg.delete()
            return

        archivo = max(archivos, key=os.path.getctime)
        base = os.path.splitext(archivo)[0]

        # Busca thumbnail (preferimos jpg)
        thumb = None
        for ext in ("jpg", "jpeg", "png", "webp"):
            cand = f"{base}.{ext}"
            if os.path.exists(cand):
                thumb = cand
                break

        titulo = os.path.splitext(os.path.basename(archivo))[0]

        with open(archivo, "rb") as audio_file:
            if thumb:
                with open(thumb, "rb") as thumb_file:
                    await update.message.reply_audio(
                        audio=audio_file,
                        title=titulo,
                        filename=f"{titulo}.mp3",
                        thumbnail=thumb_file,   # ✅ ESTO fuerza la imagen en Telegram (si el cliente lo soporta)
                    )
            else:
                await update.message.reply_audio(
                    audio=audio_file,
                    title=titulo,
                    filename=f"{titulo}.mp3",
                )

        # limpia
        for f in archivos:
            os.remove(f)

        await msg.delete()

    except Exception as e:
        await update.message.reply_text(f"Internal error: {str(e)}")
        try:
            await msg.delete()
        except:
            pass


async def descargar_archivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    filename = "audio_recibido.mp3"

    # detect audio normal
    if update.message.audio:
        file = await update.message.audio.get_file()
        filename = update.message.audio.file_name or filename

    # detect document tipo mp3
    elif update.message.document:
        if update.message.document.mime_type.startswith("audio"):
            file = await update.message.document.get_file()
            filename = update.message.document.file_name or filename

    # detect voice notes (ogg)
    elif update.message.voice:
        file = await update.message.voice.get_file()
        filename = update.message.voice.file_name or "nota_voz.ogg"

    if file:
        path = os.path.join(DOWNLOAD_DIR, filename)
        await file.download_to_drive(path)
        await update.message.reply_text(f"File downloaded: {filename}")
    else:
        await update.message.reply_text("Not a valid audio file.")

async def stop_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_process
    if current_process:
        current_process.terminate()
        await update.message.reply_text("Download canceled.")
        current_process = None
    else:
        await update.message.reply_text("No download in progress.")

def handle_sigint(sig, frame):
    print("\n" + "\n" + "\n" + "\n" + Fore.MAGENTA + "(⸝⸝> ᴗ•⸝⸝)" + "\n")
    sys.exit(0)

if __name__ == '__main__':
    # print("--- Bot encendido ---")
    print("\n" + Fore.CYAN + " ∧,,,,,,∧  " + Fore.YELLOW + " ~ ┏━━━━━━━━━┓")
    print(Fore.CYAN + "(  ̳• · • ̳) " + Fore.YELLOW + "    AlfredBot ")
    print(Fore.CYAN + "/        づ" + Fore.YELLOW + " ~ ┗━━━━━━━━━┛")

    app = ApplicationBuilder().token(TOKEN).build()

    # handle links
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, descargar_y_enviar))

    # handle audio files sent to bot
    app.add_handler(MessageHandler(
        filters.AUDIO | filters.Document.ALL | filters.VOICE,
        descargar_archivo
    ))

    app.add_handler(CommandHandler("stop", stop_download))

    signal.signal(signal.SIGINT, handle_sigint)
    
    print("PY:", sys.executable)
    print("CWD:", os.getcwd())
    print("PATH:", os.environ.get("PATH"))
    print("NODE which:", shutil.which("node"))
    try:
        print("NODE -v:", subprocess.check_output(["node", "-v"], text=True).strip())
    except Exception as e:
        print("NODE -v failed:", e)

    app.run_polling()
