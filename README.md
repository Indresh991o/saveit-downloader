# SaveIt — Multi-platform Downloader

Frontend: `frontend/` — plain HTML/CSS/JS, 5 pages (home + 4 platforms).
Backend: `backend/app.py` — Flask API using `yt-dlp` to extract a direct
download link for Instagram, Pinterest, YouTube, and Facebook.

## Run the backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

This starts the API at `http://localhost:5000`. It exposes:

- `POST /api/download` — body: `{ "url": "...", "platform": "instagram" }` →
  returns `{ success, title, thumbnail, duration, download_url }`
- `GET /api/health` — simple check that the server is alive

## Run the frontend

Any static host works (the files have no build step). For local testing,
from `frontend/`:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`. If you host frontend and backend on
different domains, update `API_BASE` at the top of `frontend/script.js`
to your backend's full URL.

## Before going live

1. **Keep yt-dlp updated.** Instagram/Facebook/YouTube change their internal
   structure often; run `pip install -U yt-dlp` regularly or extraction will
   silently start failing.
2. **Rate-limit the API** (e.g. Flask-Limiter) so one user can't hammer your
   server or get your server IP blocked by the source platforms.
3. **HTTPS + real domain** before applying to any ad network.
4. **Ad slots**: each page has `<div class="ad-slot">...</div>` placeholders
   in the HTML — drop your Adsterra / PropellerAds / Monetag script snippets
   there once your accounts are approved.
5. **YouTube risk**: of the four, YouTube downloading is the one most likely
   to get a domain flagged or taken down, since it directly conflicts with
   YouTube's Terms of Service. Consider hosting the YouTube page on a
   separate subdomain so a takedown notice doesn't affect the other three
   sections.
6. This sandbox has no internet access, so extraction wasn't tested live —
   test it yourself against real links after deploying to a server that has
   internet access.
