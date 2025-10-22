<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Welcome Section -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Welcome, {{ clientInfo.contact_person }}!</h1>
          <p class="text-gray-600 mt-2">{{ clientInfo.company_name }} - Client Dashboard</p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-2 text-gray-600">Loading dashboard data...</p>
        </div>

        <!-- Main Dashboard Content -->
        <div v-else>
          <!-- Client Statistics -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="card">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-8 w-8 bg-blue-100 rounded-lg flex items-center justify-center">
                    <CpuChipIcon class="h-5 w-5 text-blue-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Devices</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ clientStats.totalDevices }}</dd>
                  </dl>
                </div>
              </div>
            </div>

            <div class="card">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-8 w-8 bg-green-100 rounded-lg flex items-center justify-center">
                    <CheckCircleIcon class="h-5 w-5 text-green-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Online Devices</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ clientStats.onlineDevices }}</dd>
                  </dl>
                </div>
              </div>
            </div>

            <div class="card">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-8 w-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                    <ExclamationTriangleIcon class="h-5 w-5 text-yellow-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Alerts</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ clientStats.alerts }}</dd>
                  </dl>
                </div>
              </div>
            </div>

            <div class="card">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-8 w-8 bg-purple-100 rounded-lg flex items-center justify-center">
                    <ChartBarIcon class="h-5 w-5 text-purple-600" />
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Data Points Today</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ clientStats.dataPoints }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Device Cards Section -->
          <div v-if="devices.length > 0" class="mb-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Your Devices</h2>
            <div class="space-y-6">
              <DeviceCard
    CapabilityModal 
                v-for="device in devices" 
                :key="device.id"
                :device="device"
                @refresh="handleDeviceRefresh"
                @capability-click="handleCapabilityClick"
              />
            </div>
          </div>

          <!-- No Devices State -->
          <div v-else class="text-center py-12">
            <div class="text-6xl mb-4">📱</div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">No Devices Found</h3>
            <p class="text-gray-600 mb-6">You don't have any devices assigned yet.</p>
            <button class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
              Contact Support
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Capability Details Modal -->
    <div v-if="selectedCapability" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">{{ selectedCapability.capability.name }} Details</h3>
          <button @click="closeCapabilityModal" class="text-gray-400 hover:text-gray-600">
            ✕
          </button>
        </div>
        <div class="space-y-4">
          <p><strong>Device:</strong> {{ selectedCapability.deviceId }}</p>
          <p><strong>Status:</strong> {{ selectedCapability.capability.status }}</p>
          <p><strong>Data:</strong> {{ selectedCapability.capability.data }}</p>
          <p><strong>Detail:</strong> {{ selectedCapability.capability.detail }}</p>
        </div>
        <div class="mt-6 flex justify-end">
          <button @click="closeCapabilityModal" class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Capability Modal -->
    <CapabilityModal 
      :is-open="!!selectedCapability" 
      :capability="selectedCapability?.capability || {}"
      :device-id="selectedCapability?.deviceId || ''"
      @close="closeCapabilityModal"
    />
  </div>
</template>

