# Quick Start Guide - Visual Simulation

## Get Started in 3 Steps

### Step 1: Install Flask

```bash
pip install Flask
```

### Step 2: Run the Simulation

```bash
make simulate
```

Or manually:
```bash
python3 simulator/simulate_web.py
```

### Step 3: Open Your Browser

Navigate to: **http://localhost:5000**

---

## What You'll See

A beautiful web interface with:

### Scenario Buttons (Left Panel)
Click these to simulate different cattle movements:
- **→ Single Cow Entering** - Test ENTRY detection
- **← Single Cow Exiting** - Test EXIT detection
- **⇉ Multiple Cattle (3)** - Test multi-tag handling
- **⚠ False Alarm** - Test motion without tags
- **↺ Reset Counters** - Clear all data

### System Status (Center Panel)
Real-time indicators showing:
- **PIR Motion Sensor** - Green = motion detected
- **RFID Reader** - Green = powered on
- **Scanning** - Green = actively scanning

### Daily Counts (Right Panel)
Live count updates:
- **Entries** - Number of cattle that entered
- **Exits** - Number of cattle that left
- **Net Count** - Current cattle in kraal (entries - exits)

### Event Log (Bottom Full Width)
Detailed timeline showing:
- When motion was detected
- When RFID powered on/off
- Each tag detection with RSSI value
- Direction determination results

### Tag Occurrences (Right Panel)
List of all detected tags with:
- Tag ID (truncated for display)
- Count of how many times detected

---

## Try These Tests

### Test 1: Single Entry

1. Click "→ Single Cow Entering"
2. Watch the event log populate
3. See RSSI values increase: -70 → -60 → -50 dBm
4. Verify result shows: "Direction: ENTRY"
5. Check Daily Counts: Entry = 1, Net Count = 1

### Test 2: Single Exit

1. Click "← Single Cow Exiting"
2. Watch RSSI values decrease: -45 → -60 → -70 dBm
3. Verify result shows: "Direction: EXIT"
4. Check Daily Counts: Exit = 1, Net Count = 0

### Test 3: Multiple Cattle

1. Click "⇉ Multiple Cattle (3)"
2. Watch 3 different tag IDs appear
3. See each processed independently
4. Check Tag Occurrences shows 3 tags
5. Verify Daily Counts: Entry = 3

### Test 4: False Alarm

1. Click "⚠ False Alarm"
2. See motion detected and RFID powered on
3. Note: No tags detected
4. Verify counts don't change

---

## Understanding RSSI

**RSSI** (Received Signal Strength Indicator) measures signal power in dBm:

- **-45 dBm** = Very strong (cattle very close) ████████
- **-50 dBm** = Strong (cattle close) ██████
- **-60 dBm** = Medium (cattle moderate distance) ████
- **-70 dBm** = Weak (cattle far away) ██
- **-80 dBm** = Very weak (barely detectable) ▌

**Direction Detection:**
- RSSI **increasing** (e.g., -70 → -50) = Cattle **approaching** = **ENTRY**
- RSSI **decreasing** (e.g., -50 → -70) = Cattle **departing** = **EXIT**

---

## Expected Behavior

### When You Click "Single Cow Entering":

```
[11:45:23.123] SCENARIO | Starting: Single Cow Entering
[11:45:23.124] PIR-17   | Motion detected! (duration: 10.0s)
[11:45:23.125] RFID-22  | Powered ON (GPIO 22)
[11:45:24.130] RFID-22  | Ready to scan
[11:45:24.132] RFID-22  | Tag detected: E200001111111111 @ -70.3 dBm
[11:45:24.637] RFID-22  | Tag detected: E200001111111111 @ -64.6 dBm
[11:45:25.142] RFID-22  | Tag detected: E200001111111111 @ -56.6 dBm
[11:45:25.647] RFID-22  | Tag detected: E200001111111111 @ -49.3 dBm
[11:45:26.152] RFID-22  | Tag detected: E200001111111111 @ -45.3 dBm
[11:45:27.165] PIR-17   | Motion ended (timeout)
[11:45:27.166] RFID-22  | Powered OFF (GPIO 22)
[11:45:27.167] RESULT   | Processing 1 unique tags
[11:45:27.168] RESULT   | Tag E200001111111111 - Direction: UNKNOWN, RSSI Δ: 25.1 dBm, Occurrence: 0
[11:45:27.169] RESULT   | Scenario complete: Single Cow Entering
```

**Note:** Until you implement the student modules, direction will show "UNKNOWN" and occurrence will show "0". This is expected behavior with the stub classes!

**Counts Update (after student implements CountManager):**
- Daily Entry: 0 → 1
- Net Count: 0 → 1
- Tag E200001111111111 occurrence: 1

**Current behavior with stubs:** Counts remain at 0 until you implement the count_manager.py module.

---

## Next Steps

1. **Play with the simulation** - Click all the buttons!
2. **Study the mock hardware** - See [src/hardware/mocks.py](src/hardware/mocks.py)
3. **Read the implementation guide** - See `~/.claude/plans/deep-weaving-corbato.md`
4. **Implement your modules** - Follow the specifications
5. **Use mock classes in tests** - Import from `hardware.mocks`
6. **Test your implementation** - Integrate with `main.py --sim`

---

## Troubleshooting

**"Address already in use"**
```bash
# Another process is using port 5000, try:
python3 simulator/simulate_web.py
# Then check what port it says (might auto-pick a different one)
```

**"Module not found: Flask"**
```bash
# Install Flask first:
pip install Flask
```

**"Module not found: hardware"**
```bash
# Make sure you're in the project root directory:
cd /path/to/critter-counter
python3 simulator/simulate_web.py
```

**Page not loading**
- Make sure the server is running (check terminal)
- Try http://127.0.0.1:5000 instead of localhost
- Check firewall settings

---

## Tips

- **Watch the status indicators** - They animate when active!
- **Scroll the event log** - It auto-scrolls to show latest events
- **Click Reset** - Clears everything for a fresh start
- **Run multiple scenarios** - Tag occurrences accumulate
- **Check the terminal** - Server logs show what's happening

---

## For Development

The simulation shows you the **expected behavior** of your implementation:

- How motion triggers RFID power
- How RSSI values change over time
- How direction is determined
- How counts are updated
- How tag occurrences are tracked

Use this as your reference when implementing the actual system!

---

**Ready?** Run `make simulate` and start testing! 🎮
