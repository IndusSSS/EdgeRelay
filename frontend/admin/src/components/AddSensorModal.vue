<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" @click="closeModal"></div>
    
    <!-- Modal Container -->
    <div class="flex min-h-full items-center justify-center p-4">
      <div class="relative w-full max-w-3xl transform overflow-hidden rounded-xl bg-white shadow-xl transition-all">
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-gray-200 px-6 py-4">
          <h3 class="text-xl font-semibold text-gray-900">Add New Sensor</h3>
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
                    <label class="block text-sm font-medium text-gray-700 mb-1">Sensor Name</label>
                    <input
                      v-model="form.sensorName"
                      type="text"
                      required
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                      placeholder="Enter sensor name"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Sensor Type</label>
                    <select
                      v-model="form.sensorType"
                      required
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                    >
                      <option value="">Select Sensor Type</option>
                      <option value="Temperature">Temperature</option>
                      <option value="Humidity">Humidity</option>
                      <option value="Motion">Motion</option>
                      <option value="Light">Light</option>
                      <option value="Custom">Custom</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Location</label>
                    <input
                      v-model="form.location"
                      type="text"
                      required
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
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
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                    >
                      <option value="">Select Protocol</option>
                      <option value="MQTT">MQTT</option>
                      <option value="Modbus TCP">Modbus TCP</option>
                      <option value="GPIO">GPIO</option>
                      <option value="HTTP">HTTP</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      {{ getSourceLabel() }}
                    </label>
                    <input
                      v-model="form.source"
                      type="text"
                      required
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                      :placeholder="getSourcePlaceholder()"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Reporting Interval (seconds)</label>
                    <input
                      v-model="form.reportingInterval"
                      type="number"
                      min="1"
                      required
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                      placeholder="30"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <!-- C. Thresholds & Alerts -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 mb-4">Thresholds & Alerts</h4>
                <div class="space-y-4">
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">Upper Limit</label>
                      <input
                        v-model="form.upperLimit"
                        type="number"
                        step="0.1"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                        placeholder="30.0"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">Lower Limit</label>
                      <input
                        v-model="form.lowerLimit"
                        type="number"
                        step="0.1"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                        placeholder="10.0"
                      />
                    </div>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Alert Actions</label>
                    <div class="space-y-2">
                      <label v-for="action in alertActions" :key="action" class="flex items-center">
                        <input
                          v-model="form.alertActions"
                          :value="action"
                          type="checkbox"
                          class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                        />
                        <span class="ml-2 text-sm text-gray-700">{{ action }}</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Sensor Type Specific Settings -->
              <div v-if="form.sensorType === 'Custom'">
                <h4 class="text-lg font-medium text-gray-900 mb-4">Custom Settings</h4>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Unit of Measurement</label>
                    <input
                      v-model="form.unit"
                      type="text"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                      placeholder="e.g., °C, %, lux, dB"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Data Format</label>
                    <select
                      v-model="form.dataFormat"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                    >
                      <option value="numeric">Numeric</option>
                      <option value="boolean">Boolean (True/False)</option>
                      <option value="string">String</option>
                      <option value="json">JSON</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Advanced Settings -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 mb-4">Advanced Settings</h4>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Calibration Offset</label>
                    <input
                      v-model="form.calibrationOffset"
                      type="number"
                      step="0.1"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                      placeholder="0.0"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Sampling Rate (Hz)</label>
                    <input
                      v-model="form.samplingRate"
                      type="number"
                      min="0.1"
                      max="1000"
                      step="0.1"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                      placeholder="1.0"
                    />
                  </div>
                  <div class="flex items-center">
                    <input
                      v-model="form.enableLogging"
                      type="checkbox"
                      class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                    />
                    <label class="ml-2 text-sm font-medium text-gray-700">Enable Data Logging</label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="mt-8 flex flex-col gap-4 sm:flex-row sm:justify-between">
            <button
              type="button"
              @click="testSensor"
              :disabled="isTestingSensor"
              class="inline-flex items-center justify-center rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
            >
              <svg v-if="isTestingSensor" class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isTestingSensor ? 'Testing...' : 'Test Sensor' }}
            </button>
            
            <div class="flex gap-3">
              <button
                type="button"
                @click="closeModal"
                class="inline-flex items-center justify-center rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="isSubmitting"
                class="inline-flex items-center justify-center rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
              >
                <svg v-if="isSubmitting" class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ isSubmitting ? 'Registering...' : 'Register Sensor' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
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
const emit = defineEmits(['close', 'sensorRegistered'])

// Form state
const form = reactive({
  sensorName: '',
  sensorType: '',
  location: '',
  protocol: '',
  source: '',
  reportingInterval: 30,
  upperLimit: '',
  lowerLimit: '',
  alertActions: [],
  unit: '',
  dataFormat: 'numeric',
  calibrationOffset: 0,
  samplingRate: 1.0,
  enableLogging: true
})

// UI state
const isTestingSensor = ref(false)
const isSubmitting = ref(false)

// Alert actions options
const alertActions = [
  'Notify Cloud',
  'Send Telegram',
  'Trigger Buzzer'
]

// Computed properties
const getSourceLabel = () => {
  switch (form.protocol) {
    case 'MQTT': return 'Topic'
    case 'Modbus TCP': return 'Address'
    case 'GPIO': return 'Pin Number'
    case 'HTTP': return 'Endpoint URL'
    default: return 'Source'
  }
}

const getSourcePlaceholder = () => {
  switch (form.protocol) {
    case 'MQTT': return 'sensors/temperature/room1'
    case 'Modbus TCP': return '192.168.1.100:502'
    case 'GPIO': return '18'
    case 'HTTP': return 'http://192.168.1.100/api/sensor'
    default: return 'Enter source'
  }
}

// Methods
const closeModal = () => {
  emit('close')
}

const testSensor = async () => {
  isTestingSensor.value = true
  
  try {
    // Simulate sensor test
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Mock success/error based on form validation
    if (form.source && form.protocol) {
      alert('✅ Sensor test successful!')
    } else {
      alert('❌ Please fill in Protocol and Source')
    }
  } catch (error) {
    alert('❌ Sensor test failed: ' + error.message)
  } finally {
    isTestingSensor.value = false
  }
}

const handleSubmit = async () => {
  isSubmitting.value = true
  
  try {
    const sensorData = {
      ...form,
      edgeServer: props.edgeServerName,
      status: 'offline',
      alerts: 0,
      lastUpdate: new Date().toISOString()
    }
    
    // API call to register sensor
    const response = await axios.post('/api/sensors', sensorData)
    
    if (response.status === 200 || response.status === 201) {
      alert('✅ Sensor registered successfully!')
      emit('sensorRegistered', response.data)
      closeModal()
      resetForm()
    }
  } catch (error) {
    console.error('Error registering sensor:', error)
    alert('❌ Failed to register sensor: ' + (error.response?.data?.message || error.message))
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  Object.assign(form, {
    sensorName: '',
    sensorType: '',
    location: '',
    protocol: '',
    source: '',
    reportingInterval: 30,
    upperLimit: '',
    lowerLimit: '',
    alertActions: [],
    unit: '',
    dataFormat: 'numeric',
    calibrationOffset: 0,
    samplingRate: 1.0,
    enableLogging: true
  })
}

// Watch for modal close to reset form
watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    resetForm()
  }
})
</script>
