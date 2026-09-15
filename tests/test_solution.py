#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core import CoreEngine

class TestAIRadioStation(unittest.TestCase):
    def setUp(self):
        self.engine = CoreEngine()

    def test_01_health_check(self):
        h = self.engine.health_check()
        self.assertEqual(h["status"], "HEALTHY")
        self.assertEqual(h["port"], 8811)

    def test_02_dj_segment_generation(self):
        res = self.engine.execute_feature("generate_dj_segment", {"topic": "Local AI Automation"})
        self.assertEqual(res["status"], "SUCCESS")
        seg = res["result"]
        self.assertIn("SEG-", seg["segment_id"])
        self.assertIn("Sovereign Broadcast", seg["spoken_script"])
        self.assertGreater(seg["estimated_duration_sec"], 10.0)

    def test_03_playout_mixer(self):
        res = self.engine.execute_feature("assemble_broadcast_hour", {"music_style": "CHILL_SYNTH"})
        self.assertEqual(res["status"], "SUCCESS")
        mix = res["result"]
        self.assertIn("MIX-", mix["mix_id"])
        self.assertGreater(mix["total_runtime_sec"], 50.0)

    def test_04_now_playing_and_schedule(self):
        res = self.engine.execute_feature("get_now_playing", {})
        self.assertEqual(res["status"], "SUCCESS")
        np = res["result"]
        self.assertIn("Sovereign Radio", np["station_name"])
        self.assertIn("now_playing", np)

if __name__ == "__main__":
    unittest.main(verbosity=2)