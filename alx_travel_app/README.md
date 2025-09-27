
# alx_travel_app

A travel booking application built with **Django** and **MariaDB** as part of the ALX Software Engineering program.
It allows users to browse listings, book stays, and leave reviews.

---

## Features

* User authentication (sign up, login, logout).
* Hosts can create and manage travel listings.
* Users can browse listings and make bookings.
* Users can leave reviews on listings.
* Database seeding command for sample data.

---

## Tech Stack

* **Backend**: Django (Python 3.10+)
* **Database**: MariaDB/MySQL
* **Frontend**: Django templates (extendable to React/SPA)
* **Environment**: Docker / Virtualenv (recommended)
* **Deployment**: Gunicorn + Nginx (future scope)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/alx_travel_app.git
cd alx_travel_app
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root folder:

```ini
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

# Database connection
DATABASE_URL=mysql://alxuser:strongpass@127.0.0.1:3306/alx_travel_db
```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed database with sample data

```bash
python manage.py seed          # creates default host and 10 listings
python manage.py seed --listings 20 --force   # recreate with 20 listings
```

### 7. Run the server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Database Tables

The app uses the following core tables:

* `listings_listing` → stores travel listings.
* `listings_booking` → stores bookings by users.
* `listings_review` → stores reviews for listings.

---

## Example Users

When seeded, a host user is created:

* **Username**: `seed_host`
* **Password**: `password123` (or set in your seeder)

---

## License

This project is for educational purposes under the ALX Software Engineering program.

---
