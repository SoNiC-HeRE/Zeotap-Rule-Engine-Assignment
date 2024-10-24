"""
Database handler module for Rule Engine.
Manages database connections and CRUD operations for rules.
"""

import sqlite3
from typing import List, Tuple, Any
from contextlib import contextmanager
import logging
import json
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass


class Database:
    """Database handler for Rule Engine."""

    def __init__(self, db_path: str = 'rule_engine.db'):
        """
        Initialize database handler.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.initialize_database()

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.

        Yields:
            sqlite3.Connection: Database connection

        Raises:
            DatabaseError: If connection fails
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable row factory for named columns
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise DatabaseError(f"Failed to connect to database: {e}")
        finally:
            if conn:
                conn.close()

    def initialize_database(self) -> None:
        """
        Initialize database schema if it doesn't exist.

        Raises:
            DatabaseError: If initialization fails
        """
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_string TEXT NOT NULL,
            ast TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(create_table_sql)
                conn.commit()
                logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            raise DatabaseError(f"Failed to initialize database: {e}")

    def load_rules(self) -> List[Tuple[str, Any]]:
        """
        Load all rules from database.

        Returns:
            List of tuples containing rule_string and ast

        Raises:
            DatabaseError: If loading fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT rule_string, ast 
                    FROM rules 
                    ORDER BY created_at DESC
                """)
                rules = [(row['rule_string'], json.loads(row['ast']))
                         for row in cursor.fetchall()]
                logger.debug(f"Loaded {len(rules)} rules from database")
                return rules
        except sqlite3.Error as e:
            logger.error(f"Failed to load rules: {e}")
            raise DatabaseError(f"Failed to load rules: {e}")

    def save_rule(self, rule_string: str, ast: Any) -> int:
        """
        Save a new rule to database.

        Args:
            rule_string: String representation of the rule
            ast: Abstract Syntax Tree of the rule

        Returns:
            ID of the newly inserted rule

        Raises:
            DatabaseError: If saving fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO rules (rule_string, ast) 
                    VALUES (?, ?)
                """, (rule_string, json.dumps(ast)))
                conn.commit()
                rule_id = cursor.lastrowid
                logger.info(f"Saved rule with ID: {rule_id}")
                return rule_id
        except sqlite3.Error as e:
            logger.error(f"Failed to save rule: {e}")
            raise DatabaseError(f"Failed to save rule: {e}")

    def get_rule_by_id(self, rule_id: int) -> Tuple[str, Any]:
        """
        Retrieve a specific rule by ID.

        Args:
            rule_id: ID of the rule to retrieve

        Returns:
            Tuple of rule_string and ast

        Raises:
            DatabaseError: If retrieval fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT rule_string, ast 
                    FROM rules 
                    WHERE id = ?
                """, (rule_id,))
                row = cursor.fetchone()
                if row:
                    return row['rule_string'], json.loads(row['ast'])
                return None
        except sqlite3.Error as e:
            logger.error(f"Failed to get rule {rule_id}: {e}")
            raise DatabaseError(f"Failed to get rule {rule_id}: {e}")


# Create database instance
db = Database()

# For backward compatibility
initialize_database = db.initialize_database
load_rules = db.load_rules
save_rule = db.save_rule