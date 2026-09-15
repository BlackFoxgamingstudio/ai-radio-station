"""
PlayoutMixer: Audio timeline sequencing, DSP ducking envelopes, and crossfades.
Direct implementation of Mainframe SBBMusicStationView specifications.
Author: Russell Alan Powers
"""
import time
import hashlib
from typing import Dict, Any, List

class PlayoutMixer:
    # DSP Ducking Specifications
    DUCKING_SPECS = {
        "voice_over": {
            "duck_depth_db": -14.0,  # Lower music by 14dB under voice
            "attack_ms": 250,        # Smooth 250ms ramp-down
            "release_ms": 600,       # Smooth 600ms ramp-up
            "hold_ms": 100
        },
        "station_ident": {
            "duck_depth_db": -18.0,
            "attack_ms": 150,
            "release_ms": 400,
            "hold_ms": 50
        }
    }

    def mix_hour_timeline(self, voice_segments: List[Dict[str, Any]], music_style: str = "LOFI_STUDY") -> Dict[str, Any]:
        timeline = []
        current_time = 0.0

        for idx, seg in enumerate(voice_segments, 1):
            # Music intro bed
            timeline.append({
                "type": "MUSIC_BED",
                "title": f"{music_style} Track {idx}",
                "start_sec": round(current_time, 2),
                "duration_sec": 180.0,
                "nominal_level_db": -6.0,
                "codec": "AAC_320KBPS"
            })
            current_time += 25.0  # 25 seconds of clean music before DJ talks

            # DJ Voice Track (ducks music bed)
            v_dur = seg.get("estimated_duration_sec", 25.0)
            timeline.append({
                "type": "VOICE_TRACK",
                "segment_id": seg.get("segment_id", f"SEG-{idx:03d}"),
                "start_sec": round(current_time, 2),
                "duration_sec": v_dur,
                "ducking_envelope": {
                    "applied_to": f"{music_style} Track {idx}",
                    "duck_gain_db": self.DUCKING_SPECS["voice_over"]["duck_depth_db"],
                    "attack_ms": self.DUCKING_SPECS["voice_over"]["attack_ms"],
                    "release_ms": self.DUCKING_SPECS["voice_over"]["release_ms"]
                }
            })
            current_time += v_dur + 3.0

            # Legal Station Ident / Chime
            timeline.append({
                "type": "STATION_IDENT",
                "title": "W-SBB Radio 104.2 FM Legal Station Ident",
                "start_sec": round(current_time, 2),
                "duration_sec": 4.5,
                "ducking_envelope": self.DUCKING_SPECS["station_ident"]
            })
            current_time += 4.5

        timeline_hash = "MIX-" + hashlib.sha256(f"{music_style}:{current_time}".encode()).hexdigest()[:10].upper()

        return {
            "mix_id": timeline_hash,
            "music_style": music_style,
            "total_runtime_sec": round(current_time, 2),
            "total_items": len(timeline),
            "dsp_ducking_enabled": True,
            "audio_format": "320KBPS_STEREO_48KHZ",
            "playlist_timeline": timeline
        }
