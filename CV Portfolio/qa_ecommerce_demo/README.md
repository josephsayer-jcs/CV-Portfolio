# QA E-commerce Demo

A deliberately small Flask e-commerce application intended as a target system for a software test automation portfolio.

## Features

- Product catalogue and search
- User registration and login
- Shopping basket
- Checkout
- Order history
- JSON REST API
- SQLite database
- Seeded demo data

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
python run.py
```

Open http://localhost:5000

Demo account:

- Username: `alice`
- Password: `Password123!`

## API

Useful endpoints:

- `GET /api/products`
- `GET /api/products/<id>`
- `POST /api/register`
- `POST /api/login`
- `GET /api/orders`
- `POST /api/orders`
- `GET /api/orders/<id>`

The API uses simple JSON authentication for portfolio purposes; this is not production security.

## Suggested automation exercises

Start by treating this as an application handed to you by a development team.

### UI
- Login/logout
- Registration validation
- Product search
- Product details
- Add/remove basket items
- Quantity changes
- Checkout
- Order history

### API
- Status codes
- Request validation
- Authentication
- Authorisation
- Response schemas
- Boundary values
- Invalid IDs
- Duplicate/invalid requests

### Database
- Verify orders and order items
- Verify totals
- Verify stock changes
- Verify user/order relationships

### CI
Run the automation suite against this application in GitHub Actions.

## Intentionally imperfect areas

This project is intentionally simple and contains behaviours that are useful for testing exercises. Some are design shortcuts rather than guaranteed defects. A strong portfolio approach is to discover and document the behaviour rather than assume it is a bug.

Do not use this application for real payments or sensitive information.
