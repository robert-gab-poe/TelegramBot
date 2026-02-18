# 🎵 AlfredBot - Telegram MP3 Downloader

AlfredBot es un bot de Telegram diseñado para descargar audio de YouTube y Spotify directamente en formato MP3 con metadatos (título, artista y miniatura) incluidos.

## 🚀 Requisitos Previos

Antes de ejecutar el bot, necesitas instalar y configurar las siguientes herramientas:

### 1. Herramientas del Sistema
El bot utiliza motores externos para el procesamiento de audio. Debes descargar estos archivos y pegarlos en la **carpeta raíz** del proyecto:

* **FFmpeg & FFprobe**: Descarga los ejecutables de [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (busca el `ffmpeg-git-full.7z` o la versión Essentials). 
    * *Instrucción*: Extrae el contenido y copia los archivos `ffmpeg.exe` y `ffprobe.exe` de la carpeta `bin` a la raíz de este proyecto.
* **Node.js**: Necesario para resolver las firmas de YouTube. Descárgalo e instálalo desde [nodejs.org](https://nodejs.org/).

### 2. Configuración de la API de Telegram
Para que el bot funcione, necesitas un Token de acceso:
1. Habla con [@BotFather](https://t.me/botfather) en Telegram.
2. Crea un nuevo bot con `/newbot` y guarda el **API Token**.
3. (Recomendado) Crea un archivo `.env` en la raíz del proyecto y añade:
   ```env
   TELEGRAM_TOKEN=tu_token_aqui

### 3. Cookies de YouTube (Evitar Bloqueos)
YouTube suele bloquear los scripts automáticos. Para evitarlo:
1. Instala la extensión "Get cookies.txt LOCALLY" en tu navegador (Brave, Chrome o Edge).
2. Entra en YouTube, asegúrate de tener la sesión iniciada y exporta las cookies.
3. Guarda el archivo como cookies.txt en la carpeta principal del bot.

## 📦 Instalación y Puesta en Marcha
1. Clona el repositorio:
```shell
git clone [https://github.com/tu-usuario/TelgramBot.git](https://github.com/tu-usuario/TelgramBot.git)
cd TelgramBot
```
2. Configura el entorno virtual e instala dependencias:
```shell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
3. Ejecutar el bot
```shell
python bot.py
```

## 🛠️ Uso
- Envía el comando /start para recibir el saludo de bienvenida.
- El bot activará un botón de "Pegar enlace" que facilitará la interacción con tu portapapeles.
- Pega un enlace de YouTube o Spotify y el bot te devolverá el archivo MP3 procesado.

## ⚠️ Advertencia de Archivos Grandes
Los archivos ffmpeg.exe y ffprobe.exe han sido añadidos al .gitignore debido a su tamaño superior a 100MB. Es obligatorio descargarlos manualmente para que el bot pueda realizar la conversión de audio correctamente.

---
