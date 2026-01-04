# Cattle Movement Simulation Guide

## Overview

The simulation system allows you to test your critter-counter implementation without needing physical hardware. It simulates realistic cattle movement patterns, PIR motion detection, and RFID tag readings with appropriate RSSI (signal strength) values.

## Quick Start

Run the simulation to see how the system should behave:

```bash
# Run all scenarios
python3 simulate.py

# Or use the Makefile
make simulate
```

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

## Understanding the Output

### Log Format

```
[HH:MM:SS.mmm] LEVEL | Message
```

- **SCENARIO**: Scenario description
- **PIR**: Motion sensor events
- **RFID**: RFID reader events and tag detections
- **RESULT**: Analysis and direction determination
- **EXPECTED**: What the correct output should be

### Example Output

```
[11:40:33.954] PIR   | PIR: Motion detected!
[11:40:33.954] RFID  | RFID: Powering on via MOSFET
[11:40:34.962] RFID  | RFID: Tag E200001111111111... detected, RSSI = -70.3 dBm
[11:40:35.467] RFID  | RFID: Tag E200001111111111... detected, RSSI = -64.6 dBm
[11:40:35.972] RFID  | RFID: Tag E200001111111111... detected, RSSI = -56.6 dBm
```

### RSSI Values Explained

RSSI (Received Signal Strength Indicator) is measured in dBm:
- **-45 dBm**: Strong signal (cattle very close)
- **-60 dBm**: Medium signal (cattle at moderate distance)
- **-70 dBm**: Weak signal (cattle far away)

**Direction Detection:**
- **RSSI increasing** (e.g., -70 → -50): Cattle approaching = **ENTRY**
- **RSSI decreasing** (e.g., -50 → -70): Cattle departing = **EXIT**

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

### Example: Testing Motion Sensor

```python
from src.hardware.mocks import MockMotionSensor
import time

motion = MockMotionSensor()

# Trigger 3-second motion event
motion.trigger_motion(duration=3.0)

assert motion.is_motion_detected() == True

time.sleep(3.5)

assert motion.is_motion_detected() == False
```

## Mock Hardware Classes

### MockMotionSensor

Simulates PIR motion sensor behavior.

**Methods:**
- `trigger_motion(duration)` - Start a motion event
- `is_motion_detected()` - Check if motion is currently active
- `wait_for_motion(timeout)` - Block until motion detected

### MockRFIDReader

Simulates UHF RFID reader with power control.

**Methods:**
- `power_on()` - Turn on reader
- `power_off()` - Turn off reader
- `is_powered()` - Check power status
- `scan(duration)` - Scan for tags
- `set_tag_sequence(sequence)` - Configure what tags to return
- `generate_approaching_sequence(tag_id, num_samples)` - Generate ENTRY pattern
- `generate_departing_sequence(tag_id, num_samples)` - Generate EXIT pattern

### RFIDReading

Dataclass representing a tag reading.

**Fields:**
- `tag_id: str` - EPC tag identifier (24-char hex)
- `rssi: float` - Signal strength in dBm
- `timestamp: datetime` - When reading was taken
- `antenna: Optional[int]` - Antenna number

## Testing Your Implementation

### Step 1: Test Individual Modules

Use mock hardware in your unit tests:

```bash
pytest tests/test_direction_detector.py -v
pytest tests/test_count_manager.py -v
pytest tests/test_data_logger.py -v
```

### Step 2: Test Integration

Once you've implemented `main.py`, test with the simulation:

```bash
python3 src/main.py --sim
```

Your implementation should:
1. Wait for motion
2. Power on RFID
3. Collect readings
4. Determine direction
5. Update counts
6. Log events
7. Power off RFID

### Step 3: Verify Against Scenarios

Run your implementation and verify:

- **Entry scenario**: Daily entry count increases by 1
- **Exit scenario**: Daily exit count increases by 1
- **Multiple cattle**: Each tag counted separately
- **False alarm**: No counts updated, motion logged

## Common Testing Patterns

### Pattern 1: Single Tag Detection

```python
def test_single_entry():
    rfid = MockRFIDReader()
    rfid.power_on()

    # Generate realistic approaching pattern
    sequence = rfid.generate_approaching_sequence("E200001111111111", 5)
    rfid.set_tag_sequence(sequence)

    # Your code here to process readings
    ...
```

### Pattern 2: Multiple Tags

```python
def test_multiple_tags():
    rfid = MockRFIDReader()
    rfid.power_on()

    # Interleave readings from multiple tags
    tag1 = rfid.generate_approaching_sequence("E200001111111111", 3)
    tag2 = rfid.generate_approaching_sequence("E200002222222222", 3)

    combined = []
    for i in range(3):
        combined.append(tag1[i])
        combined.append(tag2[i])

    rfid.set_tag_sequence(combined)

    # Process and verify each tag independently
    ...
```

### Pattern 3: Motion-Triggered Workflow

```python
def test_motion_workflow():
    motion = MockMotionSensor()
    rfid = MockRFIDReader()

    # Trigger motion
    motion.trigger_motion(duration=8.0)

    # Power on RFID
    rfid.power_on()

    # Scan while motion active
    all_readings = []
    while motion.is_motion_detected():
        readings = rfid.scan(duration=0.5)
        all_readings.extend(readings)
        time.sleep(0.5)

    # Process readings
    ...
```

## Customizing Scenarios

You can modify `simulate.py` to create custom scenarios:

```python
def simulate_custom_scenario(self):
    """Your custom scenario."""
    # Create your own tag sequences
    sequence = [
        ("E200001234567890", -70.0),
        ("E200001234567890", -65.0),
        ("E200001234567890", -60.0),
        # ... more readings
    ]

    # Trigger motion
    self.motion_sensor.trigger_motion(duration=10.0)

    # Set sequence and scan
    self.rfid_reader.power_on()
    self.rfid_reader.set_tag_sequence(sequence)
    # ... rest of your scenario
```

## Troubleshooting

### "No module named 'hardware'"

Make sure you're running from the project root:
```bash
cd /path/to/critter-counter
python3 simulate.py
```

### Tags Not Detected

Check that:
1. RFID reader is powered on (`rfid.power_on()`)
2. Tag sequence is set (`rfid.set_tag_sequence(...)`)
3. You're calling `scan()` to get readings

### Motion Not Detected

Check that:
1. Motion was triggered (`motion.trigger_motion(duration=...)`)
2. You're checking within the duration period
3. Motion hasn't expired

## Next Steps

1. **Run the simulation** to understand expected behavior
2. **Study the mock classes** in `src/hardware/mocks.py`
3. **Implement your modules** following the implementation guide
4. **Write tests** using the mock hardware
5. **Test integration** with `python3 src/main.py --sim`

## Resources

- [Implementation Guide](~/.claude/plans/deep-weaving-corbato.md) - Module specifications
- [Algorithm Notes](algorithm_notes.md) - RSSI direction detection
- [Test Fixtures](../tests/conftest.py) - Pre-configured test data
- [Mock Hardware](../src/hardware/mocks.py) - Full API documentation

---

**Questions?** The simulation demonstrates the expected system behavior. Use it as a reference while implementing!
