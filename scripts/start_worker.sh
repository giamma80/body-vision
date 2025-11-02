#!/bin/bash
set -e

# Start Dramatiq worker for body analysis tasks

echo "🚀 Starting Dramatiq worker for BodyVision..."

# Activate virtual environment if not already activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Check if Redis is running
echo "🔍 Checking Redis connection..."
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running. Please start Redis first:"
    echo "   redis-server --daemonize yes"
    echo "   Or: brew services start redis"
    exit 1
fi

echo "✅ Redis is running"

# Set Python path to include both backend and inference
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend:$(pwd)/inference"

# Start the worker
echo "👷 Starting worker with 4 threads..."
echo "📁 Working directory: $(pwd)"
echo ""

dramatiq inference.app.tasks.body_analysis \
    --processes 1 \
    --threads 4 \
    --verbose

# Note: For production, use supervisord or systemd to manage the worker
