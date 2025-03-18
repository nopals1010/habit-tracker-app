import sqlite3

# Name of the SQLite database file
DB_NAME = "habit_tracker.db"

# =====================
# Database Connection
# =====================

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# =====================
# Database Initialization
# =====================

def init_db():
    """
        Initializes the SQLite database by creating the required tables if they do not already exist.
        Tables:
            - habits: Stores habit information.
            - habit_records: Tracks individual records for each habit, including streak data.
        """
    conn = get_connection()
    cursor = conn.cursor()

    # Create the 'habits' table to store habit details
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            frequency TEXT CHECK(frequency IN ('daily', 'weekly', 'monthly')) NOT NULL,
            created_date DATE DEFAULT CURRENT_DATE
        )
    """)

    # Create the 'habit_records' table to track progress for each habit
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date DATE NOT NULL,
            status TEXT CHECK(status IN ('completed', 'missed')) NOT NULL,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        )
    """)

    conn.commit() # Save changes to the database
    conn.close() # Close the database connection

# If this file is run directly, initialize the database
if __name__ == "__main__":
    """
    If the script is run as the main module, initialize the database.
    This ensures that the required tables are created before any operations.
    """
    init_db()
