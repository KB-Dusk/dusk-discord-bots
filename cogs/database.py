import sqlite3

class Database:
    def __init__(self, db_path='warnings.db'):
        # connects to the database file, creates it if it doesn't exist
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # creates the warnings table if it doesn't already exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                reason TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def add_warning(self, user_id, reason):
        # inserts a new warning row for that user
        self.cursor.execute(
            'INSERT INTO warnings (user_id, reason) VALUES (?, ?)',
            (str(user_id), reason)
        )
        self.connection.commit()

    def get_warnings(self, user_id):
        # fetches all warnings for that user and returns them as a list
        self.cursor.execute(
            'SELECT reason FROM warnings WHERE user_id = ?',
            (str(user_id),)
        )
        return self.cursor.fetchall()

    def clear_warnings(self, user_id):
        # deletes all warnings for that user
        self.cursor.execute(
            'DELETE FROM warnings WHERE user_id = ?',
            (str(user_id),)
        )
        self.connection.commit()

    def close(self):
        # cleanly closes the database connection
        self.connection.close()