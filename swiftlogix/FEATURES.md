# SwiftLogix - Features Overview

## 🎨 Modern UI/UX

### Beautiful Authentication Pages
- **Login Page** (`/login`)
  - Clean, modern design with gradient backgrounds
  - Animated card entrance
  - Role selection (Customer/Driver/Admin)
  - Real-time form validation
  - Loading states with spinner
  - Error/success alerts
  
- **Register Page** (`/register`)
  - Similar beautiful design
  - Full name, email, password fields
  - Role selection with descriptions
  - Auto-redirect after successful registration
  - JWT token saved to localStorage

### Landing Page (`/`)
- Hero section with call-to-action buttons
- Feature cards with hover effects
- Statistics display (1000+ drivers, 5000+ deliveries)
- "How It Works" section with 3 steps
- CTA section for quick registration
- Fully responsive design

### Enhanced Navbar
- Dynamic user state (logged in/out)
- Shows username when logged in
- Login/Register buttons for guests
- Logout functionality
- Responsive mobile menu

## 🎨 Design Features

### Color Palette
- Primary: Purple gradient (#667eea → #764ba2)
- Secondary: Pink gradient (#f093fb → #f5576c)
- Success: Green gradient (#10b981 → #059669)

### Animations
- Fade-in on page load
- Slide-up card entrance
- Hover effects on buttons and cards
- Animated background gradients
- Loading spinners
- Smooth transitions

### Visual Effects
- Glassmorphism (frosted glass effect)
- Gradient text
- Box shadows with depth
- Rounded corners (border-radius)
- Backdrop blur
- Animated particles

## 🔐 Authentication Flow

### Registration Process
1. User fills form (name, email, password, role)
2. Frontend validates input
3. POST to `/api/auth/register`
4. Backend creates user with bcrypt password hash
5. JWT token returned
6. Token saved to localStorage
7. Auto-redirect to role-specific dashboard

### Login Process
1. User enters email and password
2. Frontend validates input
3. POST to `/api/auth/login`
4. Backend verifies credentials
5. JWT token returned
6. Token saved to localStorage
7. Redirect based on role:
   - Customer → `/customer`
   - Driver → `/driver`
   - Admin → `/admin`

### Session Management
- JWT token stored in localStorage
- Token included in all API requests via Authorization header
- User info displayed in navbar
- Logout clears localStorage and redirects to login

## 📱 Responsive Design

- Mobile-first approach
- Breakpoints for tablets and desktops
- Collapsible navbar on mobile
- Stacked cards on small screens
- Touch-friendly buttons and inputs

## 🎯 User Roles

### Customer
- Create delivery orders
- Track orders in real-time
- View order history
- See fare calculations

### Driver
- View available orders
- Accept/reject orders
- Update live location
- Mark orders as delivered
- View earnings

### Admin
- Dashboard with metrics
- Manage users
- View all orders
- Export data to CSV
- Monitor revenue

## 🗺️ Map Integration

- Leaflet.js with OpenStreetMap
- Live driver tracking
- Pickup/drop location markers
- Interactive map controls
- Responsive map sizing

## 💰 Pricing System

**Formula:** Base ₹30 + (Distance × ₹10/km) + (Weight × ₹5/kg)

**Commission:** 10% to company, 90% to driver

**Example:**
- Distance: 5 km
- Weight: 3 kg
- Total: ₹30 + (5 × ₹10) + (3 × ₹5) = ₹95
- Driver gets: ₹85.50
- Company gets: ₹9.50

## 🔒 Security Features

- Bcrypt password hashing
- JWT authentication
- Role-based access control (RBAC)
- Input validation and sanitization
- CORS configuration
- Secure cookie support (production)
- HTTPS-ready

## 📊 Tech Stack

**Backend:**
- Flask 3.0.3
- SQLAlchemy (ORM)
- Flask-Migrate (DB migrations)
- Flask-JWT-Extended (Auth)
- Flask-Bcrypt (Password hashing)
- Flask-CORS (Cross-origin)

**Frontend:**
- HTML5
- CSS3 (Custom + Bootstrap 5.3.3)
- JavaScript (Vanilla)
- Leaflet.js 1.9.4
- Bootstrap Icons

**Database:**
- SQLite (development)
- MySQL/PostgreSQL supported

## 🚀 Quick Start

```powershell
cd "d:\coding python\swiftlogix"
.\run.ps1
```

Then visit:
- http://127.0.0.1:5000/ - Landing page
- http://127.0.0.1:5000/login - Login
- http://127.0.0.1:5000/register - Register

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login

### Customer
- `POST /api/customer/orders` - Create order
- `GET /api/customer/orders` - List orders
- `GET /api/customer/orders/<id>/track` - Track order

### Driver
- `GET /api/driver/orders/available` - Available orders
- `POST /api/driver/orders/<id>/accept` - Accept order
- `POST /api/driver/location` - Update location
- `POST /api/driver/orders/<id>/status` - Update status
- `GET /api/driver/earnings` - View earnings

### Admin
- `GET /api/admin/dashboard` - Dashboard metrics
- `GET /api/admin/orders/export` - Export CSV

## 🎨 CSS Architecture

- **style.css** - Global styles, components, utilities
- **auth.css** - Authentication page specific styles
- CSS variables for theming
- BEM-like naming convention
- Mobile-first media queries

## ✨ Next Steps

1. Test the login/register flow
2. Create test accounts for each role
3. Customize colors in CSS variables
4. Add more features (payment, notifications)
5. Deploy to production
