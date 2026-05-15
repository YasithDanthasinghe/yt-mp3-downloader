import os
import re
import uuid
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import yt_dlp

app = FastAPI()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def get_html():
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=get_html())


@app.get("/info")
async def get_info(url: str):
    ydl_opts = {"quiet": True, "skip_download": True, "extract_flat": "in_playlist"}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if "entries" in info:
                tracks = [
                    {"title": e.get("title", "Unknown"), "id": e.get("id")}
                    for e in info["entries"] if e
                ]
                return {"type": "playlist", "title": info.get("title"), "tracks": tracks}
            else:
                return {"type": "video", "title": info.get("title"), "id": info.get("id")}
    except Exception as e:
        return {"error": str(e)}


@app.get("/download")
async def download(url: str, quality: str = "192"):
    job_id = str(uuid.uuid4())
    out_template = os.path.join(DOWNLOAD_DIR, f"{job_id}_%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": quality,
        }],
    }

    loop = asyncio.get_event_loop()

    def do_download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    await loop.run_in_executor(None, do_download)

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