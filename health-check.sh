#!/bin/bash

# EdgeRelay Health Check Script

echo "=== EdgeRelay Health Check ==="
echo "Date: $(date)"
echo ""

# Check if Docker is running
echo "1. Checking Docker status..."
if systemctl is-active --quiet docker; then
    echo "   ✅ Docker is running"
else
    echo "   ❌ Docker is not running"
    exit 1
fi

# Check EdgeRelay containers
echo ""
echo "2. Checking EdgeRelay containers..."
cd /home/edgerelay/EdgeRelay

# Start containers if not running
echo "   Starting EdgeRelay services..."
docker-compose up -d

# Wait for services to start
echo "   Waiting for services to start..."
sleep 30

# Check container status
echo "   Container Status:"
docker-compose ps

# Test PostgreSQL connection
echo ""
echo "3. Testing PostgreSQL connection..."
if docker-compose exec -T edgerelay-postgres pg_isready -U edgerelay_user -d edgerelay_db; then
    echo "   ✅ PostgreSQL is healthy"
else
    echo "   ❌ PostgreSQL connection failed"
fi

# Test Redis connection
echo ""
echo "4. Testing Redis connection..."
if docker-compose exec -T edgerelay-redis redis-cli ping | grep -q PONG; then
    echo "   ✅ Redis is healthy"
else
    echo "   ❌ Redis connection failed"
fi

# Test MQTT connection
echo ""
echo "5. Testing MQTT connection..."
if docker-compose exec -T edgerelay-mqtt mosquitto_pub -h localhost -t test -m "health_check" -q 1; then
    echo "   ✅ MQTT broker is healthy"
else
    echo "   ❌ MQTT connection failed"
fi

echo ""
echo "=== Health Check Complete ==="
