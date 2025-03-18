from pydantic import BaseModel
from typing import Optional

# =====================
# Schemas for Habits
# =====================

#Habits
class HabitCreate(BaseModel):
    """
    Schema for creating a new habit.
    Attributes:
        name (str): The name of the habit.
        description (Optional[str]): A brief explanation of the habit (optional).
        frequency (str): The frequency of the habit (e.g., 'daily', 'weekly', 'monthly').
    """
    name: str
    description: Optional[str]
    frequency: str

class HabitUpdate(BaseModel):
    """
    Schema for updating an existing habit.
    Attributes:
        name (Optional[str]): The updated name of the habit (optional).
        description (Optional[str]): The updated description of the habit (optional).
        frequency (Optional[str]): The updated frequency of the habit (optional).
    """
    name: Optional[str]
    description: Optional[str]
    frequency: Optional[str]

class Habit(BaseModel):
    """
    Schema for a habit retrieved from the database.
    Attributes:
        id (int): The unique identifier for the habit.
        name (str): The name of the habit.
        description (Optional[str]): A brief explanation of the habit.
        frequency (str): The frequency of the habit.
        created_date (str): The date when the habit was created.
    """
    id: int
    name: str
    description: Optional[str]
    frequency: str
    created_date: str  # Matches the created_date field in the database.

    class Config:
        """
        Configuration for Pydantic model to enable ORM compatibility.
        """
        orm_mode = True

# =====================
# Schemas for Habit Records
# =====================

class HabitRecordCreate(BaseModel):
    """
    Schema for creating a new habit record.
    Attributes:
        status (str): The status of the habit record ('completed' or 'missed').
    """
    status: str  # 'completed' or 'missed'

class HabitRecord(BaseModel):
    """
    Schema for a habit record retrieved from the database.
    Attributes:
        id (int): The unique identifier for the record.
        habit_id (int): The ID of the associated habit.
        date (str): The date when the habit was tracked.
        status (str): The status of the habit record ('completed' or 'missed').
        current_streak (int): The current streak of consecutive completions.
        longest_streak (int): The longest streak of consecutive completions.
    """
    id: int
    habit_id: int
    date: str  # Date when the habit was tracked
    status: str  # 'completed' or 'missed'
    current_streak: int
    longest_streak: int

    class Config:
        """
        Configuration for Pydantic model to enable ORM compatibility.
        """
        orm_mode = True