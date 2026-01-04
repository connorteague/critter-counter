"""
Mock hardware classes for simulation and testing.

These classes simulate the hardware interfaces without requiring actual GPIO
or RFID hardware. They're used for development, testing, and demonstration.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple, Callable
import time
import random


@dataclass
class RFIDReading:
    """
    Single RFID tag reading.

    Attributes:
        tag_id: EPC tag identifier (24-character hex string)
        rssi: Signal strength in dBm (more negative = weaker signal)
        timestamp: When the reading was taken
        antenna: Antenna number (optional, for multi-antenna systems)
    """

    tag_id: str
    rssi: float
    timestamp: datetime
    antenna: Optional[int] = None


class MockMotionSensor:
    """
    Mock PIR motion sensor for simulation and testing.

    Simulates motion detection with configurable duration and decay.
    """

    def __init__(
        self,
        pin: int = 17,
        debounce_time: float = 0.5,
        log_callback: Optional[Callable] = None,
    ):
        """
        Initialize mock motion sensor.

        Args:
            pin: GPIO pin number (not used in mock, for interface compatibility)
            debounce_time: Minimum time between motion events
            log_callback: Optional callback function for logging (func(device, message, level))
        """
        self.pin = pin
        self.debounce_time = debounce_time
        self.device_id = f"PIR-{pin}"
        self._log_callback = log_callback
        self._motion_active = False
        self._motion_start_time: Optional[float] = None
        self._motion_duration = 0.0
        self._last_trigger_time = 0.0

    def _log(self, message: str, level: str = "INFO"):
        """Internal logging method."""
        if self._log_callback:
            self._log_callback(self.device_id, message, level)

    def trigger_motion(self, duration: float = 10.0) -> None:
        """
        Trigger a motion event (test helper).

        Args:
            duration: How long motion should last in seconds
        """
        current_time = time.time()

        # Check debounce
        if current_time - self._last_trigger_time < self.debounce_time:
            self._log(f"Motion ignored (debounce: {self.debounce_time}s)", "DEBUG")
            return

        self._motion_active = True
        self._motion_start_time = current_time
        self._motion_duration = duration
        self._last_trigger_time = current_time
        self._log(f"Motion detected! (duration: {duration}s)", "INFO")

    def is_motion_detected(self) -> bool:
        """
        Check if motion is currently detected.

        Returns:
            bool: True if motion is active, False otherwise
        """
        if not self._motion_active:
            return False

        if self._motion_start_time is None:
            return False

        elapsed = time.time() - self._motion_start_time
        if elapsed >= self._motion_duration:
            self._motion_active = False
            self._log("Motion ended (timeout)", "INFO")
            return False

        return True

    def wait_for_motion(self, timeout: Optional[float] = None) -> bool:
        """
        Block until motion is detected or timeout.

        Args:
            timeout: Maximum seconds to wait (None = wait forever)

        Returns:
            bool: True if motion detected, False if timeout
        """
        start_time = time.time()

        while True:
            if self.is_motion_detected():
                return True

            if timeout is not None:
                if time.time() - start_time >= timeout:
                    return False

            time.sleep(0.1)  # Poll every 100ms


class MockRFIDReader:
    """
    Mock RFID reader for simulation and testing.

    Simulates UHF RFID scanning with configurable tag sequences and RSSI patterns.
    """

    def __init__(
        self, power_pin: Optional[int] = None, log_callback: Optional[Callable] = None
    ):
        """
        Initialize mock RFID reader.

        Args:
            power_pin: GPIO pin for MOSFET power control (not used in mock)
            log_callback: Optional callback function for logging (func(device, message, level))
        """
        self.power_pin = power_pin
        self.device_id = f"RFID-{power_pin}" if power_pin else "RFID"
        self._log_callback = log_callback
        self._powered = False
        self._tag_sequence: List[Tuple[str, float]] = []
        self._sequence_index = 0
        self._scan_count = 0

    def _log(self, message: str, level: str = "INFO"):
        """Internal logging method."""
        if self._log_callback:
            self._log_callback(self.device_id, message, level)

    def power_on(self) -> None:
        """Turn on RFID reader via MOSFET."""
        if not self._powered:
            self._powered = True
            self._log(f"Powered ON (GPIO {self.power_pin})", "INFO")
        else:
            self._log("Already powered on", "DEBUG")

    def power_off(self) -> None:
        """Turn off RFID reader via MOSFET."""
        if self._powered:
            self._powered = False
            self._log(f"Powered OFF (GPIO {self.power_pin})", "INFO")
            # Reset sequence when powered off
            self._sequence_index = 0
            self._scan_count = 0
        else:
            self._log("Already powered off", "DEBUG")

    def is_powered(self) -> bool:
        """
        Check if RFID reader is powered on.

        Returns:
            bool: True if powered, False otherwise
        """
        return self._powered

    def set_tag_sequence(self, sequence: List[Tuple[str, float]]) -> None:
        """
        Configure tag reading sequence for testing.

        Args:
            sequence: List of (tag_id, rssi) tuples to return on subsequent scans

        Example:
            reader.set_tag_sequence([
                ("E200001111111111", -70.0),  # Far away
                ("E200001111111111", -60.0),  # Getting closer
                ("E200001111111111", -50.0),  # Close
            ])
        """
        self._tag_sequence = sequence
        self._sequence_index = 0

    def scan(self, duration: float = 3.0) -> List[RFIDReading]:
        """
        Scan for RFID tags.

        Args:
            duration: How long to scan in seconds (ignored in mock)

        Returns:
            List of RFIDReading objects for detected tags
        """
        if not self._powered:
            self._log("Scan attempted while powered off!", "WARNING")
            return []

        readings = []

        # Return next reading(s) from sequence
        if self._sequence_index < len(self._tag_sequence):
            tag_id, rssi = self._tag_sequence[self._sequence_index]

            # Add some realistic noise to RSSI
            noisy_rssi = rssi + random.uniform(-2.0, 2.0)

            reading = RFIDReading(
                tag_id=tag_id, rssi=noisy_rssi, timestamp=datetime.now(), antenna=1
            )
            readings.append(reading)

            self._log(f"Tag detected: {tag_id[:16]}... @ {noisy_rssi:.1f} dBm", "INFO")
            self._sequence_index += 1
        else:
            self._log(f"Scan #{self._scan_count + 1}: No tags in range", "DEBUG")

        self._scan_count += 1
        return readings

    def read_single(self, timeout: float = 5.0) -> Optional[RFIDReading]:
        """
        Read a single tag (blocking until tag detected or timeout).

        Args:
            timeout: Maximum seconds to wait for tag

        Returns:
            RFIDReading if tag detected, None if timeout
        """
        if not self._powered:
            return None

        start_time = time.time()

        while time.time() - start_time < timeout:
            readings = self.scan(duration=0.5)
            if readings:
                return readings[0]
            time.sleep(0.1)

        return None

    def generate_approaching_sequence(
        self,
        tag_id: str,
        num_samples: int = 5,
        start_rssi: float = -75.0,
        end_rssi: float = -45.0,
    ) -> List[Tuple[str, float]]:
        """
        Generate a realistic approaching cattle RSSI sequence.

        Args:
            tag_id: Tag identifier
            num_samples: Number of RSSI samples to generate
            start_rssi: Starting RSSI (far away)
            end_rssi: Ending RSSI (close)

        Returns:
            List of (tag_id, rssi) tuples showing signal strengthening
        """
        step = (end_rssi - start_rssi) / (num_samples - 1)
        return [(tag_id, start_rssi + i * step) for i in range(num_samples)]

    def generate_departing_sequence(
        self,
        tag_id: str,
        num_samples: int = 5,
        start_rssi: float = -45.0,
        end_rssi: float = -75.0,
    ) -> List[Tuple[str, float]]:
        """
        Generate a realistic departing cattle RSSI sequence.

        Args:
            tag_id: Tag identifier
            num_samples: Number of RSSI samples to generate
            start_rssi: Starting RSSI (close)
            end_rssi: Ending RSSI (far away)

        Returns:
            List of (tag_id, rssi) tuples showing signal weakening
        """
        step = (end_rssi - start_rssi) / (num_samples - 1)
        return [(tag_id, start_rssi + i * step) for i in range(num_samples)]


# Example usage and testing
if __name__ == "__main__":
    print("=== Mock Hardware Test ===\n")

    # Test motion sensor
    print("1. Testing MockMotionSensor")
    motion = MockMotionSensor()
    print(f"   Initial motion: {motion.is_motion_detected()}")

    motion.trigger_motion(duration=2.0)
    print(f"   After trigger: {motion.is_motion_detected()}")

    time.sleep(2.5)
    print(f"   After 2.5s: {motion.is_motion_detected()}")
    print()

    # Test RFID reader
    print("2. Testing MockRFIDReader")
    rfid = MockRFIDReader(power_pin=22)
    print(f"   Powered: {rfid.is_powered()}")

    rfid.power_on()
    print(f"   After power_on: {rfid.is_powered()}")

    # Test approaching cattle
    print("\n3. Simulating approaching cattle (ENTRY)")
    sequence = rfid.generate_approaching_sequence("E200001234567890", num_samples=3)
    rfid.set_tag_sequence(sequence)

    for i in range(3):
        readings = rfid.scan()
        if readings:
            r = readings[0]
            print(f"   Scan {i+1}: RSSI = {r.rssi:.1f} dBm")

    # Test departing cattle
    print("\n4. Simulating departing cattle (EXIT)")
    rfid.power_off()
    rfid.power_on()
    sequence = rfid.generate_departing_sequence("E200009876543210", num_samples=3)
    rfid.set_tag_sequence(sequence)

    for i in range(3):
        readings = rfid.scan()
        if readings:
            r = readings[0]
            print(f"   Scan {i+1}: RSSI = {r.rssi:.1f} dBm")

    print("\n✓ Mock hardware test complete!")
