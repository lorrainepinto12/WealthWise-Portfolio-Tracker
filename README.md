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

## 1\. Create a User

  * **Endpoint:** `POST /users/`

### Request Body (JSON)

```json
{
  "name": "Lorraine Pinto",
  "email": "lorraine@example.com"
}
```

### Response (JSON)

```json
{
  "id": 1,
  "name": "Lorraine Pinto",
  "email": "lorraine@example.com"
}
```

-----

## 2\. Get All Users

  * **Endpoint:** `GET /users/`

### Request

*No body required.*

### Response (JSON)

```json
[
  {
    "id": 1,
    "name": "Lorraine Pinto",
    "email": "lorraine@example.com"
  }
]
```

-----

## 3\. Add a Buy Transaction

  * **Endpoint:** `POST /transactions/`

### Request Body (JSON)

```json
{
  "user_id": 1,
  "symbol": "AAPL",
  "type": "BUY",
  "quantity": 5,
  "price": 180.5
}
```

### Response (JSON)

```json
{
  "id": 1,
  "user_id": 1,
  "symbol": "AAPL",
  "type": "BUY",
  "quantity": 5,
  "price": 180.5,
  "timestamp": "2025-11-11T10:23:45"
}
```

-----

## 4\. Add a Sell Transaction

  * **Endpoint:** `POST /transactions/`

### Request Body (JSON)

```json
{
  "user_id": 1,
  "symbol": "AAPL",
  "type": "SELL",
  "quantity": 2,
  "price": 190.0
}
```

### Response (JSON)

```json
{
  "id": 2,
  "user_id": 1,
  "symbol": "AAPL",
  "type": "SELL",
  "quantity": 2,
  "price": 190.0,
  "timestamp": "2025-11-11T10:28:12"
}
```

-----

## 5\. Get Portfolio Summary

  * **Endpoint:** `GET /portfolio/summary?user_id=1`

### Query Parameter

  * `user_id=1`

### Response (JSON)

```json
{
  "user_id": 1,
  "total_invested": 902.5,
  "current_value": 950.0,
  "total_profit_loss": 47.5,
  "holdings": [
    {
      "symbol": "AAPL",
      "quantity": 3,
      "average_cost": 180.5,
      "current_price": 190.0,
      "profit_loss": 28.5
    }
  ]
}
```

-----

## 6\. Get All Transactions for a User

  * **Endpoint:** `GET /transactions/{user_id}`

### Query Parameter

  * `user_id=1`

### Response (JSON)

```json
[
  {
    "id": 1,
    "symbol": "AAPL",
    "type": "BUY",
    "quantity": 5,
    "price": 180.5
  },
  {
    "id": 2,
    "symbol": "AAPL",
    "type": "SELL",
    "quantity": 2,
    "price": 190.0
  }
]
```
-----

