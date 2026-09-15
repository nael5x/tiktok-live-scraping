# Nexus Engine

**Local TikTok Live browser automation prototype · Python / FastAPI / Playwright**

Nexus Engine provides a dashboard for an asynchronous process that reads usernames from TikTok Live search links and appends new results to local text files. It uses Playwright and playwright-stealth with a visible Chromium browser and persistent browser profile.

## Current capabilities

- General (`Genel`) and gaming (`Oyun`) keyword collections targeting Turkish-language searches; other keyword values become individual search queries.
- Repeated keyword cycles, scrolling, and a stop flag checked by the loop.
- Daily, per-keyword deduplication using previously saved usernames.
- Dashboard controls and polling of the count and active flag.
- Windows-specific asyncio event-loop configuration.

The tool collects usernames from search links. It does not record streams or read live chat.

## Stack

| Component | Purpose |
| --- | --- |
| FastAPI | Start, stop, and status HTTP endpoints |
| Uvicorn | Local ASGI server |
| Playwright | Asynchronous Chromium control |
| playwright-stealth 2.x | `Stealth().use_async(...)` integration |
| asyncio | Standard-library concurrency and timing |
| HTML / CSS / JavaScript | Standalone dashboard |

`requirements.txt` lists all four third-party packages imported by the source. `asyncio`, `sys`, `os`, `random`, and `datetime` are standard-library modules.

The [playwright-stealth documentation](https://pypi.org/project/playwright-stealth/) describes the 2.x API used here. Successful access to TikTok is not guaranteed.

## Local setup

Use Python 3.10+ and a desktop environment capable of displaying Chromium.

```bash
git clone https://github.com/nael5x/tiktok-live-scraping.git
cd tiktok-live-scraping
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` on Windows PowerShell or `source .venv/bin/activate` on macOS/Linux, then:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
python main.py
```

Open `index.html` in your browser. It calls `http://127.0.0.1:8000` directly; FastAPI does not serve the HTML file. API docs: `http://127.0.0.1:8000/docs`.

If a Windows console cannot encode the Arabic/emoji log messages, run `python -X utf8 main.py` (or set `PYTHONIOENCODING=utf-8`) without changing the application code.

## API

| Endpoint | Behavior |
| --- | --- |
| `GET /api/start?keyword=Genel&speed=100` | Starts and awaits the loop until it exits; a long-running request |
| `GET /api/stop` | Clears the shared active flag |
| `GET /api/status` | Returns `count` and `active` |

## Files and output

- `main.py`: API, shared state, and local server.
- `scraper.py`: browser loop and file writing.
- `index.html`: dashboard.
- `NexusProfile/`: persistent Chromium profile created at runtime.
- `TikTokLiveBot/Scraper/DD-MM-YYYY/<keyword>_TR.txt`: one username per line.

The count can include usernames reloaded from an existing daily file. Run from the repository root for predictable relative paths. Keep browser profiles and result files out of commits.

## Checks and status

```bash
python -m pip check
python -m compileall -q main.py scraper.py
python -c "import main, scraper; print('Imports OK')"
```

No automated test suite is committed. Syntax/import checks do not verify live TikTok behavior, which depends on page structure, login/challenge requirements, and network access.

This is a single-user local prototype with shared in-memory state, no authentication or job queue, and permissive CORS. Multiple starts are not isolated; errors are printed rather than reported as structured job states; completion/error paths do not reliably reset the active flag. Keep the default loopback binding. Concurrent jobs and production hosting require further engineering.

## Author

[nael5x](https://github.com/nael5x)
