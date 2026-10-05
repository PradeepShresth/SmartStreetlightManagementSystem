# Smart Streetlight Management System

## Assignment Report

### 1. Introduction
Urban infrastructure management is a key part of smart city development. Streetlights are one of the most important public services because they ensure safety, improve visibility, and support the flow of traffic during nighttime hours. Managing a large number of streetlights manually is difficult, time-consuming, and often inefficient. This project addresses that problem by developing a simple Smart Streetlight Management System that can monitor the condition of streetlights and support maintenance activities.

The system is designed as a student-friendly and practical project that demonstrates the main concepts of web application development, database management, and live data handling. It uses Python and Flask for the application layer, MongoDB for persistent data storage, and Redis for fast real-time updates. The project is intentionally simple, readable, and suitable for academic submission.

### 2. Problem Statement
The traditional method of managing streetlights is manual inspection, which creates several issues:
- maintenance teams cannot quickly determine which lights are faulty
- energy usage is difficult to monitor efficiently
- lamp status is not updated in real time
- fault records are often stored in an unstructured or informal way
- delayed maintenance can cause poor lighting conditions in public areas

This project aims to solve these issues by creating a centralized system that tracks lamp details, status, and maintenance records in an organized manner.

### 3. Objectives
The main objectives of this project are:
- to create a dashboard for streetlight monitoring
- to manage lamp records efficiently
- to detect and highlight faulty lights
- to monitor brightness and power usage
- to track maintenance activities
- to store persistent data in MongoDB
- to use Redis for live operational data and alerts
- to design a simple but effective student-level solution that satisfies the assignment requirement

### 4. Scope of the Project
The project focuses on the essential features needed for a smart streetlight system. It does not aim to be a full industrial control system, but it successfully demonstrates the core functionalities expected in a student assignment.

The system includes:
- streetlight registration
- lamp status tracking
- monitoring of brightness and energy values
- fault identification
- maintenance history records
- summary dashboard cards
- API-based interaction with data

### 5. Methodology
A practical and student-friendly development approach was used for this system.

The project followed these stages:
1. Requirement analysis of the smart streetlight system.
2. Selection of technologies suitable for a small web application.
3. Design of the application architecture.
4. Development of backend logic and API endpoints.
5. Integration with MongoDB and Redis.
6. Testing of core routes and data operations.
7. Documentation of the system for assignment submission.

### 6. Technologies and Tools Used

#### Python
Python was selected because it is simple, reliable, and suitable for creating the backend logic of the project.

#### Flask
Flask was used as the web framework to create the dashboard and handle API routes. It is lightweight and ideal for a small project such as this.

#### MongoDB
MongoDB was used as the database for long-term data storage. It stores lamp records, maintenance information, and energy-related data.

#### Redis
Redis was used as the live data layer because it supports fast access to current lamp states and recent alert information.

#### HTML and CSS
HTML and CSS were used to design a simple dashboard interface that displays the summary and lamp records clearly.

### 7. System Architecture
The system architecture is divided into three main parts:

#### Frontend layer
This layer is the dashboard shown in the browser. It displays lamp information and summary cards for the user.

#### Application logic layer
This layer is handled by Flask. It receives requests, processes them, and returns JSON responses or renders HTML pages.

#### Data layer
The data layer consists of:
- MongoDB for persistent data storage
- Redis for live state and alerts

This separation is important because MongoDB is well suited for permanent data while Redis is useful for current operational data and faster access.

### 8. Functional Requirements Implemented

#### 8.1 Lamp registration
The system allows a new streetlight to be added with fields such as lamp ID, zone, type, location, power rating, status, and fault condition.

#### 8.2 Lamp listing and monitoring
The dashboard displays all streetlights and shows whether each one is on, dim, or faulty.

#### 8.3 Summary view
The dashboard provides summary cards for:
- total lamps
- active lamps
- dim lamps
- faulty lamps
- total energy consumed

#### 8.4 Update operation
Existing streetlight data can be modified, including brightness level, status, and fault value.

#### 8.5 Delete operation
A lamp can be removed if it is decommissioned or no longer needed.

#### 8.6 Maintenance record
Users can add repair or inspection records with a description and technician name.

#### 8.7 Fault alert mechanism
Faulty lights are identified and stored in a quick alert list using Redis so that the system responds rapidly.

### 9. Data Design
The project stores streetlight information in a structured way. Each lamp contains essential fields such as:
- lamp_id
- zone
- lamp_type
- location
- power_rating
- brightness
- status
- power_usage
- fault
- energy_today_kwh
- last_updated
- maintenance_history

This structure ensures that the system can monitor each lamp effectively and keep a record of maintenance activity over time.

### 10. Implementation Details
The project was implemented using modular programming for readability and simpler maintenance.

The main files are:
- app.py - main application and API routes
- database/mongo_service.py - MongoDB operations
- database/redis_service.py - Redis data handling and alert management
- templates/dashboard.html - dashboard user interface
- static/style.css - front-end styling

This modular structure keeps the project easy to understand and suitable for a student assignment.

### 11. API Design
The application exposes the following endpoints:
- GET /
- GET /dashboard
- GET /api/summary
- GET /api/lights
- POST /api/lights
- PUT /api/lights/<lamp_id>
- DELETE /api/lights/<lamp_id>
- POST /api/maintenance
- GET /api/refresh

These routes allow the dashboard and external clients to interact with the system easily.

### 12. Testing and Verification
The system was verified by running the application and testing the main route responses.

The following checks were confirmed:
- HOME route → 200
- SUMMARY route → 200
- LIGHTS route → 200
- POST operation → 201
- MAINTENANCE route → 200
- REFRESH route → 200

These results show that the core application is working successfully and that the API is responding as expected.

### 13. Results and Discussion
The project successfully demonstrates a basic but useful smart streetlight management system. It fulfils the assignment requirement by showing how a web-based application can be connected with both MongoDB and Redis to manage city infrastructure in a practical way.

The most important result is that the project combines:
- persistent data storage in MongoDB
- quick operational data access in Redis
- web-based monitoring in Flask
- a simple dashboard for user interaction

Although the project is intentionally simple, it clearly demonstrates understanding of the required technologies and system concepts.

### 14. Challenges Encountered
During development, a few issues were addressed to make the project stable:
- database connection checks were handled carefully
- sample fallback data was added for demonstration when databases were unavailable
- JSON serialization was required for MongoDB data
- live state updates needed to work correctly with Redis data structures

These issues were resolved while keeping the code clear and student-friendly.

### 15. Conclusion
This project meets the main objectives of the assignment by creating a functional Smart Streetlight Management System that monitors streetlight operations, records maintenance activity, and stores data using MongoDB and Redis. The project is simple, easy to understand, and suitable for a student submission while still presenting a realistic smart-city application concept.

The final result shows that the student was able to apply the knowledge of web development, database integration, and live data handling to create a working and relevant system for smart infrastructure management.
