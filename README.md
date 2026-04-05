# Travel Planner API

Professional RESTful service for managing travel projects and trip planning. Integrated with the **Art Institute of Chicago API** to validate and fetch real-world locations.

---

##  Architecture & Design Patterns

The project is built using a **Layered Architecture (Clean Architecture lite)**. This ensures high maintainability and testability by separating concerns:

1.  **Data Layer (Models):** Defined with modern Django constraints (`UniqueConstraint`). Business states like `is_completed` are calculated dynamically to maintain a single source of truth in the DB.
2.  **Service Layer (Business Logic):** All heavy lifting is moved to `services.py`. This includes external API calls, transaction management (`@transaction.atomic`), and complex validation rules (e.g., deletion constraints).
3.  **Validation Layer (Serializers):** Responsible for data integrity, checking limits (max 10 places), and preventing duplicate entries in a single request.
4.  **Controller Layer (Thin Views):** Views are kept strictly minimal. They only handle request/response flow and delegate all logic to the Service layer.

---

##  Tech Stack

* **Framework:** Django + Django REST Framework (DRF)
* **Database:** SQLite (Default for easy testing)
* **External Integration:** Requests (Art Institute of Chicago API)
* **Environment:** django-environ (Twelve-Factor App methodology)

---

##  Installation & Setup

Follow these steps to get the environment ready:

### 1. Clone & Environment
```
git clone https://github.com/SueRix/Interview_task_DevelopsToday
cd travel_config
```
# Create virtual environment
```
python -m venv venv
```
# Activate (Windows)
```
venv\Scripts\activate
```
# Activate (macOS/Linux)
```
source venv/bin/activate
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Database Setup
```
python manage.py migrate
```

### 4. Run the App
```
python manage.py runserver
```


# API Usage Guide (How to Test)

### Create a Project with Places
POST ```/api/projects/```
Use this JSON to test real-time validation with the Chicago Art API:

JSON
```
{
  "name": "Chicago Culture Trip",
  "description": "Weekend exploring art museums.",
  "start_date": "2026-05-20",
  "places": [
    {
      "external_id": "129884",
      "notes": "Must see Starry Night!"
    },
    {
      "external_id": "117266",
      "notes": "City Landscape"
    }
  ]
}
```

### Mark a Place as Visited

PATCH ```/api/projects/1/places/1/```

JSON
```
{
  "is_visited": true,
  "notes": "Update: It was breathtaking!"
}
```
### Add a Place to an Existing Project

POST ``` /api/projects/1/places/``` 

JSON
```
{
  "external_id": "27992",
  "notes": "American Gothic - Grant Wood"
}
``` 

### Try to DELETE the project at
DELETE ```/api/projects/1/.```

Expected Result: 400 Bad Request. The system prevents deletion because the project has visited places (as per requirements).

### Endpoints Summary

GET ```/api/projects/``` - List all travel projects

POST ```/api/projects/```, - Create project (nested places supported)

GET ```/api/projects/<id>/``` - Retrieve project (shows is_completed status)

DELETE ```/api/projects/<id>/``` - Delete project (if safe)

POST ```/api/projects/<id>/places/``` - Add new place to existing project

PATCH``` /api/projects/<id>/places/<id>/``` - Update place/Mark as visited
