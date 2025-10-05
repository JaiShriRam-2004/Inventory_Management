CREATE DATABASE inventory_manage;
use inventory_manage;
-- Create Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create Locations Table
CREATE TABLE IF NOT EXISTS locations (
    location_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create Product Movements Table
CREATE TABLE IF NOT EXISTS product_movements (
    movement_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    from_location VARCHAR(50),
    to_location VARCHAR(50),
    product_id VARCHAR(50) NOT NULL,
    qty INTEGER NOT NULL,
    FOREIGN KEY (from_location) REFERENCES locations(location_id) ON DELETE CASCADE,
    FOREIGN KEY (to_location) REFERENCES locations(location_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    CHECK (qty > 0),
    CHECK (from_location IS NOT NULL OR to_location IS NOT NULL)
);


CREATE INDEX idx_movements_product ON product_movements(product_id);
CREATE INDEX idx_movements_from_location ON product_movements(from_location);
CREATE INDEX idx_movements_to_location ON product_movements(to_location);
CREATE INDEX idx_movements_timestamp ON product_movements(timestamp DESC);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_locations_name ON locations(name);

SHOW INDEXES FROM product_movements;
SHOW INDEXES FROM products;
SHOW INDEXES FROM locations;

EXPLAIN SELECT * FROM product_movements WHERE product_id = 'P123';
EXPLAIN SELECT * FROM products WHERE name = 'Laptop';
select * from products;





