🎵 YT-MP3 Downloader

A simple, clean web app that runs on your local machine — paste a YouTube video or playlist URL and download MP3 files with full metadata and cover art embedded.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)
![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

Features

🎵 Download single YouTube videos as MP3
📋 Download full playlists at once
🖼️ Embeds cover art (thumbnail) into MP3
📝 Embeds metadata (title, artist, album, year)
🎚️ Choose audio quality: 128 / 192 / 320 kbps
🖥️ Runs in your browser — no complicated setup
💻 Can be built as a clickable `.exe` (Windows)

Preview


Requirements

Make sure these are installed on your system:

Tools Should Download 

| Python 3.10+ | https://www.python.org/downloads/ |
| ffmpeg | https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip |


Installation & Setup

1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/yt-mp3-downloader.git
cd yt-mp3-downloader
```

2. Install Python Packages

```bash
pip install -r requirements.txt
```

3. Install ffmpeg (Windows)

1. Download from 👉 https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2. Extract and rename the folder to `ffmpeg`
3. Move it to `C:\ffmpeg`
4. Add `C:\ffmpeg\bin` to your System **PATH** environment variable
5. Verify with:
```bash
ffmpeg -version
```

---

▶️ Running the App

```bash
python launcher.py
```

Your browser will automatically open at `http://127.0.0.1:8000`

---

📦 Building as a Windows .exe

1. Install PyInstaller

```bash
pip install pyinstaller
```

2. Build the executable

```bash
pyinstaller --onefile --name "YT-MP3-Downloader" launcher.py
```

3. Copy the templates folder

After building, copy the `templates` folder into the `dist` folder:

```
dist/
 ├── YT-MP3-Downloader.exe
 └── templates/
      └── index.html
```

4. Run

Double-click `YT-MP3-Downloader.exe` — browser opens automatically! 🎉

---

📁 Project Structure

```
yt-mp3-downloader/
│
├── launcher.py          ← Main app (backend + server launcher)
├── requirements.txt     ← Python dependencies
├── README.md            ← This file
├── .gitignore           ← Files to exclude from git
└── templates/
     └── index.html      ← Frontend UI
```

---

📋 How to Use

1. Paste a YouTube **video URL** or **playlist URL**
2. Click **Fetch**
3. Select audio quality (128 / 192 / 320 kbps)
4. Click **Download** on individual tracks — or **Download All** for playlists
5. MP3 files will be saved with full metadata and cover art ✅

---

⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| YouTube Downloading | yt-dlp |
| Audio Conversion | ffmpeg |
| Metadata & Cover Art | mutagen + yt-dlp EmbedThumbnail |
| Frontend | HTML + CSS + JavaScript |
| Server | Uvicorn |

---

⚠️ Disclaimer

This tool is intended for **personal use only**. Downloading YouTube content may violate [YouTube's Terms of Service](https://www.youtube.com/t/terms). Only download content you own or that is licensed for free download.

---

## 📄 License

MIT License — free to use, modify, and distribute.
