# Cattle Movement Simulation Guide

## Overview

The simulation system allows you to test your critter-counter implementation without needing physical hardware. It simulates realistic cattle movement patterns, PIR motion detection, and RFID tag readings with appropriate RSSI (signal strength) values.

## Available Scenarios

### 1. Single Cow Entering (ENTRY)

Simulates one cow approaching and entering the kraal.

```bash
python3 simulate.py --scenario entry
# or
make simulate-entry
```

**Expected behavior:**
- PIR detects motion
- RFID powers on
- Tag readings show RSSI increasing (e.g., -70 → -60 → -50 dBm)
- Direction algorithm should detect: **ENTRY**
- Tag occurrence count should increment

### 2. Single Cow Exiting (EXIT)

Simulates one cow leaving the kraal.

```bash
python3 simulate.py --scenario exit
# or
make simulate-exit
```

**Expected behavior:**
- PIR detects motion
- RFID powers on
- Tag readings show RSSI decreasing (e.g., -45 → -60 → -70 dBm)
- Direction algorithm should detect: **EXIT**
- Tag occurrence count should increment

### 3. Multiple Cattle Entering

Simulates three cows passing through together.

```bash
python3 simulate.py --scenario multiple
# or
make simulate-multiple
```

**Expected behavior:**
- PIR detects motion
- RFID powers on
- Multiple different tags detected
- Each tag processed independently
- Three ENTRY detections
- Tag occurrence count increments for each unique tag

### 4. False Alarm (No Tags)

Simulates motion without any tagged cattle (e.g., person walking by).

```bash
python3 simulate.py --scenario false-alarm
```

**Expected behavior:**
- PIR detects motion
- RFID powers on
- No tags detected
- No count updates
- Motion events logged only

## Using Mock Hardware in Your Code

The simulation uses mock hardware classes from `src/hardware/mocks.py`. You can use these in your tests:

### Example: Testing Direction Detector

```python
from src.hardware.mocks import MockRFIDReader
from src.direction_detector import DirectionDetector

# Create mock reader
rfid = MockRFIDReader()
detector = DirectionDetector()

# Generate realistic approaching sequence
sequence = rfid.generate_approaching_sequence(
    tag_id="E200001234567890",
    num_samples=5,
    start_rssi=-70.0,
    end_rssi=-45.0
)

# Process readings
rfid.power_on()
rfid.set_tag_sequence(sequence)

for _ in range(5):
    readings = rfid.scan()
    for r in readings:
        detector.add_reading(r.tag_id, r.rssi, r.timestamp)

# Check direction
direction = detector.detect_direction("E200001234567890")
assert direction == Direction.ENTRY
```

For more details on mock hardware and testing patterns, refer to the `SIMULATOR_GUIDE.md`.
