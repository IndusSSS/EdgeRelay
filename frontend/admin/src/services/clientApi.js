/**
 * API Service for IoT Platform
 * Handles all API communication with the backend
 * HARDCODED to use relative /api path - NO environment variables
 */

class ApiService {
  constructor() {
    // HARDCODED - Use relative API path that will be proxied by nginx
    this.baseURL = ''
    this.token = localStorage.getItem('admin_token')
    console.log('API Service initialized with baseURL:', this.baseURL)
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
    console.log('Making API request to:', url)
    
    const config = {
      headers: this.getHeaders(),
      ...options
    }

    try {
      const response = await fetch(url, config)
      console.log('API response status:', response.status, 'for URL:', url)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
      }
      
      // Handle 204 No Content responses (like DELETE operations)
      if (response.status === 204) {
        console.log("API response: 204 No Content")
        return null
      }
      const data = await response.json()
      console.log('API response data:', data)
      return data
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error)
      throw error
    }
  }

  // Generic GET method
  async get(endpoint) {
    return this.request(endpoint)
  }

  // Device Management API
  async getDevices(params = {}) {
    console.log('Getting devices with params:', params)
    const queryParams = new URLSearchParams()
    
    if (params.limit) queryParams.append('limit', params.limit)
    if (params.offset) queryParams.append('offset', params.offset)
    if (params.status_filter) queryParams.append('status_filter', params.status_filter)
    if (params.template_id) queryParams.append('template_id', params.template_id)
    
    const queryString = queryParams.toString()
    // FastAPI routes are defined without a trailing slash, so preserve that format
    const endpoint = queryString ? `/api/devices?${queryString}` : '/api/devices'
    
    return this.request(endpoint)
  }

  async getDevice(deviceId) {
    return this.request(`/api/devices/${deviceId}`)
  }

  async updateDevice(deviceId, data) {
    return this.request(`/api/devices/${deviceId}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async deleteDevice(deviceId) {
    return this.request(`/api/devices/${deviceId}`, {
      method: 'DELETE'
    })
  }

  // Device Discovery API
  async getDiscoveredDevices(params = {}) {
    const queryParams = new URLSearchParams()
    
    if (params.status) queryParams.append('status', params.status)
    if (params.page) queryParams.append('page', params.page)
    if (params.page_size) queryParams.append('page_size', params.page_size)
    
    const queryString = queryParams.toString()
    const endpoint = `/api/api/devices/discovery${queryString ? `?${queryString}` : ''}`
    
    return this.request(endpoint)
  }

  async getDiscoveryStats() {
    return this.request('/api/api/devices/discovery/stats')
  }

  async approveDevice(deviceId, approvalData) {
    return this.request(`/api/api/devices/${deviceId}/approve`, {
      method: 'POST',
      body: JSON.stringify(approvalData)
    })
  }

  async rejectDevice(deviceId, reason = 'Device rejected by admin') {
    return this.request(`/api/api/devices/${deviceId}/reject`, {
      method: 'POST',
      body: JSON.stringify({ reason })
    })
  }

  // Managed Devices API
  async getManagedDevices(params = {}) {
    const queryParams = new URLSearchParams()
    
    if (params.page) queryParams.append('page', params.page)
    if (params.page_size) queryParams.append('page_size', params.page_size)
    if (params.search) queryParams.append('search', params.search)
    if (params.status) queryParams.append('status', params.status)
    
    const queryString = queryParams.toString()
    const endpoint = `/api/api/devices/managed${queryString ? `?${queryString}` : ''}`
    
    return this.request(endpoint)
  }

  async getManagedDevicesStats() {
    return this.request('/api/api/devices/managed/stats')
  }

  async updateManagedDevice(deviceId, deviceData) {
    return this.request(`/api/api/devices/managed/${deviceId}`, {
      method: 'PUT',
      body: JSON.stringify(deviceData)
    })
  }

  async deleteManagedDevice(deviceId) {
    return this.request(`/api/api/devices/managed/${deviceId}`, {
      method: 'DELETE'
    })
  }

  // Device Statistics
  // Device Assignment API
  async assignDeviceToClient(deviceId, clientId) {
    return this.request(`/api/devices/${deviceId}/assign`, {
      method: "PUT",
      body: JSON.stringify({ client_id: clientId })
    })
  }

  async unassignDeviceFromClient(deviceId) {
    return this.request(`/api/devices/${deviceId}/unassign`, {
      method: "PUT"
    })
  }


  async getDeviceStats() {
    try {
      console.log('Getting device stats...')
      const devices = await this.getDevices({ limit: 1000 })
      
      const stats = {
        total: devices.length,
        online: 0,
        offline: 0,
        warning: 0
      }
      
      devices.forEach(device => {
        switch (device.status) {
          case 'ONLINE':
            stats.online++
            break
          case 'OFFLINE':
            stats.offline++
            break
          case 'ERROR':
            stats.warning++
            break
          default:
            break
        }
      })
      
      console.log('Device stats calculated:', stats)
      return stats
    } catch (error) {
      console.error('Failed to get device stats:', error)
      return {
        total: 0,
        online: 0,
        offline: 0,
        warning: 0
      }
    }
  }

  // User Management API
  async getUsers() {
    return this.request('/admin/users')
  }


  async getAllUsersAndClients() {
    try {
      const users = await this.getUsers().catch(() => [])
      
      // Transform users to match frontend format
      const transformedUsers = users.map(user => ({
        id: user.admin_id,
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        roles: [user.role],
        is_active: user.is_active,
        last_login: user.last_login,
        type: 'admin'
      }))
      
      return transformedUsers
    } catch (error) {
      console.error('Failed to get users:', error)
      return []
    }
  }

  async createUser(userData) {
    return this.request('/admin/users', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  }

  async updateUser(userId, userData) {
    return this.request(`/admin/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData)
    })
  }

  async deleteUser(userId) {
    return this.request(`/admin/users/${userId}`, {
      method: 'DELETE'
    })
  }

  async toggleUserStatus(userId, isActive) {
    return this.request(`/admin/users/${userId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ is_active: isActive })
    })
  }


  // Authentication methods
  async login(email, password) {
    return this.request('/admin/login', {
      method: 'POST',
      body: JSON.stringify({ username: email, password })
    })
  }

  async clientLogin(clientUsername, password) {
    return this.request('/api/client-management/auth/login', {
      method: 'POST',
      body: JSON.stringify({ client_username: clientUsername, password })
    })
  }

  getToken() {
    return this.token
  }

  setUser(user) {
    localStorage.setItem('admin_user', JSON.stringify(user))
  }

  getUser() {
    const user = localStorage.getItem('admin_user')
    return user ? JSON.parse(user) : null
  }

  isAuthenticated() {
    return !!this.token
  }

  // Health check
  async healthCheck() {
    return this.request('/health')
  }

  // Client Management API
  async getClients(params = {}) {
    const queryParams = new URLSearchParams()
    
    if (params.skip) queryParams.append('skip', params.skip)
    if (params.limit) queryParams.append('limit', params.limit)
    if (params.is_active !== undefined) queryParams.append('is_active', params.is_active)
    
    const queryString = queryParams.toString()
    const endpoint = `/api/clients${queryString ? `?${queryString}` : ''}`
    
    return this.request(endpoint)
  }

  async createClient(clientData) {
    return this.request('/api/clients', {
      method: 'POST',
      body: JSON.stringify(clientData)
    })
  }

  async updateClient(clientId, clientData) {
    return this.request(`/api/clients/${clientId}`, {
      method: 'PUT',
      body: JSON.stringify(clientData)
    })
  }

  async deleteClient(clientId) {
    return this.request(`/api/clients/${clientId}`, {
      method: 'DELETE'
    })
  }

  async getClient(clientId) {
    return this.request(`/api/clients/${clientId}`)
  }
  async getClientUuids() {
    return this.request("/api/clients/uuids")
  }

  async getClientDeviceCounts() {
    return this.request("/api/clients/device-counts")
  }
  async generateUniqueClientId() {
    return this.request("/api/clients/generate-unique-id", {
      method: "POST"
    })
  }
  async getClientDevices(clientId) {
    return this.request(`/api/device-assignment/clients/${clientId}/devices`)
  }
}

// Export the class for proper instantiation
export default new ApiService()
