"""
Orders router - handles order creation and management
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from ..database import get_db
from ..models.order import Order, OrderItem, OrderStatus
from ..models.product import Product
from ..models.user import User
from ..routers.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

# Pydantic schemas
class OrderItemCreate(BaseModel):
    """Schema for creating an order item"""
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    """Schema for creating an order"""
    items: List[OrderItemCreate]
    shipping_address: str
    shipping_city: str
    shipping_postal_code: str

class OrderItemResponse(BaseModel):
    """Schema for order item in responses"""
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    """Schema for order in responses"""
    id: int
    order_number: str
    total_amount: float
    status: OrderStatus
    shipping_address: str
    shipping_city: str
    shipping_postal_code: str
    created_at: str
    order_items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new order"""
    
    if not order_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )
    
    # Calculate total and validate products
    total_amount = 0
    order_items_data = []
    
    for item in order_data.items:
        # Get product and check availability
        product = db.query(Product).filter(
            Product.id == item.product_id,
            Product.is_active == True
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found"
            )
        
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}. Available: {product.stock_quantity}"
            )
        
        # Calculate item total
        item_total = product.price * item.quantity
        total_amount += item_total
        
        order_items_data.append({
            "product_id": product.id,
            "quantity": item.quantity,
            "unit_price": product.price,
            "total_price": item_total
        })
    
    # Create order
    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    new_order = Order(
        order_number=order_number,
        user_id=current_user.id,
        total_amount=total_amount,
        shipping_address=order_data.shipping_address,
        shipping_city=order_data.shipping_city,
        shipping_postal_code=order_data.shipping_postal_code
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # Create order items and update stock
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=new_order.id,
            **item_data
        )
        db.add(order_item)
        
        # Update product stock
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        product.stock_quantity -= item_data["quantity"]
    
    db.commit()
    db.refresh(new_order)
    
    return new_order

@router.get("/", response_model=List[OrderResponse])
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all orders for the current user"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific order"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order

@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    status: OrderStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update order status (Admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update order status"
        )
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.status = status
    db.commit()
    
    return {"message": f"Order status updated to {status.value}"}

@router.get("/admin/all", response_model=List[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all orders (Admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can view all orders"
        )
    
    orders = db.query(Order).all()
    return orders