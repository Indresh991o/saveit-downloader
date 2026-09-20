"""
SaveIt backend — extracts a direct download URL for a given social link
using yt-dlp. Supports instagram, pinterest, youtube, facebook.

Run locally:
    pip install -r requirements.txt
    python app.py

Deploy this on a server with real internet access (this sandbox has none).
yt-dlp needs to be kept updated regularly — these platforms change their
internal structure often and old yt-dlp versions stop working.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # allow the frontend (possibly on a different domain) to call this API

ALLOWED_PLATFORMS = {
    "instagram": ["instagram.com"],
    "pinterest": ["pinterest.com", "pin.it"],
    "youtube": ["youtube.com", "youtu.be"],
    "facebook": ["facebook.com", "fb.watch"],
}


def detect_platform(url: str):
    for platform, domains in ALLOWED_PLATFORMS.items():
        if any(domain in url for domain in domains):
            return platform
    return None


def format_duration(seconds):
    if not seconds:
        return None
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes}:{secs:02d}"


@app.route("/api/download", methods=["POST"])
def download():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    claimed_platform = data.get("platform")

    if not url:
        return jsonify(success=False, error="Link missing hai."), 400

    detected = detect_platform(url)
    if not detected:
        return jsonify(
            success=False,
            error="Ye link kisi supported platform ka nahi lag raha (Instagram/Pinterest/YouTube/Facebook).",
        ), 400

    if claimed_platform and claimed_platform != detected:
        return jsonify(
            success=False,
            error=f"Ye link {detected} ka hai, {claimed_platform} section me paste na kare.",
        ), 400

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best",
        "noplaylist": True,
        "skip_download": True,  # we only want metadata + direct URL, not to save server-side
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        return jsonify(
            success=False,
            error="Video fetch nahi ho paya. Link public hai ya nahi check karo, ya link expire ho gaya ho sakta hai.",
        ), 422
    except Exception:
        return jsonify(success=False, error="Server error, thodi der baad try karo."), 500

    direct_url = info.get("url")
    if not direct_url and info.get("formats"):
        # fall back to the best available format
        direct_url = info["formats"][-1].get("url")

    if not direct_url:
        return jsonify(success=False, error="Download link nahi mila is post ke liye."), 422

    return jsonify(
        success=True,
        platform=detected,
        title=info.get("title"),
        author=info.get("uploader") or info.get("channel"),
        thumbnail=info.get("thumbnail"),
        duration=format_duration(info.get("duration")),
        download_url=direct_url,
    )


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
