<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Navigation for Admin Portal -->
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
    
    const showNavigation = computed(() => {
      // Show navigation on all pages except login
      return route.name !== 'Login'
    })
    
    return {
      showNavigation
    }
  }
}
</script>
