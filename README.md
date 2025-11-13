# WealthWise Portfolio Tracker

A **FastAPI-based backend** that helps users manage investment portfolios by tracking their holdings, transactions, and overall portfolio performance.

Built with **Python**, **FastAPI**, and **PostgreSQL**, this project demonstrates **RESTful API design**, database integration with **SQLAlchemy ORM**, and a proper backend structure for scalability.

-----

## Features

  * **User Management** — Create and fetch user profiles.
  * **Portfolio Summary** — Get total holdings, current value, and realized/unrealized gains.
  * **Transaction Management** — Add and view buy/sell transactions with validation.
  * **Error Handling & Data Validation** — Implemented using Pydantic schemas.

-----

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI | High-performance API development |
| **Database** | PostgreSQL | Robust and scalable data storage |
| **ORM** | SQLAlchemy | Python SQL Toolkit and Object Relational Mapper |
| **Validation** | Pydantic | Data validation and settings management |
| **Server** | Uvicorn | ASGI server for running the application |

-----

## Project Structure

```
WealthWise-Portfolio-Tracker/
│
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application entry point
│   ├── database.py         # Database session setup
│   ├── models.py           # SQLAlchemy ORM models
│   ├── schemas.py          # Pydantic data schemas
│   ├── crud.py             # Create, Read, Update, Delete functions
│   ├── routes/
│   │   ├── users.py        # API endpoints for User Management
│   │   ├── transactions.py # API endpoints for Transaction Management
│   │   └── portfolio.py    # API endpoints for Portfolio Summary
│
├── setup.sql               # Database schema and initial data script
├── requirements.txt        # Python package dependencies
└── README.md
```

-----

## Setup Instructions

### 1\. Clone the repository

```bash
git clone https://github.com/lorrainepinto12/WealthWise-Portfolio-Tracker.git
cd WealthWise-Portfolio-Tracker
```

### 2\. Create and activate a virtual environment

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install dependencies

```bash
pip install -r requirements.txt
```

### 4\. Configure environment variables

Create a file named **`.env`** in the project root directory and add your database connection string:

```
DATABASE_URL=postgresql://username:password@localhost:5432/wealthwise_db
```

### 5\. Initialize the database

You can use the provided `setup.sql` script to create the necessary schema and insert sample data. Ensure your PostgreSQL service is running.

```bash
psql -U postgres -d wealthwise_db -f setup.sql
```

*Note: You may need to adjust the command based on your PostgreSQL setup.*

### 6\. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

The application will be live at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

-----

## API Documentation

FastAPI automatically generates interactive API documentation:

  * **Swagger UI** → `http://127.0.0.1:8000/docs`
    
-----
Here is the improved structure for the "Example API Calls" section, using clear headings and code blocks for readability, similar to standard API documentation.

# Example API Calls

Below are example requests to demonstrate the core functionality of the API. Assume the server is running at `http://127.0.0.1:8000`.

-----

## **1. Users**

### **1.1 Create User**

**POST** `/users`

**Description:** Create a new user in the system.



**Request Body**

```json
{
  "name": "Test User",
  "email": "testuser@example.com"
}
```

**Response**

```json
{
  "id": 8,
  "name": "Test User",
  "email": "testuser@example.com"
}
```

---

### **1.2 Get All Users**

**GET** `/users`

**Description:** Fetch all registered users.

