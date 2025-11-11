// create_order.js - Handles order creation with proper validation and error handling

/**
 * Creates a new order with all required fields for the logistics platform
 * @param {Object} orderData - The order data containing all required fields
 * @param {number} orderData.pickup_lat - Pickup latitude
 * @param {number} orderData.pickup_lng - Pickup longitude
 * @param {number} orderData.drop_lat - Drop latitude
 * @param {number} orderData.drop_lng - Drop longitude
 * @param {string} orderData.pickup_address - Pickup address
 * @param {string} orderData.drop_address - Drop address
 * @param {string} orderData.material_type - Type of material being shipped
 * @param {number} orderData.weight_kg - Weight in kilograms
 * @param {string} [orderData.material_description] - Optional description of material
 * @returns {Promise<Object>} The response data from the server
 */
async function createOrder(orderData) {
  // Validate input parameters
  const requiredFields = [
    'pickup_lat', 'pickup_lng', 'drop_lat', 'drop_lng',
    'pickup_address', 'drop_address', 'material_type', 'weight_kg'
  ];
  
  // Check for missing required fields
  const missingFields = requiredFields.filter(field => 
    orderData[field] === undefined || orderData[field] === null || 
    (typeof orderData[field] === 'string' && orderData[field].trim() === '')
  );
  
  if (missingFields.length > 0) {
    throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
  }
  
  // Validate numeric fields with enhanced validation
  const numericFields = ['pickup_lat', 'pickup_lng', 'drop_lat', 'drop_lng', 'weight_kg'];
  for (const field of numericFields) {
    // Convert to float first
    const fieldValue = parseFloat(orderData[field]);
    
    // Check if it's a valid number
    if (isNaN(fieldValue) || !isFinite(fieldValue)) {
      throw new Error(`${field} must be a valid number`);
    }
    
    // Additional validation for longitude and latitude
    if (field === 'pickup_lng' || field === 'drop_lng') {
      if (fieldValue < -180 || fieldValue > 180) {
        throw new Error(`${field} must be between -180 and 180`);
      }
    }
    
    if (field === 'pickup_lat' || field === 'drop_lat') {
      if (fieldValue < -90 || fieldValue > 90) {
        throw new Error(`${field} must be between -90 and 90`);
      }
    }
    
    // Additional validation for weight
    if (field === 'weight_kg' && fieldValue <= 0) {
      throw new Error('Weight must be greater than 0');
    }
  }
  
  // Parse numeric values
  const parsedData = {
    ...orderData,
    pickup_lat: parseFloat(orderData.pickup_lat),
    pickup_lng: parseFloat(orderData.pickup_lng),
    drop_lat: parseFloat(orderData.drop_lat),
    drop_lng: parseFloat(orderData.drop_lng),
    weight_kg: parseFloat(orderData.weight_kg)
  };
  
  // Get token from localStorage
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('Authentication token not found. Please login first.');
  }
  
  try {
    // Make the POST request to create the order
    const response = await fetch('/api/customer/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(parsedData)
    });
    
    // Handle HTTP errors
    if (!response.ok) {
      // Try to get error details from response
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      try {
        const errorData = await response.json();
        if (errorData.message) {
          errorMessage = `HTTP ${response.status}: ${errorData.message}`;
        }
      } catch (e) {
        // If we can't parse the error response, use the default message
        console.error('Error parsing error response:', e);
      }
      
      throw new Error(errorMessage);
    }
    
    // Parse and return the successful response
    const data = await response.json();
    return data;
    
  } catch (error) {
    // Log the error for debugging purposes
    console.error('Error creating order:', error);
    
    // Re-throw the error for the caller to handle
    throw error;
  }
}

/**
 * Creates a new order by collecting data from form inputs
 * This function gets values from HTML form elements and creates an order
 * @returns {Promise<Object>} The response data from the server
 */
async function createOrderFromForm() {
  try {
    // Get values from form inputs
    const orderData = {
      pickup_lat: document.getElementById('pickup_lat').value,
      pickup_lng: document.getElementById('pickup_lng').value,
      drop_lat: document.getElementById('drop_lat').value,
      drop_lng: document.getElementById('drop_lng').value,
      pickup_address: document.getElementById('pickup_address').value,
      drop_address: document.getElementById('drop_address').value,
      material_type: document.getElementById('material_type').value,
      weight_kg: document.getElementById('weight_kg').value,
      material_description: document.getElementById('material_description') ? 
        document.getElementById('material_description').value : undefined
    };
    
    // Create the order
    const result = await createOrder(orderData);
    
    // Handle success
    console.log('Order created successfully:', result);
    return result;
    
  } catch (error) {
    // Handle errors
    console.error('Failed to create order:', error);
    throw error;
  }
}

/**
 * Example usage of the createOrder function
 * This would typically be called from an event handler
 */
async function handleCreateOrder() {
  try {
    // Create the order from form data
    const result = await createOrderFromForm();
    
    // Show success message
    alert(`Order created successfully! Order ID: ${result.order_id}, Fare: ₹${result.fare_total}`);
    
    // Optionally redirect to customer dashboard
    // window.location.href = '/customer';
    
  } catch (error) {
    // Handle errors
    console.error('Failed to create order:', error);
    alert(`Error creating order: ${error.message}`);
  }
}

// Export the function for use in other modules (if using modules)
// export { createOrder, createOrderFromForm, handleCreateOrder };

// Make the function available globally (for direct script inclusion)
window.createOrder = createOrder;
window.createOrderFromForm = createOrderFromForm;
window.handleCreateOrder = handleCreateOrder;