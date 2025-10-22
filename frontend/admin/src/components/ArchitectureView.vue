<template>
  <div class="architecture-view">
    <!-- Architecture Header -->
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-2">System Architecture</h3>
      <p class="text-sm text-gray-600">Complete visual overview of the IoT platform architecture</p>
    </div>

    <!-- Architecture Controls -->
    <div class="mb-6 flex flex-wrap gap-4">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">View:</label>
        <select v-model="selectedView" class="rounded-md border-gray-300 text-sm">
          <option value="overview">Service Overview</option>
          <option value="detailed">Detailed Breakdown</option>
          <option value="database">Database Schema</option>
          <option value="frontend">Frontend Structure</option>
          <option value="files">File Structure</option>
        </select>
      </div>
      
      <!-- Zoom Controls -->
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">Zoom:</label>
        <button @click="zoomOut" class="btn-secondary text-sm" title="Zoom Out">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7" />
          </svg>
          -
        </button>
        
        <input 
          type="range" 
          v-model="zoomLevel" 
          @input="updateZoom"
          min="50" 
          max="200" 
          step="10"
          class="w-20 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          title="Zoom Slider"
        />
        
        <button @click="zoomIn" class="btn-secondary text-sm" title="Zoom In">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
          </svg>
          +
        </button>
        
        <span class="text-sm text-gray-600 min-w-[3rem]">{{ zoomLevel }}%</span>
        
        <button @click="resetZoom" class="btn-secondary text-sm" title="Reset Zoom">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Reset
        </button>
      </div>
      
      <div class="flex items-center space-x-4">
        <button @click="refreshData" class="btn-primary text-sm">
          <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh
        </button>
        
        <button @click="exportDiagram" class="btn-secondary text-sm">
          <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Export
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
      <span class="ml-3 text-gray-600">Loading architecture data...</span>
    </div>

    <!-- Architecture Diagram with Zoom Container -->
    <div v-else class="architecture-diagram-container">
      <div 
        ref="diagramContainer" 
        class="diagram-zoom-container"
        :style="{ transform: `scale(${zoomLevel / 100})`, transformOrigin: 'top left' }"
      >
        <div ref="mermaidContainer" class="mermaid-container"></div>
      </div>
    </div>

    <!-- Architecture Details Panel -->
    <div v-if="selectedService" class="mt-6 bg-gray-50 p-4 rounded-lg">
      <h4 class="text-lg font-semibold text-gray-900 mb-2">{{ selectedService.name }}</h4>
      <p class="text-sm text-gray-600 mb-4">{{ selectedService.description }}</p>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-if="selectedService.endpoints">
          <h5 class="font-medium text-gray-900 mb-2">API Endpoints</h5>
          <ul class="text-sm text-gray-600 space-y-1">
            <li v-for="endpoint in selectedService.endpoints" :key="endpoint.path">
              <code class="bg-gray-200 px-2 py-1 rounded">{{ endpoint.method }} {{ endpoint.path }}</code>
              <span class="ml-2">{{ endpoint.description }}</span>
            </li>
          </ul>
        </div>
        
        <div v-if="selectedService.components">
          <h5 class="font-medium text-gray-900 mb-2">Components</h5>
          <ul class="text-sm text-gray-600 space-y-1">
            <li v-for="component in selectedService.components" :key="component">
              {{ component }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, nextTick } from 'vue'
import mermaid from 'mermaid'

