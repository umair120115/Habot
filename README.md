# HaBot API 🤖

A robust backend API built with **Django REST Framework**, featuring custom User Authentication, JWT security, and a scalable Role-Based Access Control (RBAC) system.

## 🚀 Features

- **Custom User Model:** Built on `AbstractBaseUser` using Email as the primary identifier.
- **Secure Authentication:** Implementation of `SimpleJWT` for Access and Refresh tokens.
- **Role-Based Access Control (RBAC):** Custom permission classes (`HasRolePermission`) to manage user authorization levels.
- **UUID Primary Keys:** Enhanced security and scalability using UUIDs for user IDs.
- **Scalable Architecture:** Modular Django app structure.

## 🛠 Tech Stack

- **Language:** Python 3.x
- **Framework:** Django 5.x, Django REST Framework
- **Authentication:** djangorestframework-simplejwt
- **Database:** SQLite (Default) / PostgreSQL (Production ready)

---

## ⚙️ Installation & Setup Guide

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone [https://github.com/umair120115/HaBot.git](https://github.com/umair120115/HaBot.git)
cd HaBot




2. Create a Virtual EnvironmentIsolate your project dependencies by creating a virtual environment.
Windows:Bash
python -m venv venv
macOS / Linux:Bash
python3 -m venv venv
3. Activate the EnvironmentWindows:Bash
venv\Scripts\activate
macOS / Linux:Bash
source venv/bin/activate
4. Install DependenciesBashpip install -r requirements.txt
🏃‍♂️ Running the ApplicationThis project uses a nested structure where the main Django files are located in the core directory.1. Navigate to the Project CoreYou must enter the core directory to access manage.py.Bashcd core
2. Apply Database MigrationsInitialize the database and create the custom user table.Bashpython manage.py makemigrations
python manage.py migrate
3. Create a Superuser (Admin)To access the Django Admin interface:Bashpython manage.py createsuperuser
4. Start the ServerBashpython manage.py runserver
The API will be available at: http://127.0.0.1:8000/🔌 API EndpointsAuthenticationMethodEndpointDescriptionPOST/api/signup/Register a new userPOST/api/token/Login (Obtain Access & Refresh Tokens)POST/api/token/refresh/Refresh expired Access TokenSample Request: SignupURL: /api/signup/Body (JSON):JSON{
    "email": "user@example.com",
    "password": "StrongPassword123!",
    "username": "newuser",
    "name": "John Doe"
}
📂 Project Structure
HaBot/
├── venv/                   # Virtual Environment
├── requirements.txt        # Dependencies
└── core/                   # Main Django Project Folder
    ├── manage.py           # Entry point
    ├── core/               # Settings & WSGI
    └── employee/           # App: Users, Serializers, Views
