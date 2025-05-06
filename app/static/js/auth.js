// ESTO AHORA MISMO NO FUNCIONA

document.addEventListener('DOMContentLoaded', () => {
  // Leer el token de sessionStorage
  const token = sessionStorage.getItem('token');

  // Si no hay token, redirigir al login
  if (!token) {
    if (window.location.pathname !== '/login') {
      window.location.href = '/login';
    }
    return;
  }

  // Sobrescribir fetch para agregar el token al encabezado Authorization
  const originalFetch = window.fetch;
  window.fetch = async (url, options = {}) => {
    options.headers = options.headers || {};
    options.headers['Authorization'] = `Bearer ${token}`;
    return originalFetch(url, options);
  };
});