# 💰 Smart Expense Tracker

This repository contains a full-stack web application for tracking personal expenses using Flask. The application allows users to manage their financial records, visualize spending habits through interactive charts, manage categories, and customize the interface with a Dark/Light mode toggle.

---

## 🧠 Features

- User Authentication: Secure Login and Registration system using Flask-Login.
- Dashboard: Interactive financial overview with real-time clock and date display.
- Data Visualization: Dynamic bar charts using Chart.js to visualize expenses by category.
- Expense Management: CRUD (Create, Read, Update, Delete) operations for transaction records.
- Category Management: CRUD operations for expense categories.
- Modern UI/UX: Responsive design with Bootstrap 5, Glassmorphism effects, and native Dark/Light mode support.
- Database: Persistent storage using SQLite and SQLAlchemy ORM.

---

## 🛠️ Tech Stack

- **Python** 
- **Flask**
- **Flask-SQLAlchemy** 
- **Flask-Login** 
- **SQLite** 
- **Bootstrap 5**
- **Chart.js** 
- **Vanilla JavaScript** 

---

## 📁 Project Structure

```
flask-expense-tracker-webapp/
│
├── static/
│   └── css/
│       └── style.css       # Custom styling and theme variables
│
├── templates/
│   ├── add_category.html   # Form to add new categories
│   ├── add_expense.html    # Form to add new expenses
│   ├── base.html           # Base template with Navbar & Footer
│   ├── categories.html     # List of categories
│   ├── dashboard.html      # Main dashboard with Charts & Stats
│   ├── edit_expense.html   # Form to edit existing expenses
│   ├── login.html          # User login page
│   └── register.html       # User registration page
│
├── app.py                  # Main application entry point & routes
├── models.py               # Database models (User, Expense, Category)
├── requirements.txt        
└── README.md               
```

---

## 🚀 How to Run

To run this project on your local machine, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/abidalfrz/flask-expense-tracker-webapp.git
cd flask-expense-tracker-webapp
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Linux/macOS
venv\Scripts\activate.bat     # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Run the Flask application
python app.py

# The API will be accessible at http://localhost:5000
```

### 5. Access the Application
Open your web browser and navigate to `http://localhost:5000` to access the Smart Expense Tracker application.

1. Register a new user account.
2. Log in with your credentials.
3. Start managing your expenses and categories!

---





