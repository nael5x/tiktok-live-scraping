# 🚀 Nexus Engine: TikTok Live Scraper

**Nexus Engine** is a specialized automation tool designed to scrape real-time data from TikTok Live streams. Built with **FastAPI** and **Selenium**, it allows users to search for live streamers across various categories or specific keywords and archives the results automatically.

---

## 🌟 Key Features

* **Multi-Category Scraping:** Supports searching by "General," "Gaming," "Chat," or custom user-defined keywords.
* **Automated Keyword Queue:** Efficiently processes one keyword and automatically transitions to the next once completed.
* **Live Web Dashboard:** A web-based interface to control the bot and monitor progress in real-time.
* **Smart Data Archiving:** Automatically organizes scraped data into timestamped directories (e.g., `Scraper/Date/Time/Results.txt`).
* **Asynchronous Backend:** Powered by `FastAPI` and `Asyncio` to ensure the server remains responsive during heavy scraping tasks.
* **Windows Optimized:** Configured with specific event loop policies to maintain stability on Windows environments.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Backend Framework:** FastAPI
* **Automation Tool:** Selenium WebDriver
* **Server:** Uvicorn
* **Frontend:** HTML/JS (CORS enabled for seamless communication)

## 📂 Project Structure

* `main.py`: The API entry point. Manages the server, bot status, and command routing.
* `scraper.py`: The core scraping logic utilizing Selenium for data extraction.
* `index.html`: The web interface for interacting with the Nexus Engine.
* `TikTokLiveBot/Scraper/`: The primary output directory for all collected data.


## ⚙️ Getting Started

### 1. Installation
Install the required Python libraries:
```bash
pip install fastapi uvicorn selenium webdriver-manager
```

Developed by: nael5x
