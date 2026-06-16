import aiosqlite
import os

DB_PATH = "data/gf_threats.db"

async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                url TEXT,
                score REAL,
                category TEXT,
                blocked BOOLEAN,
                user_agent TEXT,
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                browser TEXT,
                start_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_ts TIMESTAMP,
                ip_hash TEXT
            )
        """)
        await db.commit()

async def log_threat(session_id: str, url: str, score: float, category: str, blocked: bool, user_agent: str = ""):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO threats (session_id, url, score, category, blocked, user_agent) VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, url, score, category, blocked, user_agent)
        )
        await db.commit()

async def get_threats(limit: int = 50):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM threats ORDER BY ts DESC LIMIT ?", (limit,)) as cursor:
            return [dict(row) for row in await cursor.fetchall()]

async def get_threat_summary():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT category, COUNT(*) as count FROM threats GROUP BY category") as cursor:
            rows = await cursor.fetchall()
            return {row[0]: row[1] for row in rows}

async def delete_threat(threat_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM threats WHERE id = ?", (threat_id,))
        await db.commit()
