import os
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import (generate_hash, save_file_record, get_last_file_by_user,
                   save_torrent_record, get_torrent_record)
from torrent_engine import create_torrent, start_download, get_download_status
import asyncio
import threading
from streamer import run_flask

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
FILE_CHANNEL = int(os.getenv("LOG_CHANNEL"))  # file channel to forward files

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    await message.reply(
        "👋 Welcome to TorrentBot!\n\n"
        "📤 Upload any file and I will forward it to the file channel and create a torrent for you.\n"
        "Commands:\n"
        "/maketorrent - Create torrent for last uploaded file\n"
        "/download - Send me a .torrent file or magnet link to start downloading\n"
        "/status - Check your active downloads\n"
        "/directlink <hash> - Get direct download link for a file\n"
    )

@app.on_message(filters.private & filters.document)
async def handle_file_upload(client, message: Message):
    await message.reply("📤 Upload received! Forwarding your file to the storage channel...")
    forwarded = await message.forward(FILE_CHANNEL)
    hash_id = generate_hash()
    file_name = message.document.file_name or "file"
    save_file_record(message.from_user.id, hash_id, FILE_CHANNEL, forwarded.message_id, file_name)
    await message.reply(f"✅ File forwarded to storage channel.\nUse /maketorrent to create a torrent file.")

@app.on_message(filters.command("maketorrent") & filters.private)
async def make_torrent_cmd(client, message: Message):
    record = get_last_file_by_user(message.from_user.id)
    if not record:
        await message.reply("⚠️ You have no files uploaded yet. Please upload a file first.")
        return

    await message.reply("⏳ Creating torrent file. This may take a moment...")
    # Download file from telegram channel
    file_path = f"{os.getenv('DOWNLOAD_DIR', 'downloads')}/{record['file_name']}"
    if not os.path.exists(os.getenv('DOWNLOAD_DIR', 'downloads')):
        os.makedirs(os.getenv('DOWNLOAD_DIR', 'downloads'))

    # Download file using pyrogram Client
    await app.download_media(await app.get_messages(record["chat_id"], record["message_id"]), file_path)

    torrent_path = create_torrent(file_path)
    await message.reply_document(torrent_path, caption="🎉 Here is your torrent file!")

@app.on_message(filters.command("download") & filters.private)
async def download_cmd(client, message: Message):
    if not message.reply_to_message:
        await message.reply("⚠️ Please reply to a .torrent file or send a magnet link with this command.")
        return

    # Handle torrent file or magnet link
    if message.reply_to_message.document and message.reply_to_message.document.file_name.endswith(".torrent"):
        await message.reply("⏳ Download starting from torrent file...")
        torrent_file = await message.reply_to_message.download()
        hash_id = generate_hash()
        save_torrent_record(message.from_user.id, hash_id, {"type": "torrent", "path": torrent_file})
        def progress_cb(text): asyncio.run_coroutine_threadsafe(message.reply(text), app.loop)
        threading.Thread(target=start_download, args=(torrent_file, None, hash_id, progress_cb)).start()
        await message.reply(f"✅ Download started with ID: {hash_id}")

    elif message.reply_to_message.text and message.reply_to_message.text.startswith("magnet:"):
        magnet_link = message.reply_to_message.text.strip()
        await message.reply("⏳ Download starting from magnet link...")
        hash_id = generate_hash()
        save_torrent_record(message.from_user.id, hash_id, {"type": "magnet", "link": magnet_link})
        def progress_cb(text): asyncio.run_coroutine_threadsafe(message.reply(text), app.loop)
        threading.Thread(target=start_download, args=(None, magnet_link, hash_id, progress_cb)).start()
        await message.reply(f"✅ Download started with ID: {hash_id}")
    else:
        await message.reply("⚠️ Please reply to a valid .torrent file or magnet link.")

@app.on_message(filters.command("status") & filters.private)
async def status_cmd(client, message: Message):
    # List active downloads for this user
    

@app.on_message(filters.command("directlink") & filters.private)
async def directlink_cmd(client, message: Message):
    args = message.text.split()
    if len(args) != 2:
        await message.reply("⚠️ Usage: /directlink <hash>")
        return
    hash_id = args[1]
    record = get_file_record(hash_id)
    if not record:
        await message.reply("⚠️ Invalid file hash.")
        return

    link = f"{os.getenv('HOST')}/{hash_id}"
    await message.reply(f"🔗 Here is your direct download link:\n{link}")

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_flask).start()
    app.run()
