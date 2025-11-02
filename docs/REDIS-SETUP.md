# Redis Setup Guide

Redis is required for BodyVision's background job queue (Dramatiq). This guide covers installation, configuration, and management.

---

## Quick Start

```bash
# Check if Redis is installed
make redis-check

# Start Redis
make redis-start

# Check status
make redis-status

# Stop Redis
make redis-stop
```

---

## Installation

### macOS (Homebrew)
```bash
brew install redis

# Auto-start on boot (optional)
brew services start redis
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install redis-server

# Start service
sudo systemctl start redis-server
sudo systemctl enable redis-server  # Auto-start on boot
```

### Windows (WSL)
```bash
# Install via WSL (Ubuntu)
sudo apt-get install redis-server

# Start manually
redis-server --daemonize yes
```

### Docker (Alternative)
```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

---

## Makefile Commands

The project includes automated Redis management via Make targets:

### `make redis-check`
Verifies if Redis is installed on your system.

**Output:**
- ✓ Redis is installed
- Error with installation instructions if not found

### `make redis-status`
Checks if Redis server is currently running.

**Output:**
- ✓ Redis is running
- Redis is not running (with start instructions)

### `make redis-start`
Starts Redis server automatically.

**Behavior:**
- Auto-detects platform (Homebrew vs manual)
- Skips if already running
- Waits 1 second for initialization
- Verifies connection

### `make redis-stop`
Stops Redis server gracefully.

**Behavior:**
- Auto-detects platform (Homebrew vs manual)
- Skips if not running
- Uses `redis-cli shutdown`

### `make redis-restart`
Stops and starts Redis (equivalent to `redis-stop` + `redis-start`)

---

## Manual Management

### Start Redis
```bash
# Foreground (for debugging)
redis-server

# Background (daemon mode)
redis-server --daemonize yes

# With custom config
redis-server /path/to/redis.conf
```

### Stop Redis
```bash
redis-cli shutdown
```

### Check Status
```bash
# Ping test
redis-cli ping
# Expected: PONG

# Server info
redis-cli info server
```

### Monitor Activity
```bash
# Real-time command monitoring
redis-cli monitor

# View stats
redis-cli info stats
```

---

## Configuration

### Default Settings
- **Port:** 6379
- **Host:** localhost (127.0.0.1)
- **Max Memory:** Unlimited
- **Persistence:** RDB snapshots + AOF log

### Environment Variables

Configure Redis connection in `.env`:

```bash
# Redis URL format
REDIS_URL=redis://localhost:6379/0

# With password
REDIS_URL=redis://:password@localhost:6379/0

# Remote Redis
REDIS_URL=redis://redis.example.com:6379/0
```

### Custom Configuration

Create `redis.conf`:

```conf
# Network
bind 127.0.0.1
port 6379
protected-mode yes

# Memory
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Performance
tcp-keepalive 300
timeout 0
```

Start with config:
```bash
redis-server /path/to/redis.conf
```

---

## Troubleshooting

### Redis won't start
```bash
# Check if port is in use
lsof -i :6379

# Kill existing process
redis-cli shutdown

# Start with verbose logging
redis-server --loglevel debug
```

### Connection refused
```bash
# Verify Redis is running
redis-cli ping

# Check firewall
sudo ufw allow 6379  # Ubuntu

# Check bind address in redis.conf
# Should be: bind 127.0.0.1
```

### High memory usage
```bash
# Check memory stats
redis-cli info memory

# Set max memory limit
redis-cli CONFIG SET maxmemory 256mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru

# Flush all data (careful!)
redis-cli FLUSHALL
```

### Lost connection
```bash
# Check Redis logs
tail -f /var/log/redis/redis-server.log  # Ubuntu
tail -f /usr/local/var/log/redis.log     # macOS Homebrew

# Restart Redis
make redis-restart
```

---

## Development Workflow

### Starting the Full Stack

1. **Start Redis:**
   ```bash
   make redis-start
   ```

2. **Start API Server:**
   ```bash
   make dev
   ```

3. **Start Worker (separate terminal):**
   ```bash
   make worker
   ```

4. **Test the API:**
   ```bash
   python scripts/test_api.py
   ```

### Shutdown

```bash
# Stop worker: Ctrl+C
# Stop API: Ctrl+C
# Stop Redis:
make redis-stop
```

---

## Production Considerations

### Security
- Change default port
- Set password: `requirepass your-password`
- Enable protected mode
- Use firewall rules
- Disable dangerous commands: `rename-command FLUSHALL ""`

### Performance
- Set `maxmemory` limit
- Use appropriate eviction policy
- Enable persistence (RDB + AOF)
- Monitor with Redis Sentinel

### High Availability
- Redis Sentinel for automatic failover
- Redis Cluster for horizontal scaling
- Use managed Redis (AWS ElastiCache, Redis Cloud)

### Monitoring
```bash
# Check queue size
redis-cli LLEN default.DQ

# View all keys
redis-cli KEYS '*'

# Monitor commands
redis-cli --latency
redis-cli --stat
```

---

## Testing

### Verify Redis Installation
```bash
# Ping test
redis-cli ping
# Expected: PONG

# Set/Get test
redis-cli SET test "hello"
redis-cli GET test
# Expected: "hello"

# Delete test key
redis-cli DEL test
```

### Test with BodyVision
```bash
# Start Redis
make redis-start

# Start worker (background)
make worker &

# Run test
python scripts/test_api.py
```

---

## Common Commands Reference

```bash
# Connection
redis-cli                    # Connect to localhost:6379
redis-cli -h HOST -p PORT    # Connect to remote
redis-cli -a PASSWORD        # With password

# Keys
KEYS *                       # List all keys (dev only!)
GET key                      # Get value
SET key value                # Set value
DEL key                      # Delete key
EXISTS key                   # Check if exists
TTL key                      # Time to live

# Server
INFO                         # Server info
DBSIZE                       # Number of keys
FLUSHDB                      # Clear current DB
FLUSHALL                     # Clear all DBs (careful!)
SAVE                         # Force snapshot
BGSAVE                       # Background snapshot

# Monitoring
MONITOR                      # Watch commands
CLIENT LIST                  # Connected clients
SLOWLOG GET 10               # Slow queries
```

---

## Additional Resources

- [Redis Official Docs](https://redis.io/documentation)
- [Redis Commands](https://redis.io/commands)
- [Redis Best Practices](https://redis.io/topics/best-practices)
- [Dramatiq Documentation](https://dramatiq.io)

---

Last Updated: 2025-11-02
