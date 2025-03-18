from fastapi import APIRouter, HTTPException, Query
from schemas import HabitRecordCreate, HabitRecord, Habit
import crud

# Initialize a router for record-related endpoints
router = APIRouter()

# ==============================
# Routes for Habit Records
# ==============================

@router.post("/records", response_model=int)
def create_record(habit_id: int, record: HabitRecordCreate):
    """
    Create a new record for a habit.
    Args:
        habit_id (int): The ID of the habit to associate the record with.
        record (HabitRecordCreate): The record data, including status ('completed' or 'missed').
    Returns:
        int: The ID of the newly created record.
    """
    record_id = crud.create_record(habit_id, record.status)
    return record_id

@router.get("/records", response_model=list[HabitRecord])
def get_all_records():
    """
    Retrieve all habit records.
    Returns:
        list: A list of all habit records.
    Raises:
        HTTPException: If no records are found.
    """
    records = crud.get_all_records()
    if not records:
        raise HTTPException(status_code=404, detail="No records found")
    return records

@router.get("/records/streaks/longest", response_model=int)
def get_longest_streak_all():
    """
    Retrieve the longest streak across all habits.
    Returns:
        int: The longest streak value.
    """
    longest_streak = crud.get_longest_run_streak_all()
    return longest_streak

@router.get("/records/{habit_id}/longest_streak", response_model=int)
def get_longest_streak_by_habit(habit_id: int):
    """
    Retrieve the longest streak for a specific habit.
    Args:
        habit_id (int): The ID of the habit to retrieve the streak for.
    Returns:
        int: The longest streak value.
    Raises:
        HTTPException: If no streak is found for the habit.
    """
    longest_streak = crud.get_longest_run_streak_by_habit(habit_id)
    if longest_streak == 0:
        raise HTTPException(status_code=404, detail="No streak found for this habit")
    return longest_streak

@router.get("/records/{habit_id}", response_model=list[HabitRecord])
def get_records_by_habit(habit_id: int):
    """
    Retrieve all records for a specific habit.
    Args:
        habit_id (int): The ID of the habit to retrieve records for.
    Returns:
        list: A list of records for the specified habit.
    Raises:
        HTTPException: If no records are found for the habit.
    """
    records = crud.get_records_by_habit(habit_id)
    if not records:
        raise HTTPException(status_code=404, detail="No records found for the specified habit")
    return records

@router.get("/record/{record_id}", response_model=HabitRecord)
def get_record_by_id(record_id: int):
    """
    Retrieve a specific habit record by its ID.
    Args:
        record_id (int): The ID of the record to retrieve.
    Returns:
        HabitRecord: The record details.
    Raises:
        HTTPException: If the record is not found.
    """
    record = crud.get_record_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/record/{record_id}")
def update_record(record_id: int, status: str):
    """
    Update the status of a specific habit record.
    Args:
        record_id (int): The ID of the record to update.
        status (str): The new status ('completed' or 'missed').
    Returns:
        dict: A success message.
    Raises:
        HTTPException: If the record is not found.
    """
    try:
        crud.update_record(record_id, status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Record updated successfully"}

@router.delete("/record/{record_id}")
def delete_record(record_id: int):
    """
    Delete a specific habit record by its ID.
    Args:
        record_id (int): The ID of the record to delete.
    Returns:
        dict: A success message.
    """
    crud.delete_record(record_id)
    return {"message": "Record deleted successfully"}



