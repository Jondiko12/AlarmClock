import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('alarms.db')
        self.create_tables()

    def create_tables(self):
        """Create necessary database tables"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alarms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                sound_path TEXT,
                note TEXT,
                active BOOLEAN,
                snooze_count INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.conn.commit()

    def save_alarm(self, time, sound_path, note, active=True):
        """Save a new alarm to the database"""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO alarms (time, sound_path, note, active) VALUES (?, ?, ?, ?)",
                      (time, sound_path, note, active))
        self.conn.commit()

    def load_alarms(self):
        """Load active alarms from database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT time, sound_path, note, active FROM alarms WHERE active = 1")
        return [{"time": row[0], "sound_path": row[1], "note": row[2]} for row in cursor.fetchall()]

    def update_alarm_time(self, alarm, new_time):
        """Update alarm time (for snooze)"""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE alarms SET time = ? WHERE time = ? AND sound_path = ? AND note = ?",
                      (new_time, alarm["time"], alarm["sound_path"], alarm["note"]))
        self.conn.commit()

    def deactivate_alarm(self, alarm):
        """Deactivate an alarm"""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE alarms SET active = 0 WHERE time = ? AND sound_path = ? AND note = ?",
                      (alarm["time"], alarm["sound_path"], alarm["note"]))
        self.conn.commit()

    def delete_alarm(self, alarm):
        """Delete an alarm"""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE alarms SET active = 0 WHERE time = ? AND sound_path = ? AND note = ?",
                      (alarm["time"], alarm["sound_path"], alarm["note"]))
        self.conn.commit()

    def close(self):
        """Close database connection"""
        self.conn.close()