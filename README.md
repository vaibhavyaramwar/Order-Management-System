# Order Management System

## Overview
The Order Management System is a FastAPI-based application designed to manage products and orders. It provides APIs for creating, updating, retrieving, and deleting products and orders, along with handling stock management and order statuses.

## Features
- **Product Management**:
  - Create, retrieve, update, and delete products.
  - Manage product stock and pricing.
- **Order Management**:
  - Create, retrieve, update, and delete orders.
  - Handle order statuses (e.g., PENDING, SHIPPED, DELIVERED, CANCELLED, PAID).
  - Validate stock availability during order creation.
- **Centralized Response Handling**:
  - Unified response format using `CommonResponseUtil`.
- **Database Integration**:
  - SQLAlchemy ORM for database operations.
  - SQLite as the database backend.
- **Validation**:
  - Pydantic models for request and response validation.
  - Enum-based status validation.

## Project Structure
```
Order-Management-System/
├── OrderService.py          # Main entry point for the FastAPI application
├── requirements.txt         # Python dependencies
├── Apps/                    # Application-specific modules
│   ├── Order/               # Order-related services
│   ├── Product/             # Product-related services
│   └── Response/            # Response models
├── Database/                # Database models and utilities
├── Modules/                 # Pydantic models for validation
├── Tests/                   # Test cases
├── Utils/                   # Utility functions and Enums
└── ecommerce.db             # SQLite database file
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Order-Management-System
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn OrderService:app --reload
   ```

5. Access the API documentation at:
   - Swagger UI: [https://order-management-system-xggd.onrender.com/docs]
   - ReDoc: [https://order-management-system-xggd.onrender.com/redoc]

## API Endpoints
### Product Endpoints
- **POST /products**: Create a new product.
- **GET /products**: Retrieve all products with pagination.
- **GET /products/{product_id}**: Retrieve a product by ID.
- **DELETE /products/{product_id}**: Delete a product by ID.

### Order Endpoints
- **POST /orders**: Create a new order.
- **GET /orders/{order_id}**: Retrieve an order by ID.
- **PUT /orders/{order_id}**: Update the status of an order.
- **DELETE /orders/{order_id}**: Delete an order if not in a terminal state.

## Database
- **SQLite** is used as the database backend.
- SQLAlchemy ORM is used for database operations.
- The database file is `ecommerce.db`.

## Validation
- **Pydantic Models**:
  - `ProductBO`: Validates product-related requests.
  - `OrderBO`: Validates order-related requests.
  - `OrderResponse` and `ProductResponse`: Define response structures.
- **Enums**:
  - `OrderStatus`: Defines valid order statuses (PENDING, SHIPPED, DELIVERED, CANCELLED, PAID).

## Testing
- Test cases are located in the `Tests/` directory.
- Use `pytest` to run the tests:
  ```bash
  pytest
  ```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.
