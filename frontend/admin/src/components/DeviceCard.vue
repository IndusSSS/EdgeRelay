<template>
  <div class="device-card bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
    <!-- Device Header -->
    <div class="flex justify-between items-start mb-4">
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-gray-900">{{ device.name || 'Unknown Device' }}</h3>
        <p class="text-sm text-gray-600">{{ device.device_id || device.id || "No UUID" }}</p>
        <p class="text-xs text-gray-500">{{ device.platform || 'Unknown Platform' }}</p>
      </div>
      <div class="flex items-center space-x-2">
        <!-- Online Status -->
        <div class="flex items-center space-x-1">
          <div 
            class="w-2 h-2 rounded-full"
            :class="deviceStatus.isOnline ? 'bg-green-500' : 'bg-red-500'"
          ></div>
          <span class="text-xs text-gray-600">
            {{ deviceStatus.isOnline ? 'Online' : 'Offline' }}
          </span>
        </div>
        
        <!-- MQTT Status -->
        <div class="flex items-center space-x-1">
          <div 
            class="w-2 h-2 rounded-full"
            :class="mqttStatus.isConnected ? 'bg-blue-500' : 'bg-gray-400'"
          ></div>
          <span class="text-xs text-gray-600">
            {{ mqttStatus.isConnected ? 'MQTT' : 'No MQTT' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Device Info -->
    <div class="grid grid-cols-2 gap-4 mb-4">
      <div class="text-center">
        <div class="text-2xl font-bold text-gray-900">{{ deviceStatus.battery || 'N/A' }}%</div>
        <div class="text-xs text-gray-600">Battery</div>
      </div>
      <div class="text-center">
        <div class="text-2xl font-bold text-gray-900">{{ deviceStatus.signal || 'N/A' }}</div>
        <div class="text-xs text-gray-600">Signal</div>
      </div>
    </div>

    <!-- Last Seen -->
    <div class="text-center mb-4">
      <div class="text-sm text-gray-600">Last Seen</div>
      <div class="text-xs text-gray-500">{{ formatTimestamp(deviceStatus.lastSeen) }}</div>
    </div>

    <!-- Capability Cards -->
    <div class="space-y-2">
      <div class="text-sm font-medium text-gray-700 mb-2">Capabilities:</div>
      <div class="grid grid-cols-2 gap-2">
        <div 
          v-for="capability in capabilityCards" 
          :key="capability.type"
          @click="handleCapabilityClick(capability)"
          class="p-2 rounded-lg border cursor-pointer hover:bg-gray-50 transition-colors"
          :class="getCapabilityClass(capability.type)"
        >
          <div class="flex items-center space-x-2">
            <i :class="capability.icon" class="text-sm"></i>
            <span class="text-xs font-medium">{{ capability.name }}</span>
          </div>
          <div v-if="capability.hasData" class="text-xs text-green-600 mt-1">
            <i class="fas fa-circle text-xs"></i>
            Data Available
          </div>
        </div>
      </div>
    </div>

    <!-- Device Controls -->
    <div class="mt-4 pt-4 border-t border-gray-200">
      <div class="flex space-x-2">
        <button
          @click="refreshDevice"
          :disabled="isLoading"
          class="flex-1 px-3 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 disabled:opacity-50"
        >
          <i class="fas fa-sync-alt mr-1" :class="{ 'animate-spin': isLoading }"></i>
          Refresh
        </button>
        <button
          @click="toggleDeviceStatus"
          :disabled="isLoading"
          class="flex-1 px-3 py-2 text-sm rounded"
          :class="deviceStatus.isOnline ? 'bg-red-600 text-white hover:bg-red-700' : 'bg-green-600 text-white hover:bg-green-700'"
        >
          <i class="fas fa-power-off mr-1"></i>
          {{ deviceStatus.isOnline ? 'Disable' : 'Enable' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import mqttClient from '../services/mqttClient.js'
import cacheManager from '../services/cacheManager.js'

export default {
  name: 'DeviceCard',
  props: {
    device: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      // MQTT connection status
      mqttStatus: {
        isConnected: false
      },
      
      // Device status
      deviceStatus: {
        isOnline: false,
        battery: null,
        signal: null,
        lastSeen: null
      },
      
      // UI state
      isLoading: false,
      
      // MQTT message handlers
      messageHandlers: []
    }
  },
  computed: {
    /**
     * Generate capability cards from device capabilities
     */
    capabilityCards() {
      const capabilities = this.device.capabilities || []
      const capabilityList = Array.isArray(capabilities) ? capabilities : capabilities.split(',').map(c => c.trim())
      
      return capabilityList.map(capability => {
        const capType = capability.toLowerCase()
        
        switch (capType) {
          case 'gps':
            return {
              type: 'gps',
              name: 'GPS Location',
              icon: 'fas fa-map-marker-alt',
              hasData: this.hasCapabilityData('gps')
            }
          case 'audio':
            return {
              type: 'audio',
              name: 'Audio Recording',
              icon: 'fas fa-microphone',
              hasData: this.hasCapabilityData('audio')
            }
          case 'video':
            return {
              type: 'video',
              name: 'Video Recording',
              icon: 'fas fa-video',
              hasData: this.hasCapabilityData('video')
            }
          case 'sensor':
            return {
              type: 'sensor',
              name: 'Sensors',
              icon: 'fas fa-thermometer-half',
              hasData: this.hasCapabilityData('sensor')
            }
          case 'network':
            return {
              type: 'network',
              name: 'Network',
              icon: 'fas fa-wifi',
              hasData: this.hasCapabilityData('network')
            }
          case 'monitoring':
            return {
              type: 'monitoring',
              name: 'Monitoring',
              icon: 'fas fa-chart-line',
              hasData: this.hasCapabilityData('monitoring')
            }
          default:
            return {
              type: capType,
              name: capability,
              icon: 'fas fa-cog',
              hasData: false
            }
        }
      })
    }
  },
  async mounted() {
    await this.initializeMQTT()
    this.setupMessageHandlers()
    this.loadDeviceStatus()
  },
  beforeUnmount() {
    this.cleanup()
  },
  methods: {
    /**
     * Initialize MQTT connection
     */
    async initializeMQTT() {
      try {
        // Add event listeners
        mqttClient.addEventListener('connected', this.onMQTTConnected)
        mqttClient.addEventListener('disconnected', this.onMQTTDisconnected)
        mqttClient.addEventListener('dataUpdate', this.onDataUpdate)
        
        // Connect if not already connected
        if (!mqttClient.isConnected) {
          await mqttClient.connect()
        }
        
        // Subscribe to device status updates
        mqttClient.subscribeToDevice(this.device.device_id, ['status', 'heartbeat'])
        
        this.mqttStatus.isConnected = mqttClient.isConnected
        
      } catch (error) {
        console.error('❌ Failed to initialize MQTT:', error)
        this.$emit('error', 'Failed to connect to real-time data service')
      }
    },

    /**
     * Setup message handlers for device data
     */
    setupMessageHandlers() {
      const statusHandler = (deviceId, data, topic) => {
        if (deviceId === this.device.device_id) {
          this.handleStatusUpdate(data)
        }
      }
      
      const heartbeatHandler = (deviceId, data, topic) => {
        if (deviceId === this.device.device_id) {
          this.handleHeartbeat(data)
        }
      }
      
      mqttClient.addMessageHandler('status', statusHandler)
      mqttClient.addMessageHandler('heartbeat', heartbeatHandler)
      
      this.messageHandlers.push(
        { type: 'status', handler: statusHandler },
        { type: 'heartbeat', handler: heartbeatHandler }
      )
    },

    /**
     * Load device status from cache
     */
    loadDeviceStatus() {
      // Load from cache
      const cachedStatus = cacheManager.get(this.device.device_id, 'status', 'latest')
      if (cachedStatus) {
        this.deviceStatus = { ...this.deviceStatus, ...cachedStatus }
      }
      
      // Load capability data status
      this.updateCapabilityDataStatus()
    },

    /**
     * Handle status update from MQTT
     */
    handleStatusUpdate(data) {
      try {
        this.deviceStatus = {
          isOnline: data.status === 'online',
          battery: data.battery,
          signal: data.signal,
          lastSeen: data.timestamp || new Date().toISOString()
        }
        
        // Cache the status
        cacheManager.set(this.device.device_id, 'status', this.deviceStatus, 'latest')
        
        console.log('📊 Device status updated:', this.deviceStatus)
        
      } catch (error) {
        console.error('❌ Error handling status update:', error)
      }
    },

    /**
     * Handle heartbeat from MQTT
     */
    handleHeartbeat(data) {
      try {
        this.deviceStatus.lastSeen = data.timestamp || new Date().toISOString()
        this.deviceStatus.isOnline = true
        
        // Cache the heartbeat
        cacheManager.set(this.device.device_id, 'status', this.deviceStatus, 'latest')
        
        console.log('💓 Device heartbeat received:', this.device.device_id)
        
      } catch (error) {
        console.error('❌ Error handling heartbeat:', error)
      }
    },

    /**
     * Check if capability has data
     */
    hasCapabilityData(capabilityType) {
      const cachedData = cacheManager.get(this.device.device_id, capabilityType, 'latest')
      return cachedData !== null
    },

    /**
     * Update capability data status
     */
    updateCapabilityDataStatus() {
      // This will trigger reactivity for capability cards
      this.$forceUpdate()
    },

    /**
     * Handle capability card click
     */
    handleCapabilityClick(capability) {
      if (capability.hasData) {
        this.$emit('capability-click', {
          device: this.device,
          capability: capability
        })
      } else {
        this.$emit('capability-click', {
          device: this.device,
          capability: capability,
          message: 'No data available for this capability'
        })
      }
    },

    /**
     * Get capability card class
     */
    getCapabilityClass(capabilityType) {
      const baseClass = 'border-gray-200'
      const hasData = this.hasCapabilityData(capabilityType)
      
      if (hasData) {
        return `${baseClass} border-green-200 bg-green-50`
      }
      
      return baseClass
    },

    /**
     * Refresh device data
     */
    async refreshDevice() {
      this.isLoading = true
      
      try {
        // Request device status
        await mqttClient.publishMessage(`devices/${this.device.device_id}/commands/status`, {
          command: 'request_status',
          timestamp: new Date().toISOString()
        })
        
        // Wait a bit for response
        await new Promise(resolve => setTimeout(resolve, 2000))
        
      } catch (error) {
        console.error('❌ Error refreshing device:', error)
        this.$emit('error', 'Failed to refresh device data')
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Toggle device status
     */
    async toggleDeviceStatus() {
      this.isLoading = true
      
      try {
        const command = this.deviceStatus.isOnline ? 'disable' : 'enable'
        
        await mqttClient.publishMessage(`devices/${this.device.device_id}/commands/control`, {
          command: command,
          timestamp: new Date().toISOString()
        })
        
        console.log(`🔧 Device ${command} command sent`)
        
      } catch (error) {
        console.error('❌ Error toggling device status:', error)
        this.$emit('error', 'Failed to toggle device status')
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Format timestamp for display
     */
    formatTimestamp(timestamp) {
      if (!timestamp) return 'Never'
      return new Date(timestamp).toLocaleString()
    },

    /**
     * MQTT event handlers
     */
    onMQTTConnected() {
      this.mqttStatus.isConnected = true
      console.log('✅ MQTT connected for device card')
    },

    onMQTTDisconnected() {
      this.mqttStatus.isConnected = false
      console.log('🔌 MQTT disconnected for device card')
    },

    onDataUpdate(event) {
      if (event.deviceId === this.device.device_id) {
        if (event.dataType === 'status') {
          this.handleStatusUpdate(event.data)
        } else if (event.dataType === 'heartbeat') {
          this.handleHeartbeat(event.data)
        }
        
        // Update capability data status
        this.updateCapabilityDataStatus()
      }
    },

    /**
     * Cleanup resources
     */
    cleanup() {
      // Remove message handlers
      this.messageHandlers.forEach(({ type, handler }) => {
        mqttClient.removeMessageHandler(type, handler)
      })
      
      // Remove event listeners
      mqttClient.removeEventListener('connected', this.onMQTTConnected)
      mqttClient.removeEventListener('disconnected', this.onMQTTDisconnected)
      mqttClient.removeEventListener('dataUpdate', this.onDataUpdate)
    }
  }
}
</script>

<style scoped>
.device-card {
  transition: all 0.3s ease;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
