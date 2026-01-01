"""
Product model - represents products in the e-commerce store
"""
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Category(Base):
    """Category model for organizing products"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship: One category can have many products
    products = relationship("Product", back_populates="category")

class Product(Base):
    """Product model for store items"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    sku = Column(String, unique=True, index=True)  # Stock Keeping Unit
    is_active = Column(Boolean, default=True)
    image_url = Column(String)
    
    # Foreign key to link product to category
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship: Each product belongs to one category
    category = relationship("Category", back_populates="products")