<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <div class="flex justify-between items-center">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">User Management</h1>
              <p class="text-gray-600 mt-2">Manage system users and their permissions</p>
            </div>
            <button @click="showAddUserModal = true" class="btn-primary">
              <PlusIcon class="h-4 w-4 mr-2" />
              Add User
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <span class="ml-2 text-gray-600">Loading users...</span>
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
              <h3 class="text-sm font-medium text-red-800">Error loading users</h3>
              <div class="mt-2 text-sm text-red-700">{{ error }}</div>
              <div class="mt-4">
                <button @click="loadUsers" class="bg-red-100 px-3 py-2 rounded-md text-sm font-medium text-red-800 hover:bg-red-200">
                  Try Again
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- User Statistics -->
        <div v-else class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <UsersIcon class="h-5 w-5 text-blue-600" />
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Users</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ userStats.total }}</dd>
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
                  <dt class="text-sm font-medium text-gray-500 truncate">Active Users</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ userStats.active }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <ShieldCheckIcon class="h-5 w-5 text-purple-600" />
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Admins</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ userStats.admins }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-8 w-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <ClockIcon class="h-5 w-5 text-yellow-600" />
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Clients</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ userStats.clients }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <!-- Filters and Search -->
        <div v-if="!loading && !error" class="card mb-6">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
            <div class="flex items-center space-x-4">
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search users..."
                  class="input-field"
                />
              </div>
              <select v-model="roleFilter" class="input-field">
                <option value="">All Roles</option>
                <option value="admin">Admin</option>
                <option value="operator">Operator</option>
                <option value="client">Client</option>
              </select>
              <select v-model="statusFilter" class="input-field">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <div class="flex items-center space-x-2">
              <button @click="loadUsers" class="btn-secondary">
                <ArrowPathIcon class="h-4 w-4 mr-2" />
                Refresh
              </button>
            </div>
          </div>
        </div>

        <!-- Users Table -->
        <div v-if="!loading && !error" class="card">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Login</th>                                                                                                                          
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-if="filteredUsers.length === 0">
                  <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                    No users found. Click "Add User" to create your first user.
                  </td>
                </tr>
                <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center mr-3">
                        <UserIcon class="h-4 w-4 text-gray-600" />
                      </div>
                      <div>
                        <div class="text-sm font-medium text-gray-900">{{ user.full_name || user.company_name }}</div>
                        <div class="text-sm text-gray-500">{{ user.username }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ user.email }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getRoleBadgeColor(user.roles[0])">                                                                                                                                                                                                                                       
                      {{ user.roles[0] }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getStatusBadgeColor(user.is_active)">                                                                                                                                                                                                                                    
                      {{ user.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatLastLogin(user.last_login) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button @click="editUser(user)" class="text-primary-600 hover:text-primary-900 mr-3">Edit</button>
                    <button @click="toggleUserStatus(user)" class="text-green-600 hover:text-green-900 mr-3">
                      {{ user.is_active ? 'Deactivate' : 'Activate' }}
                    </button>
                    <button @click="deleteUser(user)" class="text-red-600 hover:text-red-900">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Add User Modal -->
        <div v-if="showAddUserModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Add New User</h3>
            <form @submit.prevent="addUser">
              <div class="space-y-4">
                <div v-if="newUser.role === 'client'">
                  <label class="block text-sm font-medium text-gray-700">Company Name</label>
                  <input v-model="newUser.company_name" type="text" required class="input-field" />
                </div>
                <div v-else>
                  <label class="block text-sm font-medium text-gray-700">Full Name</label>
                  <input v-model="newUser.full_name" type="text" required class="input-field" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Username</label>
                  <input v-model="newUser.username" type="text" required class="input-field" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Email</label>
                  <input v-model="newUser.email" type="email" required class="input-field" />
                </div>
                <div v-if="newUser.role === 'client'">
                  <label class="block text-sm font-medium text-gray-700">Contact Person</label>
                  <input v-model="newUser.contact_person" type="text" required class="input-field" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Password</label>
                  <input v-model="newUser.password" type="password" required class="input-field" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Role</label>
                  <select v-model="newUser.role" required class="input-field">
                    <option value="">Select Role</option>
                    <option value="admin">Admin</option>
                    <option value="operator">Operator</option>
                    <option value="client">Client</option>
                  </select>
                </div>
              </div>
              <div class="mt-6 flex justify-end space-x-3">
                <button type="button" @click="showAddUserModal = false" class="btn-secondary">
                  Cancel
                </button>
                <button type="submit" class="btn-primary">
                  Add User
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, inject } from 'vue'
import {
  BellIcon,
  UserIcon,
  UsersIcon,
  CheckCircleIcon,
  ShieldCheckIcon,
  ClockIcon,
  PlusIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'
// API service will be injected

export default {
  name: 'Users',
  components: {
    BellIcon,
    UserIcon,
    UsersIcon,
    CheckCircleIcon,
    ShieldCheckIcon,
    ClockIcon,
    PlusIcon,
    ArrowPathIcon
  },
  setup() {
    const apiService = inject('$api')
    
    const userStats = ref({
      total: 0,
      active: 0,
      admins: 0,
      clients: 0
    })

    const users = ref([])
    const loading = ref(false)
    const error = ref(null)


    const searchQuery = ref('')
    const roleFilter = ref('')
    const statusFilter = ref('')
    const showAddUserModal = ref(false)
    const newUser = ref({
      full_name: '',
      company_name: '',
      contact_person: '',
      username: '',
      email: '',
      password: '',
      role: ''
    })

    // Load users from API
    const loadUsers = async () => {
      loading.value = true
      error.value = null
      
      try {
        console.log('Loading users and clients...')
        const allUsers = await apiService.getAllUsersAndClients()
        users.value = allUsers
        
        // Calculate stats
        userStats.value = {
          total: allUsers.length,
          active: allUsers.filter(u => u.is_active).length,
          admins: allUsers.filter(u => u.roles.includes('admin')).length,
          clients: allUsers.filter(u => u.roles.includes('client')).length
        }
        
        console.log('Users loaded successfully:', allUsers.length)
      } catch (err) {
        console.error('Failed to load users:', err)
        error.value = err.message || 'Failed to load users'
      } finally {
        loading.value = false
      }
    }

    const filteredUsers = computed(() => {
      return users.value.filter(user => {
        const matchesSearch = !searchQuery.value || 
          (user.full_name && user.full_name.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
          (user.company_name && user.company_name.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
          user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesRole = !roleFilter.value || user.roles.includes(roleFilter.value)
        const matchesStatus = !statusFilter.value || 
          (statusFilter.value === 'active' && user.is_active) ||
          (statusFilter.value === 'inactive' && !user.is_active)
        
        return matchesSearch && matchesRole && matchesStatus
      })
    })

    const getRoleBadgeColor = (role) => {
      const colors = {
        admin: 'bg-red-100 text-red-800',
        operator: 'bg-blue-100 text-blue-800',
        client: 'bg-green-100 text-green-800'
      }
      return colors[role] || 'bg-gray-100 text-gray-800'
    }

    const getStatusBadgeColor = (isActive) => {
      return isActive 
        ? 'bg-green-100 text-green-800'
        : 'bg-gray-100 text-gray-800'
    }

    const formatLastLogin = (timestamp) => {
      if (!timestamp) return 'Never'
      const now = new Date()
      const time = new Date(timestamp)
      const diff = now - time
      const minutes = Math.floor(diff / (1000 * 60))
      
      if (minutes < 1) return 'Just now'
      if (minutes < 60) return `${minutes} min ago`
      const hours = Math.floor(minutes / 60)
      if (hours < 24) return `${hours} hours ago`
      const days = Math.floor(hours / 24)
      return `${days} days ago`
    }

    const editUser = (user) => {
      alert(`Editing user: ${user.username}`)
    }

    const toggleUserStatus = async (user) => {
      try {
        await apiService.toggleUserStatus(user.id, !user.is_active)
        user.is_active = !user.is_active
        
        // Update stats
        if (user.is_active) {
          userStats.value.active++
        } else {
          userStats.value.active--
        }
      } catch (err) {
        console.error('Failed to toggle user status:', err)
        alert('Failed to update user status')
      }
    }

    const deleteUser = async (user) => {
      if (confirm(`Are you sure you want to delete user ${user.username}?`)) {
        try {
          await apiService.deleteUser(user.id)
          const index = users.value.findIndex(u => u.id === user.id)
          if (index > -1) {
            users.value.splice(index, 1)
            userStats.value.total--
            if (user.is_active) userStats.value.active--
            if (user.roles.includes('admin')) userStats.value.admins--
            if (user.roles.includes('client')) userStats.value.clients--
          }
        } catch (err) {
          console.error('Failed to delete user:', err)
          alert('Failed to delete user')
        }
      }
    }

    const addUser = async () => {
      try {
        await apiService.createUser(newUser.value)
        
        // Reload users to get the updated list
        await loadUsers()
        
        newUser.value = { 
          full_name: '', 
          company_name: '', 
          contact_person: '',
          username: '', 
          email: '', 
          password: '', 
          role: '' 
        }
        showAddUserModal.value = false
      } catch (err) {
        console.error('Failed to create user:', err)
        alert('Failed to create user')
      }
    }

    const refreshUsers = () => {
      loadUsers()
    }

    // Load users on component mount
    onMounted(() => {
      loadUsers()
    })

    return {
      userStats,
      
      
      users,
      loading,
      error,
      searchQuery,
      roleFilter,
      statusFilter,
      showAddUserModal,
      newUser,
      filteredUsers,
      getRoleBadgeColor,
      getStatusBadgeColor,
      formatLastLogin,
      editUser,
      toggleUserStatus,
      deleteUser,
      addUser,
      refreshUsers,
      loadUsers
    }
  }
}
</script>
