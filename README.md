# Habit Tracker App  
A simple habit tracking application built with FastAPI and SQLite.

## Features
- Create, update, and delete habits.
- Track habit completion with streak calculations.
- View longest streaks and filter habits by frequency.
- Interactive API documentation via Swagger UI.

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/habit-tracker-app.git
   cd habit-tracker-app

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload

4. Open http://127.0.0.1:8000/docs to interact with the API.
