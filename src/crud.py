from models import Order, Inventory
from datetime import datetime

def create_order(db, order_data):
    inventory_status = check_inventory(
        db,
        order_data.lens_type,
        order_data.power
    )
    sla_hours = get_sla_hours(order_data.lens_type)
    order = Order(
        customer_name=order_data.customer_name,
        lens_type=order_data.lens_type,
        power=order_data.power,
        inventory_status=inventory_status,
        sla_hours = sla_hours
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    return order

def get_orders(db):
    return db.query(Order).all()

def check_inventory(db, lens_type, power):
    inventory = db.query(Inventory).filter(
        Inventory.lens_type == lens_type,
        Inventory.power == power,
        Inventory.stock_count > 0
    ).first()

    if inventory:
        return "IN_HOUSE"

    return "OUTSOURCED"

def update_status(db, order_id, status):
    order = db.query(Order).filter(Order.id == order_id).first()
    order.status = status
    if status == "PRODUCTION":
        order.risk = "HIGH"

    db.commit()
    return order

def get_sla_hours(lens_type):
    sla_map = {
        "single vision": 24,
        "blue cut": 48,
        "progressive": 72,
        "tts": 48
    }

    return sla_map.get(lens_type.lower(), 48)

def calculate_sla_status(order):
    elapsed_hours = (
        datetime.utcnow() - order.created_at
    ).total_seconds() / 3600
    remaining_hours = order.sla_hours - elapsed_hours
    breached = remaining_hours < 0

    return {
        "remaining_hours": round(remaining_hours, 2),
        "breached": breached
    }

def predict_risk(order):
    if order.inventory_status == "OUTSOURCED":
        return "HIGH"

    sla_status = calculate_sla_status(order)

    if sla_status["remaining_hours"] < 12:
        return "HIGH"

    if order.status == "PRODUCTION":
        return "MEDIUM"

    return "LOW"

def update_inventory(db, inventory_id, stock_count):
    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if not inventory:
        return None

    inventory.stock_count = stock_count

    db.commit()
    db.refresh(inventory)

    return inventory