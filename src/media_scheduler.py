"""
MediaScheduler: Persistent SQLite broadcast scheduling and playout logging for W-SBB Radio.
Direct implementation of Mainframe SBBMusicStationView specifications.
Author: Russell Alan Powers
"""
import sqlite3
import time
from pathlib import Path
from typing import Dict, Any, List

class MediaScheduler:
    def __init__(self, db_path: Optional[str] = None):
        if not db_path:
            db_path = str(Path(__file__).resolve().parent.parent / "data" / "radio_schedule.db")
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS radio_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                daypart TEXT NOT NULL,
                show_name TEXT NOT NULL,
                genre TEXT NOT NULL,
                start_hour INTEGER NOT NULL,
                end_hour INTEGER NOT NULL,
                dj_personality TEXT NOT NULL,
                active BOOLEAN DEFAULT 1
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS playout_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                item_type TEXT NOT NULL,
                title TEXT NOT NULL,
                duration_sec REAL NOT NULL,
                status TEXT DEFAULT 'PLAYED'
            )
        """)
        # Seed default schedule if empty
        cur.execute("SELECT count(*) FROM radio_schedule")
        if cur.fetchone()[0] == 0:
            default_grid = [
                ("MORNING_DRIVE", "The Morning Mainframe Drive", "TECH_UPBEAT", 6, 11, "DJ Nova"),
                ("MIDDAY_SPRINT", "Midday Autonomous Pulse", "LOFI_STUDY", 11, 16, "DJ Sovereign"),
                ("EVENING_CODE", "Late Night Deep Build & Lo-Fi", "CHILL_SYNTH", 16, 23, "DJ Sentinel"),
                ("OVERNIGHT", "Bare-Metal Ambient Drones", "AMBIENT_SPACE", 23, 6, "DJ Core")
            ]
            cur.executemany("""
                INSERT INTO radio_schedule (daypart, show_name, genre, start_hour, end_hour, dj_personality)
                VALUES (?, ?, ?, ?, ?, ?)
            """, default_grid)
        conn.commit()
        conn.close()

    def get_schedule(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT daypart, show_name, genre, start_hour, end_hour, dj_personality FROM radio_schedule WHERE active = 1")
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "daypart": r[0],
                "show_name": r[1],
                "genre": r[2],
                "hours": f"{r[3]:02d}:00 - {r[4]:02d}:00",
                "dj": r[5]
            }
            for r in rows
        ]

    def get_current_show(self) -> Dict[str, Any]:
        current_hour = time.localtime().tm_hour
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT daypart, show_name, genre, dj_personality
            FROM radio_schedule
            WHERE (start_hour <= end_hour AND ? >= start_hour AND ? < end_hour)
               OR (start_hour > end_hour AND (? >= start_hour OR ? < end_hour))
            LIMIT 1
        """, (current_hour, current_hour, current_hour, current_hour))
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                "daypart": row[0],
                "show_name": row[1],
                "genre": row[2],
                "dj": row[3],
                "current_time_hour": current_hour
            }
        return {
            "daypart": "GENERAL",
            "show_name": "Sovereign Audio Stream",
            "genre": "LOFI_STUDY",
            "dj": "DJ Sovereign",
            "current_time_hour": current_hour
        }

    def log_playout(self, item_type: str, title: str, duration_sec: float):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO playout_logs (item_type, title, duration_sec) VALUES (?, ?, ?)", (item_type, title, duration_sec))
        conn.commit()
        conn.close()
