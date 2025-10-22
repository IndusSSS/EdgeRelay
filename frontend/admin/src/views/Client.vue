<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <div class="flex justify-between items-center">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">Client Management</h1>
              <p class="text-gray-600 mt-2">Manage system clients and their permissions</p>
            </div>
            <button @click="openAddClientModal" class="btn-primary">
              <PlusIcon class="h-4 w-4 mr-2" />
              Add Client
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <span class="ml-2 text-gray-600">Loading clients...</span>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Error loading clients</h3>
              <div class="mt-2 text-sm text-red-700">{{ error }}</div>
              <div class="mt-4">
                <button @click="loadClients" class="bg-red-100 px-3 py-2 rounded-md text-sm font-medium text-red-800 hover:bg-red-200">
                  Try Again
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Client Statistics -->
        <div v-else class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <UsersIcon class="h-5 w-5 text-blue-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Clients</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ clientStats.total }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <CheckCircleIcon class="h-5 w-5 text-green-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Active Clients</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ clientStats.active }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <BuildingOfficeIcon class="h-5 w-5 text-purple-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Companies</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ clientStats.companies }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <CpuChipIcon class="h-5 w-5 text-yellow-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Client Devices</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ clientStats.devices }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <!-- Filters and Search -->
        <div v-if="!loading && !error" class="card mb-6">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
            <div class="flex flex-col sm:flex-row sm:items-center space-y-4 sm:space-y-0 sm:space-x-4">
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search clients.."
                  class="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
                </div>
              </div>
              <select
                v-model="statusFilter"
                class="px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <button @click="loadClients" class="btn-secondary">
              <ArrowPathIcon class="h-4 w-4 mr-2" />
              Refresh
            </button>
          </div>
        </div>

        <!-- Clients Table -->
        <div v-if="!loading && !error" class="card">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contact Person
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contact Number
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Devices
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created On
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="client in filteredClients" :key="client.client_id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div>
                        <div class="text-sm font-medium text-gray-900">{{ client.contact_person }}</div>
                        <div class="text-sm text-gray-500">{{ client.company_name }}</div>
                        <div class="text-sm text-gray-400">client_id: {{ client.client_id }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ client.phone }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ client.email }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="client.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" 
                          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ client.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <button @click="viewClientDevices(client)" class="text-blue-600 hover:text-blue-900">
                      {{ getClientDeviceCount(client.client_id) }} device{{ getClientDeviceCount(client.client_id) !== 1 ? 's' : '' }}
                    </button>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(client.created_at) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex space-x-2">
                      <button @click="editClient(client)" class="px-3 py-1 bg-green-500 text-white text-xs rounded hover:bg-green-600">
                        Edit
                      </button>
                      <button @click="deleteClient(client)" class="px-3 py-1 bg-red-500 text-white text-xs rounded hover:bg-red-600">
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Client Modal -->
    <div v-if="showAddClientModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-11/12 max-w-2xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-900">Add New Client</h3>
            <p class="text-sm text-gray-600">Create a new client account</p>
          </div>
          
          
            <div>
              <label class="block text-sm font-medium text-gray-700">Client ID</label>
              <input v-model="newClient.client_id" type="text" readonly placeholder="Auto-generated UUID" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm bg-gray-100" />
            </div>
          <form @submit.prevent="addClient" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Company Name</label>
                <input v-model="newClient.company_name" type="text" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Contact Person</label>
                <input v-model="newClient.contact_person" type="text" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Email</label>
                <input v-model="newClient.email" type="email" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Phone</label>
                <input v-model="newClient.phone" type="tel" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Address</label>
              <textarea v-model="newClient.address" rows="3" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"></textarea>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Client Username</label>
                <input v-model="newClient.client_username" type="text" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Password</label>
                <input v-model="newClient.password" type="password" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button type="button" @click="closeAddClientModal" class="btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn-primary">
                Add Client
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Edit Client Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-11/12 max-w-2xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-900">Edit Client</h3>
            <p class="text-sm text-gray-600">Update client information</p>
          </div>
          
          <form @submit.prevent="updateClient" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Company Name</label>
                <input v-model="editForm.company_name" type="text" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Contact Person</label>
                <input v-model="editForm.contact_person" type="text" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Email</label>
                <input v-model="editForm.email" type="email" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Phone</label>
                <input v-model="editForm.phone" type="tel" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Address</label>
              <textarea v-model="editForm.address" rows="3" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"></textarea>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Client Username</label>
                <input v-model="editForm.client_username" type="text" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Password (leave blank to keep current)</label>
                <input v-model="editForm.password" type="password" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
            </div>
            
            <div class="flex items-center">
              <input v-model="editForm.is_active" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
              <label class="ml-2 block text-sm text-gray-900">Active</label>
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button type="button" @click="closeEditModal" class="btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn-primary">
                Update Client
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import ApiService from '../services/clientApi.js'
import { 
  PlusIcon, 
  UsersIcon, 
  CheckCircleIcon, 
  BuildingOfficeIcon,
  CpuChipIcon,
  MagnifyingGlassIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()

// Reactive data
const loading = ref(false)
const error = ref(null)
const clients = ref([])

const deviceCounts = ref({})
const clientStats = ref({
  total: 0,
  active: 0,
  companies: 0,
  devices: 0
})
const searchQuery = ref('')
const statusFilter = ref('')

// Modal states
const showAddClientModal = ref(false)
const showEditModal = ref(false)

// Form data
const newClient = ref({
  client_id: '',
  company_name: '',
  contact_person: '',
  email: '',
  phone: '',
  address: '',
  client_username: '',
  password: ''
})

const editForm = ref({
  client_id: '',
  company_name: '',
  contact_person: '',
  email: '',
  phone: '',
  address: '',
  client_username: '',
  password: '',
  is_active: true
})

// Computed properties
const filteredClients = computed(() => {
  let filtered = clients.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(client => 
      client.company_name.toLowerCase().includes(query) ||
      client.contact_person.toLowerCase().includes(query) ||
      client.email.toLowerCase().includes(query) ||
      client.client_id.toLowerCase().includes(query)
    )
  }

  // Filter by status
  if (statusFilter.value) {
    filtered = filtered.filter(client => 
      statusFilter.value === 'active' ? client.is_active : !client.is_active
    )
  }

  return filtered
})

