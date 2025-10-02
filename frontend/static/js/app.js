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
  options.headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
  if (token) options.headers['Authorization'] = 'Bearer ' + token;
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || ('HTTP ' + res.status));
  }
  return res.json();
}

window.SwiftLogix = { initMap, addMarker, authFetch };
