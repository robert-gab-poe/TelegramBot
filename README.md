# 🎵 Telegram Audio Downloader Bot

This project is a Telegram bot that allows users to download audio from supported links (such as YouTube or Spotify) and receive it as an MP3 file directly in Telegram.

It also supports downloading audio files sent by users and saving them locally.

---

## 🚀 Features

* 🎧 Download audio from:

  * YouTube links
  * Spotify links (searched via YouTube)
* 🔊 Convert audio to MP3 (192 kbps)
* 🖼 Embed thumbnail and metadata
* 🧹 Clean titles automatically
* 📤 Send audio back to the user
* 📥 Download and store audio files sent to the bot
* ⛔ Cancel downloads with `/stop`

---

## 📁 Project Structure

```
.
├── downloads/        # Downloaded audio files
├── venv/             # Virtual environment
└── bot.py            # Main bot script
```

---

## ⚙️ Requirements

Make sure you have:

* Python 3.10+
* pip
* Telegram account

---

## 📦 Python dependencies

Install required libraries:

```bash
pip install python-telegram-bot yt-dlp colorama
```

---

## 🎬 Install FFmpeg (REQUIRED)

This bot requires **ffmpeg** and **ffprobe** to convert audio into MP3.

### ✅ Option 1 — Install via command (recommended)

If you have a package manager:

**Windows (winget):**

```bash
winget install ffmpeg
```

**Or using Chocolatey:**

```bash
choco install ffmpeg
```

---

### ⚠️ Option 2 — Manual installation

If the command method does not work:

1. Download FFmpeg from:
   https://www.gyan.dev/ffmpeg/builds/

2. Download the **Essentials build**

3. Extract the zip file

4. Go to the `/bin` folder and locate:

```
ffmpeg.exe
ffprobe.exe
```

5. You have two options:

#### Option A — Add to PATH (recommended)

Add this folder to your system PATH:

```
C:\path\to\ffmpeg\bin
```

#### Option B — Place inside the project

Copy these files into your project directory:

```
/bin/ffmpeg.exe
/bin/ffprobe.exe
```

And make sure your script can access them.

---

### 🔍 Verify installation

Run:

```bash
ffmpeg -version
```

If you see version info → everything is working ✅

---

## 🤖 Create Your Telegram Bot

1. Open Telegram and search for **BotFather**
2. Run:

   ```
   /start
   ```
3. Create a new bot:

   ```
   /newbot
   ```
4. Choose:

   * Bot name
   * Username (must end in `bot`)
5. Copy the **token** provided

---

## 🔑 Set Environment Variable

You must store your bot token as an environment variable.

### Windows (CMD):

```bash
set TELEGRAM_TOKEN=your_token_here
```

### Windows (PowerShell):

```powershell
$env:TELEGRAM_TOKEN="your_token_here"
```

---

## 🍪 Export YouTube Cookies

This is required for some videos (age-restricted, private, etc.)

### Steps:

1. Install a browser extension:

   * "Get cookies.txt" (Chrome/Firefox)

2. Go to:
   https://www.youtube.com/

3. Make sure you are logged in

4. Export cookies as `cookies.txt`

5. Place the file in the project root:

```
.
├── bot.py
├── cookies.txt   ✅
```

---

## ▶️ Run the Bot

Activate your virtual environment:

```bash
venv\Scripts\activate
```

Run the bot:

```bash
python bot.py
```

---

## 💬 How to Use the Bot

1. Open your bot in Telegram
2. Press **Start**
3. Send:

   * A YouTube or Spotify link
4. Wait for download
5. Receive the MP3 file 🎵

---

## 📥 Sending Audio to the Bot

You can also send:

* Audio files
* Voice notes
* MP3 documents

The bot will download and store them in `/downloads`.

---

## ⛔ Cancel a Download

Use the command:

```
/stop
```

This will terminate the current download process.

---

## ⚠️ Important Notes

* Only one instance of the bot can run at a time
* Downloads are stored locally (can fill disk if not cleaned)
* Spotify links are searched on YouTube (not direct download)
* FFmpeg is required for audio conversion

---

## 🛠️ Possible Improvements

* Auto-delete files after sending
* Multi-user download queue
* Progress feedback
* Docker support
* Database integration

---

## 📄 License

This project is for educational purposes.
