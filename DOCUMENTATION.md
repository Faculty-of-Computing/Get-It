# Get-It: Your Trusted E-commerce Platform

**Get-It** is a web-based e-commerce application designed to provide users with a seamless shopping experience. Built with Python's Flask framework, it offers features like product browsing, cart management, order placement, and user account management. The application is scalable, responsive, and integrates payment gateways for secure transactions.

---

## Features

- **User Authentication**: Secure login, registration, and account management.
- **Product Management**: Add, edit, and categorize products.
- **Cart Functionality**: Add items to the cart, view cart details, and remove items.
- **Order Management**: Place orders, view order history, and edit orders.
- **Payment Integration**: Paystack payment gateway for secure transactions.
- **Responsive Design**: Optimized for both desktop and mobile devices.
- **Light/Dark Mode**: Toggle between light and dark themes for better user experience.

---

## Technologies Used

- **Python 3.x**: Core programming language.
- **Flask**: Web framework for routing, templating, and server logic.
- **Jinja2**: Templating engine for dynamic HTML rendering.
- **SQLite**: Default database for local development.
- **SQLAlchemy**: ORM for database interactions.
- **Flask-WTF**: Form handling and validation.
- **Flask-Login**: User authentication and session management.
- **Paystack**: Payment gateway integration.
- **HTML/CSS**: Frontend styling and layout.

---

## Project Structure
```
Get-It/
├── README.md
├── requirements.txt
├── main.py
├── instance/
│   └── app.db
├── core/
│   ├── __init__.py
│   ├── configs.py
│   ├── database.py
│   └── __pycache__/
├── models/
│   ├── __init__.py
│   ├── cart.py
│   ├── order.py
│   ├── products.py
│   ├── users.py
│   └── __pycache__/
├── forms/
│   ├── edit_account_form.py
│   ├── loginform.py
│   ├── product_form.py
│   └── __pycache__/
├── services/
│   ├── auth.py
│   ├── cart.py
│   ├── product.py
│   ├── user.py
│   └── __pycache__/
├── blueprints/
│   ├── __init__.py
│   ├── account.py
│   ├── auth.py
│   ├── cart.py
│   ├── order.py
│   ├── product.py
│   ├── public.py
│   └── __pycache__/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── account/
│   │   ├── account.html
│   │   ├── edit_account.html
│   │   ├── login.html
│   │   ├── register.html
│   ├── cart/
│   │   ├── cart.html
│   │   ├── checkout.html
│   ├── order/
│   │   ├── edit_order.html
│   │   ├── paystack_payment.html
│   │   ├── view_order.html
│   ├── products/
│   │   ├── add_product.html
│   ├── public/
│   │   ├── about.html
│   │   ├── contact.html
│   │   ├── faq.html
│   │   ├── privacy.html
│   │   ├── terms.html
├── static/
│   ├── styles.css
│   ├── imgs/
│   │   ├── logo.png
│   │   ├── star3.png
│   │   ├── uploads/
├── utils/
│   ├── __init__.py
│   ├── enums.py
│   ├── utils.py
│   └── __pycache__/
```

### Folder and File Details

#### `main.py`
- Entry point of the application.
- Initializes Flask app, configures database, and registers blueprints.
- Handles global application settings like secret keys and debug mode.

#### `requirements.txt`
- Lists all Python dependencies required to run the project.

#### `instance/`
- Contains the SQLite database file (`app.db`) for persistent storage.

#### `core/`
- **`configs.py`**: Contains configuration variables like database URI, secret keys, and debug mode.
- **`database.py`**: Initializes SQLAlchemy for database interactions.

#### `models/`
- Contains ORM models for database tables:
  - **`users.py`**: User model with fields like `username`, `email`, and `password`.
  - **`products.py`**: Product model with fields like `name`, `price`, and `category`.
  - **`cart.py`**: Cart and CartItem models for managing user carts.
  - **`order.py`**: Order and OrderItem models for managing orders.

#### `forms/`
- Contains Flask-WTF form classes for handling user input:
  - **`loginform.py`**: Login form.
  - **`edit_account_form.py`**: Form for editing user account details.
  - **`product_form.py`**: Form for adding products.

#### `services/`
- Contains business logic for various functionalities:
  - **`auth.py`**: Handles user authentication.
  - **`cart.py`**: Manages cart-related operations.
  - **`product.py`**: Handles product-related operations.
  - **`user.py`**: Manages user registration and updates.

#### `blueprints/`
- Modularizes routes for different parts of the application:
  - **`auth.py`**: Routes for login, registration, and logout.
  - **`account.py`**: Routes for user account management.
  - **`cart.py`**: Routes for cart operations.
  - **`order.py`**: Routes for order management.
  - **`product.py`**: Routes for product management.
  - **`public.py`**: Routes for static pages like About, Contact, FAQ, etc.

#### `templates/`
- Contains Jinja2 HTML templates for rendering pages:
  - **`base.html`**: Base template with common layout (header, footer).
  - **`index.html`**: Homepage displaying featured products and categories.
  - **`account/`**: Templates for user account management.
  - **`cart/`**: Templates for cart and checkout pages.
  - **`order/`**: Templates for order-related pages.
  - **`products/`**: Template for adding new products.
  - **`public/`**: Static pages like About, Contact, FAQ, Privacy, and Terms.

#### `static/`
- Contains static assets like CSS files and images:
  - **`styles.css`**: Main stylesheet for the application.
  - **`imgs/`**: Folder for images like logos and product images.

#### `utils/`
- Contains utility functions and enumerations:
  - **`utils.py`**: Helper functions like file validation and phone number validation.
  - **`enums.py`**: Enumerations for product categories and order statuses.

---

## Database Schema

### **Users Table**
| Column Name   | Type        | Description                  |
|---------------|-------------|------------------------------|
| `id`          | Integer     | Primary key                 |
| `username`    | String      | Unique username             |
| `email`       | String      | Unique email address        |
| `password`    | String      | Hashed password             |
| `created_at`  | DateTime    | Account creation timestamp  |
| `updated_at`  | DateTime    | Last update timestamp       |

### **Products Table**
| Column Name   | Type        | Description                  |
|---------------|-------------|------------------------------|
| `id`          | Integer     | Primary key                 |
| `name`        | String      | Product name                |
| `price`       | Float       | Product price               |
| `category`    | Enum        | Product category            |
| `images`      | JSON        | Product images              |

### **Cart Table**
| Column Name   | Type        | Description                  |
|---------------|-------------|------------------------------|
| `id`          | Integer     | Primary key                 |
| `user_id`     | Integer     | Foreign key to Users table  |

### **Orders Table**
| Column Name   | Type        | Description                  |
|---------------|-------------|------------------------------|
| `id`          | Integer     | Primary key                 |
| `user_id`     | Integer     | Foreign key to Users table  |
| `status`      | Enum        | Order status                |
| `total_price` | Float       | Total price of the order    |

---

## How to Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up environment variables:** Create a .env file in the project root with the following content:
   ```plaintext
   DATABASE_URL=sqlite:///instance/app.db
   SECRET_KEY=your-secret-key
   PAYSTACK_PUBLIC_KEY=your-paystack-public-key
   PAYSTACK_SECRET_KEY=your-paystack-secret-key
   ```
3. **Initialize the database:**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
4. **Run the application:** 
   ```bash
   python main.py
   ```
5. **Access the app:** Open your browser and navigate to http://localhost:8000.

## Contribution

- Fork the repository, create a feature branch, and submit a pull request.
- Ensure code is well-documented and tested.

## License

This project is licensed under the MIT License.
