from fastapi import APIRouter, HTTPException, Query
from schemas import Habit, HabitCreate, HabitUpdate
import crud

# Initialize a router for habit-related endpoints
router = APIRouter()

# =====================
# Habit Management Endpoints
# =====================
@router.post("/habits/", response_model=int)
def create_habit(habit: HabitCreate):
    """
       Creates a new habit.
       Args:
           habit (HabitCreate): The habit data to create (name, description, frequency).
       Returns:
           int: The ID of the newly created habit.
    """
    habit_id = crud.create_habit(habit.name, habit.description, habit.frequency)
    return habit_id

@router.get("/habits/", response_model=list[Habit])
def list_habits():
    """
        Retrieves a list of all habits.
        Returns:
            list: A list of Habit objects.
    """
    return crud.get_all_habits()

@router.get("/habits/by-frequency", response_model=list[Habit])
def get_habits_by_frequency(frequency: str):
    """
       Retrieves habits that match a specific frequency.
       Args:
           frequency (str): The frequency to filter habits by (e.g., 'daily', 'weekly', 'monthly').
       Returns:
           list: A list of Habit objects with the specified frequency.
       Raises:
           HTTPException: If no habits match the specified frequency.
    """
    habits = crud.get_habits_by_frequency(frequency)
    if not habits:
        raise HTTPException(status_code=404, detail="No habits found with the specified frequency")
    return habits

@router.get("/habits/{habit_id}", response_model=Habit)
def retrieve_habit(habit_id: int):
    """
        Retrieves a habit by its ID.
        Args:
            habit_id (int): The ID of the habit to retrieve.
        Returns:
            Habit: The habit object if found.
        Raises:
            HTTPException: If the habit with the specified ID does not exist.
    """
    habit = crud.get_habit_by_id(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.put("/habits/{habit_id}")
def update_habit(habit_id: int, habit: HabitUpdate):
    """
        Updates an existing habit by its ID.
        Args:
            habit_id (int): The ID of the habit to update.
            habit (HabitUpdate): The updated habit data (name, description, frequency).
        Returns:
            dict: A success message indicating the habit was updated.
    """
    crud.update_habit(habit_id, habit.name, habit.description, habit.frequency)
    return {"message": "Habit updated successfully"}

@router.delete("/habits/{habit_id}")
def delete_habit(habit_id: int):
    """
        Deletes a habit by its ID.
        Args:
            habit_id (int): The ID of the habit to delete.
        Returns:
            dict: A success message indicating the habit was deleted.
    """
    crud.delete_habit(habit_id)
    return {"message": "Habit deleted successfully"}





