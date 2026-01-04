#!/usr/bin/env python3
"""
Cattle Movement Simulator

Simulates realistic cattle movement scenarios for testing the critter-counter system.
Run this to see how the system would behave with different cattle patterns.

Usage:
    python simulate.py                    # Interactive mode
    python simulate.py --scenario entry   # Run specific scenario
    python simulate.py --help             # Show all options
"""

import argparse
import time
import sys
from datetime import datetime
from pathlib import Path

# Add src to path (go up to project root, then into src)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hardware.mocks import MockMotionSensor, MockRFIDReader
from direction_detector import DirectionDetector, Direction
from count_manager import CountManager
from data_logger import DataLogger


class CattleSimulator:
    """Simulates cattle movement through the detection gate using student's stub classes."""

    def __init__(self, verbose: bool = True):
        """
        Initialize simulator.

        Args:
            verbose: Print detailed output
        """
        self.verbose = verbose

        # Initialize student's stub classes
        self.direction_detector = DirectionDetector()
        self.count_manager = CountManager()
        self.data_logger = DataLogger()

        # Initialize mock hardware with logging callbacks
        self.motion_sensor = MockMotionSensor(pin=17, log_callback=self.hardware_log)
        self.rfid_reader = MockRFIDReader(power_pin=22, log_callback=self.hardware_log)

    def hardware_log(self, device_id: str, message: str, level: str = "INFO"):
        """Callback for hardware device logging."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] {device_id:8s} | {message}")

    def log(self, message: str, level: str = "INFO"):
        """Print log message if verbose."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] {level:8s} | {message}")

    def simulate_single_entry(self):
        """Simulate a single cow entering the kraal."""
        self.log("=== Scenario: Single Cow Entering ===", "SCENARIO")
        self.log("A cow with tag E200001111111111 approaches the gate", "SCENARIO")

        # Generate approaching RSSI pattern
        tag_id = "E200001111111111"
        sequence = self.rfid_reader.generate_approaching_sequence(
            tag_id=tag_id,
            num_samples=5,
            start_rssi=-70.0,
            end_rssi=-45.0
        )

        self.log(f"Generated {len(sequence)} RSSI readings (signal strengthening)", "SCENARIO")

        # Clear detector for new event
        self.direction_detector.clear_all()

        # Trigger motion - hardware logs this
        motion_start = datetime.now()
        self.motion_sensor.trigger_motion(duration=8.0)

        # Power on RFID - hardware logs this
        self.rfid_reader.power_on()

        # Set sequence
        self.rfid_reader.set_tag_sequence(sequence)

        # Simulate scanning
        time.sleep(1.0)  # Warm-up delay
        self.log("Ready to scan", "RFID-22")

        all_readings = []
        scan_count = 0

        while self.motion_sensor.is_motion_detected() or scan_count < len(sequence):
            readings = self.rfid_reader.scan(duration=0.5)

            if readings:
                for r in readings:
                    # Hardware already logged the tag detection
                    all_readings.append(r)
                    # Add reading to student's direction detector
                    self.direction_detector.add_reading(r.tag_id, r.rssi, r.timestamp)

            scan_count += 1
            time.sleep(0.5)

            if scan_count >= len(sequence) + 2:  # Stop after sequence complete
                break

        # Motion ended
        time.sleep(0.5)
        motion_end = datetime.now()

        # Power off RFID - hardware logs this
        self.rfid_reader.power_off()

        # Process readings using student's stub classes
        self._process_tags(all_readings, motion_start, motion_end, expected="ENTRY")
        print()

    def _process_tags(self, readings, motion_start, motion_end, expected=None):
        """Process tag readings using student's stub classes."""
        self.log("", "")
        self.log("=== Analysis (using student's stub classes) ===", "RESULT")

        if not readings:
            self.log("No tags detected", "RESULT")
            return

        # Group by tag
        by_tag = {}
        for r in readings:
            if r.tag_id not in by_tag:
                by_tag[r.tag_id] = []
            by_tag[r.tag_id].append(r)

        self.log(f"Processing {len(by_tag)} unique tag(s)", "RESULT")

        # Analyze each tag using student's stub classes
        for tag_id in by_tag.keys():
            # Use student's DirectionDetector (stub returns UNKNOWN until implemented)
            direction = self.direction_detector.detect_direction(tag_id)

            # Calculate RSSI delta for display
            tag_readings = by_tag[tag_id]
            if len(tag_readings) >= 2:
                first_rssi = tag_readings[0].rssi
                last_rssi = tag_readings[-1].rssi
                delta = last_rssi - first_rssi
            else:
                first_rssi = tag_readings[0].rssi if tag_readings else 0
                last_rssi = first_rssi
                delta = 0.0

            self.log(f"Tag {tag_id[:16]}...", "RESULT")
            self.log(f"  RSSI: {first_rssi:.1f} → {last_rssi:.1f} dBm (Δ {delta:+.1f})", "RESULT")

            # Update counts using student's CountManager (stub does nothing until implemented)
            if direction == Direction.ENTRY:
                self.count_manager.add_entry(count=1, tag_id=tag_id)
                direction_str = "ENTRY"
            elif direction == Direction.EXIT:
                self.count_manager.add_exit(count=1, tag_id=tag_id)
                direction_str = "EXIT"
            else:
                # For UNKNOWN, just track occurrence
                direction_str = "UNKNOWN"

            # Get occurrence count (stub returns 0 until implemented)
            occurrence = self.count_manager.get_tag_occurrence_count(tag_id)

            # Log using student's DataLogger (stub does nothing until implemented)
            avg_rssi = sum(r.rssi for r in tag_readings) / len(tag_readings)
            self.data_logger.log_tag_detection(
                tag_id=tag_id,
                direction=direction_str,
                rssi=avg_rssi,
                occurrence_count=occurrence,
                motion_start=motion_start,
                motion_end=motion_end
            )

            self.log(f"  Direction: {direction_str} (from student's DirectionDetector)", "RESULT")
            self.log(f"  Occurrence: {occurrence} (from student's CountManager)", "RESULT")

        # Show current counts
        count_data = self.count_manager.data
        self.log("", "RESULT")
        self.log(f"Daily counts (from student's CountManager):", "RESULT")
        self.log(f"  Entries: {count_data.daily_entry}", "RESULT")
        self.log(f"  Exits: {count_data.daily_exit}", "RESULT")
        self.log(f"  Net: {count_data.net_count}", "RESULT")

        if expected:
            self.log("", "EXPECTED")
            self.log(f"Expected direction: {expected}", "EXPECTED")

    def simulate_single_exit(self):
        """Simulate a single cow exiting the kraal."""
        self.log("=== Scenario: Single Cow Exiting ===", "SCENARIO")
        self.log("A cow with tag E200002222222222 leaves the kraal", "SCENARIO")

        tag_id = "E200002222222222"
        sequence = self.rfid_reader.generate_departing_sequence(
            tag_id=tag_id,
            num_samples=5,
            start_rssi=-45.0,
            end_rssi=-70.0
        )

        self.log(f"Generated {len(sequence)} RSSI readings (signal weakening)", "SCENARIO")

        # Clear detector for new event
        self.direction_detector.clear_all()

        # Trigger motion - hardware logs this
        motion_start = datetime.now()
        self.motion_sensor.trigger_motion(duration=8.0)

        # Power on RFID - hardware logs this
        self.rfid_reader.power_on()
        self.rfid_reader.set_tag_sequence(sequence)

        time.sleep(1.0)
        self.log("Ready to scan", "RFID-22")

        all_readings = []
        scan_count = 0

        while self.motion_sensor.is_motion_detected() or scan_count < len(sequence):
            readings = self.rfid_reader.scan(duration=0.5)

            if readings:
                for r in readings:
                    # Hardware already logged the tag detection
                    all_readings.append(r)
                    # Add reading to student's direction detector
                    self.direction_detector.add_reading(r.tag_id, r.rssi, r.timestamp)

            scan_count += 1
            time.sleep(0.5)

            if scan_count >= len(sequence) + 2:
                break

        # Motion ended
        time.sleep(0.5)
        motion_end = datetime.now()

        # Power off RFID - hardware logs this
        self.rfid_reader.power_off()

        # Process readings using student's stub classes
        self._process_tags(all_readings, motion_start, motion_end, expected="EXIT")
        print()

    def simulate_multiple_cattle(self):
        """Simulate multiple cattle passing through together."""
        self.log("=== Scenario: Multiple Cattle Entering ===", "SCENARIO")
        self.log("Three cows pass through the gate together", "SCENARIO")

        # Create sequences for 3 different tags
        tag1_seq = self.rfid_reader.generate_approaching_sequence("E200001111111111", 4)
        tag2_seq = self.rfid_reader.generate_approaching_sequence("E200002222222222", 4)
        tag3_seq = self.rfid_reader.generate_approaching_sequence("E200003333333333", 3)

        # Interleave the sequences to simulate multiple cattle
        combined = []
        max_len = max(len(tag1_seq), len(tag2_seq), len(tag3_seq))

        for i in range(max_len):
            if i < len(tag1_seq):
                combined.append(tag1_seq[i])
            if i < len(tag2_seq):
                combined.append(tag2_seq[i])
            if i < len(tag3_seq):
                combined.append(tag3_seq[i])

        self.log(f"Generated {len(combined)} total readings for 3 cattle", "SCENARIO")

        # Clear detector for new event
        self.direction_detector.clear_all()

        # Trigger motion - hardware logs this
        motion_start = datetime.now()
        self.motion_sensor.trigger_motion(duration=12.0)

        # Power on RFID - hardware logs this
        self.rfid_reader.power_on()
        self.rfid_reader.set_tag_sequence(combined)

        time.sleep(1.0)
        self.log("Ready to scan", "RFID-22")

        all_readings = []
        scan_count = 0

        while self.motion_sensor.is_motion_detected() or scan_count < len(combined):
            readings = self.rfid_reader.scan(duration=0.5)

            if readings:
                for r in readings:
                    # Hardware already logged the tag detection
                    all_readings.append(r)
                    # Add reading to student's direction detector
                    self.direction_detector.add_reading(r.tag_id, r.rssi, r.timestamp)

            scan_count += 1
            time.sleep(0.5)

            if scan_count >= len(combined) + 2:
                break

        # Motion ended
        time.sleep(0.5)
        motion_end = datetime.now()

        # Power off RFID - hardware logs this
        self.rfid_reader.power_off()

        # Process readings using student's stub classes
        self._process_tags(all_readings, motion_start, motion_end, expected="3 ENTRY detections")
        print()

    def simulate_false_alarm(self):
        """Simulate motion without any tags (false alarm)."""
        self.log("=== Scenario: False Alarm (No Tags) ===", "SCENARIO")
        self.log("Motion detected but no cattle with tags present", "SCENARIO")

        # Clear detector for new event
        self.direction_detector.clear_all()

        # Trigger motion - hardware logs this
        motion_start = datetime.now()
        self.motion_sensor.trigger_motion(duration=5.0)

        # Power on RFID - hardware logs this
        self.rfid_reader.power_on()

        # No tags - empty sequence
        self.rfid_reader.set_tag_sequence([])

        time.sleep(1.0)
        self.log("Ready to scan", "RFID-22")

        all_readings = []
        scan_count = 0
        while scan_count < 8 and self.motion_sensor.is_motion_detected():
            readings = self.rfid_reader.scan(duration=0.5)

            if readings:
                for r in readings:
                    # Hardware already logged the tag detection (shouldn't happen)
                    all_readings.append(r)
                    self.direction_detector.add_reading(r.tag_id, r.rssi, r.timestamp)
            else:
                self.log("No tags in range", "RFID-22")

            scan_count += 1
            time.sleep(0.5)

        # Motion ended
        time.sleep(0.5)
        motion_end = datetime.now()

        # Power off RFID - hardware logs this
        self.rfid_reader.power_off()

        # Process readings using student's stub classes
        self._process_tags(all_readings, motion_start, motion_end, expected="No count updates")
        print()


