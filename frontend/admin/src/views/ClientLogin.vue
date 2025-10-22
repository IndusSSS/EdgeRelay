<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="mx-auto h-12 w-12 bg-primary-600 rounded-lg flex items-center justify-center">
          <CpuChipIcon class="h-8 w-8 text-white" />
        </div>
        <h2 class="mt-6 text-3xl font-bold text-gray-900">IoT Platform</h2>
        <p class="mt-2 text-sm text-gray-600">Client Portal Access</p>
      </div>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow-sm border border-gray-200 sm:rounded-lg sm:px-10">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <!-- Client Username Field -->
          <div>
            <label for="client-username" class="block text-sm font-medium text-gray-700">
              Client Username
            </label>
            <div class="mt-1 relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <UserIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="client-username"
                name="client_username"
                type="text"
                autocomplete="username"
                required
                v-model="form.client_username"
                class="appearance-none block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Enter your client username"
              />
            </div>
          </div>

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1 relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <LockClosedIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="password"
                name="password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                required
                v-model="form.password"
                class="appearance-none block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Enter your password"
              />
              <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="text-gray-400 hover:text-gray-600 focus:outline-none"
                >
                  <EyeIcon v-if="!showPassword" class="h-5 w-5" />
                  <EyeSlashIcon v-else class="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>

          <!-- Remember Me -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                v-model="form.rememberMe"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <ExclamationTriangleIcon class="h-5 w-5 text-red-400" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  {{ errorMessage }}
                </h3>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <div>
            <button
              type="submit"
              :disabled="isLoading"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
                <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              </span>
              <span v-else class="absolute left-0 inset-y-0 flex items-center pl-3">
                <ArrowRightOnRectangleIcon class="h-4 w-4 text-primary-500 group-hover:text-primary-400" />
              </span>
              {{ isLoading ? 'Signing in...' : 'Sign in' }}
            </button>
          </div>
        </form>

      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import {
  CpuChipIcon,
  UserIcon,
  LockClosedIcon,
  EyeIcon,
  EyeSlashIcon,
  ArrowRightOnRectangleIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'Login',
  components: {
    CpuChipIcon,
    UserIcon,
    LockClosedIcon,
    EyeIcon,
    EyeSlashIcon,
    ArrowRightOnRectangleIcon,
    ExclamationTriangleIcon
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const apiService = inject('$api')
    
    const isLoading = ref(false)
    const showPassword = ref(false)
    const errorMessage = ref('')

    const form = reactive({
      client_username: '',
      password: '',
      rememberMe: false
    })

    const handleLogin = async () => {
      isLoading.value = true
      errorMessage.value = ""

      try {
        // Use client authentication instead of admin
        const response = await apiService.clientLogin(form.client_username, form.password)
        
        if (response.access_token) {
          // Store token and client data
          apiService.setToken(response.access_token)
          apiService.setUser(response.client)
          
          // Update auth store with client role
          authStore.login({...response.client, role: 'client'}, response.access_token)
          
          // Redirect to client dashboard
          router.push("/client-dashboard")
        } else {
          errorMessage.value = "Invalid credentials"
        }
      } catch (error) {
        console.error("Client login error:", error)
        errorMessage.value = error.message || "Login failed. Please try again."
      } finally {
        isLoading.value = false
      }
    }

    return {
      form,
      isLoading,
      showPassword,
      errorMessage,
      handleLogin
    }
  }
}
</script>