// Methods
const loadClients = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await ApiService.getClients()
    clients.value = response.clients || []

    
    // Load device counts for all clients
    try {
      const deviceCountsResponse = await ApiService.getClientDeviceCounts()
      deviceCounts.value = deviceCountsResponse.device_counts || {}
    } catch (err) {
      console.error("Error loading device counts:", err)
      deviceCounts.value = {}
    }
    
    // Calculate stats
    clientStats.value = {
      total: clients.value.length,
      active: clients.value.filter(c => c.is_active).length,
      companies: new Set(clients.value.map(c => c.company_name)).size,
      devices: await getTotalDeviceCount()
    }
  } catch (err) {
    error.value = err.message || 'Failed to load clients'
    console.error('Error loading clients:', err)
  } finally {
    loading.value = false
  }
}

const getTotalDeviceCount = async () => {
  try {
    const response = await ApiService.getDevices()
    return response.devices ? response.devices.length : 0
  } catch (err) {
    console.error('Error loading device count:', err)
    return 0
  }
}

const getClientDeviceCount = (clientId) => {
  // Surface the count fetched from the backend; default to 0 when absent
  return deviceCounts.value[clientId] || 0
}

const openAddClientModal = async () => {
  try {
    const uniqueId = await ApiService.generateUniqueClientId()
    newClient.value.client_id = uniqueId.client_id
  } catch (err) {
    console.error("Error generating client ID:", err)
    newClient.value.client_id = ""
  }
  showAddClientModal.value = true
}

const addClient = async () => {
  try {
    await ApiService.createClient(newClient.value)
    await loadClients()
    closeAddClientModal()
    alert('Client added successfully!')
  } catch (err) {
    console.error('Error adding client:', err)
    alert('Failed to add client: ' + (err.message || 'Unknown error'))
  }
}

const editClient = (client) => {
  editForm.value = { ...client }
  showEditModal.value = true
}

const updateClient = async () => {
  try {
    await ApiService.updateClient(editForm.value.client_id, editForm.value)
    await loadClients()
    closeEditModal()
    alert('Client updated successfully!')
  } catch (err) {
    console.error('Error updating client:', err)
    alert('Failed to update client: ' + (err.message || 'Unknown error'))
  }
}

const deleteClient = async (client) => {
  if (!confirm(`Are you sure you want to delete ${client.company_name}?`)) {
    return
  }
  
  try {
    await ApiService.deleteClient(client.client_id)
    await loadClients()
    alert('Client deleted successfully!')
  } catch (err) {
    console.error('Error deleting client:', err)
    alert('Failed to delete client: ' + (err.message || 'Unknown error'))
  }
}

const viewClientDevices = (client) => {
  router.push(`/devices?client=${client.client_id}`)
}

const closeAddClientModal = () => {
  showAddClientModal.value = false
  newClient.value = {
    client_id: '',
    company_name: '',
    contact_person: '',
    email: '',
    phone: '',
    address: '',
    client_username: '',
    password: ''
  }
}

const closeEditModal = () => {
  showEditModal.value = false
  editForm.value = {
    client_id: '',
    company_name: '',
    contact_person: '',
    email: '',
    phone: '',
    address: '',
    client_username: '',
    password: '',
    is_active: true
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(() => {
  loadClients()
})
</script>

<style scoped>
.btn-primary {
  @apply inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500;
}

.btn-secondary {
  @apply inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500;
}

.card {
  @apply bg-white overflow-hidden shadow rounded-lg;
}
</style>
