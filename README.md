# 📦 Inventory Management System

A production-style mini ERP system built with Django REST Framework and vanilla HTML/JS frontend. Designed for small to medium businesses to track stock, record sales & purchases, and monitor profit/loss in real time.

---

## 🚀 Features

- **Stock Tracking** — Real-time inventory management with auto stock update on every sale/purchase
- **Sales & Purchase Records** — Complete transaction history with profit calculation per sale
- **Dashboard Analytics** — Today's revenue, profit, sales count, top products, and low stock alerts
- **Role-Based Access** — Admin, Manager, and Staff roles with different permission levels
- **Low Stock Alerts** — Automatic detection when stock falls below threshold
- **JWT Authentication** — Secure token-based login system

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2 + Django REST Framework |
| Database | PostgreSQL |
| Authentication | JWT (djangorestframework-simplejwt) |
| Frontend | HTML, CSS, Vanilla JavaScript |
| CORS | django-cors-headers |

---

## 📁 Project Structure

```
inventory_system/
│
├── config/                  # Django project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                # Custom User model with roles
│   ├── models.py            # User (Admin / Manager / Staff)
│   └── permissions.py       # Role-based permission classes
│
├── inventory/               # Products & Categories
│   ├── models.py            # Category, Product
│   ├── serializers.py
│   └── views.py
│
├── transactions/            # Sales & Purchases
│   ├── models.py            # Sale, Purchase
│   ├── serializers.py
│   ├── views.py
│   └── signals.py           # Auto stock update on save
│
├── dashboard/               # Analytics API
│   └── views.py             # Revenue, Profit, Low Stock, Top Products
│
├── frontend/                # HTML/JS UI
│   ├── login.html
│   ├── index.html           # Dashboard
│   ├── products.html
│   ├── sales.html
│   ├── purchases.html
│   └── js/
│       └── api.js           # Shared API utility functions
│
├── .env                     # Environment variables (never commit this)
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/inventory-system.git
cd inventory-system
```

### 2. Create & activate virtual environment

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL database

Open pgAdmin4 or psql and run:

```sql
CREATE DATABASE inventory_db;
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key-here
DB_NAME=inventory_db
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run migrations

```bash
python manage.py makemigrations accounts inventory transactions
python manage.py migrate
```

### 7. Create superuser

```bash
python manage.py createsuperuser
```

### 8. Start the server

```bash
python manage.py runserver
```

### 9. Open frontend

Serve the `frontend/` folder using any static server:

```bash
cd frontend
python -m http.server 3000
```

Open `http://localhost:3000/login.html` in your browser.

---

## 🔑 API Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/token/` | Public | Login & get JWT token |
| POST | `/api/token/refresh/` | Public | Refresh access token |
| GET | `/api/products/` | All users | List all products |
| POST | `/api/products/` | Manager+ | Add new product |
| GET | `/api/products/low-stock/` | All users | Low stock items |
| GET/POST | `/api/categories/` | All users / Manager+ | Categories |
| GET/POST | `/api/sales/` | Manager+ | Sales records |
| GET/POST | `/api/purchases/` | Manager+ | Purchase records |
| GET | `/api/dashboard/` | All users | Analytics summary |

---

## 🧠 Key Design Decisions

### Auto Stock Update via Django Signals
Stock updates automatically when a sale or purchase is saved — no manual update needed.

```python
# transactions/signals.py
@receiver(post_save, sender=Sale)
def update_stock_on_sale(sender, instance, created, **kwargs):
    if created:
        instance.product.current_stock -= instance.quantity
        instance.product.save(update_fields=['current_stock'])
```

### Profit Calculated at DB Level
Instead of computing profit in Python loops, we use Django ORM expressions for efficiency.

```python
today_profit = Sale.objects.aggregate(
    profit=Sum(
        ExpressionWrapper(
            (F('unit_price') - F('product__cost_price')) * F('quantity'),
            output_field=DecimalField()
        )
    )
)['profit']
```

### Role-Based Permissions
Three roles — Admin, Manager, Staff — with clear access boundaries defined in `accounts/permissions.py`.

---

## 🔒 Security Notes

- `SECRET_KEY` and database credentials are stored in `.env` — never hardcoded
- `.env` is listed in `.gitignore` — never pushed to version control
- JWT tokens expire automatically
- `CORS_ALLOW_ALL_ORIGINS = True` is for development only — restrict in production

---

## 🌱 Future Improvements

- [ ] Purchase page UI
- [ ] PDF invoice generation for sales
- [ ] Date range filter for analytics
- [ ] Monthly/weekly profit chart
- [ ] Low stock email notifications
- [ ] Multi-branch support
- [ ] Production deployment (Nginx + Gunicorn)

---

## 📦 Requirements

```
django==4.2
djangorestframework==3.15
psycopg2-binary==2.9.9
django-filter==23.5
python-decouple==3.8
djangorestframework-simplejwt==5.3
django-cors-headers==4.3
```

---

## 👨‍💻 Author

Built as a learning project — mini ERP system with Django REST Framework.

> ⚠️ This project is for educational purposes. Review security settings before deploying to production.