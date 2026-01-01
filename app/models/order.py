"""
Order models - handles customer orders and order items
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base

class OrderStatus(enum.Enum):
    """Enum for order status - defines possible order states"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    """Order model - represents a customer's order"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True, nullable=False)
    
    # Link to user who made the order
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Order details
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    
    # Shipping information
    shipping_address = Column(String, nullable=False)
    shipping_city = Column(String, nullable=False)
    shipping_postal_code = Column(String, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")  # Link to User model
    order_items = relationship("OrderItem", back_populates="order")  # Order can have many items

class OrderItem(Base):
    """OrderItem model - individual items within an order"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Item details
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # Price at time of order
    total_price = Column(Float, nullable=False)  # quantity * unit_price
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")