# Li-fi-based-Appliances-Control-System
# 💡 Li-Fi Based Appliances Control System

<div align="center">

![Li-Fi](https://img.shields.io/badge/Communication-Li--Fi%20%7C%20OOK%20Modulation-yellow?style=for-the-badge&logo=lightbulb)
![Arduino](https://img.shields.io/badge/Transmitter-Arduino%20Uno-teal?style=for-the-badge&logo=arduino)
![NodeMCU](https://img.shields.io/badge/Receiver-NodeMCU%20ESP8266-blue?style=for-the-badge&logo=espressif)
![Python](https://img.shields.io/badge/Code-MicroPython-3776AB?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Wireless appliance control using visible light — no RF, no EMI, no spectrum congestion.**

[📖 Overview](#-overview) · [🔧 Hardware](#-hardware-setup) · [🚀 Getting Started](#-getting-started) · [📡 How It Works](#-how-it-works) · [📊 Performance](#-performance) · [🔮 Future Scope](#-future-scope)

</div>

---

## 📖 Overview

This project implements a **Li-Fi (Light Fidelity) based wireless control system** for toggling electrical appliances using **visible light communication** instead of traditional RF (Radio Frequency) signals.

Designed for **EMI-sensitive industrial environments** — such as automation plants, hospitals, and high-voltage installations — where RF-based communication (Wi-Fi, Bluetooth, Zigbee) is restricted or unsafe.

### ✅ What It Does

| Feature | Details |
|--------|---------|
| 📤 Transmitter | Arduino Uno encodes button commands via **On-Off Keying (OOK)** and flashes a 1W LED |
| 📥 Receiver | NodeMCU reads light pulses via a **5W solar panel** (used as photodetector) |
| ⚡ Control | Decodes OOK signal and toggles appliances (DC motor, buzzer) via **dual-channel relay** |
| 🚫 RF-Free | Zero electromagnetic radiation — safe for EMI-restricted zones |

---

## 🏗️ System Architecture

```
┌──────────────────────────────┐          ┌──────────────────────────────────┐
│        TX UNIT               │          │           RX UNIT                │
│  ┌─────────────┐             │          │  ┌──────────────────────┐        │
│  │ Push Button │             │   Light  │  │  5W Solar Panel      │        │
│  └──────┬──────┘             │  Pulses  │  │  (Photodetector)     │        │
│         │                   │  ~~~~~~> │  └──────────┬───────────┘        │
│  ┌──────▼──────┐             │          │             │                    │
│  │ Arduino Uno │ OOK Encode  │          │  ┌──────────▼───────────┐        │
│  └──────┬──────┘             │          │  │  NodeMCU (ESP8266)   │        │
│         │                   │          │  │  OOK Decode          │        │
│  ┌──────▼──────┐             │          │  └──────────┬───────────┘        │
│  │IRFZ44N MOSFET│            │          │             │                    │
│  └──────┬──────┘             │          │  ┌──────────▼───────────┐        │
│         │                   │          │  │  Dual Relay Module   │        │
│  ┌──────▼──────┐             │          │  └──────────┬───────────┘        │
│  │  1W LED     │ ════════════╪══════════╪═>  DC Motor │ Buzzer            │
│  └─────────────┘             │          └─────────────────────────────────┘
│   Power: 12V, 1A             │                 Power: 5V, 2A
└──────────────────────────────┘
```

---

## 🔧 Hardware Setup

### 📤 Transmitter Components

| Component | Specification | Purpose |
|-----------|--------------|---------|
| Arduino Uno | ATmega328P | OOK encoding + button input |
| 1W LED | High-power white LED | Light signal transmission |
| IRFZ44N MOSFET | N-channel, logic-level | High-speed LED switching |
| Push Buttons | 2x momentary | Load 1 & Load 2 toggle commands |
| Power Supply | 12V, 1A | Transmitter power |

### 📥 Receiver Components

| Component | Specification | Purpose |
|-----------|--------------|---------|
| NodeMCU | ESP8266 (3.3V logic) | OOK decoding + relay control |
| Solar Panel | 5W (as photodetector) | Converts light pulses to voltage |
| Dual Relay Module | 5V trigger | Switches AC/DC loads |
| DC Motor | 5V | Controlled load (Fan simulation) |
| Passive Buzzer | 5V | Controlled load (Alert simulation) |
| Power Supply | 5V, 2A | Receiver + loads power |

### 🔌 Wiring Reference

**Transmitter (TX.ino — Arduino Uno):**
```
Arduino Pin 2  → Push Button 1 (Load 1 toggle)
Arduino Pin 3  → Push Button 2 (Load 2 toggle)
Arduino Pin 9  → IRFZ44N Gate (MOSFET)
IRFZ44N Drain  → LED Cathode (-)
LED Anode (+)  → 12V via current-limiting resistor
GND            → Common ground
```

**Receiver (RX.py — NodeMCU):**
```
Solar Panel (+) → NodeMCU A0 (Analog input)
Solar Panel (-) → GND
NodeMCU D1     → Relay IN1 (Buzzer control)
NodeMCU D2     → Relay IN2 (Fan/Motor control)
Relay VCC      → 5V
Relay GND      → GND
```

---

## 🚀 Getting Started

### Prerequisites

**Software Required:**
- [Arduino IDE](https://www.arduino.cc/en/software) (v1.8+) — for TX firmware
- [Thonny IDE](https://thonny.org/) — for NodeMCU MicroPython
- MicroPython firmware flashed on NodeMCU

### Step 1 — Flash MicroPython on NodeMCU

```bash
# Install esptool
pip install esptool

# Erase existing firmware
esptool.py --port COM_PORT erase_flash

# Flash MicroPython (download from micropython.org)
esptool.py --port COM_PORT --baud 460800 write_flash --flash_size=detect 0 esp8266-20231005-v1.21.0.bin
```

### Step 2 — Upload Transmitter Code (TX.ino)

1. Open **Arduino IDE**
2. Open `TX.ino` from this repository
3. Select **Board**: `Arduino Uno`
4. Select correct **COM Port**
5. Click **Upload ▶**

### Step 3 — Upload Receiver Code (RX.py)

1. Open **Thonny IDE**
2. Set interpreter to **MicroPython (ESP8266)**
3. Open `RX.py` from this repository
4. Click **Run ▶** or save as `main.py` on NodeMCU for auto-start

### Step 4 — Test the System

1. Power TX unit (12V) and RX unit (5V)
2. Align LED (TX) directly facing the Solar Panel (RX) — ~5 to 10 cm
3. Press **Button 1** → Buzzer toggles ON/OFF
4. Press **Button 2** → DC Motor (Fan) toggles ON/OFF
5. Monitor serial output in Thonny:

```
Buzzer ON
Buzzer OFF
Fan ON
Fan OFF
```

---

## 📡 How It Works

### On-Off Keying (OOK) Modulation

OOK is the simplest form of Amplitude Shift Keying (ASK) — the LED is switched ON/OFF at a specific frequency to encode binary data:

```
LED State:   ─────╮   ╭──╮   ╭───────────────
                  │   │  │   │
              0   1   0  1   1  1  1  1  ← Binary stream
                                           (Command encoding)
```

### Command Encoding Flow

```
[Button Press]
     │
     ▼
Arduino generates unique OOK pulse pattern
     │
     ▼
MOSFET switches 1W LED at high speed
     │
     ▼ (visible light pulses)
Solar panel converts light → analog voltage
     │
     ▼
NodeMCU reads A0, decodes pulse pattern
     │
     ▼
Relay triggered → Load toggled (ON/OFF)
```

---

## 📊 Performance

| Parameter | Value |
|-----------|-------|
| Transmission Range | ~10 cm (prototype) |
| Modulation Type | On-Off Keying (OOK) |
| Communication Mode | Line-of-sight (LoS) |
| Response Time | Real-time |
| RF Emissions | Zero |
| Power (TX) | 12V, 1A |
| Power (RX) | 5V, 2A |

### ⚠️ Known Limitations

- **Short range** — Solar panel has slower response than dedicated photodiodes
- **Line-of-sight required** — Cannot transmit through obstacles
- **Ambient light sensitivity** — Bright sunlight or fluorescent lights may cause false reads
- **Low data rate** — Suitable for control commands only, not data streaming

---

## 🔮 Future Scope

These are practical upgrades to take this prototype to a production-ready system:

| Upgrade | Implementation | Benefit |
|---------|---------------|---------|
| 🔬 BPW34 Photodiode | Replace solar panel with BPW34 | 10–100× faster detection, longer range |
| 📏 Extended Range | Collimated LED + optical lens | Range increase to 1–5 meters |
| 🔁 Manchester Encoding | Implement in firmware | Error-resistant, self-clocking signal |
| 🛡️ CRC Error Detection | Add CRC-8 to command packets | Reliable operation in noisy environments |
| 🔢 Multi-Channel | Frequency-division multiplexing | Control 8+ loads independently |
| 📱 OLED Display | Add SSD1306 to RX unit | Real-time load status display |
| 🌐 MQTT Integration | NodeMCU WiFi + MQTT broker | Remote monitoring via dashboard |
| 🏭 PLC Replacement | RS485 + Li-Fi hybrid | Industrial-grade automation |

---

## 📁 Repository Structure

```
Li-Fi-Appliance-Control/
│
├── TX.ino           # Arduino Uno transmitter firmware (OOK encoding)
├── RX.py            # NodeMCU MicroPython receiver code (OOK decoding + relay)
├── README.md        # This file
└── docs/
    └── Project_Report.pdf   # Full project report with circuit diagrams
```

---

## 🧰 Software Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| Arduino IDE | 1.8+ | TX firmware development |
| Thonny IDE | 4.x | NodeMCU MicroPython development |
| MicroPython | 1.21+ | ESP8266 firmware |

---

## 🎯 Use Cases

- 🏥 **Hospitals** — RF-free zones near MRI/CT equipment
- 🏭 **Automation Plants** — EMI-sensitive industrial floors
- ⚡ **High-Voltage Installations** — Safe wireless control without RF interference
- 🔬 **Research Labs** — Controlled environments needing interference-free communication
- 🏠 **Smart Home Prototypes** — Educational IoT + optical communication experiments

---

## 📜 License

This project is licensed under the **MIT License** — free to use, modify, and distribute with attribution.

---

## 🙌 Acknowledgements

- Li-Fi concept inspired by Prof. Harald Haas (University of Edinburgh)
- MicroPython community for NodeMCU support libraries
- Arduino open-source ecosystem

---

<div align="center">

**Built with 💡 light — not radio waves.**

If this project helped you, please ⭐ star the repository!

</div>
<br>
Author - Anand Kumar Bharti
