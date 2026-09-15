"""
PlayoutMixer: Audio timeline sequencing, ducking, and crossfades.
Author: Russell Alan Powers
"""
import time
import hashlib
from typing import Dict, Any, List

class PlayoutMixer:
    def mix_hour_timeline(self, voice_segments: List[Dict[str, Any]], music_style: str = "LOFI_STUDY") -> Dict[str, Any]:
        timeline = []
        current_time = 0.0

        for idx, seg in enumerate(voice_segments, 1):
            # Music intro
            timeline.append({
                "type": "MUSIC_BED",
                "title": f"{music_style} Track {idx}",
                "start_sec": round(current_time, 2),
                "duration_sec": 180.0,
                "volume_level_db": -18.0 if idx % 2 == 0 else -6.0
            })
            current_time += 30.0

            # DJ Voice Track (ducks music)
            v_dur = seg.get("estimated_duration_sec", 25.0)
            timeline.append({
                "type": "VOICE_TRACK",
                "segment_id": seg.get("segment_id", "SEG-000"),
                "start_sec": round(current_time, 2),
                "duration_sec": v_dur,
                "ducking_applied_db": -12.0
            })
            current_time += v_dur + 5.0

            # Station Ident
            timeline.append({
                "type": "STATION_IDENT",
                "title": "Sovereign Biz Box Legal ID",
                "start_sec": round(current_time, 2),
                "duration_sec": 4.5
            })
            current_time += 4.5

        timeline_hash = "MIX-" + hashlib.sha256(f"{music_style}:{current_time}".encode()).hexdigest()[:10].upper()

        return {
            "mix_id": timeline_hash,
            "music_style": music_style,
            "total_runtime_sec": round(current_time, 2),
            "total_items": len(timeline),
            "playlist_timeline": timeline
        }