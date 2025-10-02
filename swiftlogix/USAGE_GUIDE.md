# SwiftLogix Usage Guide

## 🚀 Getting Started

Your SwiftLogix app is now running at **http://127.0.0.1:5000**

## 📱 User Interfaces

### 1. Customer Interface
**Access:** http://127.0.0.1:5000/customer

**Features:**
- View dashboard with map
- Create new shipping orders
- Track orders in real-time
- View order history

**Create Order Page:** http://127.0.0.1:5000/customer/create_order
- Fill in pickup/drop addresses and coordinates
- Enter material type and weight
- Fare is auto-calculated: Base ₹30 + ₹10/km + ₹5/kg

**Track Order Page:** http://127.0.0.1:5000/customer/track_order
- Enter order ID to see live driver location on map

### 2. Driver Interface
**Access:** http://127.0.0.1:5000/driver

**Features:**
- View available orders
- Accept/reject orders
- Update live location
- Mark orders as delivered
- View earnings

**Orders Page:** http://127.0.0.1:5000/driver/orders
- See all pending orders
- Click "Accept" to take an order

### 3. Admin Interface
**Access:** http://127.0.0.1:5000/admin

**Features:**
- Dashboard with metrics (customers, drivers, orders, revenue)
- View active orders
- Manage users
- Export order data to CSV

## 🔐 API Endpoints

### Authentication
```bash
# Register a new user
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "customer"
  }'

# Login
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Customer APIs
```bash
# Create order (requires JWT token)
curl -X POST http://127.0.0.1:5000/api/customer/orders \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pickup_address": "123 Main St",
    "pickup_lat": 28.6139,
    "pickup_lng": 77.2090,
    "drop_address": "456 Park Ave",
    "drop_lat": 28.6200,
    "drop_lng": 77.2150,
    "material_type": "Documents",
    "weight_kg": 2
  }'

# Get my orders
curl http://127.0.0.1:5000/api/customer/orders \
  -H "Authorization: Bearer YOUR_TOKEN"

# Track order
curl http://127.0.0.1:5000/api/customer/orders/1/track \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Driver APIs
```bash
# Get available orders
curl http://127.0.0.1:5000/api/driver/orders/available \
  -H "Authorization: Bearer YOUR_TOKEN"

# Accept order
curl -X POST http://127.0.0.1:5000/api/driver/orders/1/accept \
  -H "Authorization: Bearer YOUR_TOKEN"

# Update location
curl -X POST http://127.0.0.1:5000/api/driver/location \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lat": 28.6150, "lng": 77.2100}'

# Update order status
curl -X POST http://127.0.0.1:5000/api/driver/orders/1/status \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "delivered"}'

# Get earnings
curl http://127.0.0.1:5000/api/driver/earnings \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Admin APIs
```bash
# Get dashboard metrics
curl http://127.0.0.1:5000/api/admin/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"

# Export orders to CSV
curl http://127.0.0.1:5000/api/admin/orders/export \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o orders.csv
```

## 💰 Pricing Logic

**Fare Calculation:**
- Base Fare: ₹30
- Distance: ₹10 per km
- Weight: ₹5 per kg
- **Total = 30 + (distance × 10) + (weight × 5)**

**Commission:**
- Company keeps 10% of total fare
- Driver receives 90% of total fare

**Example:**
- Distance: 5 km
- Weight: 3 kg
- Total: ₹30 + (5 × ₹10) + (3 × ₹5) = ₹95
- Driver gets: ₹85.50
- Company gets: ₹9.50

## 🗺️ Map Integration

The app uses **Leaflet.js** with **OpenStreetMap** tiles for:
- Displaying pickup/drop locations
- Live driver tracking
- Route visualization

Maps are initialized automatically on dashboard pages.

## 🧪 Testing the Flow

### 1. Register Users
```powershell
# Register a customer
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/register" -Method POST -ContentType "application/json" -Body '{"name":"Alice","email":"alice@test.com","password":"pass123","role":"customer"}'

# Register a driver
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/register" -Method POST -ContentType "application/json" -Body '{"name":"Bob","email":"bob@test.com","password":"pass123","role":"driver"}'

# Register an admin
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/register" -Method POST -ContentType "application/json" -Body '{"name":"Admin","email":"admin@test.com","password":"admin123","role":"admin"}'
```

### 2. Login and Get Token
```powershell
$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/login" -Method POST -ContentType "application/json" -Body '{"email":"alice@test.com","password":"pass123"}'
$token = $response.token
```

### 3. Create Order
```powershell
$headers = @{ "Authorization" = "Bearer $token" }
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/customer/orders" -Method POST -Headers $headers -ContentType "application/json" -Body '{"pickup_address":"A","pickup_lat":28.6,"pickup_lng":77.2,"drop_address":"B","drop_lat":28.61,"drop_lng":77.21,"material_type":"Docs","weight_kg":2}'
```

## 🛠️ Development Tips

- **Database location:** `swiftlogix.db` in project root
- **View database:** Use SQLite browser or `sqlite3 swiftlogix.db`
- **Reset database:** Delete `swiftlogix.db` and run migrations again
- **Debug mode:** Flask runs in debug mode by default (auto-reload on code changes)
- **Logs:** Check terminal for Flask request logs

## 📝 Next Steps

1. **Test the APIs** using the examples above
2. **Create test users** for each role
3. **Try the UI flows** in your browser
4. **Customize styling** in `frontend/static/css/style.css`
5. **Add payment integration** (Razorpay/Stripe sandbox)
6. **Deploy to production** (see deployment guide)

## 🐛 Troubleshooting

**Port already in use:**
```powershell
# Kill process on port 5000
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force
```

**Module not found:**
```powershell
# Reinstall dependencies
D:\coding` python\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

**Database errors:**
```powershell
# Reset migrations
Remove-Item -Recurse -Force migrations
$env:FLASK_APP="backend.app:create_app"
D:\coding` python\.venv\Scripts\python.exe -m flask db init
D:\coding` python\.venv\Scripts\python.exe -m flask db migrate -m "init"
D:\coding` python\.venv\Scripts\python.exe -m flask db upgrade
```
