# 👗 Yzak Fashion Store - Ethiopian E-Commerce Platform

**Yzak Fashion Store** - A complete, production-ready **Ethiopian fashion e-commerce system** with branches in **Dire Dawa** and **Hawassa**. Built with **FastAPI**, **SQLAlchemy**, and a beautiful Amazon-style admin interface!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange.svg)
![Ethiopia](https://img.shields.io/badge/Currency-Ethiopian%20Birr-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🏪 **About Yzak Fashion Store**

**Yzak Fashion Store** is a premium Ethiopian fashion retailer with locations in:
- 📍 **Main Branch:** Dire Dawa, Ethiopia
- 📍 **Branch:** Hawassa, Ethiopia

Specializing in both traditional Ethiopian fashion and modern clothing with competitive Ethiopian Birr (ETB) pricing.

## 🌟 **Live Demo**

- **Yzak Fashion Store Admin:** `http://localhost:8000`
- **API Documentation:** `http://localhost:8000/docs`
- **Login:** Username: `admin` | Password: `admin`

## ✨ **Features**

### 🇪🇹 **Ethiopian Fashion-Focused Admin Interface**
- **Beautiful Dashboard** - Modern, responsive design for Ethiopian fashion retail
- **Ethiopian Birr (ETB) Pricing** - All prices displayed in local currency
- **Traditional & Modern Fashion** - Support for both traditional Ethiopian and modern clothing
- **Image Support** - Product images for better visual management
- **Size & Color Management** - Ethiopian sizing and color preferences
- **Category Organization** - Women's/Men's Clothing and Footwear categories

### 🔧 **Technical Features**
- **JWT Authentication** - Secure token-based auth
- **RESTful API** - Clean, documented endpoints
- **Fashion Data Models** - Size, color, image, and category attributes
- **Ethiopian Birr Support** - Local currency integration
- **Input Validation** - Pydantic models for fashion data
- **Error Handling** - Comprehensive error responses
- **Auto Documentation** - Swagger UI and ReDoc

### 🛡️ **Security & Best Practices**
- Password hashing with bcrypt
- JWT token authentication
- SQL injection prevention
- Input sanitization
- CORS configuration
- Environment variable management

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)

### **Installation**

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/ethiopian-fashion-store.git
cd ethiopian-fashion-store
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment:**
```bash
cp .env.example .env
```

4. **Initialize database with Ethiopian fashion data:**
```bash
python init_db.py
```

5. **Start the server:**
```bash
python -m app.main
```

6. **Open your browser:**
- Ethiopian Fashion Store Admin: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🇪🇹 **Sample Ethiopian Fashion Products**

### **Traditional Ethiopian Fashion**
- **Traditional Ethiopian Dress** - ETB 4,599.99
- **Habesha Kemis** - Traditional white dress with colorful borders

### **Modern Fashion Items**
- **Elegant Black Dress** - ETB 2,699.99
- **Classic White Sneakers** - ETB 2,399.99
- **Men's Casual Shirt** - ETB 1,399.99
- **Leather Boots** - ETB 3,899.99
- **Women's High Heels** - ETB 1,899.99

## 📱 **Screenshots**

### Ethiopian Fashion Admin Dashboard
![Ethiopian Fashion Dashboard](https://via.placeholder.com/800x400/667eea/ffffff?text=Ethiopian+Fashion+Store+Dashboard)

### Product Management with ETB Pricing
![ETB Product Management](https://via.placeholder.com/800x400/764ba2/ffffff?text=Ethiopian+Birr+Product+Management)

## 🏗️ **Project Structure**

```
ethiopian-fashion-store/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup and connection
│   ├── models/              # SQLAlchemy database models
│   │   ├── user.py          # User model
│   │   ├── product.py       # Product & Category models
│   │   └── order.py         # Order & OrderItem models
│   └── routers/             # API route handlers
│       ├── auth.py          # Authentication endpoints
│       ├── products.py      # Product management endpoints
│       └── orders.py        # Order management endpoints
├── static/
│   └── admin.html           # Beautiful Ethiopian fashion admin interface
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── init_db.py              # Database initialization with Ethiopian data
└── README.md               # This file
```

## 🔌 **API Endpoints**

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Products
- `GET /products/` - List products (with pagination & filters)
- `POST /products/` - Create product (admin only)
- `GET /products/{id}` - Get specific product
- `PUT /products/{id}` - Update product (admin only)
- `DELETE /products/{id}` - Delete product (admin only)

### Categories
- `GET /products/categories` - List categories
- `POST /products/categories` - Create category (admin only)

### Orders
- `POST /orders/` - Create new order
- `GET /orders/` - Get user's orders
- `GET /orders/{id}` - Get specific order
- `PUT /orders/{id}/status` - Update order status (admin only)
- `GET /orders/admin/all` - Get all orders (admin only)

## 🧪 **Testing**

Run the test script to verify everything works:
```bash
python test_login.py
```

## 🌐 **Deployment**

This Ethiopian fashion store is ready for deployment on:
- **Heroku** - Web applications
- **Railway** - Modern deployment platform  
- **DigitalOcean** - Cloud servers
- **AWS** - Enterprise cloud
- **Vercel** - Serverless deployment

## �️ **Builte With**

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Python SQL toolkit and ORM
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type annotations
- **[JWT](https://jwt.io/)** - JSON Web Tokens for authentication
- **[Passlib](https://passlib.readthedocs.io/)** - Password hashing library
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server implementation

## 💰 **Ethiopian Birr (ETB) Integration**

All prices are displayed in Ethiopian Birr with proper formatting:
- Traditional Ethiopian Dress: **ETB 4,599.99**
- Modern Fashion Items: **ETB 1,399.99 - ETB 3,899.99**
- Automatic ETB currency symbol display
- Local pricing suitable for Ethiopian market

## 👨‍💻 **Developer**

**Your Name** - *Full Stack Developer*
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)
- Email: your.email@example.com

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 **Contributing**

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 **Acknowledgments**

- FastAPI team for the amazing framework
- SQLAlchemy for the powerful ORM
- The Python community for excellent libraries
- Ethiopian fashion community for inspiration

---

⭐ **Star this repository if it helped you build your Ethiopian fashion store!**