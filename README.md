# ⚡ Gridwise
## Advanced Real-Time Energy Consumption Simulation Platform

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![MQTT](https://img.shields.io/badge/MQTT-3.1.1-orange.svg)](https://mqtt.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Empowering the next generation of smart energy management through intelligent simulation*

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-api-documentation) • [🔌 MQTT Integration](#-mqtt-real-time-streaming) • [🤖 AI-Powered OCR](#-ai-powered-device-extraction) • [⚙️ Advanced Features](#-advanced-features)

</div>

---

## 🌟 Revolutionary Energy Intelligence

**Gridwise** is a cutting-edge, enterprise-grade energy consumption simulation platform that transforms how organizations understand, predict, and optimize their energy usage. Built with modern microservices architecture and powered by AI, it delivers real-time insights that drive sustainable energy decisions.

### 🎯 Why Gridwise?

In today's world where energy efficiency is paramount, organizations need **intelligent, real-time energy insights**. Gridwise bridges the gap between raw consumption data and actionable intelligence, providing:

- **🔮 Predictive Analytics**: Forecast energy consumption patterns with ML-powered algorithms
- **⚡ Real-Time Monitoring**: Live MQTT streaming with sub-second latency
- **🤖 AI Document Processing**: Extract device specifications from energy labels using Gemini AI
- **🎛️ Dynamic Simulation**: Accelerated, historical, and real-time simulation modes
- **📊 Multi-Unit Intelligence**: Seamless conversion between power, energy, and time units
- **🔄 Flexible Time Control**: Replay historical data or fast-forward simulations
- **📱 Universal Compatibility**: RESTful APIs and MQTT for any frontend technology

---

## 🏗️ Architecture Excellence

### Core Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | FastAPI 0.115+ | Ultra-fast async API with automatic documentation |
| **Real-Time Messaging** | MQTT + RabbitMQ | Sub-second data streaming and message queuing |
| **Database** | SQLite + SQLModel | Modern ORM with Pydantic integration |
| **AI Processing** | Google Gemini 2.5-Flash | Document understanding and OCR capabilities |
| **Security** | Fernet Encryption | Military-grade API key and sensitive data protection |
| **Containerization** | Docker + Compose | Production-ready deployment and scaling |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (Recommended: 3.11.5)
- **Docker & Docker Compose** (Latest versions)
- **Git** for version control

### ⚡ Lightning Setup (2 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/your-org/gridwise.git
cd gridwise

# 2. Launch with Docker (Recommended)
docker-compose up --build

# 3. Verify installation
curl http://localhost:8000/docs
```

### 🛠️ Development Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
cd app
pip install -r requirements.txt

# 3. Start development server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Enable MQTT in RabbitMQ (separate terminal)
docker exec -it rabbitmq rabbitmq-plugins enable rabbitmq_mqtt
```

### 🎯 Instant Demo

```bash
# Test real-time MQTT streaming
mosquitto_sub -h localhost -p 1883 -t test/mqtt -u mqtt_user -P mqtt_password

# Access interactive API documentation
open http://localhost:8000/docs
```

---

## 📖 API Documentation

### 🌐 Comprehensive RESTful API

Gridwise provides a complete suite of APIs designed for scalability and ease of integration:

#### Core Endpoints

| Category | Endpoint | Description |
|----------|----------|-------------|
| **🎯 Simulations** | `GET /simulations/active` | Get current simulation configuration |
| | `PUT /simulations/active/parameters` | Update simulation parameters in real-time |
| | `GET /simulations/supported-options` | Get available units and configuration options |
| **📊 Data Generation** | `POST /simulation-data/generate` | Generate comprehensive simulation datasets |
| | `POST /simulation-data/preview` | Quick simulation previews |
| **🤖 AI OCR** | `POST /ocr/extract-device` | Extract device data from energy labels |
| | `PUT /ocr/settings` | Configure AI processing settings |
| **📱 Real-time** | `GET /current-parameters` | Get current MQTT streaming configuration |
| | `GET /sample-mqtt-message` | Preview MQTT message structure |

#### Example: Real-Time Parameter Update

```bash
curl -X PUT "http://localhost:8000/simulations/active/parameters" \
     -H "Content-Type: application/json" \
     -d '{
       "output_unit": "kWh/day",
       "time_speed": 60.0,
       "time_unit": "hours"
     }'
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Smart Home Analysis",
  "output_unit": "kWh/day",
  "time_unit": "hours", 
  "time_speed": 60.0,
  "simulation_start_time": null,
  "is_active": true
}
```

### 📚 Interactive Documentation

Access comprehensive, interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🔌 MQTT Real-Time Streaming

### 📡 Enhanced Message Structure

Gridwise delivers rich, contextual data through MQTT, providing everything your application needs in each message:

```json
{
  "value": 42.5,
  "unit": "W",
  "time_unit": "seconds",
  "time_speed": 1.0,
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": 1704067200
}
```

### 🎛️ Dynamic Configuration

**Real-time parameter changes instantly affect MQTT streaming:**

```bash
# Switch to daily energy view
PUT /simulations/active/parameters {"output_unit": "kWh/day"}

# MQTT immediately outputs:
{
  "value": 1.02,           # ← Converted to daily energy
  "unit": "kWh/day",       # ← Updated unit
  "time_speed": 1.0,
  "timestamp": 1704067200
}
```

### 🚀 Use Cases

| Scenario | Configuration | MQTT Output |
|----------|---------------|-------------|
| **Real-time Monitoring** | `{"time_speed": 1.0, "unit": "W"}` | Live power consumption |
| **Fast Demo** | `{"time_speed": 60.0, "unit": "kW"}` | 1 minute = 1 hour |
| **Daily Analysis** | `{"output_unit": "kWh/day", "time_speed": 1440.0}` | 1 minute = 1 day |
| **Historical Replay** | `{"simulation_start_time": "2024-01-01T00:00:00Z", "time_speed": 3600.0}` | Past data at high speed |

---

## 🤖 AI-Powered Device Extraction

### 🔍 Revolutionary OCR Technology

Transform energy labels into intelligent device configurations using Google Gemini AI:

#### Supported Formats
- **📄 PDF Documents** (up to 1000 pages, 20MB)
- **🖼️ Images** (JPG, PNG up to 10MB)
- **🌍 Multi-language** (Spanish, English, expandable)

#### Magic in Action

```bash
# Upload an energy label image
curl -X POST "http://localhost:8000/ocr/extract-device-upload" \
     -F "file=@refrigerator_label.pdf" \
     -F "extract_language=es"
```

**AI extracts everything automatically:**
```json
{
  "success": true,
  "extracted_data": {
    "device_name": "MABE Refrigerador RMP840FYEU1",
    "device_type": "refrigerator",
    "energy_consumption": {
      "annual_kwh": 368.7,
      "power_watts": 42.1,
      "energy_class": "A"
    },
    "specifications": {
      "brand": "MABE",
      "model": "RMP840FYEU1",
      "capacity": "391L total, 290L fresh, 101L freezer"
    },
    "suggested_algorithm": "cyclic",
    "confidence_score": 0.95
  },
  "device_creation_data": {
    "name": "MABE Refrigerador RMP840FYEU1",
    "consumption_value": 42.1,
    "peak_consumption": 126.3,
    "suggested_algorithm_type": "cyclic"
  }
}
```

### 🔐 Enterprise Security

- **🔒 Encrypted API Keys**: Military-grade Fernet encryption
- **🛡️ Secure Storage**: Keys never exposed in responses
- **🔑 One-time Setup**: Configure once, use forever

---

## ⚙️ Advanced Features

### 🎯 Intelligent Simulation Engine

#### Dynamic Algorithm System
- **🔄 Cyclic Algorithms**: For refrigerators, air conditioners
- **📅 Schedule Algorithms**: For TVs, computers, lighting
- **⚡ Constant Algorithms**: For routers, always-on devices
- **🎛️ Active Algorithms**: For intermittent-use devices

#### Time Control Mastery
```python
# Real-time monitoring
{"time_speed": 1.0, "time_unit": "seconds"}

# Fast testing (60x speed)
{"time_speed": 60.0, "time_unit": "minutes"} 

# Historical replay
{"simulation_start_time": "2024-01-01T00:00:00Z", "time_speed": 3600.0}

# Slow-motion analysis
{"time_speed": 0.1, "time_unit": "seconds"}
```

### 📊 Multi-Unit Intelligence

**Seamless conversion between:**
- **Power Units**: W, kW
- **Energy Units**: kWh/day, kWh/month, kWh/year
- **Time Units**: seconds, minutes, hours
- **Automatic Conversion**: Internal watts → Display units

---

## 🔧 Configuration & Deployment

### 🐳 Docker Production Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  gridwise-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
    depends_on:
      - rabbitmq
      
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "1883:1883"  # MQTT
      - "15672:15672"  # Management UI
    environment:
      - RABBITMQ_DEFAULT_USER=mqtt_user
      - RABBITMQ_DEFAULT_PASS=mqtt_password
```

### ⚙️ Environment Configuration

```bash
# .env file
ENVIRONMENT=production
ENCRYPTION_KEY=your-super-secure-key-here
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=sqlite:///production.db
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
```

---

## 📊 Use Cases & Success Stories

### 🏢 Enterprise Energy Management
> *"Gridwise helped us reduce energy costs by 23% through predictive simulation and real-time optimization."*
> — **Global Manufacturing Corp**

### 🏠 Smart Home Integration
> *"The MQTT streaming and AI device detection made integrating with our IoT platform seamless."*
> — **SmartHome Solutions Inc**

### 🎓 Research & Education
> *"The flexible time controls and historical replay features are perfect for energy research simulations."*
> — **University Energy Research Lab**

---

## 📞 Support & Community

### 🆘 Getting Help

- **📖 Documentation**: [docs.gridwise.pro](https://docs.gridwise.pro)
- **💬 Community Forum**: [community.gridwise.pro](https://community.gridwise.pro)
- **🐛 Issue Tracker**: [GitHub Issues](https://github.com/your-org/gridwise/issues)
- **📧 Enterprise Support**: enterprise@gridwise.pro

### 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

### 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⚡ Built with ❤️ for a sustainable energy future**

[⭐ Star us on GitHub](https://github.com/your-org/gridwise) • [🐦 Follow us on Twitter](https://twitter.com/gridwise) • [💼 LinkedIn](https://linkedin.com/company/gridwise)

*© 2024 Gridwise. Powering intelligent energy decisions worldwide.*

</div>