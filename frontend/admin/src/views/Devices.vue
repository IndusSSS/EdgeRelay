<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Device Management</h1>
            <p class="mt-1 text-sm text-gray-500">Manage and monitor your IoT devices</p>
          </div>
          <div class="flex space-x-3">
            <button
              @click="refreshDevices"
              :disabled="loading"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              {{ loading ? 'Refreshing...' : 'Refresh' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">

      <!-- Device Status Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-blue-50 overflow-hidden shadow rounded-lg border border-blue-200">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-blue-600 truncate">Total Devices</dt>
                  <dd class="text-lg font-medium text-blue-900">{{ deviceStats.total_devices }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-green-50 overflow-hidden shadow rounded-lg border border-green-200">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-green-600 truncate">Active</dt>
                  <dd class="text-lg font-medium text-green-900">{{ deviceStats.active_devices }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-yellow-50 overflow-hidden shadow rounded-lg border border-yellow-200">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-yellow-600 truncate">Pending</dt>
                  <dd class="text-lg font-medium text-yellow-900">{{ deviceStats.pending_devices }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Devices Table -->
      <div class="bg-white shadow overflow-hidden sm:rounded-md">
        <div class="px-4 py-5 sm:px-6">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg leading-6 font-medium text-gray-900">Devices</h3>
              <p class="mt-1 max-w-2xl text-sm text-gray-500">View and manage all devices</p>
            </div>
            <div class="flex items-center space-x-3">
              <select
                v-model="selectedClient"
                @change="filterDevices"
                class="border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="">All Clients</option>
                <option v-for="client in clients" :key="client.client_id" :value="client.client_id">
                  {{ client.company_name }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- Devices Table Content -->
        <div class="border-t border-gray-200">
          <div v-if="loading" class="text-center py-12">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            <p class="mt-2 text-sm text-gray-500">Loading devices...</p>
          </div>

          <div v-else-if="filteredDevices.length === 0" class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No devices found</h3>
            <p class="mt-1 text-sm text-gray-500">Get started by adding a new device.</p>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Device Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Capabilities</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Device Type</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="device in paginatedDevices" :key="device.device_id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div>
                        <div class="text-sm font-medium text-gray-900">{{ device.device_name || 'Nil' }}</div>
                        <div class="text-sm text-gray-500">device_id: {{ device.device_id }}</div>
                        <div class="text-sm text-gray-500">client_id: {{ device.client_id || 'Not assigned' }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex flex-wrap gap-1">
                      <span v-for="capability in parseCapabilities(device.capabilities)" :key="capability" 
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {{ formatCapability(capability) }}
                      </span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ getDeviceType(device.capabilities) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusBadgeClass(device.status)" 
                          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ device.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(device.created_at) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex space-x-2">
                      <button @click="editDevice(device)" 
                              class="inline-flex items-center px-3 py-1 rounded-md text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors">Edit</button>
                      <button @click="deleteDevice(device)" 
                              class="inline-flex items-center px-3 py-1 rounded-md text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors">Delete</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pagination -->
        <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
          <div class="flex-1 flex justify-between sm:hidden">
            <button @click="currentPage = Math.max(1, currentPage - 1)" 
                    :disabled="currentPage === 1"
                    class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Previous
            </button>
            <button @click="currentPage = Math.min(totalPages, currentPage + 1)" 
                    :disabled="currentPage === totalPages"
                    class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Next
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Showing <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                to <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, filteredDevices.length) }}</span>
                of <span class="font-medium">{{ filteredDevices.length }}</span> results
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button @click="currentPage = Math.max(1, currentPage - 1)" 
                        :disabled="currentPage === 1"
                        class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  Previous
                </button>
                <button v-for="page in visiblePages" :key="page" 
                        @click="currentPage = page"
                        :class="[
                          page === currentPage
                            ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
                            : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
                          'relative inline-flex items-center px-4 py-2 border text-sm font-medium'
                        ]">
                  {{ page }}
                </button>
                <button @click="currentPage = Math.min(totalPages, currentPage + 1)" 
                        :disabled="currentPage === totalPages"
                        class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  Next
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Device Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-11/12 max-w-md shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-900">Edit Device</h3>
            <p class="text-sm text-gray-600">Update device name</p>
          </div>
          
          <form @submit.prevent="updateDevice" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Device Name</label>
              <input v-model="editForm.device_name" type="text" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500" />
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button type="button" @click="closeEditModal" class="btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn-primary">
                Update Device
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import ApiService from '../services/clientApi.js'

export default {
  name: 'Devices',
  setup() {
    const toast = useToast()
    
    // Reactive data
    const loading = ref(false)
    const devices = ref([])
    const clients = ref([])
    const selectedClient = ref('')
    const currentPage = ref(1)
    const itemsPerPage = ref(10)
    
    // Modal states
    const showEditModal = ref(false)
    const editingDevice = ref(null)
    const editForm = ref({
      device_name: ''
    })
    
    // Device statistics
    const deviceStats = ref({
      total_devices: 0,
      active_devices: 0,
      pending_devices: 0
    })
    
    // Computed properties
    const filteredDevices = computed(() => {
      let filtered = devices.value
      
      // Filter by client
      if (selectedClient.value) {
        filtered = filtered.filter(device => device.client_id === selectedClient.value)
      }
      
      return filtered
    })
    
    const totalPages = computed(() => {
      return Math.ceil(filteredDevices.value.length / itemsPerPage.value)
    })
    
    const paginatedDevices = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return filteredDevices.value.slice(start, end)
    })
    
    const visiblePages = computed(() => {
      const pages = []
      const start = Math.max(1, currentPage.value - 2)
      const end = Math.min(totalPages.value, currentPage.value + 2)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    })
    
    // Methods
    const loadDevices = async () => {
      loading.value = true
      try {
        const data = await ApiService.getDevices()
        devices.value = data.devices || []
        updateDeviceStats()
      } catch (error) {
        console.error('Error loading devices:', error)
        toast.error('Failed to load devices')
      } finally {
        loading.value = false
      }
    }
    
    const loadClients = async () => {
      try {
        const data = await ApiService.getClients()
        clients.value = data.clients || []
      } catch (error) {
        console.error('Error loading clients:', error)
      }
    }
    
    const updateDeviceStats = () => {
      deviceStats.value = {
        total_devices: devices.value.length,
        active_devices: devices.value.filter(d => d.status === 'active').length,
        pending_devices: devices.value.filter(d => d.status === 'pending').length
      }
    }
    
    const refreshDevices = async () => {
      await loadDevices()
      toast.success('Devices refreshed successfully')
    }
    
    const filterDevices = () => {
      currentPage.value = 1 // Reset to first page when filtering
    }
    
    const parseCapabilities = (capabilities) => {
      if (!capabilities) return []
      try {
        if (typeof capabilities === 'string') {
          return JSON.parse(capabilities)
        }
        return capabilities
      } catch (e) {
        return []
      }
    }
    
    const formatCapability = (capability) => {
      // Convert capability to proper format
      const capabilityMap = {
        'gps': 'GPS',
        'audio': 'Audio',
        'video': 'Video',
        'sensor': 'Sensor',
        'camera': 'Camera',
        'microphone': 'Microphone'
      }
      return capabilityMap[capability.toLowerCase()] || capability.charAt(0).toUpperCase() + capability.slice(1)
    }
    
    const getDeviceType = (capabilities) => {
      const caps = parseCapabilities(capabilities)
      if (caps.length > 0) {
        return formatCapability(caps[0])
      }
      return 'Unknown'
    }
    
    const getStatusBadgeClass = (status) => {
      const classes = {
        'active': 'bg-green-100 text-green-800',
        'online': 'bg-green-100 text-green-800',
        'pending': 'bg-yellow-100 text-yellow-800',
        'offline': 'bg-red-100 text-red-800',
        'inactive': 'bg-gray-100 text-gray-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString('en-IN', {
        timeZone: 'Asia/Kolkata',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }
    
    const editDevice = (device) => {
      editingDevice.value = device
      editForm.value = {
        device_name: device.device_name || 'Nil'
      }
      showEditModal.value = true
    }
    
    const updateDevice = async () => {
      try {
        await ApiService.updateDevice(editingDevice.value.device_id, editForm.value)
        
        // Update the device in the local array
        const deviceIndex = devices.value.findIndex(d => d.device_id === editingDevice.value.device_id)
        if (deviceIndex !== -1) {
          devices.value[deviceIndex].device_name = editForm.value.device_name
        }
        closeEditModal()
        toast.success('Device updated successfully')
      } catch (error) {
        console.error('Error updating device:', error)
        toast.error('Failed to update device')
      }
    }
    
    const deleteDevice = async (device) => {
      if (!confirm(`Are you sure you want to delete device ${device.device_name || device.device_id}?`)) {
        return
      }
      
      try {
        await ApiService.deleteDevice(device.device_id)
        
        devices.value = devices.value.filter(d => d.device_id !== device.device_id)
        updateDeviceStats()
        toast.success('Device deleted successfully')
      } catch (error) {
        console.error('Error deleting device:', error)
        toast.error('Failed to delete device')
      }
    }
    
    const closeEditModal = () => {
      showEditModal.value = false
      editingDevice.value = null
      editForm.value = {
        device_name: ''
      }
    }
    
    // Lifecycle
    onMounted(() => {
      loadDevices()
      loadClients()
    })
    
    return {
      loading,
      devices,
      clients,
      selectedClient,
      currentPage,
      itemsPerPage,
      showEditModal,
      editingDevice,
      editForm,
      deviceStats,
      filteredDevices,
      totalPages,
      paginatedDevices,
      visiblePages,
      loadDevices,
      loadClients,
      refreshDevices,
      filterDevices,
      parseCapabilities,
      formatCapability,
      getDeviceType,
      getStatusBadgeClass,
      formatDate,
      editDevice,
      updateDevice,
      deleteDevice,
      closeEditModal
    }
  }
}
</script>
