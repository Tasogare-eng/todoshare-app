#!/bin/bash

# Deploy script for TodoShare App
# Usage: ./deploy.sh

echo "🚀 Starting deployment..."

# Pull latest changes
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Check if .env.production exists
if [ ! -f backend/.env.production ]; then
    echo "⚠️  .env.production not found!"
    echo "📝 Creating from template..."
    cp backend/.env.production.example backend/.env.production
    echo "✏️  Please edit backend/.env.production with your production values"
    echo "Then run this script again."
    exit 1
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker compose -f docker-compose.prod.yml down

# Build images
echo "🔨 Building Docker images..."
docker compose -f docker-compose.prod.yml build --no-cache

# Start containers
echo "🎯 Starting containers..."
docker compose -f docker-compose.prod.yml up -d

# Check status
echo "✅ Checking container status..."
docker compose -f docker-compose.prod.yml ps

echo "🎉 Deployment complete!"
echo "📊 View logs: docker compose -f docker-compose.prod.yml logs -f"