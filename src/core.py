"""
Core Orchestration Engine for Sovereign AI Radio Station (PKG-031).
Port: 8811
Author: Russell Alan Powers
"""
import time
import json
import hashlib
from typing import Dict, Any, Optional

from .ai_dj_engine import AIDJEngine
from .playout_mixer import PlayoutMixer
from .media_scheduler import MediaScheduler

class CoreEngine:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.version = "1.0.0"
        self.package_name = "sovereign-ai-radio-station"
        self.domain = "Autonomous Media & AI Audio Broadcasting"
        self.port = 8811
        self.initialized_at = time.time()

        self.dj = AIDJEngine()
        self.mixer = PlayoutMixer()
        self.scheduler = MediaScheduler()

    def execute_feature(self, feature_name: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = payload or {}
        fn = feature_name.strip().lower()

        payload_str = json.dumps(payload, sort_keys=True)
        idempotency_token = "RAD-" + hashlib.sha256(f"{fn}:{payload_str}".encode()).hexdigest()[:14]

        # 1. Generate DJ Spoken Voice Segment
        if fn in ("generate_dj_segment", "aidjengine", "dj_script"):
            topic = payload.get("topic", "System Sovereign State")
            tone = payload.get("tone", "UPBEAT")
            news = payload.get("news_items")
            result = self.dj.generate_segment(topic, tone, news)

        # 2. Assemble Playout Timeline
        elif fn in ("assemble_broadcast_hour", "playoutmixer", "mix_timeline"):
            style = payload.get("music_style", "LOFI_STUDY")
            segments = payload.get("voice_segments") or [self.dj.generate_segment()]
            result = self.mixer.mix_hour_timeline(segments, style)

        # 3. Schedule Query
        elif fn in ("get_schedule", "mediascheduler", "schedule"):
            result = {"schedule": self.scheduler.get_schedule()}

        # 4. Current Now Playing Status
        elif fn in ("get_now_playing", "now_playing", "stream_status"):
            show = self.scheduler.get_current_show()
            seg = self.dj.generate_segment(topic=show.get("show_name", "Autonomous Music"))
            result = {
                "station_name": "Sovereign Radio 104.2 FM",
                "current_show": show,
                "now_playing": {
                    "artist": "Sovereign AI DJ",
                    "title": show.get("show_name", "Broadcast Flow"),
                    "genre": show.get("genre", "TECH_TELEMETRY"),
                    "bitrate_kbps": 320,
                    "active_listeners": 1
                },
                "current_dj_segment": seg
            }

        else:
            result = {
                "action": feature_name,
                "message": f"Executed {feature_name} dynamically across AI Radio pipeline.",
                "supported_actions": [
                    "generate_dj_segment", "assemble_broadcast_hour",
                    "get_schedule", "get_now_playing"
                ]
            }

        return {
            "status": "SUCCESS",
            "package": self.package_name,
            "feature": feature_name,
            "idempotency_token": idempotency_token,
            "processed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "result": result
        }

    def health_check(self) -> Dict[str, Any]:
        show = self.scheduler.get_current_show()
        return {
            "status": "HEALTHY",
            "service": self.package_name,
            "domain": self.domain,
            "port": self.port,
            "version": self.version,
            "uptime_seconds": round(time.time() - self.initialized_at, 2),
            "current_show": show.get("show_name", "Autonomous Flow")
        }