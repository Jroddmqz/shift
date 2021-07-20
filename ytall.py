import os
from os import remove
from os import path
import time
import asyncio
from pyrogram import filters
from main_startup import Friday
from youtube_dl import YoutubeDL
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, progress, humanbytes
from pyrogram.errors import RPCError

@Friday.on_message(filters.regex(pattern="^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be|m\.youtube\.com|vm\.tiktok\.com)\/.+$") & filters.incoming)
async def ytall(client, message):
    input_str = message.text
    pablo = await client.send_message(message.chat.id, f"`Processing...`")

    await pablo.edit(f"`Downloading Please Wait..`")
    url = input_str
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    size = os.stat(file_stark).st_size
    capy = f"<< **{file_stark}** [`{humanbytes(size)}`] >>"
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {file_stark}.`",
            file_stark,
        ),
    )
    await pablo.delete()
    if os.path.exists(file_stark):
        os.remove(file_stark)