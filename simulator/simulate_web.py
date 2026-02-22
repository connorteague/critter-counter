#!/usr/bin/env python3
"""
Visual Cattle Movement Simulator (Flask Web App)

Interactive web-based simulation for testing the critter-counter system.
Click buttons to simulate different cattle movement scenarios.

Usage:
    python3 simulate_web.py
    Then open http://localhost:5000 in your browser
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
from pathlib import Path
import sys
import threading
import time

# Add src to path (go up to project root, then into src)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hardware.mocks import MockMotionSensor, MockRFIDReader, RFIDReading
from direction_detector import DirectionDetector, Direction
from count_manager import CountManager
from data_logger import DataLogger

app = Flask(__name__)

# Global simulation state
class SimulationState:
    def __init__(self):
        # Initialize student's stub classes
        self.direction_detector = DirectionDetector()
        self.count_manager = CountManager()
        self.counts_logger = DataLogger()

        # Initialize mock hardware with logging callbacks
        self.motion_sensor = MockMotionSensor(pin=17, log_callback=self.hardware_log)
        self.rfid_reader = MockRFIDReader(power_pin=22, log_callback=self.hardware_log)

        self.events = []
        self.is_scanning = False
        self.lock = threading.Lock()

    def hardware_log(self, device_id: str, message: str, level: str = "INFO"):
        """Callback for hardware device logging."""
        # Determine event type based on device
        if device_id.startswith("PIR"):
            event_type = "pir"
        elif device_id.startswith("RFID"):
            event_type = "rfid"
        else:
            event_type = "system"

        self.add_event(event_type, f"{device_id} | {message}", level)

    def add_event(self, event_type, message, level="INFO"):
        """Add event to log."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        with self.lock:
            self.events.append({
                "timestamp": timestamp,
                "type": event_type,
                "message": message,
                "level": level
            })
            # Keep only last 50 events
            if len(self.events) > 50:
                self.events = self.events[-50:]

    def reset(self):
        """Reset all counters."""
        with self.lock:
            self.events = []
            self.direction_detector.clear_all()
            self.count_manager.manual_reset()
            self.rfid_reader.power_off()
            self.is_scanning = False

state = SimulationState()


def process_motion_event(tag_sequences, scenario_name):
    """Process a complete motion event with tag readings."""
    state.is_scanning = True
    state.add_event("scenario", f"SCENARIO | Starting: {scenario_name}", "SCENARIO")

    # Motion detected - hardware mock logs this
    motion_start = datetime.now()
    state.motion_sensor.trigger_motion(duration=10.0)

    # Power on RFID - hardware mock logs this
    state.rfid_reader.power_on()

    # Warm-up delay
    time.sleep(1.0)
    state.add_event("rfid", "RFID-22 | Ready to scan", "RFID")

    # Combine all tag sequences
    all_readings = []

    # Scan while motion active
    scan_count = 0
    max_scans = sum(len(seq) for seq in tag_sequences.values()) + 2

    # Set up reading sequence
    combined_sequence = []
    for tag_id, sequence in tag_sequences.items():
        combined_sequence.extend(sequence)

    state.rfid_reader.set_tag_sequence(combined_sequence)

    # Clear detector for new event
    state.direction_detector.clear_all()

    while (state.motion_sensor.is_motion_detected() or scan_count < len(combined_sequence)) and scan_count < max_scans:
        readings = state.rfid_reader.scan(duration=0.5)

        for r in readings:
            # Hardware mock already logged the tag detection
            all_readings.append(r)
            # Add reading to direction detector (student's stub)
            state.direction_detector.add_reading(r.tag_id, r.rssi, r.timestamp)

        scan_count += 1
        time.sleep(0.5)

    # Motion ended
    time.sleep(0.5)
    motion_end = datetime.now()
    # Note: Motion sensor will log motion ended when is_motion_detected() returns False

    # Power off RFID - hardware mock logs this
    state.rfid_reader.power_off()

    # Process readings using student's stub classes
    process_readings(all_readings, motion_start, motion_end)

    state.is_scanning = False
    state.add_event("result", f"RESULT | Scenario complete: {scenario_name}", "RESULT")


