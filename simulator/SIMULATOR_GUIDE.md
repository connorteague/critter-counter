# Simulator Guide

Both simulators now use **stub classes** that students will implement, demonstrating the complete workflow while showing device-specific hardware logging.

## Quick Start

### Visual Web Simulator
```bash
make simulate
# Open http://localhost:5000
# Click scenario buttons
```

### CLI Terminal Simulator
```bash
python3 simulate.py --scenario entry
```

## What You'll See

### Before Student Implementation (Current State)

Both simulators will show:

**Hardware Logging (Working):**
```
[PIR-17]   | Motion detected! (duration: 10.0s)
[RFID-22]  | Powered ON (GPIO 22)
[RFID-22]  | Tag detected: E200001111111111... @ -70.3 dBm
[RFID-22]  | Tag detected: E200001111111111... @ -60.5 dBm
[RFID-22]  | Tag detected: E200001111111111... @ -50.1 dBm
[PIR-17]   | Motion ended (timeout)
[RFID-22]  | Powered OFF (GPIO 22)
```

**Analysis (Using Stubs):**
```
Direction: UNKNOWN (from student's DirectionDetector)
Occurrence: 0 (from student's CountManager)
Daily Entries: 0
Daily Exits: 0
Net Count: 0
```

**Expected:**
```
Expected direction: ENTRY
```

### After Student Implementation

Once you implement the stub classes, the same simulation will show:

**Hardware Logging (Same):**
```
[PIR-17]   | Motion detected! (duration: 10.0s)
[RFID-22]  | Powered ON (GPIO 22)
[RFID-22]  | Tag detected: E200001111111111... @ -70.3 dBm
[RFID-22]  | Tag detected: E200001111111111... @ -60.5 dBm
[RFID-22]  | Tag detected: E200001111111111... @ -50.1 dBm
[PIR-17]   | Motion ended (timeout)
[RFID-22]  | Powered OFF (GPIO 22)
```

**Analysis (Using Your Implementation):**
```
Direction: ENTRY (from student's DirectionDetector) ✓
Occurrence: 1 (from student's CountManager) ✓
Daily Entries: 1 ✓
Daily Exits: 0
Net Count: 1 ✓
```

## Key Features

### Device-Specific Logging

Every log message shows which hardware component generated it:
- `PIR-17` = Motion sensor on GPIO pin 17
- `RFID-22` = RFID reader powered via MOSFET on GPIO pin 22

This makes it easy to:
- Understand hardware state transitions
- Debug timing issues
- See the complete event flow

### Stub Class Integration

Both simulators:
1. **Instantiate your stub classes:**
   ```python
   direction_detector = DirectionDetector()
   count_manager = CountManager()
   data_logger = DataLogger()
   ```

2. **Call your methods:**
   ```python
   # Add readings
   direction_detector.add_reading(tag_id, rssi, timestamp)

   # Detect direction
   direction = direction_detector.detect_direction(tag_id)

   # Update counts
   count_manager.add_entry(count=1, tag_id=tag_id)
   occurrence = count_manager.get_tag_occurrence_count(tag_id)

   # Log events
   data_logger.log_tag_detection(tag_id, direction, rssi, ...)
   ```

3. **Display results:**
   - Shows what your stubs return (currently defaults)
   - Shows what's expected
   - Updates in real-time as you implement

## Comparison: Web vs CLI

| Feature | Web Simulator | CLI Simulator |
|---------|---------------|---------------|
| **Interface** | Browser at localhost:5000 | Terminal output |
| **Interaction** | Click buttons | Command line args |
| **Event Log** | Color-coded, scrollable | Timestamped text |
| **Status** | Visual indicators | Text descriptions |
| **Best For** | Visual learners, demos | Terminal users, debugging |
| **Real-time** | Auto-updates every 500ms | Runs once per scenario |
| **Counts Display** | Live dashboard | Text summary |

## Scenarios

Both simulators support:

1. **Single Cow Entering** - RSSI increasing (-70 → -45 dBm)
2. **Single Cow Exiting** - RSSI decreasing (-45 → -70 dBm)
3. **Multiple Cattle (3)** - Interleaved tag readings
4. **False Alarm** - Motion but no tags

## Testing Flow

1. **Run simulator** → See stub behavior (UNKNOWN, zeros)
2. **Implement DirectionDetector** → Direction changes to ENTRY/EXIT
3. **Implement CountManager** → Counts and occurrences update
4. **Implement DataLogger** → Events saved to CSV
5. **Verify** → All values match expected behavior

## File References

- **Web Simulator:** [simulate_web.py](simulate_web.py)
- **CLI Simulator:** [simulate.py](simulate.py)
- **Mock Hardware:** [src/hardware/mocks.py](src/hardware/mocks.py)
- **Stub Classes:**
  - [src/direction_detector.py](src/direction_detector.py)
  - [src/count_manager.py](src/count_manager.py)
  - [src/data_logger.py](src/data_logger.py)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
- **Implementation Guide:** ~/.claude/plans/deep-weaving-corbato.md

## Troubleshooting

**Imports fail:**
```bash
# Make sure you're in the project root
cd /path/to/critter-counter
python3 simulate.py
```

**Web simulator port in use:**
```bash
# Try a different port
python3 simulate_web.py
# Flask will auto-detect and suggest alternative
```

**No device logging visible:**
- Check that you're using the updated mock hardware
- Verify log callbacks are passed to constructors
- Look for `device_id | message` format

**Stub methods not being called:**
- Check imports in simulator files
- Verify stub classes are instantiated
- Look for "from student's DirectionDetector" messages

## Summary

Both simulators are **test harnesses** that:
- ✓ Provide working mock hardware with device-specific logging
- ✓ Call your stub classes to demonstrate the API
- ✓ Show current stub behavior vs expected behavior
- ✓ Update in real-time as you implement
- ✓ Help you learn by doing

Start with the web simulator for visual feedback, then use the CLI simulator for detailed debugging!
