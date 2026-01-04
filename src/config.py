"""
Configuration constants for Critter Counter system.

All configurable parameters are defined here for easy modification.
"""

# ============================================================================
# GPIO PIN ASSIGNMENTS
# ============================================================================
# TODO: Connor will provide actual pin assignments after hardware setup

PIR_SENSOR_PIN = 17  # GPIO pin for PIR motion sensor
RESET_BUTTON_PIN = 27  # GPIO pin for manual reset button
RFID_POWER_PIN = 22  # GPIO pin to control RFID reader power (if needed)

# ============================================================================
# RFID SETTINGS
# ============================================================================

RFID_SCAN_DURATION = 3.0  # Duration in seconds to scan for tags
RFID_READ_RANGE_MIN = 3.0  # Minimum expected read range in meters
RFID_READ_RANGE_MAX = 10.0  # Maximum expected read range in meters
MAX_TAGS_PER_SCAN = 10  # Maximum number of tags to process per scan

# ============================================================================
# DIRECTION DETECTION PARAMETERS
# ============================================================================

# RSSI (Received Signal Strength Indicator) thresholds in dBm
# More negative = weaker signal (farther away)
RSSI_THRESHOLD_APPROACHING = -50  # Strong signal threshold
RSSI_THRESHOLD_DEPARTING = -70  # Weak signal threshold
RSSI_DELTA_THRESHOLD = 5.0  # Minimum RSSI change to determine direction

# Number of RFID readings to collect for direction determination
DIRECTION_SAMPLES = 3

# Time between direction samples in seconds
DIRECTION_SAMPLE_INTERVAL = 0.5

# ============================================================================
# COUNT MANAGEMENT
# ============================================================================

DAILY_RESET_HOUR = 0  # Hour of day (0-23) for automatic daily reset (0 = midnight)
MAX_DAILY_COUNT = 500  # Safety limit - alert if exceeded

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================

DISPLAY_UPDATE_DELAY = 2.0  # Seconds to wait after count change before updating
FULL_REFRESH_INTERVAL = 24  # Hours between full display refreshes (prevents ghosting)
DISPLAY_WIDTH = 250  # Display width in pixels (update based on actual hardware)
DISPLAY_HEIGHT = 122  # Display height in pixels (update based on actual hardware)

# ============================================================================
# DATA LOGGING
# ============================================================================

LOG_FILE_PATH = "data/events.csv"  # Path to event log file
MAX_LOG_ENTRIES = 10000  # Maximum entries before log rotation
LOG_LEVEL = "INFO"  # Logging level: DEBUG, INFO, WARNING, ERROR

# ============================================================================
# SYSTEM SETTINGS
# ============================================================================

WATCHDOG_TIMEOUT = 30  # Seconds before watchdog resets system
MOTION_DEBOUNCE_TIME = 2  # Seconds to ignore motion after processing event

# Power saving mode behavior
POWER_SAVE_REDUCE_SCANS = True  # Reduce RFID scan frequency when battery low
POWER_SAVE_DISABLE_LOGGING = False  # Continue logging even in power save mode
