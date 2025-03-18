from fastapi import FastAPI
from routes import habits, records
from database import init_db

# Create the FastAPI application instance
app = FastAPI()

# Initialize the database when the application starts
# Ensures that the necessary tables are created if they don't exist
init_db()

# Include the routes for habits and habit records
# All routes related to habits will be prefixed with '/api' and tagged as 'habits'
# All routes related to habit records will be prefixed with '/api' and tagged as 'habit_records'
app.include_router(habits.router, prefix="/api", tags=["habits"])
app.include_router(records.router, prefix="/api", tags=["habit_records"])

# Define the root endpoint
# This is a simple health check or welcome message for the API
@app.get("/")
def read_root():
    return {"message": "Welcome to the Habit Tracker API"}
