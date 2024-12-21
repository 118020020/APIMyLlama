import sqlite3
from datetime import datetime

class Database:
    _instance = None

    def __init__(self):
        self.db = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize_database(self):
        self.db = sqlite3.connect('./apiKeys.db', check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        print('Connected to the apiKeys.db database.')
        self.create_tables()
        return self.db

    def create_tables(self):
        cursor = self.db.cursor()
        
        # Create apiKeys table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS apiKeys (
                key TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tokens INTEGER DEFAULT 10,
                rate_limit INTEGER DEFAULT 10,
                active INTEGER DEFAULT 1,
                description TEXT
            )
        ''')

        # Create apiUsage table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS apiUsage (
                key TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create webhooks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS webhooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL
            )
        ''')

        self.ensure_columns()
        self.db.commit()

    def ensure_columns(self):
        cursor = self.db.cursor()
        columns = [row[1] for row in cursor.execute("PRAGMA table_info(apiKeys)")]
        
        if 'active' not in columns:
            cursor.execute("ALTER TABLE apiKeys ADD COLUMN active INTEGER DEFAULT 1")
            print("Added 'active' column to 'apiKeys' table.")
        
        if 'description' not in columns:
            cursor.execute("ALTER TABLE apiKeys ADD COLUMN description TEXT")
            print("Added 'description' column to 'apiKeys' table.")
        
        self.db.commit()

    def close_database(self):
        if self.db:
            self.db.close()
            print('Closed the database connection.')

    def get_db(self):
        return self.db

# Create a global instance
db_instance = Database()
