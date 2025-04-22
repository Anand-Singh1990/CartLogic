# Cart Logic - Campaign Management System

This is a Django-based backend project to manage marketing campaigns, targeted users, discount applications, and campaign usage tracking.

---

## 🔧 Features

- Create and manage campaigns
- Assign campaigns to specific users
- Track campaign usage per user per day
- Apply discounts using campaigns
- Role-based access (via Django admin)

---

## 📁 Project Structure

cart_logic/
├── campaign/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── create_dummy_data.py
│   ├── models.py
│   ├── views.py
│   └── …
├── cart_logic/
│   ├── settings.py
│   ├── urls.py
│   └── …
├── manage.py
├── db.sqlite3
├── requirements.txt
└── README.md

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/cart_logic.git
cd cart_logic
```

### 2. Create and activate a virtual environment
```bash
python -m venv env
source env/bin/activate  # For Mac/Linux
env\Scripts\activate     # For Windows
```


### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create a superuser
```bash
python manage.py createsuperuser
```

### 6. Create dummy data (optional)
```bash
python manage.py create_dummy_data
```

### 7. Run the server
```bash
python manage.py runserver
```

Access the admin panel at http://localhost:8000/admin