import threading
import webbrowser
import time
import sys
import os
import uvicorn
import uuid
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse

# ── Path helper (works both as .py and .exe) ──────────────────
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "index.html")

# ── FastAPI app ────────────────────────────────────────────────
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/info")
async def get_info(url: str):
    import yt_dlp
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": "in_playlist"
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if "entries" in info:
                tracks = [
                    {"title": e.get("title", "Unknown"), "id": e.get("id")}
                    for e in info["entries"] if e
                ]
                return {
                    "type": "playlist",
                    "title": info.get("title"),
                    "tracks": tracks
                }
            else:
                return {
                    "type": "video",
                    "title": info.get("title"),
                    "id": info.get("id")
                }
    except Exception as e:
        return {"error": str(e)}


@app.get("/download")
async def download(url: str, quality: str = "192"):
    import yt_dlp
    job_id = str(uuid.uuid4())
    out_template = os.path.join(DOWNLOAD_DIR, f"{job_id}_%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "quiet": True,
        "writethumbnail": True,          # download thumbnail for cover art
        "postprocessors": [
            {
                # Step 1: Convert to MP3
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            },
            {
                # Step 2: Embed metadata (title, artist, album, year)
                "key": "FFmpegMetadata",
                "add_metadata": True,
            },
            {
                # Step 3: Embed thumbnail as cover art
                "key": "EmbedThumbnail",
            },
        ],
        # Makes cover art show correctly in Windows Media Player & phones
        "postprocessor_args": [
            "-id3v2_version", "3"
        ],
    }

    loop = asyncio.get_event_loop()

    def do_download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    await loop.run_in_executor(None, do_download)

    # Find the finished MP3 file
    for f in os.listdir(DOWNLOAD_DIR):
        if f.startswith(job_id) and f.endswith(".mp3"):
            filepath = os.path.join(DOWNLOAD_DIR, f)
            filename = f[len(job_id)+1:]
            return FileResponse(
                filepath,
                media_type="audio/mpeg",
                filename=filename
            )

    return {"error": "Download failed"}


# ── Launcher ───────────────────────────────────────────────────
def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)

def open_browser():
    time.sleep(3)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    # Hide CMD window on Windows
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0
        )

    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    open_browser()
    t.join()