def process_readings(readings, motion_start, motion_end):
    """Process RFID readings using student's stub classes."""
    if not readings:
        state.add_event("result", "RESULT | No tags detected", "RESULT")
        return

    # Group by tag
    by_tag = {}
    for r in readings:
        if r.tag_id not in by_tag:
            by_tag[r.tag_id] = []
        by_tag[r.tag_id].append(r)

    state.add_event("result", f"RESULT | Processing {len(by_tag)} unique tags", "RESULT")

    # Analyze each tag using student's stub classes
    for tag_id in by_tag.keys():
        # Use student's DirectionDetector (stub will return UNKNOWN until implemented)
        direction = state.direction_detector.detect_direction(tag_id)

        # Get RSSI delta for display (even if student hasn't implemented yet)
        tag_readings = by_tag[tag_id]
        if len(tag_readings) >= 2:
            delta = tag_readings[-1].rssi - tag_readings[0].rssi
        else:
            delta = 0.0

        # Update counts using student's CountManager (stub does nothing until implemented)
        if direction == Direction.ENTRY:
            state.count_manager.add_entry(count=1, tag_id=tag_id)
            direction_str = "ENTRY"
        elif direction == Direction.EXIT:
            state.count_manager.add_exit(count=1, tag_id=tag_id)
            direction_str = "EXIT"
        else:
            # For UNKNOWN, still track occurrence
            state.count_manager.add_entry(count=0, tag_id=tag_id)  # Increment occurrence only
            direction_str = "UNKNOWN"

        # Get occurrence count (stub returns 0 until implemented)
        occurrence = state.count_manager.get_tag_occurrence_count(tag_id)

        # Log using student's DataLogger (stub does nothing until implemented)
        avg_rssi = sum(r.rssi for r in tag_readings) / len(tag_readings)
        state.data_logger.log_tag_detection(
            tag_id=tag_id,
            direction=direction_str,
            rssi=avg_rssi,
            occurrence_count=occurrence,
            motion_start=motion_start,
            motion_end=motion_end
        )

        state.add_event(
            "result",
            f"RESULT | Tag {tag_id[:16]}... - Direction: {direction_str}, RSSI Δ: {delta:.1f} dBm, Occurrence: {occurrence}",
            "RESULT"
        )


@app.route('/')
def index():
    """Serve the main simulation page."""
    return render_template('simulation.html')


@app.route('/api/status')
def get_status():
    """Get current simulation status."""
    with state.lock:
        # Get counts from student's CountManager (stub returns defaults until implemented)
        count_data = state.count_manager.data
        tag_occurrences = state.count_manager.get_all_tag_occurrences()

        return jsonify({
            "motion_detected": state.motion_sensor.is_motion_detected(),
            "rfid_powered": state.rfid_reader.is_powered(),
            "is_scanning": state.is_scanning,
            "daily_entry": count_data.daily_entry,
            "daily_exit": count_data.daily_exit,
            "net_count": count_data.net_count,
            "tag_occurrences": tag_occurrences,
            "events": state.events[-20:]  # Last 20 events
        })


@app.route('/api/simulate/entry', methods=['POST'])
def simulate_entry():
    """Simulate a cow entering."""
    if state.is_scanning:
        return jsonify({"error": "Simulation already running"}), 400

    tag_id = "E200001111111111"
    sequence = state.rfid_reader.generate_approaching_sequence(tag_id, num_samples=5)

    threading.Thread(
        target=process_motion_event,
        args=({tag_id: sequence}, "Single Cow Entering")
    ).start()

    return jsonify({"status": "started"})


@app.route('/api/simulate/exit', methods=['POST'])
def simulate_exit():
    """Simulate a cow exiting."""
    if state.is_scanning:
        return jsonify({"error": "Simulation already running"}), 400

    tag_id = "E200002222222222"
    sequence = state.rfid_reader.generate_departing_sequence(tag_id, num_samples=5)

    threading.Thread(
        target=process_motion_event,
        args=({tag_id: sequence}, "Single Cow Exiting")
    ).start()

    return jsonify({"status": "started"})


@app.route('/api/simulate/multiple', methods=['POST'])
def simulate_multiple():
    """Simulate multiple cows entering."""
    if state.is_scanning:
        return jsonify({"error": "Simulation already running"}), 400

    sequences = {
        "E200001111111111": state.rfid_reader.generate_approaching_sequence("E200001111111111", 4),
        "E200002222222222": state.rfid_reader.generate_approaching_sequence("E200002222222222", 4),
        "E200003333333333": state.rfid_reader.generate_approaching_sequence("E200003333333333", 3),
    }

    threading.Thread(
        target=process_motion_event,
        args=(sequences, "Multiple Cattle Entering")
    ).start()

    return jsonify({"status": "started"})


@app.route('/api/simulate/false-alarm', methods=['POST'])
def simulate_false_alarm():
    """Simulate motion without tags."""
    if state.is_scanning:
        return jsonify({"error": "Simulation already running"}), 400

    threading.Thread(
        target=process_motion_event,
        args=({}, "False Alarm (No Tags)")
    ).start()

    return jsonify({"status": "started"})


@app.route('/api/reset', methods=['POST'])
def reset_simulation():
    """Reset all counters."""
    state.reset()
    state.add_event("system", "Simulation reset", "SYSTEM")
    return jsonify({"status": "reset"})


if __name__ == '__main__':
    print()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║      Cattle Movement Simulator - Visual Web Interface        ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()
    print("Starting server...")
    print()
    print("Open your browser to: http://localhost:5000")
    print()
    print("Press Ctrl+C to stop")
    print()

    app.run(debug=True, use_reloader=False)