**Response**

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  {
    "id": 2,
    "name": "Jane Doe",
    "email": "jane@example.com"
  }
]
```

---

### **1.3 Get User by ID**

**GET** `/users/{user_id}`

**Description:** Retrieve details for a specific user by ID.

**Example**

```
GET /users/2
```

**Response**

```json
{
  "id": 2,
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

---

### **1.4 Get User by ID (User Not Found)**

**Example**

```
GET /users/12
```

**Response**

```json
{
  "detail": "User not found"
}
```

---

## **2. Transactions**

### **2.1 Create BUY Transaction**

**POST** `/transactions`

**Description:** Record a BUY transaction for a user.

**Request Body**

```json
{
  "user_id": 8,
  "symbol": "TCS",
  "type": "BUY",
  "units": 5,
  "price": 3200,
  "date": "2025-11-10"
}
```

**Response**

```json
{
  "id": 15,
  "user_id": 8,
  "symbol": "TCS",
  "type": "BUY",
  "units": 5,
  "price": 3200,
  "date": "2025-11-10"
}
```

---

### **2.2 Create SELL Transaction (Valid)**

**POST** `/transactions`

**Description:** Record a valid SELL transaction for a user.

**Request Body**

```json
{
  "user_id": 8,
  "symbol": "TCS",
  "type": "SELL",
  "units": 2,
  "price": 3400,
  "date": "2025-05-15"
}
```

**Response**

```json
{
  "id": 16,
  "user_id": 8,
  "symbol": "TCS",
  "type": "SELL",
  "units": 2,
  "price": 3400,
  "date": "2025-05-15"
}
```

---

### **2.3 Create SELL Transaction (Exceeds Holdings)**

**Request Body**

```json
{
  "user_id": 8,
  "symbol": "TCS",
  "type": "SELL",
  "units": 100,
  "price": 3400,
  "date": "2025-05-15"
}
```

**Response**

```json
{
  "detail": "Not enough units to sell for symbol: TCS"
}
```

---

### **2.4 Invalid Symbol**

**Request Body**

```json
{
  "user_id": 1,
  "symbol": "INVALID",
  "type": "BUY",
  "units": 1,
  "price": 100,
  "date": "2025-05-10"
}
```

**Response**

```json
{
  "detail": "Invalid symbol: INVALID"
}
```

---

### **2.5 Invalid Transaction Type**

**Request Body**

```json
{
  "user_id": 1,
  "symbol": "TCS",
  "type": "NEITHER",
  "units": 1,
  "price": 100,
  "date": "2025-05-10"
}
```

**Response**

```json
{
  "detail": "Invalid transaction type: NEITHER. Must be 'BUY' or 'SELL'."
}
```

---

### **2.6 Get Transactions by User**

**GET** `/transactions/{user_id}`

**Example**

```
GET /transactions/8
```

**Response**

```json
[
  {
    "id": 15,
    "user_id": 8,
    "symbol": "TCS",
    "type": "BUY",
    "units": 5,
    "price": 3200,
    "date": "2025-11-10"
  },
  {
    "id": 16,
    "user_id": 8,
    "symbol": "TCS",
    "type": "SELL",
    "units": 2,
    "price": 3400,
    "date": "2025-05-15"
  }
]
```

---

### **2.7 Get Transactions (User Not Found)**

```
GET /transactions/15
```

**Response**

```json
{
  "detail": "User not found"
}
```

---

## **3. Portfolio**

### **3.1 Get Portfolio Summary**

**GET** `/portfolio/summary?user_id={user_id}`

**Example**

```
GET /portfolio/summary?user_id=1
```

**Response**

```json
{
    "user_id": 1,
    "holdings": [
        {
            "symbol": "TCS",
            "units": 1.0,
            "avg_cost": 3200.0,
            "current_price": 3400.0,
            "unrealized_pl": 200.0
        },
        {
            "symbol": "INFY",
            "units": 5.0,
            "avg_cost": 1500.0,
            "current_price": 1500.0,
            "unrealized_pl": 0.0
        },
        {
            "symbol": "HDFC",
            "units": 6.0,
            "avg_cost": 2500.0,
            "current_price": 2500.0,
            "unrealized_pl": 0.0
        },
        {
            "symbol": "HUL",
            "units": 4.0,
            "avg_cost": 2800.0,
            "current_price": 2800.0,
            "unrealized_pl": 0.0
        }
    ],
    "total_value": 37100.0,
    "total_gain": 200.0
}
```


