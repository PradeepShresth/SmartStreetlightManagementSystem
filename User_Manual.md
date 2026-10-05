# Smart Streetlight Management System - User Manual

## 1. Introduction
This project is a basic but functional Smart Streetlight Management System designed for a student assignment. The system allows a city maintenance team or administrator to monitor streetlights, identify faults, track energy consumption, and record repair work. It is intentionally simple and easy to understand while still showing good design practice.

The application is built using Python and Flask, with MongoDB used for permanent storage and Redis used for fast live data updates. The dashboard shows a summary of the current state of the system and lets users manage lamp records.

## 2. Purpose of the Project
The purpose of the system is to provide a simple tool for:
- monitoring streetlight status
- checking which lamps are turned on, dim, or faulty
- tracking total energy usage
- registering new streetlights
- updating existing streetlight details
- recording maintenance actions
- responding quickly to lamp faults

This makes the system useful in a real smart-city environment, even though the implementation is intentionally kept simple for academic use.

## 3. System Features
The system includes the following major features:

### 3.1 Dashboard view
The main dashboard shows:
- total number of lamps
- number of lamps currently on
- number of dim lamps
- number of faulty lamps
- total energy used
- latest alerts

### 3.2 Lamp management
The user can:
- add a new lamp
- update lamp properties
- delete a lamp record
- view the full list of lamps

### 3.3 Maintenance tracking
Every maintenance action can be saved with:
- lamp ID
- action performed
- description of work
- technician name
- date and time

### 3.4 Fault detection
Faulty lamps are highlighted and can be seen in the dashboard summary and alert area.

### 3.5 Live refresh
The system simulates live updates so the dashboard can refresh statuses and recalculate summary information.

## 4. Technologies Used

### Python
Python is used because it is simple, readable, and well-suited for backend logic and web applications.

### Flask
Flask is the web framework used to build the application routes, render the user interface, and provide API endpoints.

### MongoDB
MongoDB is used for persistent storage. It holds the lamp data and maintenance history. This is the system of record for the application.

### Redis
Redis is used for fast access to live data and alerts. It stores quick information about the current state of lamps and recent fault events.

### HTML and CSS
HTML and CSS are used to create a simple dashboard interface for displaying data to the user.

## 5. Software and Environment Requirements
To run this project, the machine should have:
- Windows 10 or later
- Python 3.12 installed
- Flask
- MongoDB installed and running locally
- Redis installed and running locally
- a browser such as Chrome or Edge

## 6. Project Structure
The folder contains these important files:

- app.py - main Flask application
- database/mongo_service.py - MongoDB logic and data handling
- database/redis_service.py - Redis logic and live alerts
- templates/dashboard.html - dashboard HTML page
- static/style.css - dashboard styling
- README.md - short project overview
- User_Manual.md - detailed user guidance
- Assignment_Report.md - academic report
- SmartStreetlight_Project_Documentation.docx - Word version of the assignment report
- SmartStreetlight_User_Manual.docx - Word version of the user manual

## 7. System Architecture
The project uses a simple architecture with three main layers:

1. Frontend layer
   - The dashboard is displayed in the browser.
   - It shows summary cards and a lamp table.

2. Application layer
   - Flask receives HTTP requests and routes them to the correct logic.
   - It exposes both HTML pages and JSON APIs.

3. Data layer
   - MongoDB stores long-term data.
   - Redis stores live operational data and recent alerts.

This design is useful because it separates permanent storage from quick, temporary live data access.

## 8. How the Application Works
When the system starts:
1. Flask starts the web application.
2. MongoDB is checked for stored lamp data.
3. Redis is checked for live state synchronization.
4. The dashboard loads summary data and lamp records.
5. Users can interact with the API or the dashboard to add, update, delete, or refresh data.

If MongoDB or Redis is not available, the app still runs with sample fallback data so the project can be demonstrated without full local services.

## 9. Installation and Setup
Follow these steps:

### Step 1: Open PowerShell
Open PowerShell in the project folder.

### Step 2: Install dependencies
Run the following command:

```powershell
pip install -r requirements.txt
```

The project dependencies are:
- Flask
- pymongo
- redis

### Step 3: Start MongoDB
Make sure MongoDB is running locally on:

```text
mongodb://localhost:27017/
```

### Step 4: Start Redis
Make sure Redis is running locally on:

```text
localhost:6379
```

### Step 5: Run the application
Use:

```powershell
python app.py
```

If the project does not run with the plain `python` command on your Windows machine, use the installed Python path explicitly:

```powershell
& 'C:\Users\Pradeep\AppData\Local\Programs\Python\Python312\python.exe' app.py
```

## 10. Running the Project
Once the server starts successfully, open the browser and visit:

```text
http://127.0.0.1:5000/
```

The dashboard opens and shows the current lamp summary and data table.

## 11. Dashboard Guide
The dashboard contains:

### Summary cards
These show:
- total lamps
- active lamps
- dim lamps
- faulty lamps
- total energy consumption

### Lamp table
This table contains rows for each lamp and includes information such as:
- lamp ID
- zone
- status
- brightness
- power usage
- fault condition
- last update time

### Alerts section
This section shows recent fault or event alerts. It helps maintenance teams quickly see which lamp needs attention.

