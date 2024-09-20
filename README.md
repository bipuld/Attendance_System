## Project Overview - Attendance System  (Hajiri)
The Attendance System is a web-based application create in Djnago — a high-level Python Web framework that encourages rapid development and clean, pragmatic design.There are different classes, students and can take attendance class wise daily/weekly/monthly.

## Tech Stack 
Backend: Django
API: Django REST Framework
Database: MySQL (for localhost development)


## Challenges faced during development and how I overcame them
Challenges faced during development Process:
Multi-Tenancy Features:

Issue: The problem with tracking student attendance across different users (teachers, administrators) was that none of them could concurrently track

Resolution: I overcame this by securing the database architecture with deliberate support for multi-tenancy.
I made sure that all records of every user were only accessible to a particular user and encourage them to use the other shared data (students, classes) by joining in on it. By planning relationships logically and writing out the multiple rounds of testing performed for data integrity, we made sure each user had a feel for one seamless way to manage pay and hours.

## Features.
1.**Student Management**:
- Add Student
- Edit Student
- Delete Student
Note: - Unique Student ID per user. 
2. **Class Management** - 
Creation of classes along with students. 
- Avoid multiple inclusions of the same student for more than one class. - Multiple select field on Students list with better UX. 
3. **Attendance Tracking**: Mark students present or absent on particular dates Dynamic form to input multiple attendance records simultaneously View and search attendance records by date range 
4. **Reports** : 
- Generate attendance reports by class and date range. 
- Chart using chart An Attendance Trends App, 
- A chartjs to visualize attendance trends.


### Endpoints
#### User Authentication
- **Login:** `POST /auth/login/` - Authenticate user and retrieve JWT access token.
- **Logout:** `POST /auth/logout/` - Invalidate JWT access token and logout.

#### JWT Token Management
- **Token Refresh:** `POST /auth/token/refresh/` - Refresh JWT access token.
- **Token Verify:** `POST /auth/token/verify/` - Verify JWT access token.

## Setup and Installation

### Prerequisites
Ensure you have the following installed on your local machine:
- Python 3.12
- Django 5.1.1



### This project provides setup instructions for local development.

### Step-by-Step Setup
1. **Clone the Repository:**
git clone https://github.com/bipuld/Attendance_System.git
cd attendance_attendance
2.  **Create and Activate a Virtual Environment**:
python -m venv en
3.  **Install Required Package**:
pip install -r requirements.txt
4. **Database**:
python manage.py migrate
5. **Create a Superuser**:
python manage.py createsuperuser
Note-Create two superuser
-Admin Used
-Login only 
6. **Login Admin panel**
Assign the user to User_info and the disable that user (is_superuser,is_staff) who is assigned to userinfo  
and used that assign user as login user
6. **Load Data for testing purpouse**:
python manage.py loaddata testing_data.json 
Note-(update testing_data.json with created_by id(i.e userinfo who created this user) with user_info) and ID of userinfo can be seen through the amdin panel 
7. **Run server** :
python manage.py runserver



