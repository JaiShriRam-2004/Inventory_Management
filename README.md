# Inventory_Management

## 📖 Introduction
InventoryPro is a **web-based application** designed to streamline inventory handling for small and mid-sized businesses.  
The system is built on a **Flask backend** with a **vanilla JavaScript frontend**, making it lightweight, easy to deploy, and scalable.  

It provides real-time control over **products, storage points, and stock transactions**, ensuring managers always have a clear picture of their inventory health.

---

## 🎯 Goals of the Project
- Automate manual stock management tasks  
- Provide transparency on product movement across multiple branches or warehouses  
- Enable quick insights through summarized reports  
- Deliver a modular architecture that can grow with business needs  

---

## 🏗️ System Blueprint

### 🖼️ Frontend
- Pure **HTML, CSS, and JavaScript** (no heavy frameworks)  
- Organized inside the `frontend/` directory  
- Communicates exclusively with backend services via **REST APIs**  
- Provides clean forms and dashboards for users  

### ⚡ Backend
- **Flask (Python)** acts as the core engine (`app.py`)  
- Responsible for routing, validations, and business rules  
- Employs **Flask-SQLAlchemy** to interact with the database  

### 🗃️ Database
- **MySQL** (`inventory_manage`)  
- Core tables:  
  - `products` → Stores product info  
  - `locations` → Tracks storage/retail units  
  - `product_movements` → Logs transfers, stock-ins, and stock-outs  
- Integrity maintained using **foreign keys & constraints**  

---

## 🚀 Key Capabilities

- **Product Registry** → Add new items with IDs, names, and details  
- **Location Control** → Register warehouses, outlets, or rooms  
- **Stock Flow Tracking** → Record incoming, outgoing, and shifted stock  
- **Reports Dashboard** → Summarize product and location data for quick analysis  
- **API-First Design** → Every action has a corresponding RESTful endpoint  

---

## 🛢️ Data Model

### Products
- `product_id` – Unique identifier  
- `name` – Product name  
- `description` – Additional details  
- `created_at` – Timestamp of creation  

### Locations
- `location_id` – Unique identifier  
- `name` – Storage or branch name  
- `address` – Location address (optional)  
- `created_at` – Timestamp  

### Product Movements
- `movement_id` – Auto-increment primary key  
- `timestamp` – Time of transaction  
- `from_location` – Source location (nullable)  
- `to_location` – Destination location (nullable)  
- `product_id` – Associated product  
- `qty` – Quantity moved (must be > 0)  

---

## 🔄 Workflow in Action
1. **Add Product** → Admin registers a new product entry  
2. **Set Location** → Define warehouses or stores where items reside  
3. **Log Movement** → Record stock going in/out or moving across locations  
4. **Generate Reports** → API collates movement logs for visual summaries  

---

## ⚙️ Technology Stack
- **Backend:** Flask + SQLAlchemy (Python)  
- **Frontend:** HTML, CSS, Vanilla JS  
- **Database:** MySQL  
- **API:** REST-based endpoints   

## 📡 API Examples

### 1. Fetch Products
```http
GET /api/products
