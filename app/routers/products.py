"""
Products router - handles all product-related API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..models.product import Product, Category
from ..models.user import User
from ..routers.auth import get_current_user

# Create router
router = APIRouter(prefix="/products", tags=["Products"])

# Pydantic schemas
class CategoryCreate(BaseModel):
    """Schema for creating a category"""
    name: str
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    """Schema for category in responses"""
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    """Schema for creating a product"""
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    sku: str
    category_id: int
    image_url: Optional[str] = None

class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    image_url: Optional[str] = None

class ProductResponse(BaseModel):
    """Schema for product in responses"""
    id: int
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int
    sku: str
    is_active: bool
    image_url: Optional[str]
    category: CategoryResponse
    
    class Config:
        from_attributes = True

# Category endpoints
@router.post("/categories", response_model=CategoryResponse)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new product category (Admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create categories"
        )
    
    # Check if category already exists
    existing_category = db.query(Category).filter(Category.name == category_data.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    new_category = Category(**category_data.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Get all active categories"""
    categories = db.query(Category).filter(Category.is_active == True).all()
    return categories

# Product endpoints
@router.post("/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new product (Admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create products"
        )
    
    # Check if category exists
    category = db.query(Category).filter(Category.id == product_data.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Check if SKU already exists
    existing_product = db.query(Product).filter(Product.sku == product_data.sku).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists"
        )
    
    new_product = Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of products to return"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    search: Optional[str] = Query(None, description="Search in product names"),
    db: Session = Depends(get_db)
):
    """Get products with optional filtering and pagination"""
    query = db.query(Product).filter(Product.is_active == True)
    
    # Apply filters
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    # Apply pagination
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a product (Admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update products"
        )
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update only provided fields
    update_data = product_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft delete a product (Admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete products"
        )
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Soft delete - just mark as inactive
    product.is_active = False
    db.commit()
    
    return {"message": "Product deleted successfully"}