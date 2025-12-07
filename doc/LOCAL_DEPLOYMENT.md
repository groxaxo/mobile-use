# 🏠 Local & Home Server Deployment Guide

This guide covers deploying mobile-use on your local machine or home server for complete privacy and control.

## 🎯 Why Deploy Locally?

- **🔒 Complete Privacy**: All data stays on your local network
- **🌐 No Internet Required**: Works offline with local LLMs
- **⚡ Low Latency**: Direct communication with devices on your network
- **💰 Cost Effective**: No cloud hosting fees
- **🛠️ Full Control**: Complete control over updates and configuration

## 📋 Prerequisites

### Hardware Requirements

**Minimum:**
- CPU: 2+ cores
- RAM: 4GB (8GB recommended for local LLMs)
- Storage: 10GB free space (more if using local LLM models)
- Network: WiFi or Ethernet connection

**Recommended for Local LLMs:**
- CPU: 4+ cores
- RAM: 16GB+
- GPU: Optional but significantly improves performance

**Supported Platforms:**
- **Linux**: Ubuntu, Debian, Raspberry Pi OS (64-bit), Fedora, etc.
- **macOS**: 10.15+ (Intel or Apple Silicon)
- **Windows**: 10/11 with WSL2 (for Docker) or native

### Software Requirements

