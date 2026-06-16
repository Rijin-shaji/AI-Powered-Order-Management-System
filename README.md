## AI-Powered Order Management System

An AI-assisted order management system for an eyewear brand that handles order lifecycle tracking, inventory validation, SLA monitoring, risk prediction, and alert generation.

## Features

## Lens Inventory Management

* Store lens inventory
* Check lens availability during order creation
* Identify whether lenses are available in-house or require outsourcing

### Order Lifecycle Management

* Create orders
* Update order status
* Track order progress through fulfilment stages

### SLA Monitoring

* Assign SLA based on lens type
* Calculate remaining SLA time
* Detect SLA breaches

### AI Risk Prediction

* Predict orders likely to miss SLA
* Risk categories:

  * HIGH
  * MEDIUM
  * LOW

### Dashboard

* View all active orders
* View inventory status
* View risk levels
* View SLA information

### Alert System

* Generate alerts for:

  * High-risk orders
  * SLA breaches
  * Orders nearing SLA deadlines

## Technology Stack

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Eluno
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

## API Documentation

After starting the server:

```text
http://127.0.0.1:8000/docs
```

## Available APIs

### Orders

* POST /orders
* GET /orders
* PATCH /orders/{order_id}

### Inventory

* POST /inventory
* GET /inventory
* PATCH /inventory/{inventory_id}

### SLA

* GET /orders/{order_id}/sla

### Risk Prediction

* GET /orders/{order_id}/risk

### Dashboard

* GET /dashboard

### Alerts

* GET /alerts

## AI Logic

The current implementation uses a rule-based AI engine.

Risk is predicted using:

* Inventory availability
* Remaining SLA time
* Order status

Future versions can be extended using machine learning models trained on historical order data.

## Author

Developed as part of the Eluno AI Product Engineer assessment.

