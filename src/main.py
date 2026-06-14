from src.database import engine, Base, SessionLocal
from src.models import Inventory, Order
from src import schemas
from src import crud
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/orders")
def create_order(order: schemas.OrderCreate, db=Depends(get_db)):
    return crud.create_order(db, order)

@app.get("/orders")
def get_orders(db=Depends(get_db)):
    return crud.get_orders(db)

@app.patch("/orders/{order_id}")
def update_order(order_id: int, status: str, db=Depends(get_db)):
    return crud.update_status(db, order_id, status)

@app.post("/inventory")
def create_inventory(
    power: str,
    lens_type: str,
    stock_count: int,
    db=Depends(get_db)
):
    inventory = Inventory(
        power=power,
        lens_type=lens_type,
        stock_count=stock_count
    )

    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    return inventory

@app.get("/orders/{order_id}/sla")
def get_order_sla(order_id: int, db=Depends(get_db)):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    return crud.calculate_sla_status(order)

@app.get("/orders/{order_id}/risk")
def get_order_risk(order_id: int, db=Depends(get_db)):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    return {
        "order_id": order.id,
        "risk": crud.predict_risk(order)
    }

@app.get("/dashboard")
def dashboard(db=Depends(get_db)):
    orders = crud.get_orders(db)

    result = []

    for order in orders:
        sla_data = crud.calculate_sla_status(order)

        result.append({
            "id": order.id,
            "customer_name": order.customer_name,
            "lens_type": order.lens_type,
            "status": order.status,
            "inventory_status": order.inventory_status,
            "risk": crud.predict_risk(order),
            "remaining_hours": sla_data["remaining_hours"],
            "breached": sla_data["breached"]
        })

    return result

@app.get("/inventory")
def get_inventory(db=Depends(get_db)):
    return db.query(Inventory).all()

@app.patch("/inventory/{inventory_id}")
def update_inventory(
    inventory_id: int,
    stock_count: int,
    db=Depends(get_db)
):
    inventory = crud.update_inventory(
        db,
        inventory_id,
        stock_count
    )

    if not inventory:
        return {"error": "Inventory not found"}

    return inventory

@app.get("/alerts")
def get_alerts(db=Depends(get_db)):
    orders = crud.get_orders(db)

    alerts = []

    for order in orders:
        sla_data = crud.calculate_sla_status(order)
        risk = crud.predict_risk(order)

        if risk == "HIGH" or sla_data["breached"] or sla_data["remaining_hours"] < 12:
            alerts.append({
                "order_id": order.id,
                "customer_name": order.customer_name,
                "risk": risk,
                "remaining_hours": sla_data["remaining_hours"],
                "breached": sla_data["breached"]
            })

    return alerts
