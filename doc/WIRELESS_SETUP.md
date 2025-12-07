# Wireless Setup with scrcpy

This guide explains how to set up and use wireless screen mirroring with scrcpy for enhanced performance.

## Overview

mobile-use now supports high-performance wireless screen mirroring using [scrcpy](https://github.com/Genymobile/scrcpy). This provides:

- **Better performance**: 30-60 FPS wireless screen mirroring
- **Lower latency**: 35-70ms compared to traditional ADB screenshots
- **Higher quality**: Maintains device resolution with configurable bitrate
- **Automatic fallback**: Falls back to UIAutomator2 if scrcpy unavailable

## Prerequisites

### 1. Hardware Requirements
- Android device (API 21+ / Android 5.0+)
- USB cable (for initial setup)
- Computer and device on the same Wi-Fi network

### 2. Software Requirements

#### Using Docker (Recommended)
No additional installation needed - scrcpy is pre-installed in Docker images.

#### Manual Installation

**Linux:**
```bash
# Debian/Ubuntu
sudo apt-get install scrcpy

# Or download from releases
wget https://github.com/Genymobile/scrcpy/releases/latest/download/scrcpy-linux.tar.gz
```

**macOS:**
```bash
brew install scrcpy
```

**Windows:**
Download from [scrcpy releases](https://github.com/Genymobile/scrcpy/releases)

## Setup

### Step 1: Enable USB Debugging

1. On your Android device, go to Settings → About Phone
2. Tap "Build Number" 7 times to enable Developer Options
3. Go to Settings → Developer Options
4. Enable "USB Debugging"
5. (Optional) Enable "USB debugging (Security Settings)" for better control

### Step 2: Configure Environment

Add to your `.env` file:

```bash
# Enable scrcpy wireless mirroring
USE_SCRCPY=true

# Optional: Configure scrcpy settings
SCRCPY_MAX_WIDTH=0          # 0 = use device resolution
SCRCPY_BITRATE=8000000      # 8Mbps (default)
SCRCPY_MAX_FPS=60           # 60 FPS (default)
```

### Step 3: Connect Device

#### Using Docker (Automated)

The `mobile-use.sh` script automatically handles wireless connection:

```bash
# Linux/macOS
./mobile-use.sh "Your task here"

# Windows PowerShell
.\mobile-use.ps1 "Your task here"
```

The script will:
1. Detect your USB-connected device
2. Enable wireless ADB (tcpip mode)
3. Connect to device over Wi-Fi
4. Launch mobile-use with scrcpy enabled

#### Manual Connection

```bash
# 1. Connect device via USB
adb devices

# 2. Get device IP address
adb shell ip route | awk '{print $9}'

# 3. Enable TCP/IP mode
adb tcpip 5555

# 4. Connect wirelessly (replace with your device IP)
adb connect 192.168.1.100:5555

# 5. Disconnect USB cable (optional)

# 6. Verify connection
adb devices

# 7. Run mobile-use
python ./src/mobile_use/main.py "Your task"
```

## Configuration Options

### USE_SCRCPY
- **Type**: Boolean
- **Default**: `false`
- **Description**: Enable/disable scrcpy screen mirroring

```bash
USE_SCRCPY=true
```

### SCRCPY_MAX_WIDTH
- **Type**: Integer
- **Default**: `0` (device resolution)
- **Description**: Maximum frame width in pixels. Lower values reduce bandwidth.

```bash
SCRCPY_MAX_WIDTH=1080  # Limit to 1080p width
```

### SCRCPY_BITRATE
- **Type**: Integer
- **Default**: `8000000` (8 Mbps)
- **Description**: Video bitrate in bits per second. Higher = better quality but more bandwidth.

```bash
SCRCPY_BITRATE=4000000  # 4 Mbps for slower networks
```

### SCRCPY_MAX_FPS
- **Type**: Integer
- **Default**: `60`
- **Description**: Maximum frames per second. Android 10+ required for values > 60.

```bash
SCRCPY_MAX_FPS=30  # Lower FPS for slower networks
```

## Performance Tuning

### For Slow Networks

```bash
USE_SCRCPY=true
SCRCPY_MAX_WIDTH=800
SCRCPY_BITRATE=2000000
SCRCPY_MAX_FPS=30
```

### For High-Speed Networks

```bash
USE_SCRCPY=true
SCRCPY_MAX_WIDTH=0          # Full device resolution
SCRCPY_BITRATE=16000000     # 16 Mbps
SCRCPY_MAX_FPS=60
```

### For Battery Saving

```bash
USE_SCRCPY=true
SCRCPY_MAX_WIDTH=720
SCRCPY_BITRATE=4000000
SCRCPY_MAX_FPS=30
```

## Troubleshooting

### Issue: "scrcpy-client not available"

**Solution**: Install the Python package:
```bash
pip install scrcpy-client
```

Or if using uv:
```bash
uv pip install scrcpy-client
```

### Issue: "Failed to start scrcpy client"

**Possible causes:**
1. Device not connected via ADB
2. Scrcpy binary not installed
3. Device not authorized

**Solutions:**
```bash
# Check ADB connection
adb devices

# Re-authorize device
adb kill-server
adb start-server
adb devices  # Accept prompt on device

# Test scrcpy directly
scrcpy --serial=<device-ip>:5555
```

### Issue: Connection drops frequently

**Solutions:**
1. Ensure stable Wi-Fi connection
2. Reduce `SCRCPY_BITRATE`
3. Lower `SCRCPY_MAX_FPS`
4. Move device closer to Wi-Fi router
5. Use 5GHz Wi-Fi band if available

### Issue: Poor video quality

**Solutions:**
1. Increase `SCRCPY_BITRATE`
2. Increase `SCRCPY_MAX_WIDTH` or set to 0
3. Ensure good Wi-Fi signal strength

### Issue: High latency

**Solutions:**
1. Use 5GHz Wi-Fi instead of 2.4GHz
2. Reduce `SCRCPY_MAX_WIDTH`
3. Lower `SCRCPY_MAX_FPS`
4. Check network congestion

### Issue: Fallback to UIAutomator2

If you see "falling back to UIAutomator2" in logs:

1. **Check scrcpy installation**:
   ```bash
   scrcpy --version
   pip show scrcpy-client
   ```

2. **Check device compatibility**: Requires Android 5.0+ (API 21+)

3. **Verify ADB connection**:
   ```bash
   adb devices
   adb shell dumpsys battery  # Test ADB shell
   ```

4. **Check logs**: Look for error messages in the output

## Verifying Setup

Run this test to verify scrcpy is working:

```python
from adbutils import adb
from minitap.mobile_use.clients.scrcpy_client import ScrcpyClientWrapper, SCRCPY_AVAILABLE

print(f"Scrcpy available: {SCRCPY_AVAILABLE}")

if SCRCPY_AVAILABLE:
    device = adb.device_list()[0]
    client = ScrcpyClientWrapper(device=device)

    if client.start():
        print("✓ Scrcpy started successfully")
        width, height = client.get_resolution()
        print(f"✓ Resolution: {width}x{height}")
        screenshot = client.get_screenshot_base64()
        print(f"✓ Screenshot captured: {len(screenshot)} bytes")
        client.stop()
    else:
        print("✗ Failed to start scrcpy")
else:
    print("✗ Scrcpy not available")
```

## Best Practices

1. **Start with defaults**: Try default settings before tuning
2. **Monitor bandwidth**: Use network monitoring tools to check usage
3. **Battery consideration**: Lower FPS/bitrate for longer battery life
4. **Network quality**: Use 5GHz Wi-Fi for best performance
5. **Keep device awake**: Scrcpy automatically keeps device awake during mirroring

## Technical Details

### Architecture

```
┌─────────────────────┐
│  mobile-use Agent   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ AndroidController   │
│  (with scrcpy)      │
└──────────┬──────────┘
           │
      ┌────┴────┐
      │         │
      ▼         ▼
┌──────────┐  ┌──────────┐
│ scrcpy   │  │UIAutomator│
│ (video)  │  │(hierarchy)│
└─────┬────┘  └────┬─────┘
      │            │
      └────┬───────┘
           │
      ┌────▼─────────┐
      │ Android      │
      │ Device       │
      │ (wireless)   │
      └──────────────┘
```

### How It Works

1. **Initialization**: `ScrcpyClientWrapper` connects to device via ADB
2. **Server Push**: Scrcpy server pushed to device and started
3. **Video Stream**: Device streams video over socket connection
4. **Frame Capture**: Frames decoded and converted to PIL Images
5. **Screenshot**: Latest frame encoded as base64 PNG
6. **UI Hierarchy**: UIAutomator2 provides UI element tree
7. **Control**: Input commands sent via ADB shell

### Performance Characteristics

| Method | FPS | Latency | Bandwidth | CPU Usage |
|--------|-----|---------|-----------|-----------|
| scrcpy | 30-60 | 35-70ms | 2-8 Mbps | Medium |
| ADB Screenshot | 1-5 | 200-500ms | Low | Low |

## Additional Resources

- [scrcpy GitHub](https://github.com/Genymobile/scrcpy)
- [scrcpy Documentation](https://github.com/Genymobile/scrcpy/tree/master/doc)
- [scrcpy-client Python Library](https://github.com/leng-yue/py-scrcpy-client)
- [ADB Wireless Documentation](https://developer.android.com/studio/command-line/adb#wireless)

## Support

For issues or questions:
- [GitHub Issues](https://github.com/minitap-ai/mobile-use/issues)
- [Discord Community](https://discord.gg/6nSqmQ9pQs)
- [Documentation](https://docs.minitap.ai)
