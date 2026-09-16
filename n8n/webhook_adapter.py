#!/usr/bin/env python3
import os
import sys
import json
import mimetypes
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core import CoreEngine

PORT = 8811
engine = CoreEngine()

STATIC_DIR = ROOT / "src" / "static"
DATA_DIR = ROOT / "data"

AUDIO_SEARCH_DIRS = [
    DATA_DIR / "audio",
    Path("/Users/russellpowers/Sovereign Biz Box/solutions/tv-broadcast-station/data/audio"),
    Path("/Users/russellpowers/Sovereign Biz Box/solutions/storyboard-ai/backend/audio"),
    DATA_DIR
]

# Track metadata catalog (matches TV Broadcast Station & Storyboard AI)
DEFAULT_TRACKS = [
    {
        "id": "proj-yt-ep01-599-mainframe",
        "title": "Episode 1: The $599 Business Mainframe (Mac Mini + Local n8n)",
        "subtitle": "How a $599 Mac Mini eliminated $1,800/mo SaaS rent.",
        "category": "PODCAST",
        "artist": "Sovereign Biz Box Podcast",
        "duration_sec": 656.85,
        "audio_url": "/audio/proj-yt-ep01-599-mainframe_voiceover.m4a",
        "genre": "TECH_DEEP_DIVE"
    },
    {
        "id": "proj-chicago-chess-dream",
        "title": "The Sicilian Defense of Grant Park (A Chicago Dream)",
        "subtitle": "A cold autumn evening, a leather chess book, and an impossible translation.",
        "category": "PODCAST",
        "artist": "SBB Narrative Audio Studio",
        "duration_sec": 976.35,
        "audio_url": "/audio/proj-chicago-chess-dream_Untitled 2 2.m4a",
        "genre": "AUDIO_DRAMA"
    },
    {
        "id": "proj-yt-ep02-goodbye-zapier",
        "title": "Episode 2: Goodbye Zapier — 15 Beats of Automation",
        "subtitle": "Full commercial promo: Rebuilding a $250/mo stack inside local n8n in 7 mins.",
        "category": "COMMERCIAL",
        "artist": "Sovereign Station Network",
        "duration_sec": 80.25,
        "audio_url": "/audio/proj-yt-ep02-goodbye-zapier_voiceover.m4a",
        "genre": "BROADCAST_PROMO"
    },
    {
        "id": "song-project-16-master",
        "title": "Project 16 — Master Stereo Studio Stem (320kbps AAC)",
        "subtitle": "High-definition Logic Pro mastered soundtrack for Episode 1.",
        "category": "SONG",
        "artist": "Russell Alan Powers",
        "duration_sec": 656.85,
        "audio_url": "/audio/Project 16.m4a",
        "genre": "STUDIO_STEM"
    },
    {
        "id": "song-freedom-master",
        "title": "Freedom — Master Audio Mix",
        "subtitle": "Cinematic lo-fi synth build for deep architectural focus.",
        "category": "SONG",
        "artist": "Russell Alan Powers",
        "duration_sec": 656.85,
        "audio_url": "/audio/freedom.m4a",
        "genre": "CINEMATIC_SYNTH"
    },
    {
        "id": "song-project-15-theme",
        "title": "Project 15 — High-Energy Theme (80s Electronic)",
        "subtitle": "Original broadcast theme song and bumper cue.",
        "category": "SONG",
        "artist": "Russell Alan Powers",
        "duration_sec": 80.25,
        "audio_url": "/audio/Project 15.m4a",
        "genre": "CYBER_THEME"
    }
]

current_track_state = {
    "track_id": DEFAULT_TRACKS[0]["id"],
    "title": DEFAULT_TRACKS[0]["title"],
    "artist": DEFAULT_TRACKS[0]["artist"],
    "category": DEFAULT_TRACKS[0]["category"],
    "audio_url": DEFAULT_TRACKS[0]["audio_url"],
    "duration_sec": DEFAULT_TRACKS[0]["duration_sec"],
    "is_playing": True,
    "active_listeners": 12,
    "bitrate_kbps": 320
}

