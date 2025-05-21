# Telegram Torrent Bot

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=35&pause=1000&color=64F72E&center=true&vCenter=true&random=true&width=435&lines=Welcome+To+AJ+BOTS!" alt="Typing SVG"/>
</p>

---

## ✨ Main Features

- ✅ **Upload Files**: Automatically forward uploaded files to a designated file channel.
- ✅ **/maketorrent**: Generate a `.torrent` file from your most recent upload.
- ✅ **/download**: Start downloads by replying to a `.torrent` file or magnet link.
- ✅ **/status**: Monitor the progress of active torrent downloads.
- ✅ **/directlink**: Create a direct download link for a file using its hash.
- ✅ **MongoDB Persistence**: Store file and torrent data securely.
- ✅ **Lightweight Flask Server**: Enable direct downloads via a Flask-based server.
- ✅ **User-Friendly Messages**: Guided and clear interaction prompts.

---

## 📋 Commands

```
/start              - Display the welcome message and help menu
(Upload file)       - Forward uploaded file to the storage channel
/maketorrent        - Create a .torrent file for the last uploaded file
/download           - Reply to a .torrent file or magnet link to start downloading
/status             - View the status of your active downloads
/directlink <hash>  - Generate a direct download link for a specific file
```

---

## ⚙️ Required Environment Variables

| Variable         | Description                                      |
|------------------|--------------------------------------------------|
| `BOT_TOKEN`      | Your bot token from @BotFather                  |
| `API_ID`         | Obtained from my.telegram.org/apps              |
| `API_HASH`       | Obtained from my.telegram.org/apps              |
| `LOG_CHANNEL`    | Telegram channel ID for file storage (e.g., -100...) |
| `MONGO_URI`      | MongoDB connection string                       |
| `DB_NAME`        | Database name (e.g., `torrent_bot`)             |
| `HOST`           | Public URL of your Flask server (e.g., `https://yourapp.onrender.com`) |
| `PORT`           | Port for Flask server (default: `8080`)         |
| `DOWNLOAD_DIR`   | Local folder for storing downloads (e.g., `downloads`) |

---

## 🚀 Deployment Instructions

### Deploy to Render

1. Push your repository to GitHub.
2. Create a new **Web Service** on Render.
3. Set the environment to **Python 3.x**.
4. **Build Command**:
   ```bash
   pip3 install -r requirements.txt
   ```
5. **Start Command**:
   ```bash
   python3 main.py
   ```
6. Configure the required environment variables (`BOT_TOKEN`, `API_ID`, `API_HASH`, `LOG_CHANNEL`, `MONGO_URI`, `DB_NAME`, `HOST`, `PORT`, `DOWNLOAD_DIR`).
7. Verify that the service is running and the bot responds to commands.

### Deploy to VPS / Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/telegram-torrent-bot.git
   cd telegram-torrent-bot
   ```
2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Create a `config.env` file with the required environment variables.
4. Run the bot:
   ```bash
   python3 main.py
   ```

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by Ajmal**