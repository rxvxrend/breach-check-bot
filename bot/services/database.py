import sqlite3
from pathlib import Path


class Database:

    def __init__(self, db_name="breach_bot.db"):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        db_path = BASE_DIR / db_name

        self.coonection = sqlite3.connect(db_path)
        self.cursor = self.coonection.cursor()

    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                check_type TEXT NOT NULL,
                value TEXT NOT NULL,
                last_count INTEGER DEFAULT 0
            )
        """)

        self.coonection.commit()

    def add_subscription(
            self,
            user_id,
            check_type,
            value,
            last_count
    ):
        
        self.cursor.execute("""
            INSERT INTO subscriptions (
                user_id,
                check_type,
                value,
                last_count
            )
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            check_type,
            value,
            last_count
        ))

        self.coonection.commit()

    def get_subscriptions(self):

        self.cursor.execute("""
            SELECT
                id,
                user_id,
                check_type,
                value,
                last_count
            FROM subscriptions
        """)

        rows = self.cursor.fetchall()

        return rows
    
    def update_subscription(
        self,
        subscription_id,
        new_count
    ):
        self.cursor.execute("""
            UPDATE subscriptions
            SET last_count = ?
            WHERE id = ?
        """, (
            new_count,
            subscription_id
        ))

    def delete_subscription(self, user_id, check_type, value):
        
        self.cursor.execute("""
            DELETE FROM subscriptions
            WHERE user_id = ?
            AND check_type = ?
            AND value = ?
        """, (user_id, check_type, value))

        self.coonection.commit()

    def is_subscribed(self, user_id, check_type, value):

        self.cursor.execute("""
            SELECT 1 FROM subscriptions
            WHERE user_id = ?
            AND check_type = ?
            AND value = ?
        """, (user_id, check_type, value))

        return self.cursor.fetchone() is not None
    
    def get_user_subscriptions(self, user_id):

        self.cursor.execute("""
            SELECT
                check_type,
                value,
                last_count
            FROM subscriptions
            WHERE user_id = ?
        """, (user_id,))

        return self.cursor.fetchall()