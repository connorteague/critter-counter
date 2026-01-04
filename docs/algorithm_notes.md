# Critter Counter Algorithm Documentation

## Direction Detection Algorithm

### Problem Statement
We need to determine whether cattle are **entering** or **exiting** the kraal based on RFID tag readings.

### Approach: RSSI Trend Analysis

**RSSI** (Received Signal Strength Indicator) is a measurement of RF signal power in dBm. More negative values indicate weaker signals (farther distance).

#### Theory
- **Approaching cattle (ENTRY):** RSSI increases over time (becomes less negative)
  - Example: -70 dBm → -60 dBm → -50 dBm
- **Departing cattle (EXIT):** RSSI decreases over time (becomes more negative)
  - Example: -50 dBm → -60 dBm → -70 dBm

#### Algorithm Steps

1. **Collect Samples:** Take N RFID readings over time (typically N=3-5)
2. **Calculate Trend:** Compare first and last RSSI values
3. **Determine Direction:**
   - If `RSSI_last - RSSI_first > threshold`: ENTRY
   - If `RSSI_last - RSSI_first < -threshold`: EXIT
   - If change is too small: UNKNOWN (cattle might be stationary)

#### Pseudocode
```python
def detect_direction(readings):
    if len(readings) < MIN_SAMPLES:
        return UNKNOWN
    
    rssi_delta = readings[-1].rssi - readings[0].rssi
    
    if abs(rssi_delta) < THRESHOLD:
        return UNKNOWN  # Not moving significantly
    
    if rssi_delta > 0:
        return ENTRY  # Signal getting stronger
    else:
        return EXIT   # Signal getting weaker
```

#### Tunable Parameters
- `MIN_SAMPLES`: Minimum readings needed (default: 3)
- `RSSI_DELTA_THRESHOLD`: Minimum change in dBm to be confident (default: 5.0)
- `SAMPLE_INTERVAL`: Time between readings (default: 0.5 seconds)

### Alternative: Dual-Zone Detection

If hardware supports two antennas, we can use spatial sequencing:

- **Antenna A** (outside kraal) + **Antenna B** (inside kraal)
- **A → B sequence** = ENTRY
- **B → A sequence** = EXIT

This is more reliable but requires additional hardware.

---

## Count Persistence Strategy

### Why Persistence Matters
The system must survive:
- Power cycles
- Software crashes
- Battery failures

### Storage Format: JSON

```json
{
  "daily_entry": 45,
  "daily_exit": 43,
  "net_count": 2,
  "last_reset": "2025-01-01T00:00:00",
  "total_events": 88
}
```

### Write Strategy
- **Synchronous writes:** Write to disk immediately after each count change
- **Atomic writes:** Write to temp file, then rename (prevents corruption)

### Daily Reset Logic
```python
if current_date > last_reset_date:
    if current_time >= DAILY_RESET_HOUR:
        reset_daily_counts()
        # Note: net_count persists across daily resets
```

---

## Display Update Strategy

### Goal: Minimize Power Consumption

E-ink displays consume power during updates but are zero-power when static.

### Update Triggers
Update display ONLY when:
1. Counts change (entry or exit detected)
2. Battery level changes significantly (>5%)
3. Status message needs to be shown
4. Full refresh interval reached (24 hours to prevent ghosting)

### Update Types
- **Partial update:** Only update changed numbers (~2 seconds, low power)
- **Full refresh:** Complete screen refresh (~5 seconds, higher power)

Use partial updates for count changes, full refresh once daily.

---

## Power Budget Calculations

### Assumptions (to be measured)
- Deep sleep: 50 µA
- PIR sensor: 50 µA
- RFID scan: 500 mA for 3 seconds
- Display update: 200 mA for 2 seconds
- Processing: 100 mA for 1 second

### Example Daily Consumption
For 100 cattle passages per day:

| Activity | Power | Duration | Energy |
|----------|-------|----------|--------|
| Sleep (24h) | 100 µA | 86,400s | 8.6 mAh |
| 100 RFID scans | 500 mA | 300s | 41.7 mAh |
| 100 display updates | 200 mA | 200s | 11.1 mAh |
| Processing | 100 mA | 100s | 2.8 mAh |
| **TOTAL** | | | **64.2 mAh/day** |

With a 5000 mAh battery: **78 days autonomy** (unrealistic - solar should recharge daily)

---

## Error Handling Philosophy

### Graceful Degradation
1. **Cannot determine direction?** Log event but don't update counts
2. **Display update fails?** Continue counting, retry on next change
3. **Storage write fails?** Keep counts in memory, retry periodically
4. **Battery critical?** Reduce scan frequency, disable non-essential features

### Never Lose Data
- Counts must persist even if display or logging fails
- Use watchdog timer to recover from hangs
- Log errors for later debugging

---

## Future Enhancements

### Ideas for v3.0
1. **Cattle identification:** Link tag IDs to farmer's records (color/markings)
2. **Time-of-day analysis:** Track entry/exit patterns
3. **Alert system:** Notify farmer if expected count not met
4. **Cloud sync:** Upload data when cellular available
5. **Multi-gate support:** Track cattle across multiple kraals

### Algorithm Improvements
1. **Kalman filtering:** Smooth noisy RSSI data
2. **Machine learning:** Train classifier on real passage data
3. **Height detection:** Use antenna pattern to ignore small animals
4. **Speed estimation:** Calculate passage speed from RSSI curve

---

## Testing Strategy

### Unit Tests
Test each algorithm component independently with synthetic data.

### Integration Tests
Simulate complete cattle passages with realistic RFID data.

### Field Tests
Deploy prototype and compare against manual counts.

### Acceptance Criteria
- Direction detection accuracy > 90%
- Zero data loss in 48-hour test
- System recovers from power cycle
- Battery lasts 3+ days without sun

---

## References

- EPC Gen2 UHF RFID Protocol Specification
- RSSI-based localization research papers
- Livestock tracking best practices
