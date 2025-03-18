class Habit:
    """
       Represents a habit in the habit tracking application.
    """
    def __init__(self, id, name, description, frequency, current_streak, longest_streak, created_date):
        self.id = id  # Unique identifier for the habit
        self.name = name  # Name of the habit
        self.description = description  # Brief description of the habit
        self.frequency = frequency  # Frequency of the habit (e.g., daily, weekly, monthly)
        self.current_streak = current_streak  # Current streak of successful completions
        self.longest_streak = longest_streak  # Longest streak of consecutive completions
        self.created_date = created_date  # Date the habit was created

class HabitRecord:
    """
       Represents a record of a habit, tracking its status on a specific date.
    """
    def __init__(self, id, habit_id, date, status):
        self.id = id # Unique identifier for the record
        self.habit_id = habit_id # ID of the habit this record is associated with
        self.date = date # Date the record was created
        self.status = status  # Status of the habit on this date (e.g., completed or missed)
