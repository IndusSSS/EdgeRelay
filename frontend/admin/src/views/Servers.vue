<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Edge Server & Sensor Management</h1>
            <p class="mt-1 text-sm text-gray-500">Manage and monitor your edge servers and connected sensors</p>
          </div>
          <div class="flex space-x-3">
            <button
              @click="refreshServers"
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

      <!-- System Overview Cards -->
      <div class="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
        <!-- Server Cards -->
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
                  <dt class="text-sm font-medium text-blue-600 truncate">Total Servers</dt>
                  <dd class="text-lg font-medium text-blue-900">{{ serverStats.total_servers }}</dd>
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
                  <dt class="text-sm font-medium text-green-600 truncate">Online Servers</dt>
                  <dd class="text-lg font-medium text-green-900">{{ serverStats.online_servers }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-red-50 overflow-hidden shadow rounded-lg border border-red-200">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-red-600 truncate">Offline Servers</dt>
                  <dd class="text-lg font-medium text-red-900">{{ serverStats.offline_servers }}</dd>
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-yellow-600 truncate">Alerts Active</dt>
                  <dd class="text-lg font-medium text-yellow-900">{{ serverStats.active_alerts }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-purple-50 overflow-hidden shadow rounded-lg border border-purple-200">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-purple-600 truncate">Total Sensors</dt>
                  <dd class="text-lg font-medium text-purple-900">{{ serverStats.total_sensors }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Additional Sensor Cards -->
      <div class="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
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
                  <dt class="text-sm font-medium text-green-600 truncate">Online Sensors</dt>
                  <dd class="text-lg font-medium text-green-900">{{ serverStats.online_sensors }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-red-50 overflow-hidden shadow rounded-lg border border-red-200">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-red-600 truncate">Offline Sensors</dt>
                  <dd class="text-lg font-medium text-red-900">{{ serverStats.offline_sensors }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-blue-50 overflow-hidden shadow rounded-lg border border-blue-200">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-blue-600 truncate">Cameras Connected</dt>
                  <dd class="text-lg font-medium text-blue-900">{{ serverStats.cameras_connected }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-indigo-50 overflow-hidden shadow rounded-lg border border-indigo-200">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-indigo-600 truncate">Sensors Active</dt>
                  <dd class="text-lg font-medium text-indigo-900">{{ serverStats.sensors_active }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-teal-50 overflow-hidden shadow rounded-lg border border-teal-200">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-teal-600 truncate">Data Points</dt>
                  <dd class="text-lg font-medium text-teal-900">{{ serverStats.data_points }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Edge Servers List -->
      <div class="bg-white shadow overflow-hidden sm:rounded-md mb-8">
        <div class="px-4 py-5 sm:px-6">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg leading-6 font-medium text-gray-900">Edge Servers List</h3>
              <p class="mt-1 max-w-2xl text-sm text-gray-500">View and manage all edge servers</p>
            </div>
          </div>
        </div>

        <!-- Servers Table Content -->
        <div class="border-t border-gray-200">
          <div v-if="loading" class="text-center py-12">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            <p class="mt-2 text-sm text-gray-500">Loading servers...</p>
          </div>

          <div v-else-if="servers.length === 0" class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No servers found</h3>
            <p class="mt-1 text-sm text-gray-500">Get started by adding a new edge server.</p>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Server Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CPU</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Memory</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cameras</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sensors</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Alerts</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="server in paginatedServers" :key="server.server_id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div>
                        <div class="text-sm font-medium text-gray-900">{{ server.server_name }}</div>
                        <div class="text-sm text-gray-500">ID: {{ server.server_id }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusBadgeClass(server.status)" 
                          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ server.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ server.location || 'Unknown' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ server.cpu_usage || '--' }}%
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ server.memory_usage || '--' }}GB
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ server.cameras_count || 0 }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ server.sensors_count || 0 }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ server.alerts_count || 0 }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button @click="viewServer(server)" 
                            class="inline-flex items-center px-3 py-1 rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
                      View
                    </button>
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
                to <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, servers.length) }}</span>
                of <span class="font-medium">{{ servers.length }}</span> results
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

      <!-- Server Details Modal (Overlay) -->
      <div v-if="showServerDetails" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
        <div class="relative top-10 mx-auto p-5 border w-11/12 max-w-7xl shadow-lg rounded-md bg-white">
          <div class="mt-3">
            <!-- Modal Header -->
            <div class="mb-6">
              <div class="flex justify-between items-center">
                <h3 class="text-xl font-semibold text-gray-900">SERVER DETAILS: {{ selectedServer?.server_name }}</h3>
                <button @click="closeServerDetails" class="text-gray-400 hover:text-gray-600">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Real-time Metrics -->
            <div class="mb-8">
              <h4 class="text-lg font-medium text-gray-900 mb-4">Real-time Metrics</h4>
              <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-gray-50 p-4 rounded-lg">
                  <h5 class="text-sm font-medium text-gray-700 mb-2">CPU Usage</h5>
                  <div class="text-2xl font-bold text-blue-600">{{ selectedServer?.cpu_usage || 0 }}%</div>
                  <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div class="bg-blue-600 h-2 rounded-full" :style="{ width: (selectedServer?.cpu_usage || 0) + '%' }"></div>
                  </div>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <h5 class="text-sm font-medium text-gray-700 mb-2">Memory Usage</h5>
                  <div class="text-2xl font-bold text-green-600">{{ selectedServer?.memory_usage || 0 }}GB</div>
                  <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div class="bg-green-600 h-2 rounded-full" :style="{ width: '60%' }"></div>
                  </div>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <h5 class="text-sm font-medium text-gray-700 mb-2">Network I/O</h5>
                  <div class="text-2xl font-bold text-purple-600">{{ selectedServer?.network_io || '0' }}MB/s</div>
                  <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div class="bg-purple-600 h-2 rounded-full" :style="{ width: '40%' }"></div>
                  </div>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <h5 class="text-sm font-medium text-gray-700 mb-2">Disk Usage</h5>
                  <div class="text-2xl font-bold text-orange-600">{{ selectedServer?.disk_usage || '0' }}%</div>
                  <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div class="bg-orange-600 h-2 rounded-full" :style="{ width: (selectedServer?.disk_usage || 0) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Cameras Table -->
            <div class="mb-8">
              <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-medium text-gray-900">Cameras</h4>
                <button @click="addCamera" class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Add Camera
                </button>
              </div>
              <div class="bg-white shadow overflow-hidden sm:rounded-md">
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Camera ID</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Resolution</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">FPS</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IP Address</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Alerts</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="camera in selectedServer?.cameras || []" :key="camera.id" class="hover:bg-gray-50">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {{ camera.name }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                          <span :class="getStatusBadgeClass(camera.status)" 
                                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                            {{ camera.status }}
                          </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {{ camera.resolution }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {{ camera.fps }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {{ camera.ip_address || 'N/A' }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {{ camera.alerts || 0 }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button class="text-blue-600 hover:text-blue-900 mr-3">View</button>
                          <button class="text-gray-600 hover:text-gray-900">Settings</button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- Sensors Table -->
            <div class="mb-8">
              <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-medium text-gray-900">Sensors</h4>
                <button @click="addSensor" class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Add Sensor
                </button>
              </div>
              <div class="bg-white shadow overflow-hidden sm:rounded-md">
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sensor ID</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Update</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Alerts</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="sensor in selectedServer?.sensors || []" :key="sensor.id" class="hover:bg-gray-50">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {{ sensor.name }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                          <span :class="getStatusBadgeClass(sensor.status)" 
                                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                            {{ sensor.status }}
                          </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {{ sensor.type }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {{ sensor.value }} {{ sensor.unit }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {{ sensor.location || 'N/A' }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {{ formatDate(sensor.last_update) }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {{ sensor.alerts || 0 }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button class="text-blue-600 hover:text-blue-900 mr-3">View</button>
                          <button class="text-gray-600 hover:text-gray-900">Settings</button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- Recent Alerts & Events -->
            <div>
              <h4 class="text-lg font-medium text-gray-900 mb-4">Recent Alerts & Events</h4>
              <div class="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
                <div v-for="event in selectedServer?.events || []" :key="event.id" 
                     class="flex items-start space-x-3 py-2 border-b border-gray-200 last:border-b-0">
                  <div class="flex-shrink-0">
                    <div :class="getEventIconClass(event.type)" 
                         class="w-2 h-2 rounded-full"></div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm text-gray-900">{{ event.message }}</p>
                    <p class="text-xs text-gray-500">{{ formatDate(event.timestamp) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'

export default {
  name: 'Servers',
  setup() {
    const toast = useToast()
    
    // Reactive data
    const loading = ref(false)
    const servers = ref([])
    const currentPage = ref(1)
    const itemsPerPage = ref(10)
    
    // Modal states
    const showServerDetails = ref(false)
    const selectedServer = ref(null)
    
    // Server statistics
    const serverStats = ref({
      total_servers: 0,
      online_servers: 0,
      offline_servers: 0,
      active_alerts: 0,
      total_sensors: 0,
      online_sensors: 0,
      offline_sensors: 0,
      cameras_connected: 0,
      sensors_active: 0,
      data_points: 0
    })
    
    // Computed properties
    const totalPages = computed(() => {
      return Math.ceil(servers.value.length / itemsPerPage.value)
    })
    
    const paginatedServers = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return servers.value.slice(start, end)
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
    const loadServers = async () => {
      loading.value = true
      try {
        // Mock data for now - replace with actual API call
        const mockServers = [
          {
            server_id: 'server-001',
            server_name: 'Edge-Server-01',
            status: 'online',
            location: 'Site-A',
            cpu_usage: 45,
            memory_usage: 2.1,
            cameras_count: 8,
            sensors_count: 12,
            alerts_count: 0,
            network_io: 15,
            disk_usage: 65,
            cameras: [
              { id: 1, name: 'Camera-01', status: 'online', resolution: '1920x1080', fps: 30, ip_address: '192.168.1.101', alerts: 0 },
              { id: 2, name: 'Camera-02', status: 'online', resolution: '1920x1080', fps: 30, ip_address: '192.168.1.102', alerts: 1 },
              { id: 3, name: 'Camera-03', status: 'offline', resolution: '--', fps: '--', ip_address: '192.168.1.103', alerts: 3 }
            ],
            sensors: [
              { id: 1, name: 'TEMP-001', type: 'Temperature', status: 'online', value: '23.5', unit: '°C', location: 'Server Room', last_update: new Date(), alerts: 0 },
              { id: 2, name: 'HUMID-002', type: 'Humidity', status: 'online', value: '65', unit: '%', location: 'Server Room', last_update: new Date(Date.now() - 300000), alerts: 0 },
              { id: 3, name: 'MOTION-003', type: 'Motion', status: 'online', value: 'Active', unit: '', location: 'Hallway', last_update: new Date(Date.now() - 600000), alerts: 1 },
              { id: 4, name: 'DOOR-001', type: 'Door', status: 'offline', value: 'Closed', unit: '', location: 'Main Entrance', last_update: new Date(Date.now() - 900000), alerts: 0 }
            ],
            events: [
              { id: 1, type: 'info', message: 'Server started successfully', timestamp: new Date() },
              { id: 2, type: 'warning', message: 'High CPU usage detected (89%)', timestamp: new Date(Date.now() - 300000) },
              { id: 3, type: 'error', message: 'Camera-03 connection lost', timestamp: new Date(Date.now() - 600000) }
            ]
          },
          {
            server_id: 'server-002',
            server_name: 'Edge-Server-02',
            status: 'online',
            location: 'Site-B',
            cpu_usage: 67,
            memory_usage: 3.2,
            cameras_count: 5,
            sensors_count: 8,
            alerts_count: 1,
            network_io: 22,
            disk_usage: 78,
            cameras: [],
            sensors: [],
            events: []
          },
          {
            server_id: 'server-003',
            server_name: 'Edge-Server-03',
            status: 'offline',
            location: 'Site-C',
            cpu_usage: null,
            memory_usage: null,
            cameras_count: 0,
            sensors_count: 0,
            alerts_count: 3,
            network_io: 0,
            disk_usage: 0,
            cameras: [],
            sensors: [],
            events: []
          }
        ]
        
        servers.value = mockServers
        updateServerStats()
      } catch (error) {
        console.error('Error loading servers:', error)
        toast.error('Failed to load servers')
      } finally {
        loading.value = false
      }
    }
    
    const updateServerStats = () => {
      serverStats.value = {
        total_servers: servers.value.length,
        online_servers: servers.value.filter(s => s.status === 'online').length,
        offline_servers: servers.value.filter(s => s.status === 'offline').length,
        active_alerts: servers.value.reduce((sum, s) => sum + (s.alerts_count || 0), 0),
        total_sensors: servers.value.reduce((sum, s) => sum + (s.sensors_count || 0), 0),
        online_sensors: 42, // Mock data
        offline_sensors: 5, // Mock data
        cameras_connected: servers.value.reduce((sum, s) => sum + (s.cameras_count || 0), 0),
        sensors_active: 38, // Mock data
        data_points: 1247 // Mock data
      }
    }
    
    const refreshServers = async () => {
      await loadServers()
      toast.success('Servers refreshed successfully')
    }
    
    const getStatusBadgeClass = (status) => {
      const classes = {
        'online': 'bg-green-100 text-green-800',
        'offline': 'bg-red-100 text-red-800',
        'warning': 'bg-yellow-100 text-yellow-800',
        'active': 'bg-green-100 text-green-800',
        'inactive': 'bg-gray-100 text-gray-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    }
    
    const getEventIconClass = (type) => {
      const classes = {
        'info': 'bg-blue-500',
        'warning': 'bg-yellow-500',
        'error': 'bg-red-500',
        'success': 'bg-green-500'
      }
      return classes[type] || 'bg-gray-500'
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
    
    const viewServer = (server) => {
      selectedServer.value = server
      showServerDetails.value = true
    }
    
    const closeServerDetails = () => {
      showServerDetails.value = false
      selectedServer.value = null
    }
    
    const addCamera = () => {
      toast.info('Add Camera functionality will be implemented')
    }
    
    const addSensor = () => {
      toast.info('Add Sensor functionality will be implemented')
    }
    
    // Lifecycle
    onMounted(() => {
      loadServers()
    })
    
    return {
      loading,
      servers,
      currentPage,
      itemsPerPage,
      showServerDetails,
      selectedServer,
      serverStats,
      totalPages,
      paginatedServers,
      visiblePages,
      loadServers,
      refreshServers,
      getStatusBadgeClass,
      getEventIconClass,
      formatDate,
      viewServer,
      closeServerDetails,
      addCamera,
      addSensor
    }
  }
}
</script>