def main():
    """Run simulation scenarios."""
    parser = argparse.ArgumentParser(
        description="Simulate cattle movement for testing critter-counter"
    )
    parser.add_argument(
        "--scenario",
        choices=["entry", "exit", "multiple", "false-alarm", "all"],
        default="all",
        help="Which scenario to run"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce output verbosity"
    )

    args = parser.parse_args()

    simulator = CattleSimulator(verbose=not args.quiet)

    print()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║         Cattle Movement Simulator - Critter Counter          ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()

    scenarios = {
        "entry": simulator.simulate_single_entry,
        "exit": simulator.simulate_single_exit,
        "multiple": simulator.simulate_multiple_cattle,
        "false-alarm": simulator.simulate_false_alarm,
    }

    if args.scenario == "all":
        for name, func in scenarios.items():
            func()
            time.sleep(1)
    else:
        scenarios[args.scenario]()

    print()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                    Simulation Complete                       ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()
    print("Next steps:")
    print("  1. Implement the modules in src/ following the implementation guide")
    print("  2. Run 'python src/main.py --sim' to test with your implementation")
    print("  3. Verify direction detection works for ENTRY and EXIT scenarios")
    print("  4. Check tag occurrence counting for multiple cattle")
    print()


if __name__ == "__main__":
    main()
