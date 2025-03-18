from database import get_connection
from datetime import date

# =====================
# CRUD for Habits
# =====================

# Create a new habit
def create_habit(name, description, frequency):
    """
        Inserts a new habit into the habits table.
        Args:
            name (str): The name of the habit.
            description (str): A brief explanation of the habit.
            frequency (str): The frequency of the habit (e.g., 'daily', 'weekly', 'monthly').
        Returns:
            int: The ID of the newly created habit.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO habits (name, description, frequency) 
        VALUES (?, ?, ?)
    """, (name, description, frequency))
    conn.commit()
    habit_id = cursor.lastrowid
    conn.close()
    return habit_id

# Retrieve all habits
def get_all_habits():
    """
        Retrieves all habits from the habits table.
        Returns:
            list: A list of dictionaries containing habit details.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits")
    habits = cursor.fetchall()
    conn.close()
    return [dict(habit) for habit in habits]

# Retrieve a specific habit by ID
def get_habit_by_id(habit_id):
    """
       Retrieves a habit by its ID.
       Args:
           habit_id (int): The ID of the habit to retrieve.
       Returns:
           dict: A dictionary containing the habit details, or None if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
    habit = cursor.fetchone()
    conn.close()
    return dict(habit) if habit else None

# Update an existing habit
def update_habit(habit_id, name=None, description=None, frequency=None):
    """
        Updates the details of an existing habit.
        Args:
            habit_id (int): The ID of the habit to update.
            name (str, optional): The updated name of the habit.
            description (str, optional): The updated description of the habit.
            frequency (str, optional): The updated frequency of the habit.
    """
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    params = []

    # Add fields to update if provided
    if name:
        fields.append("name = ?")
        params.append(name)
    if description:
        fields.append("description = ?")
        params.append(description)
    if frequency:
        fields.append("frequency = ?")
        params.append(frequency)

    params.append(habit_id)
    query = f"UPDATE habits SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()

# Delete a habit
def delete_habit(habit_id):
    """
       Deletes a habit from the habits table.
       Args:
           habit_id (int): The ID of the habit to delete.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()

# Retrieve habits by frequency
def get_habits_by_frequency(frequency):
    """
        Retrieves habits that match a specific frequency.
        Args:
            frequency (str): The frequency to filter by (e.g., 'daily').
        Returns:
            list: A list of dictionaries containing the matching habits.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM habits WHERE frequency = ?
    """, (frequency,))
    habits = cursor.fetchall()
    conn.close()
    return [dict(habit) for habit in habits]

# =====================
# CRUD for Habit Records
# =====================

# Create a new habit record
def create_record(habit_id, status):
    """
        Creates a new record for a habit and calculates streaks.
        Args:
            habit_id (int): The ID of the habit.
            status (str): The status of the record ('completed' or 'missed').
        Returns:
            int: The ID of the newly created record.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve the most recent record for the habit to calculate streaks
    cursor.execute("""
        SELECT current_streak, longest_streak FROM habit_records
        WHERE habit_id = ? ORDER BY date DESC LIMIT 1
    """, (habit_id,))
    last_record = cursor.fetchone()

    # Calculate streaks
    if last_record:
        current_streak, longest_streak = last_record
        # Update streaks based on the status
        if status == "completed":
            current_streak += 1
            longest_streak = max(current_streak, longest_streak)
        else:
            current_streak = 0
    else:
        # Initialize streaks for the first record
        current_streak = 1 if status == "completed" else 0
        longest_streak = current_streak

    # Insert the new record
    cursor.execute("""
        INSERT INTO habit_records (habit_id, date, status, current_streak, longest_streak)
        VALUES (?, DATE('now'), ?, ?, ?)
    """, (habit_id, status, current_streak, longest_streak))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

# Retrieve all habit records
def get_all_records():
    """
        Retrieves all records from the habit_records table.
        Returns:
            list: A list of dictionaries containing all habit records.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM habit_records
    """)
    records = cursor.fetchall()
    conn.close()
    return [dict(record) for record in records]

# Retrieve records for a specific habit by habit ID
def get_records_by_habit(habit_id):
    """
        Retrieves all records for a specific habit.
        Args:
            habit_id (int): The ID of the habit to retrieve records for.
        Returns:
            list: A list of dictionaries containing the records for the habit.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM habit_records WHERE habit_id = ?
    """, (habit_id,))
    records = cursor.fetchall()
    conn.close()
    return [dict(record) for record in records]

# Retrieve a single habit record by record ID
def get_record_by_id(record_id):
    """
       Retrieves a specific habit record by its ID.
       Args:
           record_id (int): The ID of the record to retrieve.
       Returns:
           dict: A dictionary containing the record details, or None if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM habit_records WHERE id = ?
    """, (record_id,))
    record = cursor.fetchone()
    conn.close()
    return dict(record) if record else None

# Update an existing habit record
def update_record(record_id, status):
    """
        Updates the status of a habit record and recalculates streaks.
        Args:
            record_id (int): The ID of the record to update.
            status (str): The new status of the record ('completed' or 'missed').
        Raises:
            ValueError: If the record is not found.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve the current streak and habit ID for the record
    cursor.execute("""
        SELECT habit_id, current_streak, longest_streak FROM habit_records WHERE id = ?
    """, (record_id,))
    record = cursor.fetchone()

    if not record:
        conn.close()
        raise ValueError("Record not found")

    habit_id, current_streak, longest_streak = record

    # Recalculate streaks based on the new status
    if status == "completed":
        current_streak += 1
        longest_streak = max(current_streak, longest_streak)
    else:
        current_streak = 0

    # Update the record in the database
    cursor.execute("""
        UPDATE habit_records
        SET status = ?, current_streak = ?, longest_streak = ?
        WHERE id = ?
    """, (status, current_streak, longest_streak, record_id))
    conn.commit()
    conn.close()

# Retrieve the longest streak across all habits
def get_longest_run_streak_all():
    """
        Retrieves the longest streak across all habits.
        Returns:
            int: The longest streak value, or 0 if no records exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(longest_streak) AS longest_streak FROM habit_records
    """)
    result = cursor.fetchone()
    conn.close()

    # Return the longest streak or 0 if no records are found
    return result["longest_streak"] if result and result["longest_streak"] is not None else 0

# Retrieve the longest streak for a specific habit
def get_longest_run_streak_by_habit(habit_id):
    """
        Retrieves the longest streak for a specific habit.
        Args:
            habit_id (int): The ID of the habit to retrieve the longest streak for.
        Returns:
            int: The longest streak value, or 0 if no records exist for the habit.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(longest_streak) AS longest_streak FROM habit_records
        WHERE habit_id = ?
    """, (habit_id,))
    result = cursor.fetchone()
    conn.close()

    # Return the longest streak or 0 if no records are found
    return result["longest_streak"] if result and result["longest_streak"] is not None else 0

# Delete a habit record by its ID
def delete_record(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM habit_records WHERE id = ?
    """, (record_id,))
    conn.commit()
    conn.close()
