<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" @click="closeModal"></div>
    
    <!-- Modal Container -->
    <div class="flex min-h-full items-center justify-center p-4">
      <div class="relative w-full max-w-4xl transform overflow-hidden rounded-xl bg-white shadow-xl transition-all">
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-gray-200 px-6 py-4">
          <h3 class="text-xl font-semibold text-gray-900">Add New Camera</h3>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form Content -->
        <form @submit.prevent="handleSubmit" class="px-6 py-6">
          <div class="grid grid-cols-1 gap-8 lg:grid-cols-2">
            <!-- A. Basic Info -->
            <div class="space-y-6">
              <div>
                <h4 class="text-lg font-medium text-gray-900 mb-4">Basic Information</h4>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Camera Name</label>
                    <input
                      v-model="form.cameraName"
                      type="text"
                      required
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="Enter camera name"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Location / Zone</label>
                    <input
                      v-model="form.location"
                      type="text"
                      required
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="e.g., Server Room, Hallway"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Edge Server</label>
                    <input
                      :value="edgeServerName"
                      type="text"
                      readonly
                      class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-gray-500"
                    />
                  </div>
                </div>
              </div>

              <!-- B. Connection Settings -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 mb-4">Connection Settings</h4>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Protocol</label>
                    <select
                      v-model="form.protocol"
                      required
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    >
                      <option value="">Select Protocol</option>
                      <option value="ONVIF">ONVIF</option>
                      <option value="RTSP">RTSP</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Stream URL</label>
                    <input
                      v-model="form.streamUrl"
                      type="url"
                      required
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="rtsp://192.168.1.100:554/stream"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">IP Address</label>
                    <input
                      v-model="form.ipAddress"
                      type="text"
                      required
                      pattern="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="192.168.1.100"
                    />
                  </div>
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
                      <input
                        v-model="form.username"
                        type="text"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        placeholder="admin"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                      <div class="relative">
                        <input
                          v-model="form.password"
                          :type="showPassword ? 'text' : 'password'"
                          class="w-full rounded-lg border border-gray-300 px-3 py-2 pr-10 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                          placeholder="••••••••"
                        />
                        <button
                          type="button"
                          @click="showPassword = !showPassword"
                          class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                          <svg v-if="!showPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                          <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Port</label>
                    <input
                      v-model="form.port"
                      type="number"
                      min="1"
                      max="65535"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="554"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <!-- C. Video Capabilities -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 mb-4">Video Capabilities</h4>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Resolution</label>
                    <select
                      v-model="form.resolution"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    >
                      <option value="">Auto-detect</option>
                      <option value="1920x1080">1920x1080 (Full HD)</option>
                      <option value="1280x720">1280x720 (HD)</option>
                      <option value="640x480">640x480 (VGA)</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">FPS</label>
                    <input
                      v-model="form.fps"
                      type="number"
                      min="5"
                      max="60"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="30"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Codec</label>
                    <select
                      v-model="form.codec"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    >
                      <option value="H.264">H.264</option>
                      <option value="H.265">H.265</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- D. AI Vision Analytics -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 mb-4">AI Vision Analytics</h4>
                <div class="space-y-4">
                  <div class="flex items-center">
                    <input
                      v-model="form.enableAI"
                      type="checkbox"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label class="ml-2 text-sm font-medium text-gray-700">Enable AI Analytics</label>
                  </div>
                  
                  <div v-if="form.enableAI" class="space-y-4 pl-6 border-l-2 border-blue-100">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">AI Modules</label>
                      <div class="space-y-2">
                        <label v-for="module in aiModules" :key="module" class="flex items-center">
                          <input
                            v-model="form.aiModules"
                            :value="module"
                            type="checkbox"
                            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                          />
                          <span class="ml-2 text-sm text-gray-700">{{ module }}</span>
                        </label>
                      </div>
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">Processing Mode</label>
                      <select
                        v-model="form.processingMode"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      >
                        <option value="Real-Time">Real-Time</option>
                        <option value="Snapshot">Snapshot</option>
                      </select>
                    </div>
                    <div class="flex items-center">
                      <input
                        v-model="form.saveEventClips"
                        type="checkbox"
                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label class="ml-2 text-sm font-medium text-gray-700">Save Event Clips</label>
                    </div>
                  </div>
                </div>
              </div>

              <!-- E. Storage Policy -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 mb-4">Storage Policy</h4>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Retention Days</label>
                    <input
                      v-model="form.retentionDays"
                      type="number"
                      min="1"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="7"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Max Storage Size (GB)</label>
                    <input
                      v-model="form.maxStorageSize"
                      type="number"
                      min="1"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="50"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Recording Mode</label>
                    <select
                      v-model="form.recordingMode"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    >
                      <option value="Continuous">Continuous</option>
                      <option value="On Event">On Event</option>
                      <option value="Schedule">Schedule</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="mt-8 flex flex-col gap-4 sm:flex-row sm:justify-between">
            <button
              type="button"
              @click="testConnection"
              :disabled="isTestingConnection"
              class="inline-flex items-center justify-center rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <svg v-if="isTestingConnection" class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isTestingConnection ? 'Testing...' : 'Test Connection' }}
            </button>
            
            <div class="flex gap-3">
              <button
                type="button"
                @click="closeModal"
                class="inline-flex items-center justify-center rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="isSubmitting"
                class="inline-flex items-center justify-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              >
                <svg v-if="isSubmitting" class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ isSubmitting ? 'Registering...' : 'Register Camera' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  edgeServerName: {
    type: String,
    default: 'Edge-Server-01'
  }
})

