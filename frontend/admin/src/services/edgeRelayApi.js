/**
 * API Service for EdgeRelay Platform
 * Handles all API communication with the EdgeRelay backend
 * Adapted for EdgeRelay endpoints and authentication
 */

class EdgeRelayApiService {
  constructor() {
    // EdgeRelay API base URL - using port 9004 for HTTP
    this.baseURL = ''
    this.token = localStorage.getItem('admin_token')
    console.log('EdgeRelay API Service initialized with baseURL:', this.baseURL)
  }

  // Set authentication token
  setToken(token) {
    this.token = token
    localStorage.setItem('admin_token', token)
  }

  // Clear authentication token
  clearToken() {
    this.token = null
    localStorage.removeItem('admin_token')
  }

  // Get headers with authentication
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    }
    
    const token = this.token
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    return headers
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    console.log('Making EdgeRelay API request to:', url)
    
    const config = {
      headers: this.getHeaders(),
      ...options
    }

    try {
      const response = await fetch(url, config)
      
      // Handle non-JSON responses
      if (!response.headers.get('content-type')?.includes('application/json')) {
        const text = await response.text()
        return { data: text, status: response.status }
      }
      
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`)
      }
      
      return { data, status: response.status }
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // System endpoints
  async getHealth() {
    return this.request('/health')
  }

  async getSystemInfo() {
    return this.request('/api/info')
  }

  async getSystemStatus() {
    return this.request('/api/status')
  }

  // Admin authentication endpoints (when implemented)
  async adminLogin(credentials) {
    const response = await this.request('/api/admin/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    })
    
    if (response.data.token) {
      this.setToken(response.data.token)
    }
    
    return response
  }

  async getAdminProfile() {
    return this.request('/api/admin/auth/me')
  }

  // Client management endpoints (when implemented)
  async getClients() {
    return this.request('/api/admin/clients')
  }

  async createClient(clientData) {
    return this.request('/api/admin/clients', {
      method: 'POST',
      body: JSON.stringify(clientData)
    })
  }

  async updateClient(clientId, clientData) {
    return this.request(`/api/admin/clients/${clientId}`, {
      method: 'PUT',
      body: JSON.stringify(clientData)
    })
  }

  async deleteClient(clientId) {
    return this.request(`/api/admin/clients/${clientId}`, {
      method: 'DELETE'
    })
  }

  // Local server management endpoints (when implemented)
  async getLocalServers() {
    return this.request('/api/admin/servers')
  }

  async createLocalServer(serverData) {
    return this.request('/api/admin/servers', {
      method: 'POST',
      body: JSON.stringify(serverData)
    })
  }

  async updateLocalServer(serverId, serverData) {
    return this.request(`/api/admin/servers/${serverId}`, {
      method: 'PUT',
      body: JSON.stringify(serverData)
    })
  }

  async deleteLocalServer(serverId) {
    return this.request(`/api/admin/servers/${serverId}`, {
      method: 'DELETE'
    })
  }

  // Camera management endpoints (when implemented)
  async getCameras(serverId = null) {
    const endpoint = serverId ? `/api/admin/cameras?server_id=${serverId}` : '/api/admin/cameras'
    return this.request(endpoint)
  }

  async createCamera(cameraData) {
    return this.request('/api/admin/cameras', {
      method: 'POST',
      body: JSON.stringify(cameraData)
    })
  }

  async updateCamera(cameraId, cameraData) {
    return this.request(`/api/admin/cameras/${cameraId}`, {
      method: 'PUT',
      body: JSON.stringify(cameraData)
    })
  }

  async deleteCamera(cameraId) {
    return this.request(`/api/admin/cameras/${cameraId}`, {
      method: 'DELETE'
    })
  }

  // Alert management endpoints (when implemented)
  async getAlerts(filters = {}) {
    const params = new URLSearchParams(filters).toString()
    const endpoint = params ? `/api/admin/alerts?${params}` : '/api/admin/alerts'
    return this.request(endpoint)
  }

  async updateAlert(alertId, alertData) {
    return this.request(`/api/admin/alerts/${alertId}`, {
      method: 'PUT',
      body: JSON.stringify(alertData)
    })
  }

  async deleteAlert(alertId) {
    return this.request(`/api/admin/alerts/${alertId}`, {
      method: 'DELETE'
    })
  }

  // System configuration endpoints (when implemented)
  async getSystemConfig() {
    return this.request('/api/admin/config')
  }

  async updateSystemConfig(configData) {
    return this.request('/api/admin/config', {
      method: 'PUT',
      body: JSON.stringify(configData)
    })
  }
}

export default new EdgeRelayApiService()
