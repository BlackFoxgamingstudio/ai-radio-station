"""
MediaScheduler: SQLite-backed 24/7 radio programming grid.
Author: Russell Alan Powers
"""
import sqlite3
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

class MediaScheduler:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            data_dir = Path(__file__).resolve().parent.parent / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = str(data_dir / "radio_schedule.db")
        else:
            self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS program_blocks (
                block_id TEXT PRIMARY KEY,
                show_name TEXT NOT NULL,
                host_agent TEXT NOT NULL,
                start_hour INTEGER NOT NULL,
                duration_hours INTEGER NOT NULL,
                genre TEXT NOT NULL,
                active INTEGER DEFAULT 1
            );
        """)
        # Seed default 24h programming if empty
        cur.execute("SELECT count(*) FROM program_blocks;")
        if cur.fetchone()[0] == 0:
            defaults = [
                ("BLK-01", "Morning SRE Drive", "Agent Sentinel", 6, 3, "TECH_TELEMETRY"),
                ("BLK-02", "Midday Deep Work Lo-Fi", "Agent Maestro", 9, 5, "LOFI_BEATS"),
                ("BLK-03", "Afternoon Market & Grants Brief", "Agent Capital", 14, 4, "BUSINESS_RADAR"),
                ("BLK-04", "Prime Time Autonomous Engineering", "Agent Architect", 18, 4, "DEEP_TECH"),
                ("BLK-05", "Overnight Autonomous Healer Beats", "Agent Healer", 22, 8, "AMBIENT_CHILL")
            ]
            cur.executemany("INSERT INTO program_blocks VALUES (?, ?, ?, ?, ?, ?, 1)", defaults)
        conn.commit()
        conn.close()

    def get_schedule(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM program_blocks ORDER BY start_hour ASC")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_current_show(self, current_hour: Optional[int] = None) -> Dict[str, Any]:
        if current_hour is None:
            current_hour = time.localtime().tm_hour
        
        schedule = self.get_schedule()
        for block in schedule:
            start = block["start_hour"]
            end = (start + block["duration_hours"]) % 24
            if start <= end and start <= current_hour < end:
                return block
            elif start > end and (current_hour >= start or current_hour < end):
                return block
        return schedule[0] if schedule else {}