class RadioStationHandler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-SBB-Auth, Range")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # 1. Health Probe
        if path in ("/health", "/healthz"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(engine.health_check()).encode("utf-8"))
            return

        # 2. Web Playout Player Console UI (/ or /radio or /player)
        is_json_accept = self.headers.get("Accept", "").startswith("application/json")
        if (path in ("/", "/radio", "/player", "/radio_player.html", "/stage") and not is_json_accept):
            player_path = STATIC_DIR / "radio_player.html"
            if player_path.exists():
                with open(player_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(content)
                return

        # 3. Root API info if json requested
        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(engine.health_check()).encode("utf-8"))
            return

        # 4. GET /api/v1/radio/tracks
        if path == "/api/v1/radio/tracks":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "tracks": DEFAULT_TRACKS}).encode("utf-8"))
            return

        # 5. GET /api/v1/radio/now-playing
        if path in ("/api/v1/radio/now-playing", "/api/v1/radio/current"):
            show = engine.scheduler.get_current_show()
            res = {
                "station_name": "W-SBB Radio 104.2 FM",
                "frequency": "104.2 MHz FM",
                "current_show": show,
                "now_playing": current_track_state,
                "dsp_ducking": {
                    "enabled": True,
                    "attenuation_db": -14.0,
                    "attack_ms": 250,
                    "release_ms": 600
                }
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # 6. GET /api/v1/radio/schedule
        if path in ("/api/v1/radio/schedule", "/api/v1/schedule"):
            schedule = engine.scheduler.get_schedule()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "schedule": schedule}).encode("utf-8"))
            return

        # 7. Static Audio Serving with HTTP 206 Partial Content (Range Support)
        if path.startswith("/audio/"):
            rel_sub = urllib.parse.unquote(path.split("/", 2)[-1]).strip()
            p_rel = Path(rel_sub)
            test_names = [rel_sub, p_rel.name]

            # Cross-format alias fallbacks (.m4a <-> .mp3 <-> .aif)
            if p_rel.suffix.lower() in (".aif", ".aiff", ".aifc"):
                test_names.extend([f"{p_rel.stem}.m4a", f"{p_rel.stem}.mp3", f"{p_rel.name}.m4a", f"{p_rel.name}.mp3"])
            elif p_rel.suffix.lower() == ".m4a":
                test_names.extend([f"{p_rel.stem}.mp3", f"{p_rel.stem}.aif", f"{p_rel.name}.mp3"])
            elif p_rel.suffix.lower() == ".mp3":
                test_names.extend([f"{p_rel.stem}.m4a", f"{p_rel.stem}.aif"])

            local_candidate = None
            for sdir in AUDIO_SEARCH_DIRS:
                if not sdir.exists():
                    continue
                for tname in test_names:
                    c = sdir / tname
                    if c.exists() and c.is_file():
                        local_candidate = c
                        break
                if local_candidate:
                    break

            if local_candidate:
                mime, _ = mimetypes.guess_type(str(local_candidate))
                if str(local_candidate).endswith(".aif") or str(local_candidate).endswith(".aiff"):
                    mime = "audio/aiff"
                elif str(local_candidate).endswith(".m4a"):
                    mime = "audio/mp4"
                elif str(local_candidate).endswith(".mp3"):
                    mime = "audio/mpeg"
                mime = mime or "application/octet-stream"
                file_size = local_candidate.stat().st_size

                range_header = self.headers.get("Range")
                if range_header and range_header.startswith("bytes="):
                    try:
                        range_spec = range_header[6:].strip()
                        start_str, end_str = range_spec.split("-", 1)
                        start = int(start_str) if start_str else 0
                        end = int(end_str) if end_str else file_size - 1
                        if end >= file_size:
                            end = file_size - 1
                        length = end - start + 1

                        self.send_response(206)
                        self.send_header("Content-Type", mime)
                        self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                        self.send_header("Content-Length", str(length))
                        self.send_header("Accept-Ranges", "bytes")
                        self.send_cors_headers()
                        self.end_headers()

                        with open(local_candidate, "rb") as mf:
                            mf.seek(start)
                            bytes_remaining = length
                            while bytes_remaining > 0:
                                chunk_size = min(65536, bytes_remaining)
                                chunk = mf.read(chunk_size)
                                if not chunk:
                                    break
                                self.wfile.write(chunk)
                                bytes_remaining -= len(chunk)
                        return
                    except Exception as e:
                        print(f"[Radio Server] Error handling Range request: {e}")

                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(file_size))
                self.send_header("Accept-Ranges", "bytes")
                self.send_cors_headers()
                self.end_headers()

                with open(local_candidate, "rb") as mf:
                    while chunk := mf.read(65536):
                        self.wfile.write(chunk)
                return

        self.send_response(404)
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(b'{"error": "Not Found"}')

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        # 1. POST /api/v1/radio/generate-dj
        if path in ("/api/v1/radio/generate-dj", "/api/v1/generate-dj"):
            topic = data.get("topic", current_track_state["title"])
            daypart = data.get("daypart", "MIDDAY_SPRINT")
            news = data.get("news_items")
            seg = engine.dj.generate_segment(topic=topic, daypart=daypart, news_items=news)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(seg).encode("utf-8"))
            return

        # 2. POST /api/v1/radio/play
        if path in ("/api/v1/radio/play", "/api/v1/play"):
            track_id = data.get("track_id")
            matching = [t for t in DEFAULT_TRACKS if t["id"] == track_id]
            if matching:
                selected = matching[0]
                current_track_state.update({
                    "track_id": selected["id"],
                    "title": selected["title"],
                    "artist": selected["artist"],
                    "category": selected["category"],
                    "audio_url": selected["audio_url"],
                    "duration_sec": selected["duration_sec"],
                    "is_playing": True
                })
                try:
                    engine.scheduler.log_playout(selected["category"], selected["title"], selected["duration_sec"])
                except Exception as log_err:
                    print(f"[Radio Server] Playout log error: {log_err}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "now_playing": current_track_state}).encode("utf-8"))
            return

        # 3. Standard /api/v1/execute (n8n & Desktop App compatibility)
        if path == "/api/v1/execute":
            auth_header = self.headers.get("X-SBB-Auth")
            expected_secret = os.environ.get("SBB_SHARED_SECRET", "sbb_local_dev_secret_2026")
            if auth_header and auth_header != expected_secret:
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(b'{"error": "Unauthorized"}')
                return

            action = data.get("action", "get_now_playing")
            payload = data.get("payload", data)
            res = engine.execute_feature(action, payload)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        self.send_response(404)
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(b'{"error": "Not Found"}')

    def log_message(self, format, *args):
        pass

def run():
    server = HTTPServer(("0.0.0.0", PORT), RadioStationHandler)
    print(f"[AI Radio Station] Playout Server listening on http://0.0.0.0:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run()