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
<pre lang="bash">
cart_logic/
├── campaign/                       # App to manage campaigns
│   ├── init.py
│   ├── admin.py
│   ├── apps.py
│   ├── constants.py                # All constants used across campaign models
│   ├── management/
│   │   └── commands/
│   │       └── create_dummy_data.py  # Script to create dummy users & campaigns
│   ├── migrations/
│   │   └── init.py
│   ├── models.py                   # Models like Campaign, CampaignCustomer, etc.
│   ├── tests.py
│   └── views.py
│   └──
├── cart_logic/                     # Project settings directory
│   ├── init.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3                      # SQLite database (if used)
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
</pre>
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
Access the API Docs panel at http://localhost:8000/api-documentation/