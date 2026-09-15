"""
AIDJEngine: Spoken banter, segment transitions, and news synthesis for W-SBB Radio.
Direct implementation of Mainframe SBBMusicStationView specifications.
Author: Russell Alan Powers
"""
import time
import hashlib
from typing import Dict, Any, List, Optional

class AIDJEngine:
    STATION_CALLSIGN = "W-SBB Radio 104.2 FM"
    
    DAYPART_FORMATS = {
        "MORNING_DRIVE": {
            "name": "The Morning Mainframe Drive",
            "tone": "UPBEAT",
            "hook": "Kickstart your autonomous day. Reclaim 3 hours of manual work before your morning coffee."
        },
        "MIDDAY_BRIEF": {
            "name": "Midday Sovereign Tech Brief",
            "tone": "ANALYTICAL",
            "hook": "Live telemetry update: server nodes running cool, SaaS costs staying at zero."
        },
        "EVENING_CODE": {
            "name": "Late Night Deep Build & Lo-Fi",
            "tone": "CHILL_LOFI",
            "hook": "The monitors are glowing, the daemons are running silently. Time for pure architectural flow."
        }
    }

    TAGLINES = [
        "Broadcasting live from the Sovereign Core on 104.2 FM, zero cloud tax, total autonomy.",
        "Your private automated frequency, streaming direct from Apple Silicon bare-metal.",
        "No ads you didn't approve, no recurring per-seat fees—this is Sovereign Radio."
    ]

    def generate_segment(
        self,
        topic: str = "Platform Telemetry",
        daypart: str = "MORNING_DRIVE",
        news_items: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        fmt = self.DAYPART_FORMATS.get(daypart, self.DAYPART_FORMATS["MORNING_DRIVE"])
        news_items = news_items or [
            "Apple Silicon Mac Mini telemetry operating at 42.1 degrees Celsius with optimal load.",
            "Zero cloud ingress egress fees recorded over the last 24 hours.",
            "All 65 n8n autonomous pipelines reporting 100 percent health."
        ]
        
        tagline = self.TAGLINES[int(time.time()) % len(self.TAGLINES)]
        
        script = f"Good hour, builders! You're locked into {self.STATION_CALLSIGN} — {fmt['name']}. {fmt['hook']} {tagline} "
        script += f"Checking in on our top topic: {topic}. "
        for i, item in enumerate(news_items, 1):
            script += f"In brief point {i}: {item} "
        script += "Up next, algorithmic lo-fi focus audio with automated ducking. Keep building."

        raw_id = f"{topic}:{fmt['tone']}:{time.time()}"
        segment_id = "SEG-" + hashlib.sha256(raw_id.encode()).hexdigest()[:10].upper()

        return {
            "segment_id": segment_id,
            "station": self.STATION_CALLSIGN,
            "show_name": fmt["name"],
            "topic": topic,
            "tone": fmt["tone"],
            "spoken_script": script,
            "estimated_duration_sec": round(max(15.0, len(script.split()) * 0.38), 1),
            "news_items_count": len(news_items),
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
