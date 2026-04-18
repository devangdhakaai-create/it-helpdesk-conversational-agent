import sqlite3
from datetime import datetime

DB = "tickets.db"

class TicketManager:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        con = sqlite3.connect(DB)
        con.execute("""CREATE TABLE IF NOT EXISTS tickets (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT,
            dept     TEXT,
            priority TEXT,
            issue    TEXT,
            status   TEXT DEFAULT 'Open',
            created  TEXT
        )""")
        con.commit(); con.close()

    def create(self, name, dept, priority, issue) -> dict:
        con = sqlite3.connect(DB)
        cur = con.execute(
            "INSERT INTO tickets (name,dept,priority,issue,status,created) VALUES (?,?,?,?,?,?)",
            (name, dept, priority, issue, "Open", datetime.now().isoformat())
        )
        con.commit()
        tid = cur.lastrowid                                     # auto-generated ticket ID
        con.close()
        return {"id":tid,"name":name,"dept":dept,"priority":priority,
                "issue":issue,"status":"Open"}

    def get_all(self) -> list:
        con = sqlite3.connect(DB)
        cur = con.execute("SELECT id,name,dept,priority,issue,status FROM tickets")
        cols= [d[0] for d in cur.description]
        rows= [dict(zip(cols,r)) for r in cur.fetchall()]
        con.close()
        return rows

    def update_status(self, ticket_id, status):
        con = sqlite3.connect(DB)
        con.execute("UPDATE tickets SET status=? WHERE id=?", (status, ticket_id))
        con.commit(); con.close()