1. **Docker & Docker Compose** (Recommended)
   - Linux: `sudo apt-get install docker.io docker-compose`
   - macOS: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Windows: [Docker Desktop with WSL2](https://docs.docker.com/desktop/windows/install/)

2. **Git**
   - Check: `git --version`
   - Install if needed from [git-scm.com](https://git-scm.com/)

3. **For Android Devices:**
   - ADB (Android Debug Bridge) - included in Docker images
   - Optional: [scrcpy](https://github.com/Genymobile/scrcpy) for better wireless mirroring

4. **For iOS Devices (macOS only):**
   - Xcode
   - fb-idb: `brew tap facebook/fb && brew install idb-companion`

## 🚀 Quick Setup

### Option 1: Docker Deployment (Recommended)

This is the easiest method for home servers and ensures all dependencies are included.

> **💡 TIP**: We provide a special `docker-compose.local-server.yml` configuration optimized for home server deployment with auto-restart, resource limits, and persistent volumes. Use this instead of the standard `docker-compose.yml` for 24/7 operation.

#### 1. Clone the Repository

```bash
git clone https://github.com/minitap-ai/mobile-use.git
cd mobile-use
```

#### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your preferred editor
nano .env
```

**For Local LLM (Complete Privacy):**
```bash
# Install Ollama on your server
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (example)
ollama pull llama3.1

# Configure .env
OPENAI_BASE_URL=http://host.docker.internal:11434/v1
OPENAI_API_KEY=ollama
```

**For Cloud LLM Providers:**
```bash
# Choose one:
OPENAI_API_KEY=your_openai_key_here
# or
GOOGLE_API_KEY=your_google_key_here
```

#### 3. Configure LLM Settings (Optional)

```bash
# Copy override template
cp llm-config.override.template.jsonc llm-config.override.jsonc

# Edit to customize models
nano llm-config.override.jsonc
```

For local LLM, update the config:
```jsonc
{
  "planning": {
    "provider": "openai",
    "model": "llama3.1"  // Your local model
  },
  "coordination": {
    "provider": "openai",
    "model": "llama3.1"
  }
  // ... update other nodes as needed
}
```

#### 4. Connect Your Device

**USB Connection:**
```bash
# Linux: Enable USB debugging on your Android device
# Then connect via USB

# macOS/Windows: Same process
```

**Wireless Connection (Same Network):**
```bash
# First, connect device via USB
# Then run:
adb tcpip 5555

# Find device IP (on Android: Settings → About → Status → IP)
# Or use: adb shell ip addr show wlan0 | grep inet

# Connect wirelessly
adb connect <DEVICE_IP>:5555

# Now you can disconnect USB cable
```

#### 5. Run Mobile-Use

**For Home Server (Recommended - with auto-restart and persistence):**

```bash
# Set device IP in environment (or add to .env file)
export ADB_CONNECT_ADDR="192.168.1.100:5555"

# Run as one-off command
docker-compose -f docker-compose.local-server.yml run --rm mobile-use \
  "Check my email and summarize any important messages"

# OR run as persistent background service
docker-compose -f docker-compose.local-server.yml up -d mobile-use

# View logs
docker-compose -f docker-compose.local-server.yml logs -f mobile-use

# Stop service
docker-compose -f docker-compose.local-server.yml down
```

**For USB connection (standard):**
```bash
docker-compose run --rm mobile-use-full-usb \
  "Check my email and summarize any important messages"
```

**For wireless/IP connection (standard):**
```bash
# Set device IP in environment
export ADB_CONNECT_ADDR="192.168.1.100:5555"

docker-compose run --rm mobile-use-full-ip \
  "Check my email and summarize any important messages"
```

### Option 2: Native Installation

For development or when you prefer not to use Docker:

#### 1. Install Python 3.12+

```bash
# Linux (Ubuntu/Debian)
sudo apt-get install python3.12 python3.12-venv

# macOS
brew install python@3.12

# Windows: Download from python.org
```

#### 2. Install UV Package Manager

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 3. Clone and Setup

```bash
git clone https://github.com/minitap-ai/mobile-use.git
cd mobile-use

# Setup environment
cp .env.example .env
nano .env  # Configure your settings

# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install dependencies
uv sync
```

#### 4. Run Mobile-Use

```bash
python minitap/mobile_use/main.py "Your command here"
```

## 🏠 Home Server Specific Setup

### Raspberry Pi Deployment

Mobile-use works great on Raspberry Pi 4+ with 4GB+ RAM:

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Reboot
sudo reboot

# After reboot, follow Docker deployment steps above
```

**For Local LLM on Raspberry Pi:**
- Use lighter models: `ollama pull llama3.1:8b` or `phi3`
- Consider using cloud LLM for better performance
- Enable swap space if needed

### NAS Deployment (Synology, QNAP, etc.)

1. Enable Docker/Container Manager from package center
2. Create a shared folder for mobile-use
3. Upload repository files via File Station
4. Create container using Docker Compose or manual configuration
5. Configure port forwarding if needed (optional, for remote access)

### Network Configuration

#### Firewall Rules

Mobile-use doesn't require inbound connections by default, but you may need to:

```bash
# Linux: Allow ADB port (if exposing ADB server)
sudo ufw allow 5037/tcp

# Allow Docker network (if using custom network)
sudo ufw allow from 172.17.0.0/16
```

#### Static IP for Device (Recommended)

Configure your router to assign a static IP to your Android device:
1. Access router admin panel
2. Find DHCP/LAN settings
3. Add MAC address → IP reservation
4. Use this IP in your scripts

### Running as a Service

Create a systemd service to run mobile-use on startup:

```bash
# Create service file
sudo nano /etc/systemd/system/mobile-use.service
```

```ini
[Unit]
Description=Mobile-Use Agent
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
User=your-username
WorkingDirectory=/home/your-username/mobile-use
Environment="ADB_CONNECT_ADDR=192.168.1.100:5555"
ExecStart=/usr/bin/docker-compose run --rm mobile-use-full-ip "Your default task"
Restart=no

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable mobile-use.service
sudo systemctl start mobile-use.service
```

## 🔒 Security Best Practices

### Local Network Only

By default, mobile-use only communicates on your local network. Keep it that way:

1. **Don't expose ADB ports to the internet**
2. **Use local LLMs for maximum privacy**
3. **Keep Docker containers on isolated networks**
4. **Use VPN for remote access** (instead of port forwarding)

### Secure Your Setup

```bash
# Change default ADB keys location permissions
chmod 700 ~/.android

# Use environment files for secrets
chmod 600 .env

# Regular updates
docker-compose pull
uv sync --upgrade
```

### VPN Access (Recommended for Remote Use)

Instead of exposing ports, use a VPN:

- **WireGuard**: Fast and secure
- **Tailscale**: Easy setup, zero-config mesh VPN
- **OpenVPN**: Widely supported

This keeps your home server accessible only to you, securely.

## 🔧 Troubleshooting

### Device Not Found

```bash
# Check ADB connection
adb devices

# If empty, reconnect
adb connect <DEVICE_IP>:5555

# Check firewall isn't blocking
sudo ufw status
```

### Docker Permission Issues

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again, or:
newgrp docker
```

### Ollama Connection Issues (from Docker)

```bash
# On Linux, use host network
docker-compose run --network host ...

# Or update .env to use host gateway
OPENAI_BASE_URL=http://host.docker.internal:11434/v1
```

### Performance Issues

1. **Check system resources**: `htop` or `docker stats`
2. **Use lighter LLM models**: phi3, llama3.1:8b
3. **Reduce max FPS** in scrcpy: `SCRCPY_MAX_FPS=30`
4. **Increase Docker memory** limits in Docker Desktop settings

### Network Issues

```bash
# Test device connectivity
ping <DEVICE_IP>

# Test ADB connectivity
adb connect <DEVICE_IP>:5555
adb shell echo "Connected!"

# Check if device and server are on same subnet
ip addr show  # Linux
ipconfig      # Windows
ifconfig      # macOS
```

## 📊 Resource Usage

### Expected Resource Usage

**Minimum Setup (Cloud LLM):**
- CPU: ~10-20% on 4-core system
- RAM: ~500MB-1GB
- Network: Minimal (LLM API calls only)

**With Local LLM:**
- CPU: 50-100% during inference
- RAM: 4-16GB depending on model size
- Network: None (except initial model download)

### Monitoring

```bash
# Monitor Docker containers
docker stats

# Monitor system
htop

# Check logs
docker-compose logs -f mobile-use
```

## 🎯 Next Steps

- ✅ Set up automatic scheduled tasks with cron
- ✅ Create custom automation scripts
- ✅ Explore the [SDK examples](../minitap/mobile_use/sdk/examples/)
- ✅ Join our [Discord](https://discord.gg/6nSqmQ9pQs) community
- ✅ Read the [Wireless Setup Guide](WIRELESS_SETUP.md)

## 💡 Tips & Tricks

1. **Use cron for scheduled automation:**
   ```bash
   # Edit crontab
   crontab -e
   
   # Run daily at 9 AM
   0 9 * * * cd /home/user/mobile-use && docker-compose run --rm mobile-use-ip "Check my calendar"
   ```

2. **Create shell aliases:**
   ```bash
   alias mobile-use='docker-compose run --rm mobile-use-ip'
   
   # Now you can just run:
   mobile-use "Your command"
   ```

3. **Batch multiple commands:**
   ```bash
   docker-compose run --rm mobile-use-ip "
     First check my email, 
     then check my calendar for today,
     then tell me the weather
   "
   ```

4. **Save outputs to files:**
   ```bash
   docker-compose run --rm mobile-use-ip \
     "List all my photos from last month" \
     --output-description "JSON array of photo filenames with dates" \
     > photos.json
   ```

## 📞 Support

- 💬 [Discord Community](https://discord.gg/6nSqmQ9pQs)
- 📖 [Official Documentation](https://docs.minitap.ai)
- 🐛 [GitHub Issues](https://github.com/minitap-ai/mobile-use/issues)
- 🤝 [Contributing Guide](../CONTRIBUTING.md)

---

**Remember**: Mobile-use is designed to be local-first. Everything runs on your network unless you explicitly configure external services. Your privacy is in your hands! 🔒