<script>
import { ref, onMounted, inject } from 'vue'
import {
  CpuChipIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'
import CapabilityModal from "../components/CapabilityModal.vue"
import DeviceCard from "../components/DeviceCard.vue"

export default {
  name: 'ClientDashboard',
  components: {
    CpuChipIcon,
    CheckCircleIcon,
    ExclamationTriangleIcon,
    ChartBarIcon,
    DeviceCard,
    CapabilityModal
  },
  setup() {
    const apiService = inject("$api")
    
    const clientInfo = ref({
      company_name: 'Navachar Ltd',
      contact_person: 'Deepak',
      email: 'deepak@navachar.com'
    })

    const clientId = ref(null)
    const loading = ref(true)
    const selectedCapability = ref(null)

    const clientStats = ref({
      totalDevices: 0,
      onlineDevices: 0,
      alerts: 0,
      dataPoints: 0
    })

    // Mock device data with professional SVG icons
    const devices = ref([])

    // API functions
    const loadClientData = async () => {
      try {
        loading.value = true
        
        // Initialize clientInfo with default values
        clientInfo.value = {
          company_name: 'Your Company',
          contact_person: 'Contact Person',
          email: 'your@email.com'
        }
        
        // Load client info from localStorage
        const user = localStorage.getItem('user')
        if (user) {
          const userData = JSON.parse(user)
          clientInfo.value = {
            company_name: userData.company_name || 'Your Company',
            contact_person: userData.contact_person || 'Contact Person',
            email: userData.email || 'your@email.com'
          }
          
          // Set client ID for capability widgets
          clientId.value = userData.client_id
          
          // Load client stats if client_id is available
          if (userData.client_id) {
            await loadClientStats(userData.client_id)
            await loadClientDevices(userData.client_id)
          }
        }
      } catch (error) {
        console.error('Error loading client data:', error)
      } finally {
        loading.value = false
      }
    }

    const loadClientStats = async (clientId) => {
      try {
        console.log('Loading client stats for:', clientId)
        
        // Get real device data to calculate stats
        const response = await apiService.getClientDevices(clientId)
        
        if (response.success && response.devices) {
          const devices = response.devices
          const onlineDevices = devices.filter(device => device.status === 'active').length
          
          clientStats.value = {
            totalDevices: devices.length,
            onlineDevices: onlineDevices,
            alerts: 0, // TODO: Implement real alerts
            dataPointsToday: 0 // TODO: Implement real data points
          }
          console.log(`✅ Loaded stats: ${devices.length} total devices, ${onlineDevices} online`)
        } else {
          // Fallback to empty stats
          clientStats.value = {
            totalDevices: 0,
            onlineDevices: 0,
            alerts: 0,
            dataPointsToday: 0
          }
        }
      } catch (error) {
        console.error('Error loading client stats:', error)
        clientStats.value = {
          totalDevices: 0,
          onlineDevices: 0,
          alerts: 0,
          dataPointsToday: 0
        }
      }
    }

    const loadClientDevices = async (clientId) => {
      try {
        console.log('Loading devices for client:', clientId)
        
        // Make real API call to get client devices
        const response = await apiService.getClientDevices(clientId)
        console.log('API response for client devices:', response)
        
        if (response.success && response.devices) {
          // Transform device data to match frontend expectations
          devices.value = response.devices.map(device => ({
            id: device.device_id,
            name: device.device_name,
            type: device.device_type,
            status: device.status,
            capabilities: device.capabilities,
            created_at: device.created_at,
            updated_at: device.updated_at,
            lastSeen: device.updated_at || device.created_at
          }))
          console.log(`✅ Loaded ${response.devices.length} devices for client ${clientId}`)
        } else {
          console.log('No devices found or API error:', response.error || 'Unknown error')
          devices.value = []
        }
      } catch (error) {
        console.error('Error loading client devices:', error)
        devices.value = []
      }
    }

    const handleDeviceRefresh = (deviceId) => {
      console.log('Refreshing device:', deviceId)
      // Update last seen timestamp
      const device = devices.value.find(d => d.id === deviceId)
      if (device) {
        device.lastSeen = new Date().toISOString()
      }
    }

    const handleCapabilityClick = (capabilityData) => {
      selectedCapability.value = capabilityData
      console.log('Capability clicked:', capabilityData)
    }

    const closeCapabilityModal = () => {
      selectedCapability.value = null
    }

    const generateCapabilityCardsFromDevice = (device) => {
      // Generate capability cards based on device capabilities
      if (!device || !device.capabilities) return []
      
      // Handle both string and array formats
      let capabilities = []
      if (typeof device.capabilities === 'string') {
        // Parse comma-separated string
        capabilities = device.capabilities.split(',').map(c => c.trim())
      } else if (Array.isArray(device.capabilities)) {
        capabilities = device.capabilities
      }
      
      return capabilities.map(capability => {
        const capType = typeof capability === 'string' ? capability : capability.type
        const capName = typeof capability === 'string' ? capability : capability.name
        
        // Generate capability data based on type
        switch (capType.toLowerCase()) {
          case 'gps':
            return {
              type: 'gps',
              name: 'GPS Location',
              icon: '/icons/gps.svg',
              status: 'Active',
              data: '21.1845316, 81.6615514',
              detail: 'Real-time location tracking'
            }
          case 'audio':
            return {
              type: 'audio',
              name: 'Audio Recording',
              icon: '/icons/audio.svg',
              status: 'Ready',
              data: 'MP3 - 30s',
              detail: 'Voice recording capability'
            }
          case 'video':
            return {
              type: 'video',
              name: 'Video Recording',
              icon: '/icons/video.svg',
              status: 'Ready',
              data: 'MP4 - 640x480',
              detail: 'Video recording capability'
            }
          case 'sensors':
            return {
              type: 'sensors',
              name: 'Sensor Data',
              icon: '/icons/sensors.svg',
              status: 'Active',
              data: 'Multiple sensors',
              detail: 'Environmental monitoring'
            }
          case 'logs':
            return {
              type: 'logs',
              name: 'System Logs',
              icon: '/icons/logs.svg',
              status: 'Available',
              data: 'Log files ready',
              detail: 'System activity logs'
            }
          case 'network':
            return {
              type: 'network',
              name: 'Network Status',
              icon: '/icons/network.svg',
              status: 'Connected',
              data: 'WiFi/Cellular',
              detail: 'Network connectivity'
            }
          default:
            return {
              type: capType,
              name: capName,
              icon: '/icons/default.svg',
              status: 'Unknown',
              data: 'No data',
              detail: 'Capability information'
            }
        }
      })
    }

    onMounted(() => {
      loadClientData()
    })

    return {
      loadClientDevices,
      generateCapabilityCardsFromDevice,
      clientInfo,
      clientStats,
      loading,
      clientId,
      devices,
      selectedCapability,
      handleDeviceRefresh,
      handleCapabilityClick,
      closeCapabilityModal
    }
  }
}
</script>

<style scoped>
.card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
  transition: all 0.2s ease;
}
</style>

    const generateCapabilityCardsFromDevice = (device) => {
      const cards = []
      if (device.capabilities) {
        const capabilities = device.capabilities.split(",").map(c => c.trim())
        capabilities.forEach(capability => {
          switch (capability.toLowerCase()) {
            case "gps":
              cards.push({
                type: "gps",
                name: "GPS",
                icon: "/icons/gps.svg",
                status: "Active",
                data: "Location tracking enabled",
                detail: "GPS positioning active"
              })
              break
            case "audio":
              cards.push({
                type: "audio",
                name: "Audio",
                icon: "/icons/audio.svg",
                status: "Available",
                data: "Audio recording ready",
                detail: "Audio capture capability"
              })
              break
            case "video":
              cards.push({
                type: "video",
                name: "Video",
                icon: "/icons/camera.svg",
                status: "Available",
                data: "Video recording ready",
                detail: "Video capture capability"
              })
              break
            case "sensors":
              cards.push({
                type: "sensors",
                name: "Sensors",
                icon: "/icons/sensors.svg",
                status: "Monitoring",
                data: "Environmental monitoring",
                detail: "Environmental sensors"
              })
              break
            case "logs":
              cards.push({
                type: "logs",
                name: "Logs",
                icon: "/icons/logs.svg",
                status: "Active",
                data: "System logs available",
                detail: "Device activity logs"
              })
              break
          }
        })
      }
      if (cards.length === 0) {
        cards.push({
          type: "default",
          name: "Basic Monitoring",
          icon: "/icons/default.svg",
          status: "Active",
          data: "Device monitoring enabled",
          detail: "Basic device status monitoring"
        })
      }
      return cards
    }

    const loadClientDevices = async (clientId) => {
      try {
        console.log('Loading devices for client:', clientId)
        const response = await apiService.getClientDevices(clientId)
        console.log('API response:', response)
        
        if (response && response.devices && response.devices.length > 0) {
          console.log('Found devices:', response.devices)
          devices.value = response.devices.map(device => ({
            id: device.device_id,
            name: device.device_name || `Device ${device.device_id.slice(0, 8)}`,
            platform: device.device_type || 'Unknown',
            status: device.status === 'active' ? 'Online' : 'Offline',
            lastSeen: device.last_seen || new Date().toISOString(),
            hasCellular: true,
            hasWifi: true,
            hasBattery: true,
            batteryLevel: 85,
            capabilities: generateCapabilityCardsFromDevice(device)
          }))
        } else {
          console.log('No devices found for client:', clientId)
          devices.value = []
        }
      } catch (error) {
        console.error('Error loading client devices:', error)
        devices.value = []
      }
    }

