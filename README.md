# EdgeRelay - Edge AI NVR Communication Platform

## 🚀 Project Overview

EdgeRelay is a comprehensive Edge AI NVR (Network Video Recorder) and Cloud management system designed for IoT surveillance ecosystems. It integrates ONVIF IP cameras, Edge Mini-PCs, Cloud backend, and mobile/web clients to create a unified surveillance platform.

### 🎯 Core Vision
Create a unified IoT surveillance ecosystem where:
- **Edge devices** handle local AI processing, video storage, and real-time analytics
- **VPS Cloud** acts as a lightweight communication hub for notifications, alerts, and live video relay
- **Mobile apps** provide real-time monitoring and control capabilities

## 🏗️ Architecture

### System Architecture Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │    │   Admin Panel   │    │  Edge Mini-PC   │
│   (Client)      │    │   (Admin)       │    │   (Local AI)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   VPS Cloud     │
                    │  (EdgeRelay)    │
                    │                 │
                    │  ┌───────────┐  │
                    │  │   API     │  │
                    │  │  Gateway  │  │
                    │  └───────────┘  │
                    │  ┌───────────┐  │
                    │  │ Database  │  │
                    │  └───────────┘  │
                    │  ┌───────────┐  │
                    │  │   Redis   │  │
                    │  └───────────┘  │
                    │  ┌───────────┐  │
                    │  │   MQTT    │  │
                    │  └───────────┘  │
                    └─────────────────┘
