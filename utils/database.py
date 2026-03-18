"""
Database Connection and Management Tools
"""
import sqlite3
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from app_config import DB_PATH


class Database:
    """Database management class (Singleton pattern)"""

    _instance: Optional['Database'] = None
    _connection: Optional[sqlite3.Connection] = None
    _initialized: bool = False

    def __new__(cls) -> 'Database':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(DB_PATH, check_same_thread=False)
                self._connection.row_factory = sqlite3.Row

                # Auto-initialize tables
                if not self._initialized:
                    self.init_tables()
                    self._initialized = True
            except Exception as e:
                print(f"Error initializing database: {e}")
                raise

    @property
    def connection(self) -> sqlite3.Connection:
        return self._connection

    @contextmanager
    def cursor(self):
        """Context manager for cursor"""
        cursor = self._connection.cursor()
        try:
            yield cursor
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            raise e
        finally:
            cursor.close()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute SQL statement"""
        with self.cursor() as cursor:
            cursor.execute(query, params)
            return cursor

    def fetchone(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch single record"""
        try:
            with self.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error in fetchone: {e}")
            return None

    def fetchall(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch multiple records"""
        try:
            with self.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error in fetchall: {e}")
            return []

    def insert(self, table: str, data: Dict) -> int:
        """Insert data"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        with self.cursor() as cursor:
            cursor.execute(query, tuple(data.values()))
            return cursor.lastrowid

    def update(self, table: str, data: Dict, where: str, where_params: tuple = ()) -> int:
        """Update data"""
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"
        with self.cursor() as cursor:
            cursor.execute(query, tuple(data.values()) + where_params)
            return cursor.rowcount

    def delete(self, table: str, where: str, where_params: tuple = ()) -> int:
        """Delete data"""
        query = f"DELETE FROM {table} WHERE {where}"
        with self.cursor() as cursor:
            cursor.execute(query, where_params)
            return cursor.rowcount

    def close(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def init_tables(self):
        """Initialize database tables"""
        tables_sql = [
            """CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                icon TEXT DEFAULT '[icon]',
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",

            """CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category_id INTEGER,
                ingredients TEXT,
                steps TEXT,
                cooking_time INTEGER DEFAULT 0,
                difficulty TEXT DEFAULT 'Easy',
                servings INTEGER DEFAULT 1,
                image_path TEXT,
                status TEXT DEFAULT 'draft',
                tags TEXT,
                rating REAL DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )""",

            """CREATE TABLE IF NOT EXISTS shares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER,
                share_method TEXT,
                share_target TEXT,
                share_content TEXT,
                shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id)
            )""",

            """CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER,
                user_name TEXT,
                favorited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id)
            )"""
        ]

        for sql in tables_sql:
            try:
                self.execute(sql)
            except Exception as e:
                print(f"Error creating table: {e}")

        # Initialize default categories
        self._init_default_categories()

    def _init_default_categories(self):
        """Initialize default categories"""
        from app_config import DEFAULT_CATEGORIES

        # Check if categories already exist
        existing_count = self.fetchone("SELECT COUNT(*) as cnt FROM categories")
        if existing_count and existing_count.get('cnt', 0) > 0:
            return  # Already has data, skip insertion

        # Insert default categories
        for cat in DEFAULT_CATEGORIES:
            try:
                self.insert('categories', {
                    'name': cat['name'],
                    'icon': cat.get('icon', '[icon]'),
                    'description': cat.get('description', ''),
                    'sort_order': 0
                })
            except Exception as e:
                print(f"Error inserting category {cat['name']}: {e}")


# Create global database instance
db = Database()
