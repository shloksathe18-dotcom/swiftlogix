# Photo Upload and Vehicle Selection Updates

## Overview
This document summarizes the changes made to implement photo upload functionality for customer order creation and enhance vehicle selection for driver registration.

## Changes Made

### 1. Backend Model Updates
- Added `material_photo_url` and `material_description` fields to the Order model
- These fields allow customers to upload photos of materials when creating orders

### 2. Customer Routes Updates
- Modified the `/api/customer/orders` endpoint to handle file uploads
- Supports both JSON and form data submissions
- Properly validates and processes photo uploads

### 3. Frontend Template Updates
- Updated the customer create order form to include:
  - Material description textarea
  - Photo upload file input
  - Proper form encoding for file uploads
- Updated JavaScript to use FormData for submission

### 4. Driver Dashboard Enhancements
- Added vehicle information display section
- Implemented profile endpoints for drivers:
  - GET `/api/driver/profile` - Retrieve driver profile information
  - PUT `/api/driver/profile` - Update driver profile information
- Enhanced profile modal to show driver details including vehicle information

### 5. Driver Registration Improvements
- Verified existing vehicle selection functionality in registration form
- Ensured proper handling of vehicle type and vehicle number during registration

## Implementation Details

### Photo Upload Process
1. Customers can now upload photos when creating orders
2. The frontend form uses `enctype="multipart/form-data"` to support file uploads
3. Backend handles both JSON and form data submissions
4. Photos are stored with a placeholder URL (in a production environment, this would be a proper file storage solution)

### Vehicle Information Display
1. Driver dashboard now shows vehicle information including:
   - Vehicle type
   - Vehicle number
   - License number
   - Driver availability status
2. Drivers can view their complete profile information in a modal
3. Drivers can edit their profile information including vehicle details

## API Endpoints Added/Modified

### Modified Endpoints
- POST `/api/customer/orders` - Now supports photo uploads

### New Endpoints
- GET `/api/driver/profile` - Retrieve driver profile
- PUT `/api/driver/profile` - Update driver profile

## Files Modified
1. `backend/models.py` - Added photo fields to Order model
2. `backend/routes/customer_routes.py` - Updated create_order endpoint
3. `backend/routes/driver_routes.py` - Added profile endpoints
4. `frontend/templates/customer/create_order.html` - Added photo upload form fields
5. `frontend/templates/driver/dashboard.html` - Added vehicle information display

## Future Improvements
1. Implement proper file storage solution for photo uploads
2. Add image validation and processing
3. Implement photo display functionality in order tracking
4. Add vehicle verification process for drivers