export default {
  name: 'ArchitectureView',
  setup() {
    const selectedView = ref('overview')
    const loading = ref(false)
    const selectedService = ref(null)
    const mermaidContainer = ref(null)
    const diagramContainer = ref(null)
    const zoomLevel = ref(100)

    const getMermaidDiagram = (view) => {
      const diagrams = {
        overview: `graph LR
    subgraph Frontend["Frontend Layer"]
        AF["Admin Frontend<br/>Vue.js + Vite<br/>Port 3000"]
        CF["Client Frontend<br/>Vue.js + PWA<br/>Port 3001"]
    end
    
    subgraph Gateway["API Gateway"]
        GW["API Gateway<br/>FastAPI + Middleware<br/>Port 8000"]
        AUTH["Authentication<br/>JWT + RBAC"]
        RL["Rate Limiting<br/>Redis-based"]
    end
    
    subgraph Backend["Backend Services"]
        AB["Admin Backend<br/>FastAPI + Optimizations<br/>Port 8080"]
        CB["Client Backend<br/>Telemetry Service<br/>Port 8002<br/>/api/client/*<br/>Authentication Service<br/>/api/device/*"]
        DD["Device Discovery<br/>Device Registration<br/>Port 8080 (Admin Backend)"]
        CM["Client Management<br/>Client Operations<br/>Port 8005"]
    end
    
    subgraph Security["Security & Optimization"]
        TI["Tenant Isolation"]
        RBAC["RBAC Manager"]
        AL["Audit Logger"]
        CM2["Cache Manager"]
        OQ["Optimized Queries"]
    end
    
    subgraph Data["Data Layer"]
        PG["PostgreSQL<br/>Primary Database<br/>Port 5435"]
        RD["Redis<br/>Caching Layer<br/>Port 6381"]
        MQ["MQTT Broker<br/>Real-time Messaging<br/>Port 1885"]
    end
    
    AF --> GW
    CF --> GW
    GW --> AUTH
    GW --> RL
    AUTH --> CB
    GW --> AB
    GW --> DD
    GW --> CM
    
    AB --> TI
    AB --> RBAC
    AB --> AL
    AB --> CM2
    AB --> OQ
    AB --> PG
    CB --> PG
    DD --> PG
    DD --> MQ
    CM --> PG
    CM --> RD
    
    
    
    classDef frontend fill:#e0f7fa,stroke:#00bcd4,stroke-width:2px
    classDef gateway fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef backend fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    classDef security fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    classDef data fill:#fce4ec,stroke:#e91e63,stroke-width:2px
    
    class AF,CF frontend
    class GW,AUTH,RL gateway
    class AB,CB,DD,CM backend
    class TI,RBAC,AL,CM2,OQ security
    class PG,RD,MQ data`,

        detailed: `graph TD
    subgraph AdminBackend["Admin Backend Service"]
        AB1["FastAPI Application"]
        AB2["Authentication Middleware"]
        AB3["Request Validation"]
        AB4["Response Formatting"]
        AB5["Error Handling"]
        AB6["Logging System"]
        AB7["Performance Monitoring"]
    end
    
    subgraph ClientBackend["Client Backend Service"]
        CB1["FastAPI Application"]
        CB2["JWT Authentication"]
        CB3["Client Validation"]
        CB4["Session Management"]
        CB5["Password Hashing"]
        CB6["Token Generation"]
    end
    
    subgraph DeviceDiscovery["Device Discovery Service"]
        DD1["Device Registration"]
        DD2["Device Validation"]
        DD3["Status Monitoring"]
        DD4["MQTT Integration"]
        DD5["Real-time Updates"]
        DD6["Device Management"]
    end
    
    AB1 --> AB2
    AB2 --> AB3
    AB3 --> AB4
    AB4 --> AB5
    AB5 --> AB6
    AB6 --> AB7
    
    CB1 --> CB2
    CB2 --> CB3
    CB3 --> CB4
    CB4 --> CB5
    CB5 --> CB6
    
    DD1 --> DD2
    DD2 --> DD3
    DD3 --> DD4
    DD4 --> DD5
    DD5 --> DD6
    
    classDef service fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    classDef component fill:#f1f8e9,stroke:#8bc34a,stroke-width:2px
    
    class AdminBackend,ClientBackend,DeviceDiscovery service
    class AB1,AB2,AB3,AB4,AB5,AB6,AB7,CB1,CB2,CB3,CB4,CB5,CB6,DD1,DD2,DD3,DD4,DD5,DD6 component`,

        database: `erDiagram
    CLIENTS {
        uuid client_id PK
        string company_name
        string contact_email
        string contact_phone
        timestamp created_at
        timestamp updated_at
        string status
    }
    
    DEVICES {
        uuid device_id PK
        uuid client_id FK
        string device_name
        string device_type
        json capabilities
        string status
        timestamp created_at
        timestamp updated_at
    }
    
    DEVICE_CREDENTIALS {
        uuid credential_id PK
        uuid device_id FK
        string credential_value
        string credential_type
        timestamp created_at
        timestamp expires_at
    }
    
    SUBSCRIPTION_PACKAGES {
        uuid package_id PK
        string package_name
        json features
        decimal price
        string currency
        integer duration_days
    }
    
    DISCOVERED_DEVICES {
        uuid discovery_id PK
        string device_id
        string device_name
        string device_type
        json capabilities
        string status
        timestamp discovered_at
        timestamp last_seen
    }
    
    CLIENTS ||--o{ DEVICES : "owns"
    DEVICES ||--o{ DEVICE_CREDENTIALS : "has"`,

        frontend: `graph TD
    subgraph ClientFrontend["Client Frontend Structure"]
        CF1["Client Views"]
        CF2["Client Components"]
        CF3["Client Services"]
        CF4["PWA Features"]
        
        CF1 --> CF11["Dashboard.vue"]
        CF1 --> CF12["Devices.vue"]
        CF1 --> CF13["MobileDashboard.vue"]
        
        CF2 --> CF21["DeviceCard.vue"]
        CF2 --> CF22["MobileDeviceCard.vue"]
        CF2 --> CF23["Capability Components"]
        
        CF3 --> CF31["ClientAPI.js"]
        CF3 --> CF32["MobileCacheManager.js"]
        CF3 --> CF33["mqtt"]
        
        CF4 --> CF41["manifest.json"]
        CF4 --> CF42["Offline Support"]
        CF4 --> CF43["Background Sync"]
    end
    
    subgraph AdminFrontend["Admin Frontend Structure"]
        AF1["Admin Views"]
        AF2["Admin Components"]
        AF3["Admin Services"]
        
        AF1 --> AF11["Dashboard.vue"]
        AF1 --> AF12["Devices.vue"]
        AF1 --> AF13["Clients.vue"]
        AF1 --> AF14["Analytics.vue"]
        AF1 --> AF15["Settings.vue"]
        
        AF2 --> AF21["DeviceCard.vue"]
        AF2 --> AF22["ClientCard.vue"]
        AF2 --> AF23["Charts.vue"]
        
        AF3 --> AF31["DeviceAPI.js"]
        AF3 --> AF32["ClientAPI.js"]
        AF3 --> AF33["AuthAPI.js"]
    end
    
    classDef frontend fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    classDef component fill:#f1f8e9,stroke:#8bc34a,stroke-width:2px
    classDef service fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    
    class ClientFrontend,AdminFrontend frontend
    class CF1,CF2,AF1,AF2 component
    class CF3,CF4,AF3 service`,

        files: `graph TD
    subgraph Config["Configuration"]
        C1["docker-compose.yml"]
        C2["init-scripts/"]
        C3["migrations/"]
        C4["Dockerfile.*"]
    end
    
    subgraph Shared["Shared Components"]
        S1["src/shared/"]
        S2["security/"]
        S3["cache/"]
        S4["database/"]
        S5["circuit_breaker/"]
        S6["audit/"]
    end
    
    subgraph Frontend["Frontend Applications"]
        F1["frontend/admin/"]
        F2["frontend/client/"]
        F3["src/"]
        F4["public/"]
        F5["package.json"]
    end
    
    subgraph Backend["Backend Services"]
        B1["services/"]
        B2["admin_backend.py"]
        B3["client_backend.py"]
        B4["client_management_backend.py"]
        B5["device_discovery_main.py"]
        B6["mobile_api_backend.py"]
        B7["gateway_backend.py"]
    end
    
    subgraph Root["Project Root"]
        R1["README.md"]
        R2["requirements.txt"]
        R3[".gitignore"]
    end
    
    S1 --> S2
    S1 --> S3
    S1 --> S4
    S1 --> S5
    S1 --> S6
    
    F1 --> F3
    F1 --> F4
    F1 --> F5
    F2 --> F3
    F2 --> F4
    F2 --> F5
    
    B1 --> B2
    B1 --> B3
    B1 --> B4
    B1 --> B5
    B1 --> B6
    B1 --> B7
    
    classDef config fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef shared fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    classDef frontend fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    classDef backend fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    classDef root fill:#fce4ec,stroke:#e91e63,stroke-width:2px
    
    class Config config
    class Shared shared
    class Frontend frontend
    class Backend backend
    class Root root`
      }
      return diagrams[view] || diagrams.overview
    }

    const renderMermaidDiagram = async () => {
      // Check if container exists
      if (!mermaidContainer.value) {
        console.warn('Mermaid container not available yet')
        return
      }
      
      loading.value = true
      try {
        // Clear previous content
        mermaidContainer.value.innerHTML = ''
        
        // Check if Mermaid is available
        if (!mermaid) {
          throw new Error('Mermaid library not loaded')
        }
        
        // Get current diagram
        const mermaidCode = getMermaidDiagram(selectedView.value)
        
        // Render with Mermaid
        const { svg } = await mermaid.render(`diagram-${selectedView.value}`, mermaidCode)
        mermaidContainer.value.innerHTML = svg
      } catch (error) {
        console.error('Error rendering Mermaid diagram:', error)
        mermaidContainer.value.innerHTML = '<p class="text-red-500 text-center py-8">Error rendering diagram: ' + error.message + '</p>'
      } finally {
        loading.value = false
      }
    }

    const zoomIn = () => {
      if (zoomLevel.value < 200) {
        zoomLevel.value += 10
      }
    }

    const zoomOut = () => {
      if (zoomLevel.value > 50) {
        zoomLevel.value -= 10
      }
    }

    const resetZoom = () => {
      zoomLevel.value = 100
    }

    const updateZoom = () => {
      // Zoom is handled by CSS transform
    }

    const refreshData = async () => {
      await renderMermaidDiagram()
    }

    const exportDiagram = () => {
      if (mermaidContainer.value) {
        const svg = mermaidContainer.value.querySelector('svg')
        if (svg) {
          const svgData = new XMLSerializer().serializeToString(svg)
          const canvas = document.createElement('canvas')
          const ctx = canvas.getContext('2d')
          const img = new Image()
          
          img.onload = () => {
            canvas.width = img.width
            canvas.height = img.height
            ctx.drawImage(img, 0, 0)
            
            const link = document.createElement('a')
            link.download = `architecture-${selectedView.value}.png`
            link.href = canvas.toDataURL()
            link.click()
          }
          
          img.src = 'data:image/svg+xml;base64,' + btoa(svgData)
        }
      }
    }

    // Watch for view changes
    watch(selectedView, () => {
      renderMermaidDiagram()
    })

    onMounted(async () => {
      // Initialize Mermaid
      if (mermaid) {
        mermaid.initialize({
          startOnLoad: false,
          theme: 'default',
          securityLevel: 'loose',
          fontFamily: 'Arial, sans-serif'
        })
        
        // Wait for DOM to be ready
        await nextTick()
        
        // Add a small delay to ensure refs are available
        setTimeout(() => {
          renderMermaidDiagram()
        }, 200)
      } else {
        console.error('Mermaid library not available')
      }
    })

    return {
      selectedView,
      loading,
      selectedService,
      mermaidContainer,
      diagramContainer,
      zoomLevel,
      zoomIn,
      zoomOut,
      resetZoom,
      updateZoom,
      refreshData,
      exportDiagram
    }
  }
}
</script>

<style scoped>
.architecture-view {
  @apply p-4;
}

.architecture-diagram-container {
  @apply bg-white border border-gray-200 rounded-lg overflow-auto;
  max-height: 80vh;
  min-height: 400px;
}

.diagram-zoom-container {
  @apply transition-transform duration-200 ease-in-out;
  min-width: fit-content;
}

.mermaid-container {
  @apply p-4;
}

.mermaid-container svg {
  @apply max-w-none;
}

.btn-primary {
  @apply bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition-colors;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-gray-300 transition-colors;
}

/* Custom slider styling */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  cursor: pointer;
}

input[type="range"]::-webkit-slider-track {
  background: #e5e7eb;
  height: 8px;
  border-radius: 4px;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  background: #3b82f6;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  cursor: pointer;
}

input[type="range"]::-moz-range-track {
  background: #e5e7eb;
  height: 8px;
  border-radius: 4px;
  border: none;
}

input[type="range"]::-moz-range-thumb {
  background: #3b82f6;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}
</style>
