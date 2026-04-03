from machine import ADC, Pin
import time

# Hardware pins (adjust if needed)
sensor = ADC(0)
threshold = 600

# Relay pins on NodeMCU (change to your pins)
fan_relay = Pin(5, Pin.OUT)     # D1 (GPIO5)
buzzer_relay = Pin(4, Pin.OUT)  # D2 (GPIO4)

# Set this according to your relay module
RELAY_ACTIVE_LOW = True   # <<-- Most common. Set False if your module is active-HIGH.

# initial states (False = OFF)
fan_state = False
buzzer_state = False

# initialize relays to OFF
fan_relay.value(1 if RELAY_ACTIVE_LOW else 0)
buzzer_relay.value(1 if RELAY_ACTIVE_LOW else 0)

def set_relay(relay_pin, on):
    """Set relay_pin to ON/OFF, respecting active-low if present."""
    if RELAY_ACTIVE_LOW:
        relay_pin.value(0 if on else 1)
    else:
        relay_pin.value(1 if on else 0)

def wait_for_low():
    while sensor.read() > threshold:
        time.sleep(0.01)

def count_pulses(max_wait=1.0):
    count = 0
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < int(max_wait*1000):
        if sensor.read() > threshold:
            count += 1
            wait_for_low()
            time.sleep(0.05)
    return count

print("RX ready. Threshold:", threshold)

while True:
    if sensor.read() > threshold:
        pulses = count_pulses()
        if pulses == 1:
            fan_state = not fan_state
            set_relay(fan_relay, fan_state)
            print("Fan ON" if fan_state else "Fan OFF")
        elif pulses == 2:
            buzzer_state = not buzzer_state
            set_relay(buzzer_relay, buzzer_state)
            print("Buzzer ON" if buzzer_state else "Buzzer OFF")
        else:
            print("Unknown command, pulses:", pulses)
        time.sleep(0.2)
