import libtorrent as lt
import time
import os
from threading import Thread

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

ses = lt.session()
ses.listen_on(6881, 6891)

active_downloads = {}

def create_torrent(file_path):
    fs = lt.file_storage()
    lt.add_files(fs, file_path)
    t = lt.create_torrent(fs)
    t.set_creator("TelegramTorrentBot")
    lt.set_piece_hashes(t, os.path.dirname(file_path))
    torrent = t.generate()
    torrent_path = file_path + ".torrent"
    with open(torrent_path, "wb") as f:
        f.write(lt.bencode(torrent))
    return torrent_path

def start_download(torrent_file=None, magnet_link=None, hash_id=None, progress_callback=None):
    def run():
        params = {
            'save_path': DOWNLOAD_DIR,
            'storage_mode': lt.storage_mode_t.storage_mode_allocate,
        }
        if torrent_file:
            info = lt.torrent_info(torrent_file)
            params['ti'] = info
        elif magnet_link:
            params['url'] = magnet_link
        else:
            if progress_callback:
                progress_callback("No torrent or magnet link provided")
            return

        h = ses.add_torrent(params)
        active_downloads[hash_id] = h

        while not h.is_seed():
            s = h.status()
            progress = s.progress * 100
            state_str = ['queued', 'checking', 'downloading metadata',
                         'downloading', 'finished', 'seeding', 'allocating'][s.state]
            if progress_callback:
                progress_callback(f"State: {state_str} — Progress: {progress:.2f}%")
            time.sleep(2)

        if progress_callback:
            progress_callback("Download completed!")
        del active_downloads[hash_id]

    Thread(target=run).start()

def get_download_status(hash_id):
    h = active_downloads.get(hash_id)
    if not h:
        return "No active download with this ID."
    s = h.status()
    progress = s.progress * 100
    state_str = ['queued', 'checking', 'downloading metadata',
                 'downloading', 'finished', 'seeding', 'allocating'][s.state]
    return f"State: {state_str} — Progress: {progress:.2f}%"
