from sqlalchemy import Column, Integer, String, DateTime, Float
from database import Base
import datetime

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    lens_type = Column(String)
    status = Column(String, default="PLACED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    sla_hours = Column(Float, default=48)
    risk = Column(String, default="LOW")
    power = Column(String)
    inventory_status = Column(String, default="PENDING")

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    power = Column(String)
    lens_type = Column(String)
    stock_count = Column(Integer)