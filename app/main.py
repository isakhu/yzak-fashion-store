"""
Main FastAPI application
This is the entry point of your e-commerce API
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .config import settings
from .database import engine, get_db
from .models import user, product, order  # Import all models
from .routers import auth, products, orders

# Create database tables
# This creates all the tables defined in your models
user.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A modern e-commerce API built with FastAPI",
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc"  # ReDoc documentation
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (API endpoints)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    """Root endpoint - Redirect to admin interface"""
    return FileResponse('static/admin.html')

@app.get("/admin")
def admin_interface():
    """Admin interface"""
    return FileResponse('static/admin.html')

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Create a default admin user on startup
@app.on_event("startup")
def create_default_admin():
    """Create a default admin user if none exists"""
    from .database import SessionLocal
    from .models.user import User
    from .routers.auth import get_password_hash
    
    db = SessionLocal()
    try:
        # Check if any admin user exists
        admin_exists = db.query(User).filter(User.is_admin == True).first()
        
        if not admin_exists:
            # Create default admin user with shorter password
            admin_user = User(
                username="admin",
                email="admin@ecommerce.com",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin"),
                is_admin=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Default admin user created: username='admin', password='admin'")
        else:
            print("✅ Admin user already exists")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )