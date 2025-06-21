-- Products Table
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(20) NOT NULL,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    role VARCHAR(20) NOT NULL,
    status VARCHAR(10) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders Table
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(username),
    status VARCHAR(20) DEFAULT 'Processing',
    total DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order Items Table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(20) REFERENCES orders(order_id),
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Shopping Cart Table (for persistent carts)
CREATE TABLE shopping_carts (
    user_id VARCHAR(50) PRIMARY KEY REFERENCES users(username),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart Items Table
CREATE TABLE cart_items (
    cart_id VARCHAR(50) REFERENCES shopping_carts(user_id),
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL,
    PRIMARY KEY (cart_id, product_id)
);