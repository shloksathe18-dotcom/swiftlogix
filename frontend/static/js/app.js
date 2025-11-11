// Global JS for maps and simple helpers

function initMap(mapId, lat = 28.6139, lng = 77.2090, zoom = 12) {
  const map = L.map(mapId).setView([lat, lng], zoom);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
  return map;
}

function addMarker(map, lat, lng, label = '') {
  return L.marker([lat, lng]).addTo(map).bindPopup(label);
}

async function authFetch(url, options = {}) {
  const token = localStorage.getItem('token');
  
  // Only set Content-Type for requests with a body (not GET requests)
  if (options.method && options.method.toUpperCase() !== 'GET') {
    options.headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
  } else {
    options.headers = options.headers || {};
  }
  
  if (token) options.headers['Authorization'] = 'Bearer ' + token;
  
  console.log('Making request to:', url, options);
  
  try {
    const res = await fetch(url, options);
    if (!res.ok) {
      const text = await res.text();
      console.error(`Request failed with status ${res.status}: ${text}`);
      
      // Handle 401 Unauthorized errors
      if (res.status === 401) {
        // Clear token and user data
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        // Redirect to login page
        window.location.href = '/login';
        throw new Error('Session expired. Please login again.');
      }
      
      throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
    }
    return res.json();
  } catch (error) {
    console.error('Request error:', error);
    throw error;
  }
}

window.SwiftLogix = { initMap, addMarker, authFetch };