## 12. API Reference
The application provides several API routes. These endpoints help users interact with the system programmatically.

### 12.1 GET /
Opens the dashboard page.

### 12.2 GET /dashboard
Also opens the dashboard page.

### 12.3 GET /api/summary
Returns overall system summary data in JSON format.

Example response:

```json
{
  "summary": {
    "total_lamps": 5,
    "on_count": 2,
    "dim_count": 2,
    "fault_count": 1,
    "total_energy": 76.1
  },
  "faulty_lamps": ["SL-304"],
  "alerts": [
    {
      "message": "SL-304 reported a fault in Industrial",
      "type": "fault"
    }
  ],
  "mongo_connected": true,
  "redis_connected": true
}
```

### 12.4 GET /api/lights
Returns all lamp records.

Example response:

```json
{
  "lamps": [
    {
      "lamp_id": "SL-101",
      "zone": "Downtown",
      "status": "on",
      "brightness": 82,
      "power_usage": 130,
      "fault": false
    }
  ],
  "summary": {
    "total_lamps": 5,
    "on_count": 2,
    "dim_count": 2,
    "fault_count": 1
  }
}
```

### 12.5 POST /api/lights
Adds a new lamp to the system.

Required fields:
- lamp_id
- zone

Optional fields:
- lamp_type
- location
- power_rating
- brightness
- status
- fault

Example JSON body:

```json
{
  "lamp_id": "SL-900",
  "zone": "Main Road",
  "location": "Near Park",
  "power_rating": 90,
  "brightness": 100,
  "status": "on",
  "fault": false,
  "lamp_type": "LED"
}
```

### 12.6 PUT /api/lights/<lamp_id>
Updates the details of a particular lamp.

Example JSON body:

```json
{
  "status": "dim",
  "brightness": 50,
  "fault": false
}
```

### 12.7 DELETE /api/lights/<lamp_id>
Deletes a lamp record from the system.

### 12.8 POST /api/maintenance
Records a maintenance event for a lamp.

Example JSON body:

```json
{
  "lamp_id": "SL-101",
  "action": "repair",
  "description": "Replaced faulty bulb and checked wiring.",
  "technician": "Technician 1"
}
```

### 12.9 GET /api/refresh
Refreshes the lamp state and updates the summary and alerts.

This endpoint simulates live monitoring and changes lamp values to reflect real-world activity.

## 13. Example API Calls
These examples can be used in PowerShell or a browser test environment.

### View all lights
```powershell
curl http://127.0.0.1:5000/api/lights
```

### Add a new lamp
```powershell
curl -X POST http://127.0.0.1:5000/api/lights -H "Content-Type: application/json" -d "{\"lamp_id\":\"SL-900\",\"zone\":\"Main Road\",\"location\":\"Near Park\",\"power_rating\":90,\"brightness\":100,\"status\":\"on\",\"fault\":false}"
```

### Update a lamp
```powershell
curl -X PUT http://127.0.0.1:5000/api/lights/SL-900 -H "Content-Type: application/json" -d "{\"status\":\"dim\",\"brightness\":50}"
```

### Remove a lamp
```powershell
curl -X DELETE http://127.0.0.1:5000/api/lights/SL-900
```

### Record maintenance
```powershell
curl -X POST http://127.0.0.1:5000/api/maintenance -H "Content-Type: application/json" -d "{\"lamp_id\":\"SL-101\",\"action\":\"repair\",\"description\":\"Replaced bulb\",\"technician\":\"Tech 1\"}"
```

### Refresh lamp data
```powershell
curl http://127.0.0.1:5000/api/refresh
```

## 14. MongoDB and Redis Roles in This Project

### MongoDB role
MongoDB is used for persistent storage. It keeps records such as:
- lamp ID and details
- fault information
- power and brightness information
- maintenance history
- timestamps

### Redis role
Redis is used for quick live operations. It keeps:
- current lamp state
- summary values
- recent alerts
- fast access sets and lists for real-time monitoring

This separation is important because MongoDB is better for long-term storage, while Redis is better for fast, temporary access.

## 15. Troubleshooting
Here are common problems and their solutions:

### Problem: The app does not start
Check whether the required Python dependencies are installed.

```powershell
pip install -r requirements.txt
```

### Problem: The browser shows no dashboard
Check whether the Flask app is running successfully. If it is not, run the app again with a working Python interpreter.

### Problem: Data is not updating
Ensure that MongoDB and Redis are both running locally.

### Problem: The app works but data looks like sample data
This usually means the database is not connected or is empty. In that case, the system automatically uses fallback sample records.

### Problem: Alerts are missing
Redis may not be running or the live refresh route may not have been called.

## 16. Notes for Student Submission
This project is intentionally kept simple and readable so it remains suitable for a student assignment. It demonstrates a practical smart-city solution without overcomplicating the system. The key learning goals are:
- understanding how to build a small Flask application
- using MongoDB for persistent data storage
- using Redis for fast real-time data access
- joining frontend and backend logic
- creating a working dashboard and API-based system

## 17. Final Summary
The Smart Streetlight Management System gives a clear demonstration of how basic city infrastructure can be monitored digitally. It helps maintenance teams keep track of lamp health, identify faults quickly, store historical records, and act on live data. The system remains simple enough for a student project while still being complete and useful.
