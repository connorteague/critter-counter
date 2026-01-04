# Simulator Guide

## Overview

This guide provides an overview of the web and CLI simulators, their features, and how they integrate with the modules you will implement.

## Key Features

### Web Simulator
- **Interface**: Browser-based at `http://localhost:5000`
- **Interaction**: Click scenario buttons to simulate events
- **Real-time Updates**: Live dashboard for counts and events
- **Best For**: Visual learners and demonstrations

### CLI Simulator
- **Interface**: Terminal-based
- **Interaction**: Use command-line arguments to run scenarios
- **Best For**: Debugging and detailed logs

## Stub Class Integration

Both simulators:
1. Instantiate your stub classes (e.g., `DirectionDetector`, `CountManager`, `DataLogger`).
2. Call your methods to process readings, detect direction, and update counts.
3. Display results, showing current stub behavior vs. expected behavior.

For detailed scenario descriptions, refer to `SIMULATION.md`.

## Troubleshooting

- **Imports fail**: Ensure you are in the project root directory.
- **Web simulator port in use**: Try a different port.
- **No device logging visible**: Verify log callbacks are passed to constructors.

For setup instructions, see `QUICKSTART.md`.
