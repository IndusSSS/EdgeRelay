<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Shared Navigation - appears on all pages -->
    <AppNavigation v-if="showNavigation" />
    
    <!-- Page Content -->
    <router-view />
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppNavigation from './components/AppNavigation.vue'

export default {
  name: 'App',
  components: {
    AppNavigation
  },
  setup() {
    const route = useRoute()
    
    // Show navigation on all pages except login
    const showNavigation = computed(() => {
      return route.name !== 'Login'
    })

    return {
      showNavigation
    }
  }
}
</script>
