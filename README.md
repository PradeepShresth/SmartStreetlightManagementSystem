# Smart Streetlight Management System

A simple student-friendly project for monitoring and managing streetlights using Python, Flask, MongoDB, and Redis.

## Project aim
The system helps track streetlight status, brightness, power usage, and fault conditions. It also stores long-term records in MongoDB and uses Redis for fast live updates.

## Technologies used
- Python
- Flask
- MongoDB
- Redis
- HTML + CSS

## How it works
- MongoDB stores the permanent data, such as lamp details, maintenance history, and energy records.
- Redis stores live lamp information, quick status updates, and alerts.
- Flask handles the dashboard and application routes.

## Run the project
1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
2. Make sure MongoDB and Redis are running locally.
3. Start the app:
   ```powershell
   python app.py
   ```
4. Open the browser at:
   ```text
   http://127.0.0.1:5000/
   ```

## Main routes
- / -> dashboard home page
- /dashboard -> same dashboard page
- /api/summary -> summary JSON data
- /api/lights -> list lights / add new light
- /api/lights/<lamp_id> -> update or delete one light
- /api/maintenance -> record maintenance activity
- /api/refresh -> refresh live system data

## Notes
This project keeps the design simple and practical for a small assignment while still covering the required database and real-time features.
