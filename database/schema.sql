-- =====================================================
-- FoodRush database schema (MySQL 8, InnoDB)
-- =====================================================
USE foodrush_db;

-- -----------------------------------------------------
-- 1. users: every person who can log in
-- -----------------------------------------------------
CREATE TABLE users (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,           -- PK
  full_name     VARCHAR(100) NOT NULL,
  email         VARCHAR(255) NOT NULL,                          -- used to log in
  phone         VARCHAR(20)  NULL,
  password_hash VARCHAR(255) NOT NULL,                          -- bcrypt hash, never the real password
  role          ENUM('customer','owner','admin') NOT NULL DEFAULT 'customer',
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,                  -- false = account suspended
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 2. restaurants
-- -----------------------------------------------------
CREATE TABLE restaurants (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,           -- PK
  owner_id      INT UNSIGNED NOT NULL,                          -- FK -> users.id
  name          VARCHAR(150) NOT NULL,
  description   TEXT NULL,
  cuisine_type  VARCHAR(100) NULL,                              -- e.g. 'North Indian'
  phone         VARCHAR(20)  NULL,
  address       VARCHAR(255) NOT NULL,
  city          VARCHAR(100) NOT NULL,
  pincode       VARCHAR(10)  NULL,
  image_url     VARCHAR(500) NULL,
  delivery_fee  DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  status        ENUM('pending','approved','rejected','suspended') NOT NULL DEFAULT 'pending',
  is_open       BOOLEAN NOT NULL DEFAULT TRUE,                  -- owner toggles "accepting orders"
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_restaurants_status (status),
  KEY idx_restaurants_city (city),
  CONSTRAINT fk_restaurants_owner
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE RESTRICT,
  CONSTRAINT chk_restaurants_delivery_fee CHECK (delivery_fee >= 0)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 3. categories: menu sections, per restaurant
-- -----------------------------------------------------
CREATE TABLE categories (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,           -- PK
  restaurant_id INT UNSIGNED NOT NULL,                          -- FK -> restaurants.id
  name          VARCHAR(100) NOT NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_categories_restaurant_name (restaurant_id, name), -- no duplicate names in one restaurant
  CONSTRAINT fk_categories_restaurant
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 4. food_items: the dishes
-- -----------------------------------------------------
CREATE TABLE food_items (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,           -- PK
  restaurant_id INT UNSIGNED NOT NULL,                          -- FK -> restaurants.id
  category_id   INT UNSIGNED NULL,                              -- FK -> categories.id (optional)
  name          VARCHAR(150) NOT NULL,
  description   TEXT NULL,
  price         DECIMAL(10,2) NOT NULL,
  image_url     VARCHAR(500) NULL,
  is_veg        BOOLEAN NOT NULL DEFAULT TRUE,
  is_available  BOOLEAN NOT NULL DEFAULT TRUE,                  -- false = "sold out" but still listed
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_food_items_name (name),                               -- speeds up food search
  CONSTRAINT fk_food_items_restaurant
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
  CONSTRAINT fk_food_items_category
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
  CONSTRAINT chk_food_items_price CHECK (price >= 0)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 5. addresses: saved delivery addresses
-- -----------------------------------------------------
CREATE TABLE addresses (
  id             INT UNSIGNED NOT NULL AUTO_INCREMENT,          -- PK
  user_id        INT UNSIGNED NOT NULL,                         -- FK -> users.id
  label          VARCHAR(50)  NOT NULL DEFAULT 'Home',          -- Home / Work / Other
  recipient_name VARCHAR(100) NOT NULL,
  phone          VARCHAR(20)  NOT NULL,
  address_line   VARCHAR(255) NOT NULL,
  city           VARCHAR(100) NOT NULL,
  state          VARCHAR(100) NOT NULL,
  pincode        VARCHAR(10)  NOT NULL,
  is_default     BOOLEAN NOT NULL DEFAULT FALSE,
  created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT fk_addresses_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 6. carts: one cart per customer (1:1 with users)
-- -----------------------------------------------------
CREATE TABLE carts (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,           -- PK
  user_id       INT UNSIGNED NOT NULL,                          -- FK -> users.id
  restaurant_id INT UNSIGNED NULL,                              -- FK -> restaurants.id; NULL while cart is empty
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_carts_user (user_id),                           -- UNIQUE makes it one-to-one
  CONSTRAINT fk_carts_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_carts_restaurant
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 7. cart_items: lines inside a cart
-- -----------------------------------------------------
CREATE TABLE cart_items (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,           -- PK
  cart_id       INT UNSIGNED NOT NULL,                          -- FK -> carts.id
  food_item_id  INT UNSIGNED NOT NULL,                          -- FK -> food_items.id
  quantity      INT UNSIGNED NOT NULL DEFAULT 1,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_cart_items_cart_food (cart_id, food_item_id),   -- same dish can't appear twice; we raise quantity instead
  CONSTRAINT fk_cart_items_cart
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
  CONSTRAINT fk_cart_items_food
    FOREIGN KEY (food_item_id) REFERENCES food_items(id) ON DELETE CASCADE,
  CONSTRAINT chk_cart_items_quantity CHECK (quantity > 0)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 8. orders: one row per placed order (contains snapshots)
-- -----------------------------------------------------
CREATE TABLE orders (
  id               INT UNSIGNED NOT NULL AUTO_INCREMENT,        -- PK
  customer_id      INT UNSIGNED NOT NULL,                       -- FK -> users.id
  restaurant_id    INT UNSIGNED NOT NULL,                       -- FK -> restaurants.id
  restaurant_name  VARCHAR(150) NOT NULL,                       -- SNAPSHOT
  delivery_name    VARCHAR(100) NOT NULL,                       -- SNAPSHOT of address
  delivery_phone   VARCHAR(20)  NOT NULL,                       -- SNAPSHOT of address
  delivery_address VARCHAR(500) NOT NULL,                       -- SNAPSHOT of address
  status           ENUM('placed','accepted','preparing','ready','delivered','rejected','cancelled')
                   NOT NULL DEFAULT 'placed',
  status_reason    VARCHAR(255) NULL,                           -- why rejected/cancelled
  notes            VARCHAR(500) NULL,                           -- customer instructions
  subtotal         DECIMAL(10,2) NOT NULL,                      -- sum of item line totals
  delivery_fee     DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  discount_amount  DECIMAL(10,2) NOT NULL DEFAULT 0.00,         -- for coupons later
  total_amount     DECIMAL(10,2) NOT NULL,                      -- subtotal + delivery_fee - discount
  placed_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_orders_status (status),
  KEY idx_orders_placed_at (placed_at),
  CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE RESTRICT,
  CONSTRAINT fk_orders_restaurant
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE RESTRICT,
  CONSTRAINT chk_orders_amounts CHECK (subtotal >= 0 AND delivery_fee >= 0 AND discount_amount >= 0 AND total_amount >= 0)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 9. order_items: lines of an order (price SNAPSHOT)
-- -----------------------------------------------------
CREATE TABLE order_items (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,           -- PK
  order_id      INT UNSIGNED NOT NULL,                          -- FK -> orders.id
  food_item_id  INT UNSIGNED NULL,                              -- FK -> food_items.id; NULL if dish deleted later
  item_name     VARCHAR(150) NOT NULL,                          -- SNAPSHOT of dish name
  unit_price    DECIMAL(10,2) NOT NULL,                         -- SNAPSHOT of price at purchase
  quantity      INT UNSIGNED NOT NULL,
  line_total    DECIMAL(10,2) NOT NULL,                         -- unit_price * quantity
  PRIMARY KEY (id),
  CONSTRAINT fk_order_items_order
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  CONSTRAINT fk_order_items_food
    FOREIGN KEY (food_item_id) REFERENCES food_items(id) ON DELETE SET NULL,
  CONSTRAINT chk_order_items_values CHECK (quantity > 0 AND unit_price >= 0 AND line_total >= 0)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- 10. payments: one payment record per order (1:1 with orders)
-- -----------------------------------------------------
CREATE TABLE payments (
  id                  INT UNSIGNED NOT NULL AUTO_INCREMENT,     -- PK
  order_id            INT UNSIGNED NOT NULL,                    -- FK -> orders.id
  method              ENUM('cod','razorpay') NOT NULL DEFAULT 'cod',
  status              ENUM('pending','paid','failed','refunded') NOT NULL DEFAULT 'pending',
  amount              DECIMAL(10,2) NOT NULL,
  provider_payment_id VARCHAR(100) NULL,                        -- Razorpay's payment id (later)
  paid_at             TIMESTAMP NULL DEFAULT NULL,
  created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_payments_order (order_id),                      -- UNIQUE makes it one-to-one
  CONSTRAINT fk_payments_order
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  CONSTRAINT chk_payments_amount CHECK (amount >= 0)
) ENGINE=InnoDB;