```

### Layer Breakdown

#### 📱 **CLIENT LAYER**
- **Mobile App**: Real-time monitoring, alert management, PTZ control
- **Admin Panel**: System configuration, user management, device monitoring

#### 💻 **EDGE LAYER** (Mini-PC)
- **Local AI Processing**: Person detection, face detection, fire detection
- **Video Storage**: Local recording and cloud synchronization
- **Camera Management**: ONVIF discovery, RTSP streaming, PTZ control
- **Real-time Analytics**: Motion detection, object recognition

#### ☁️ **CLOUD LAYER** (VPS - EdgeRelay)
- **Communication Hub**: Lightweight relay for notifications and alerts
- **User Management**: Admin and client authentication
- **Device Registry**: Local server and camera management
- **Session Management**: Secure token-based authentication

## 📁 File Structure

```
EdgeRelay/
├── 📁 backups/                    # System backups
├── 📁 config/                     # Configuration files
│   ├── 📁 mosquitto/             # MQTT broker configuration
│   │   ├── mosquitto.conf        # MQTT broker settings
│   │   ├── 📁 data/              # MQTT data persistence
│   │   └── 📁 log/               # MQTT logs
│   └── 📁 postgres/              # Database configuration
│       └── 📁 init/              # Database initialization scripts
│           └── 01-init-simple.sql # Database schema setup
├── 📁 data/                      # Application data storage
├── 📁 docker/                    # Docker configuration
│   └── Dockerfile.core-api       # Core API service Dockerfile
├── 📁 logs/                      # Application logs
├── 📁 services/                  # Core API service source code
│   ├── 📁 src/                   # Source code
│   │   ├── 📁 api/               # API route handlers
│   │   │   ├── admin.py          # Admin API endpoints
│   │   │   ├── client.py         # Client API endpoints
│   │   │   └── system.py         # System API endpoints
│   │   ├── 📁 core/              # Core functionality
│   │   │   ├── config.py         # Configuration management
│   │   │   ├── database.py       # Database connection management
│   │   │   ├── exceptions.py     # Exception handling
│   │   │   ├── logging.py        # Logging configuration
│   │   │   └── security.py       # Security and authentication
│   │   └── 📁 models/            # Data models
│   ├── main.py                   # FastAPI application entry point
│   └── requirements.txt          # Python dependencies
├── docker-compose.yml            # Docker services orchestration
├── health-check.sh              # Health monitoring script
└── PHASE1-SUMMARY.md            # Phase 1 implementation summary
```

## 🔌 Protocols & Technologies

### Communication Protocols
- **HTTP/HTTPS**: REST API communication
- **WebSocket**: Real-time bidirectional communication
- **MQTT**: IoT device communication and event publishing
- **RTSP**: Real-time video streaming
- **ONVIF**: IP camera discovery and control
- **WebRTC**: Peer-to-peer video streaming (planned)

### Technology Stack
- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Message Broker**: Mosquitto MQTT
- **Containerization**: Docker & Docker Compose
- **Authentication**: JWT (JSON Web Tokens)
- **Security**: bcrypt password hashing, CORS, HTTPS

## 🐳 Docker Services

### Service Architecture
```yaml
Services:
├── edgerelay-core-api     # Core API Service (FastAPI)
├── edgerelay-postgres     # PostgreSQL Database
├── edgerelay-redis        # Redis Cache
└── edgerelay-mqtt         # MQTT Broker (Mosquitto)
```

### Service Details

#### 🔧 **EdgeRelay Core API Service**
- **Image**: Custom FastAPI application
- **Purpose**: Main API gateway and business logic
- **Technology**: FastAPI, Python 3.11
- **Health Check**: HTTP endpoint monitoring

#### 🗄️ **PostgreSQL Database**
- **Image**: postgres:15-alpine
- **Purpose**: Primary data storage
- **Features**: Connection pooling, health monitoring
- **Data**: User management, device registry, alerts

#### ⚡ **Redis Cache**
- **Image**: redis:7-alpine
- **Purpose**: Session management, caching, real-time data
- **Features**: Persistence, authentication
- **Usage**: Token storage, temporary data

#### 📡 **MQTT Broker**
- **Image**: eclipse-mosquitto:2.0
- **Purpose**: IoT device communication
- **Features**: Message routing, topic management
- **Protocols**: MQTT 3.1.1, MQTT over WebSocket

## 🌐 Ports Configuration

### Port Allocation (9XXX Series)
```
Port 9000: MQTT Broker (TCP 1883)
Port 9001: MQTT Broker (TLS 8883)
Port 9004: Core API Service (HTTP)
Port 9005: Core API Service (HTTPS) - Reserved
Port 9022: PostgreSQL Database
Port 9024: Redis Cache
```

### Port Usage Details
- **9000**: MQTT broker standard port for IoT device communication
- **9001**: MQTT over TLS for secure communication
- **9004**: HTTP API endpoint for client and admin access
- **9005**: HTTPS API endpoint (reserved for SSL/TLS implementation)
- **9022**: PostgreSQL database access
- **9024**: Redis cache access

## 🔗 Service Endpoints

### Core API Service Endpoints

#### 🏠 **Root Endpoints**
- **`GET /`**
  - **Description**: Service information and status
  - **Response**: Service name, version, status, timestamp
  - **Authentication**: None required

- **`GET /health`**
  - **Description**: Health check endpoint for monitoring
  - **Response**: Service health status, database connectivity, cache status
  - **Authentication**: None required

#### 🔧 **System Endpoints**
- **`GET /api/status`**
  - **Description**: Detailed system status information
  - **Response**: Service details, uptime, feature availability
  - **Authentication**: None required

- **`GET /api/info`**
  - **Description**: Service information and architecture details
  - **Response**: Service description, version, endpoints, features
  - **Authentication**: None required

#### 👨‍💼 **Admin Endpoints** (Planned)
- **`POST /api/admin/auth/login`**
  - **Description**: Admin user authentication
  - **Request**: username, password
  - **Response**: JWT token, admin details
  - **Authentication**: None required

- **`GET /api/admin/auth/me`**
  - **Description**: Get current admin information
  - **Response**: Admin profile details
  - **Authentication**: JWT token required

- **`POST /api/admin/clients`**
  - **Description**: Create new client user
  - **Request**: client details
  - **Response**: Created client information
  - **Authentication**: Admin JWT token required

- **`GET /api/admin/clients`**
  - **Description**: List all client users
  - **Response**: Array of client information
  - **Authentication**: Admin JWT token required

#### 👤 **Client Endpoints** (Planned)
- **`POST /api/client/auth/login`**
  - **Description**: Client user authentication
  - **Request**: username, password
  - **Response**: JWT token, client details
  - **Authentication**: None required

- **`GET /api/client/auth/me`**
  - **Description**: Get current client information
  - **Response**: Client profile details
  - **Authentication**: JWT token required

- **`GET /api/client/status`**
  - **Description**: Get client status and permissions
  - **Response**: Client status, permissions, capabilities
  - **Authentication**: JWT token required

### Interactive Documentation
- **`GET /docs`**: Swagger UI documentation
- **`GET /redoc`**: ReDoc documentation

## 🗄️ Database Schema

### Database Structure
```sql
Database: edgerelay_db
User: edgerelay_user
Tables: 7
```

### Table Schema

#### 👨‍💼 **admin_users**
```sql
CREATE TABLE admin_users (
    admin_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 👤 **client_users**
```sql
CREATE TABLE client_users (
    client_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 🖥️ **local_servers**
```sql
CREATE TABLE local_servers (
    server_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    server_name VARCHAR(255) NOT NULL,
    server_ip VARCHAR(45) NOT NULL,
    server_port INTEGER DEFAULT 8000,
    status VARCHAR(20) DEFAULT 'offline',
    last_seen TIMESTAMP DEFAULT NOW(),
    capabilities TEXT,
    configuration JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 📹 **cameras**
```sql
CREATE TABLE cameras (
    camera_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    server_id UUID REFERENCES local_servers(server_id) ON DELETE CASCADE,
    camera_name VARCHAR(255) NOT NULL,
    rtsp_url VARCHAR(500),
    onvif_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'offline',
    capabilities TEXT,
    configuration JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 🚨 **alerts**
```sql
CREATE TABLE alerts (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    server_id UUID REFERENCES local_servers(server_id) ON DELETE CASCADE,
    camera_id UUID REFERENCES cameras(camera_id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(20) DEFAULT 'info',
    is_processed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 🔐 **sessions**
```sql
CREATE TABLE sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### ⚙️ **system_config**
```sql
CREATE TABLE system_config (
    config_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 🔒 Security Mechanism

### Authentication & Authorization

#### 🔐 **JWT Token Authentication**
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Token Expiry**: 30 minutes (access token), 7 days (refresh token)
- **Secret Key**: Environment-based secure key
- **Token Structure**: User ID, role, permissions, expiry

#### 🔑 **Password Security**
- **Hashing**: bcrypt with salt
- **Strength Validation**: Minimum 8 characters, uppercase, lowercase, numbers, special characters
- **Storage**: Hashed passwords only, never plain text

#### 🛡️ **Security Headers**
- **CORS**: Configurable cross-origin resource sharing
- **Trusted Host**: Host validation middleware
- **HTTPS**: SSL/TLS encryption (planned)
- **Rate Limiting**: Request rate limiting (planned)

### Data Protection

#### 🔒 **Database Security**
- **Connection Encryption**: TLS for database connections
- **User Isolation**: Separate admin and client databases
- **Access Control**: Role-based access control (RBAC)
- **Audit Logging**: User action logging

#### 🔐 **API Security**
- **Input Validation**: Pydantic model validation
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Input sanitization
- **Error Handling**: Secure error messages

### Network Security

#### 🌐 **Network Isolation**
- **Docker Networks**: Isolated container networking
- **Port Management**: Controlled port exposure
- **Firewall**: Network access control
- **VPN Support**: Secure remote access (planned)

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- VPS with sufficient resources
- Domain name (optional)

### Quick Start
```bash
# Clone and navigate to EdgeRelay
cd /home/edgerelay/EdgeRelay

# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# Test API endpoint
curl http://localhost:9004/health
```

### Service Management
```bash
# View logs
docker-compose logs -f edgerelay-core-api

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Rebuild and restart
docker-compose build && docker-compose up -d
```

## 📊 Current Status

### ✅ **Completed Features**
- Core API Service with FastAPI
- PostgreSQL database with complete schema
- Redis cache implementation
- MQTT broker configuration
- Docker containerization
- Basic authentication framework
- Health monitoring endpoints

### 🚧 **In Progress**
- Admin and client authentication endpoints
- Database connection optimization
- MQTT broker stability

### 📋 **Planned Features**
- Admin frontend (Vue.js)
- Client mobile app
- WebSocket real-time communication
- Video streaming service
- Notification service
- SSL/TLS implementation

## 🤝 Contributing

This project follows MESSS principles:
- **Modular**: Well-structured, reusable components
- **Efficient**: Optimized performance and resource usage
- **Scalable**: Designed for growth and expansion
- **Secure**: Industry-standard security practices
- **Stable**: Reliable and maintainable codebase

## 📄 License

EdgeRelay - Edge AI NVR Communication Platform
Copyright (c) 2025 SmartSecurity.Solutions

---

**EdgeRelay** - Connecting the future of intelligent surveillance 🚀
