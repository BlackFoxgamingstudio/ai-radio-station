import unittest
import json
import io
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from n8n.webhook_adapter import RadioStationHandler, DEFAULT_TRACKS, engine

class MockSocket:
    def __init__(self, data=b""):
        self.data = data
        self.write_buffer = io.BytesIO()

    def makefile(self, mode, *args, **kwargs):
        if "b" in mode:
            if "r" in mode:
                return io.BytesIO(self.data)
            else:
                return self.write_buffer
        return io.StringIO(self.data.decode("utf-8", errors="ignore"))

    def sendall(self, data):
        self.write_buffer.write(data)

class TestRadioPlayerAndAudio(unittest.TestCase):
    def test_tracks_catalog(self):
        self.assertGreaterEqual(len(DEFAULT_TRACKS), 6)
        categories = {t["category"] for t in DEFAULT_TRACKS}
        self.assertIn("PODCAST", categories)
        self.assertIn("COMMERCIAL", categories)
        self.assertIn("SONG", categories)

    def test_audio_files_exist_on_disk(self):
        for track in DEFAULT_TRACKS:
            audio_url = track["audio_url"]
            filename = audio_url.split("/")[-1]
            found = False
            for d in [
                ROOT / "data" / "audio",
                Path("/Users/russellpowers/Sovereign Biz Box/solutions/tv-broadcast-station/data/audio"),
                Path("/Users/russellpowers/Sovereign Biz Box/solutions/storyboard-ai/backend/audio"),
            ]:
                if (d / filename).exists():
                    found = True
                    break
            self.assertTrue(found, f"Audio file for track '{track['title']}' ({filename}) not found on disk")

    def test_dj_engine_segment_generation(self):
        seg = engine.dj.generate_segment(topic="Episode 1 Business Mainframe")
        self.assertIn("spoken_script", seg)
        self.assertIn("W-SBB Radio 104.2 FM", seg["spoken_script"])
        self.assertGreater(seg["estimated_duration_sec"], 5.0)

    def test_scheduler_grid(self):
        schedule = engine.scheduler.get_schedule()
        self.assertGreaterEqual(len(schedule), 4)
        show = engine.scheduler.get_current_show()
        self.assertIn("show_name", show)

if __name__ == "__main__":
    unittest.main()
