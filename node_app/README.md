# ShopEasy - E-commerce Platform

ShopEasy is a full-featured e-commerce platform built with Node.js and Express. It provides a complete online shopping experience with product catalog, shopping cart, order management, and user accounts.

## Features

- **Product Catalog**: Browse and search products with categories and filters
- **Shopping Cart**: Add products to cart, update quantities, and save for later
- **Order Management**: Place orders, track order status, and view order history
- **User Accounts**: User registration, authentication, and profile management
- **Admin Dashboard**: Manage products, orders, and users (planned)
- **Payment Integration**: Support for multiple payment methods (planned)

## Tech Stack

- Node.js 10+
- Express 4.16.0
- MongoDB with Mongoose ODM
- MySQL for relational data (dual database setup)
- JWT for authentication
- RESTful API architecture

## Getting Started

### Prerequisites
- Node.js 10 or higher
- MongoDB installed and running
- MySQL installed and running

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```
4. Start the server:
   ```bash
   npm start
   ```
5. For development with auto-restart:
   ```bash
   npm run dev
   ```
6. Visit `http://localhost:3000`

## Project Structure

- `config/` - Configuration files for databases and application settings
- `controllers/` - Request handlers for users, products, orders, carts
- `models/` - Data models for User, Product, Order, Cart
- `middleware/` - Authentication, validation, and other middleware
- `routes/` - API route definitions
- `utils/` - Utility functions and database helpers
- `public/` - Static assets (CSS, JavaScript, images)
- `views/` - Server-side rendered views (EJS templates)

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Products
- `GET /api/products` - List all products
- `GET /api/products/:id` - Get product details
- `POST /api/products` - Create a new product (admin)
- `PUT /api/products/:id` - Update product (admin)

### Cart
- `GET /api/cart/:userId` - Get user's cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update` - Update cart item quantity
- `DELETE /api/cart/remove` - Remove item from cart

### Orders
- `GET /api/orders` - List user's orders
- `POST /api/orders` - Create a new order
- `GET /api/orders/:id` - Get order details
- `PUT /api/orders/:id/status` - Update order status

## Development Notes

This repository is intentionally messy and contains a production-like project with various issues including security vulnerabilities, poor structure, duplicate logic, missing validation, no tests, and bugs in logic. The codebase serves as an exercise for developers to identify and fix these problems.

## License

MIT