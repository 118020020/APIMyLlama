import os
import secrets
import requests
from datetime import datetime
from typing import Optional, Dict, Any

class Utils:
    def __init__(self, db):
        self.db = db
        self.current_port = None
        self.server = None

    def generate_key(self) -> str:
        key = secrets.token_urlsafe(32)
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO apiKeys (key, created_at) VALUES (?, ?)",
            (key, datetime.now().isoformat())
        )
        self.db.commit()
        print(f"Generated new API key: {key}")
        return key

    def list_keys(self) -> list:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM apiKeys")
        keys = cursor.fetchall()
        for key in keys:
            print(f"Key: {key['key']}, Created: {key['created_at']}, Active: {key['active']}")
        return keys

    def remove_key(self, key: str) -> bool:
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM apiKeys WHERE key = ?", (key,))
        self.db.commit()
        if cursor.rowcount > 0:
            print(f"Removed API key: {key}")
            return True
        print(f"Key not found: {key}")
        return False

    def add_key(self, key: str) -> bool:
        cursor = self.db.cursor()
        try:
            cursor.execute(
                "INSERT INTO apiKeys (key, created_at) VALUES (?, ?)",
                (key, datetime.now().isoformat())
            )
            self.db.commit()
            print(f"Added API key: {key}")
            return True
        except sqlite3.IntegrityError:
            print(f"Key already exists: {key}")
            return False

    @staticmethod
    def get_ollama_url() -> str:
        if os.path.exists('ollamaURL.conf'):
            with open('ollamaURL.conf', 'r') as f:
                return f.read().strip()
        return "http://localhost:11434"

    def set_rate_limit(self, key: str, limit: int) -> bool:
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE apiKeys SET rate_limit = ? WHERE key = ?",
            (limit, key)
        )
        self.db.commit()
        if cursor.rowcount > 0:
            print(f"Set rate limit to {limit} for key: {key}")
            return True
        print(f"Key not found: {key}")
        return False

    def add_webhook(self, url: str) -> int:
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO webhooks (url) VALUES (?)", (url,))
        self.db.commit()
        webhook_id = cursor.lastrowid
        print(f"Added webhook with ID {webhook_id}: {url}")
        return webhook_id

    def delete_webhook(self, webhook_id: int) -> bool:
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM webhooks WHERE id = ?", (webhook_id,))
        self.db.commit()
        if cursor.rowcount > 0:
            print(f"Deleted webhook with ID: {webhook_id}")
            return True
        print(f"Webhook not found with ID: {webhook_id}")
        return False

    def list_webhooks(self) -> list:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM webhooks")
        webhooks = cursor.fetchall()
        for webhook in webhooks:
            print(f"Webhook ID: {webhook['id']}, URL: {webhook['url']}")
        return webhooks

    def send_webhook_notification(self, payload: Dict[str, Any]) -> None:
        cursor = self.db.cursor()
        cursor.execute("SELECT url FROM webhooks")
        webhooks = cursor.fetchall()
        
        for webhook in webhooks:
            try:
                response = requests.post(webhook['url'], json=payload)
                if response.status_code != 200:
                    print(f"Failed to send webhook to {webhook['url']}: {response.status_code}")
            except Exception as e:
                print(f"Error sending webhook to {webhook['url']}: {str(e)}")

    def activate_key(self, key: str) -> bool:
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE apiKeys SET active = 1 WHERE key = ?",
            (key,)
        )
        self.db.commit()
        if cursor.rowcount > 0:
            print(f"Activated key: {key}")
            return True
        print(f"Key not found: {key}")
        return False

    def deactivate_key(self, key: str) -> bool:
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE apiKeys SET active = 0 WHERE key = ?",
            (key,)
        )
        self.db.commit()
        if cursor.rowcount > 0:
            print(f"Deactivated key: {key}")
            return True
        print(f"Key not found: {key}")
        return False