// Emits
const emit = defineEmits(['close', 'cameraRegistered'])

// Form state
const form = reactive({
  cameraName: '',
  location: '',
  protocol: '',
  streamUrl: '',
  ipAddress: '',
  username: '',
  password: '',
  port: '554',
  resolution: '',
  fps: 30,
  codec: 'H.264',
  enableAI: false,
  aiModules: [],
  processingMode: 'Real-Time',
  saveEventClips: false,
  retentionDays: 7,
  maxStorageSize: 50,
  recordingMode: 'Continuous'
})

// UI state
const showPassword = ref(false)
const isTestingConnection = ref(false)
const isSubmitting = ref(false)

// AI modules options
const aiModules = [
  'Person Detection',
  'Face Detection',
  'Fire/Smoke',
  'Intrusion Zone',
  'Motion Detection'
]

// Methods
const closeModal = () => {
  emit('close')
}

const testConnection = async () => {
  isTestingConnection.value = true
  
  try {
    // Simulate connection test
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Mock success/error based on form validation
    if (form.ipAddress && form.port) {
      alert('✅ Connection test successful!')
    } else {
      alert('❌ Please fill in IP Address and Port')
    }
  } catch (error) {
    alert('❌ Connection test failed: ' + error.message)
  } finally {
    isTestingConnection.value = false
  }
}

const handleSubmit = async () => {
  isSubmitting.value = true
  
  try {
    const cameraData = {
      ...form,
      edgeServer: props.edgeServerName,
      status: 'offline',
      alerts: 0
    }
    
    // API call to register camera
    const response = await axios.post('/api/cameras', cameraData)
    
    if (response.status === 200 || response.status === 201) {
      alert('✅ Camera registered successfully!')
      emit('cameraRegistered', response.data)
      closeModal()
      resetForm()
    }
  } catch (error) {
    console.error('Error registering camera:', error)
    alert('❌ Failed to register camera: ' + (error.response?.data?.message || error.message))
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  Object.assign(form, {
    cameraName: '',
    location: '',
    protocol: '',
    streamUrl: '',
    ipAddress: '',
    username: '',
    password: '',
    port: '554',
    resolution: '',
    fps: 30,
    codec: 'H.264',
    enableAI: false,
    aiModules: [],
    processingMode: 'Real-Time',
    saveEventClips: false,
    retentionDays: 7,
    maxStorageSize: 50,
    recordingMode: 'Continuous'
  })
}

// Watch for modal close to reset form
watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    resetForm()
  }
})
</script>
