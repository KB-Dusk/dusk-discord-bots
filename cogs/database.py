import sqlite3
from datetime import datetime, timezone

class Database:
    def __init__(self, db_path='bot.db'):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                reason TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL UNIQUE,
                balance INTEGER DEFAULT 0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shop (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL UNIQUE,
                price INTEGER NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                item_name TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cooldowns (
                user_id TEXT PRIMARY KEY,
                last_daily TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def add_warning(self, user_id, reason):
        self.cursor.execute(
            'INSERT INTO warnings (user_id, reason) VALUES (?, ?)',
            (str(user_id), reason)
        )
        self.connection.commit()

    def get_warnings(self, user_id):
        self.cursor.execute(
            'SELECT reason FROM warnings WHERE user_id = ?',
            (str(user_id),)
        )
        return self.cursor.fetchall()

    def clear_warnings(self, user_id):
        self.cursor.execute(
            'DELETE FROM warnings WHERE user_id = ?',
            (str(user_id),)
        )
        self.connection.commit()

    def ensure_user(self, user_id):
        self.cursor.execute(
            'INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, ?)',
            (str(user_id), 0)
        )
        self.connection.commit()

    def get_balance(self, user_id):
        self.ensure_user(user_id)
        self.cursor.execute(
            'SELECT balance FROM users WHERE user_id = ?',
            (str(user_id),)
        )
        return self.cursor.fetchone()[0]

    def update_balance(self, user_id, amount):
        self.ensure_user(user_id)
        self.cursor.execute(
            'UPDATE users SET balance = balance + ? WHERE user_id = ?',
            (amount, str(user_id))
        )
        self.connection.commit()

    def get_leaderboard(self):
        self.cursor.execute(
            'SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT 10'
        )
        return self.cursor.fetchall()

    def get_shop(self):
        self.cursor.execute('SELECT item_name, price, description FROM shop')
        return self.cursor.fetchall()

    def add_shop_item(self, item_name, price, description):
        self.cursor.execute(
            'INSERT OR IGNORE INTO shop (item_name, price, description) VALUES (?, ?, ?)',
            (item_name, price, description)
        )
        self.connection.commit()

    def buy_item(self, user_id, item_name):
        self.cursor.execute(
            'SELECT price FROM shop WHERE item_name = ?',
            (item_name,)
        )
        item = self.cursor.fetchone()
        if not item:
            return 'item_not_found'
        price = item[0]
        balance = self.get_balance(user_id)
        if balance < price:
            return 'insufficient_funds'
        self.update_balance(user_id, -price)
        self.cursor.execute(
            'INSERT INTO inventory (user_id, item_name) VALUES (?, ?)',
            (str(user_id), item_name)
        )
        self.connection.commit()
        return 'success'

    def get_inventory(self, user_id):
        self.cursor.execute(
            'SELECT item_name FROM inventory WHERE user_id = ?',
            (str(user_id),)
        )
        return self.cursor.fetchall()

    def get_last_daily(self, user_id):
        self.cursor.execute(
            'SELECT last_daily FROM cooldowns WHERE user_id = ?',
            (str(user_id),)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def set_last_daily(self, user_id):
        now = datetime.now(timezone.utc).isoformat()
        self.cursor.execute(
            'INSERT OR REPLACE INTO cooldowns (user_id, last_daily) VALUES (?, ?)',
            (str(user_id), now)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()