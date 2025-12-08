# mobile-use: automate your phone with natural language

<div align="center">

![mobile-use in Action](./doc/banner-v2.png)

</div>

<div align="center">

[![Discord](https://img.shields.io/discord/1403058278342201394?color=7289DA&label=Discord&logo=discord&logoColor=white&style=for-the-badge)](https://discord.gg/6nSqmQ9pQs)
[![GitHub stars](https://img.shields.io/github/stars/minitap-ai/mobile-use?style=for-the-badge&color=e0a8dd)](https://github.com/minitap-ai/mobile-use/stargazers)

<h3>
    <a href="https://docs.minitap.ai/v2/mcp-server/introduction"><b>📚 Official Documentation</b></a>
</h3>
<p align="center">
    <a href="https://discord.gg/6nSqmQ9pQs"><b>Discord</b></a> •
    <a href="https://x.com/minitap_ai?t=iRWtI497UhRGLeCKYQekig&s=09"><b>Twitter / X</b></a>
</p>

[![PyPI version](https://img.shields.io/pypi/v/minitap-mobile-use.svg?color=blue)](https://pypi.org/project/minitap-mobile-use/)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/minitap-ai/mobile-use/blob/main/LICENSE)

</div>

Mobile-use is a powerful, open-source AI agent that controls your Android or IOS device using natural language. It understands your commands and interacts with the UI to perform tasks, from sending messages to navigating complex apps.

## 🏠 100% Local & Private by Default

> **Privacy-First Design**: Mobile-use runs **completely locally** on your machine or home server. No data is sent to external services unless you explicitly configure it. Your phone interactions, commands, and data stay on your network.

**Perfect for:**
- 🏠 **Home Server Deployment**: Run on a Raspberry Pi, NAS, or any local server
- 🔒 **Complete Privacy**: All processing happens locally - no cloud dependencies
- 🌐 **Offline Capable**: Works without internet (when using local LLMs)
- ⚡ **Low Latency**: Direct local communication with your device

> Mobile-use is quickly evolving. Your suggestions, ideas, and reported bugs will shape this project. Do not hesitate to join in the conversation on [Discord](https://discord.gg/6nSqmQ9pQs) or contribute directly, we will reply to everyone! ❤️

## ✨ Features

- 🗣️ **Natural Language Control**: Interact with your phone using your native language
- 📱 **UI-Aware Automation**: Intelligently navigates through app interfaces (note: currently has limited effectiveness with games as they don't provide accessibility tree data)
- 📊 **Data Scraping**: Extract information from any app and structure it into your desired format (e.g., JSON) using a natural language description
- 🔧 **Extensible & Customizable**: Use OpenAI, Google, local LLMs via Ollama, or any OpenAI-compatible API
- 📡 **Wireless Mirroring**: High-performance wireless screen mirroring with scrcpy for Android devices (see [Wireless Setup Guide](doc/WIRELESS_SETUP.md))
- 🏠 **Self-Hostable**: Deploy on your home server, NAS, or Raspberry Pi - no external services required
- 🔒 **Privacy-Focused**: All data stays on your local network by default

## Benchmarks

<p align="center">
  <a href="https://minitap.ai/benchmark">
    <img src="https://files.peachworlds.com/website/753680a0-c383-451e-9800-703d04489ea9/comparison.png" alt="Project banner" />
  </a>
</p>

We stand among the top performers in the AndroidWorld benchmark.
More info here: https://minitap.ai/benchmark

The official leaderboard is available [here](https://docs.google.com/spreadsheets/d/1cchzP9dlTZ3WXQTfYNhh3avxoLipqHN75v1Tb86uhHo/edit?pli=1&gid=0#gid=0)

## 🚀 Getting Started

Ready to automate your mobile experience? Mobile-use is designed to run **100% locally** on your computer or home server.

> [!IMPORTANT]
> **Local-First Architecture**: Mobile-use runs entirely on your machine by default. No telemetry, no external API calls (except to your chosen LLM provider), and no data leaves your network. Perfect for privacy-conscious users and home server deployments.

### 🏠 Deployment Options

Choose the setup that works best for you:

1. **🖥️ Local Desktop**: Run directly on your Windows, macOS, or Linux machine
2. **🏠 Home Server**: Deploy on a Raspberry Pi, NAS, or dedicated home server
3. **🐳 Docker**: Containerized deployment for easy management and isolation

All options keep your data local and private. See [Local Deployment Guide](doc/LOCAL_DEPLOYMENT.md) for home server setup.

### 🛠️ Local Setup (Recommended for Getting Started)

1.  **Set up Environment Variables:**
    Copy the example `.env.example` file to `.env` and add your API key for your preferred LLM provider.

    ```bash
    cp .env.example .env
    ```

    **Required:** Set at least one LLM provider API key (e.g., `OPENAI_API_KEY`). The `MINITAP_API_KEY` is **optional** and only needed if you want to use the Minitap platform or minitap LLM provider.

2.  **(Optional) Customize LLM Configuration:**
    To use different models or providers, create your own LLM configuration file.

    ```bash
    cp llm-config.override.template.jsonc llm-config.override.jsonc
    ```

    Then, edit `llm-config.override.jsonc` to fit your needs.

    **For Complete Privacy - Use Local LLMs:**
    
    You can run mobile-use with **fully local LLMs** using Ollama or any OpenAI-compatible local server:

    1. Install [Ollama](https://ollama.ai/) and pull a model: `ollama pull llama3.1`
    2. Set in your `.env`:
       ```bash
       OPENAI_BASE_URL=http://localhost:11434/v1
       OPENAI_API_KEY=ollama  # Can be any value
       ```
    3. In your `llm-config.override.jsonc`, set `openai` as the provider and specify your local model name (e.g., `llama3.1`)
    
    This ensures **zero external API calls** - everything runs on your machine.

    > [!NOTE]
    > If you want to use Google Vertex AI, you must either:
    >
    > - Have credentials configured for your environment (gcloud, workload identity, etc…)
    > - Store the path to a service account JSON file as the GOOGLE_APPLICATION_CREDENTIALS environment variable
    >
    > More information: - [Credential types](https://cloud.google.com/docs/authentication/application-default-credentials#GAC) - [google.auth API reference](https://googleapis.dev/python/google-auth/latest/reference/google.auth.html#module-google.auth)

### 🌐 Using the Minitap Platform (Optional)

If you prefer a managed solution, you can connect to the Minitap platform which provides:
- Hosted LLM access
- Task management and tracking
- Remote execution on cloud devices

Follow our [Platform quickstart](https://docs.minitap.ai/v2/platform-quickstart) to get started with the platform.

### 🐳 Quick Launch with Docker (Local Deployment)

> [!NOTE]
> Docker provides an easy way to run mobile-use locally with all dependencies included. Perfect for home server deployment.
> This quickstart is only available for Android devices/emulators as of now, and you must have Docker installed.

**Setup steps:**

1. **Connect your device locally:**
   - Either plug your Android device via USB and enable USB-debugging via Developer Options
   - Or launch an Android emulator on your machine/server
   - Or connect wirelessly on your local network (both device and server must be on same network)

2. **Run mobile-use** in your terminal:

**For Linux/macOS:**

```bash
chmod +x mobile-use.sh
bash ./mobile-use.sh \
  "Open Gmail, find first 3 unread emails, and list their sender and subject line" \
  --output-description "A JSON list of objects, each with 'sender' and 'subject' keys"
```

**For Windows (PowerShell):**

```powershell
powershell.exe -ExecutionPolicy Bypass -File mobile-use.ps1 `
  "Open Gmail, find first 3 unread emails, and list their sender and subject line" `
  --output-description "A JSON list of objects, each with 'sender' and 'subject' keys"
```

> [!NOTE]
> - All processing happens locally on your machine/server
> - If using your own device, accept the ADB connection request that appears on your phone
> - Your device and server must be on the same local network for wireless operation

#### 🧰 Troubleshooting

The script will try to connect to your device via IP.
Therefore, your device **must be connected to the same Wi-Fi network as your computer**.

##### 1. No device IP found

If the script fails with the following message:

```
Could not get device IP. Is a device connected via USB and on the same Wi-Fi network?
```

Then it couldn't find one of the common Wi-Fi interfaces on your device.
Therefore, you must determine what WLAN interface your phone is using via `adb shell ip addr show up`.
Then add the `--interface <YOUR_INTERFACE_NAME>` option to the script.

##### 2. Failed to connect to <DEVICE_IP>:5555 inside Docker

This is most probably an issue with your firewall blocking the connection. Therefore there is no clear fix for this.

##### 3. Failed to pull GHCR docker images (unauthorized)

Since UV docker images rely on a `ghcr.io` public repositories, you may have an expired token if you used `ghcr.io` before for private repositories.
Try running `docker logout ghcr.io` and then run the script again.

### 🏠 Home Server Deployment

Want to run mobile-use on a Raspberry Pi, NAS, or dedicated home server? We've got you covered with a complete guide:

👉 **[Local & Home Server Deployment Guide](doc/LOCAL_DEPLOYMENT.md)**

This guide covers:
- Setting up on Raspberry Pi, NAS, and other home servers
- Using fully local LLMs with Ollama (zero external API calls)
- Network configuration and security best practices
- Running as a background service
- Troubleshooting common issues

**Quick Start for Home Servers:**

```bash
# Use the optimized docker-compose configuration
export ADB_CONNECT_ADDR="192.168.1.100:5555"  # Your device IP
docker-compose -f docker-compose.local-server.yml run --rm mobile-use "Your command here"

# Or run as a persistent service
docker-compose -f docker-compose.local-server.yml up -d mobile-use
```

The `docker-compose.local-server.yml` file is pre-configured for home server deployment with:
- ✅ Persistent volumes for data and configuration
- ✅ Auto-restart on failure
- ✅ Resource limits to prevent overuse
- ✅ Optional integrated Ollama for local LLMs
- ✅ Optimized for 24/7 operation

### Manual Launch (Development Mode)

For developers who want to set up the environment manually:

#### 1. Device Support

Mobile-use currently supports the following devices:

- **Physical Android Phones**: Connect via USB with USB debugging enabled.
- **Android Simulators**: Set up through Android Studio.
- **iOS Simulators**: Supported for macOS users.

> [!NOTE]
> Physical iOS devices are not yet supported.

#### 2. Prerequisites

**For Android:**

- **[Android Debug Bridge (ADB)](https://developer.android.com/studio/releases/platform-tools)**: A tool to connect to your device.
- **[scrcpy](https://github.com/Genymobile/scrcpy)** (Optional): For enhanced wireless screen mirroring performance.

  scrcpy provides high-performance wireless screen mirroring for Android devices. To enable:

  1. Install scrcpy:
     - Linux: `apt-get install scrcpy` or download from [releases](https://github.com/Genymobile/scrcpy/releases)
     - macOS: `brew install scrcpy`
     - Windows: Download from [releases](https://github.com/Genymobile/scrcpy/releases)

  2. Enable scrcpy in your `.env` file:
     ```bash
     USE_SCRCPY=true
     ```

  > [!NOTE]
  > scrcpy is automatically included in Docker containers. For wireless operation, ensure your device is connected to the same Wi-Fi network.

**For iOS (macOS only):**

- **[Xcode](https://developer.apple.com/xcode/)**: Apple's IDE for iOS development.
- **[fb-idb](https://fbidb.io/docs/installation/)**: Facebook's iOS Development Bridge for device automation.

  ```bash
  # Install via Homebrew (macOS)
  brew tap facebook/fb
  brew install idb-companion
  ```

  > [!NOTE]
  > `idb_companion` is required to communicate with iOS simulators. Make sure it's in your PATH after installation.

**Common requirements:**

Before you begin, ensure you have the following installed:

- **[uv](https://github.com/astral-sh/uv)**: A lightning-fast Python package manager.

#### 3. Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/minitap-ai/mobile-use.git && cd mobile-use
    ```

2.  [**Setup environment variables**](#-getting-started)

3.  **Create & activate the virtual environment:**

    ```bash
    # This will create a .venv directory using the Python version in .python-version
    uv venv

    # Activate the environment
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows:
    .venv\Scripts\activate
    ```

4.  **Install dependencies:**
    ```bash
    # Sync with the locked dependencies for a consistent setup
    uv sync
    ```

## 👨‍💻 Usage

To run mobile-use, simply pass your command as an argument.

**Example 1: Basic Command**

```bash
python ./src/mobile_use/main.py "Go to settings and tell me my current battery level"
```

**Example 2: Data Scraping**

Extract specific information and get it back in a structured format. For instance, to get a list of your unread emails:

```bash
python ./src/mobile_use/main.py \
  "Open Gmail, find all unread emails, and list their sender and subject line" \
  --output-description "A JSON list of objects, each with 'sender' and 'subject' keys"
```

> [!NOTE]
> If you haven't configured a specific model, mobile-use will prompt you to choose one from the available options.

## 🔎 Agentic System Overview

<div align="center">

![Graph Visualization](doc/graph.png)

_This diagram is automatically updated from the codebase. This is our current agentic system architecture._

</div>

## ❤️ Contributing

We love contributions! Whether you're fixing a bug, adding a feature, or improving documentation, your help is welcome. Please read our **[Contributing Guidelines](CONTRIBUTING.md)** to get started.

## ⭐ Star History

<p align="center">
  <a href="https://star-history.com/#minitap-ai/mobile-use&Date">
    <img src="https://api.star-history.com/svg?repos=minitap-ai/mobile-use&type=Date" alt="Star History Chart" />
  </a>
</p>

## 🔐 Privacy & Security

Mobile-use is designed with privacy as a core principle:

- **🏠 Local by Default**: All processing happens on your machine/server
- **🔒 No Telemetry**: Zero tracking or analytics sent to external services
- **🌐 Network Control**: You choose what data (if any) leaves your network
- **🛡️ Open Source**: Fully auditable code - see exactly what runs on your system

**Local LLM Options for Complete Privacy:**
- [Ollama](https://ollama.ai/) - Easy local LLM deployment
- [LM Studio](https://lmstudio.ai/) - GUI for local models
- [LocalAI](https://localai.io/) - OpenAI-compatible local server
- Any OpenAI-compatible endpoint

See the [Local Deployment Guide](doc/LOCAL_DEPLOYMENT.md) for setup instructions.

## 📖 Documentation

- 📘 [Local & Home Server Deployment](doc/LOCAL_DEPLOYMENT.md) - Complete guide for local/home server setup
- 📗 [Wireless Setup Guide](doc/WIRELESS_SETUP.md) - Configure wireless device mirroring
- 📙 [Official Documentation](https://docs.minitap.ai/v2/mcp-server/introduction) - Full API and SDK docs
- 📕 [Contributing Guide](CONTRIBUTING.md) - How to contribute to the project

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
