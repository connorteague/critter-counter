# Critter Counter v2.0

Solar-powered RFID livestock tracking system for Botswana cattle farmers.

## Project Overview

This system helps farmers track cattle entering and exiting their kraals (livestock enclosures) using RFID technology. The goal is to prevent livestock loss to predators by providing accurate counts of cattle that haven't returned from daily grazing.

**Mission Partner:** Cheetah Conservation Botswana  
**Target Deployment:** May 2026  
**Current Phase:** Software Development

## System Architecture

```
┌───────────────────────────────────────────────────────┐
│                    Raspberry Pi                       │
│  ┌─────────────────────────────────────────────────┐  │
│  │              Main Application                   │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │  │
│  │  │  Count   │  │Direction │  │  Data    │       │  │
│  │  │ Manager  │  │ Detector │  │  Logger  │       │  │
│  │  └──────────┘  └──────────┘  └──────────┘       │  │
│  └─────────────────────────────────────────────────┘  │
│         ▲              ▲              ▲               │
│         │              │              │               │
│    ┌────┴────┐     ┌───┴───┐     ┌────┴────┐          │
│    │  PIR    │     │  UHF  │     │ E-ink   │          │
│    │ Motion  │     │ RFID  │     │Display  │          │
│    │ Sensor  │     │Reader │     │         │          │
│    └─────────┘     └───────┘     └─────────┘          │
└───────────────────────────────────────────────────────┘
```

## Technology Stack

- **Language:** Python 3.9+
- **Platform:** Raspberry Pi (Model TBD)
- **RFID:** UHF Long-Range (860-960 MHz)
- **Testing:** pytest
- **Linting:** pylint

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment support

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd critter-counter
   ```

2. **Create virtual environment:**
   ```bash
   make setup
   # or
   python -m venv venv
   
   # On Linux/Mac:
   source venv/bin/activate
   
   # On Windows:
   # venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   make install
   # or 
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

### Running Simulations

The project provides two simulation environments to test your implementation:

**1. Visual Web Simulation (recommended!):**
```bash
make simulate
# or
python3 simulator/simulate_web.py
# Then open http://localhost:5000 in your browser
```
- Interactive browser interface with click buttons
- Real-time event log with device-specific messages (PIR-17, RFID-22)
- Visual status indicators for hardware state
- Shows stub behavior before implementation
- See [QUICKSTART.md](QUICKSTART.md) for guide

**2. CLI Simulation (for terminal testing):**
```bash
python3 simulator/simulate.py --scenario entry    # Test single entry
python3 simulator/simulate.py --scenario exit     # Test single exit
python3 simulator/simulate.py --scenario multiple # Test multiple cattle
python3 simulator/simulate.py --scenario all      # Run all scenarios
```
- Terminal-based output with timestamps
- Device-specific logging (PIR-17, RFID-22)
- Detailed analysis showing stub behavior vs expected
- Great for debugging and understanding flow

**Both simulators:**
- Use your stub classes from src/
- Show device-specific hardware logging
- Display "UNKNOWN" direction and "0" counts until you implement
- Demonstrate the exact API you need to implement

### Running Tests

**Run all tests:**
```bash
make test
# or
pytest
```

**Run with coverage:**
```bash
make test-coverage
# or
pytest --cov=src --cov-report=html
```

**Run specific test file:**
```bash
test-counts
#or 
pytest tests/test_count_manager.py
```

**Run with verbose output:**
```bash
make test-verbose
# or
pytest -v
```

### Code Quality

**Run linter:**
```bash
make lint
# or
pylint src/
```

**Run type checker:**
```bash
mypy src/
```

**Auto-format code:**
```bash
make format
# or
black src/ tests/
```

## Implementation Approach

This project uses a **test harness** approach to help you learn by implementing core logic yourself:

### What's Provided
✓ **Mock hardware classes** ([src/hardware/mocks.py](src/hardware/mocks.py)) - Fully working simulations  
✓ **Configuration** ([src/config.py](src/config.py)) - All constants and parameters  
✓ **Test fixtures** ([tests/conftest.py](tests/conftest.py)) - Test helpers and sample data  
✓ **Web simulation** ([simulator/simulate_web.py](simulator/simulate_web.py)) - Interactive testing environment  
✓ **Implementation guide** (~/.claude/plans/deep-weaving-corbato.md) - Detailed specifications  

### What You Implement
☐ **Direction Detector** ([src/direction_detector.py](src/direction_detector.py)) - RSSI-based direction detection  
☐ **Count Manager** ([src/count_manager.py](src/count_manager.py)) - Entry/exit counting + tag occurrences  
☐ **Data Logger** ([src/data_logger.py](src/data_logger.py)) - CSV event logging  
☐ **Main Application** ([src/main.py](src/main.py)) - Motion-triggered workflow orchestration  
☐ **Tests** (tests/*.py) - Unit and integration tests  

### How the Simulation Works

The visual simulation ([QUICKSTART.md](QUICKSTART.md)) demonstrates the expected behavior:

1. **Mock hardware** generates realistic sensor data (motion, RFID scans)
2. **Your stub classes** process this data (currently return defaults)
3. **Web interface** displays results in real-time with device-specific logging

**Before implementation:**
- Direction shows "UNKNOWN" (stub returns default)
- Counts stay at 0 (stub methods don't update)
- Logs show hardware activity with device IDs (PIR-17, RFID-22)

**After implementation:**
- Direction correctly identifies ENTRY/EXIT based on RSSI trends
- Counts update based on detected movements
- Tag occurrences track how many times each animal has been seen
- Events are logged to CSV with full context

### Getting Started

1. **Run the visual simulation** to see expected behavior:
   ```bash
   make simulate
   # Open http://localhost:5000
   ```

2. **Implement modules following TDD:**
   - Write tests first (examples in tests/)
   - Implement to make tests pass
   - Use mock hardware for testing without GPIO

3. **Test your implementation:**
   ```bash
   
   ```

## Project Structure

```
critter-counter/
├── src/                        # Source code
│   ├── __init__.py
│   ├── main.py                 # Main application entry point
│   ├── config.py               # Configuration constants
│   ├── count_manager.py        # Count logic with persistence + tag occurrence tracking
│   ├── direction_detector.py   # Entry/exit direction detection (RSSI-based)
│   ├── data_logger.py          # Event logging to CSV (with motion context)
│   └── hardware/               # Hardware interface modules
│       ├── __init__.py
│       ├── mocks.py            # Mock hardware for testing
│       ├── rfid_reader.py      # RFID with MOSFET power control
│       ├── motion_sensor.py    # PIR motion detection
│       └── battery_monitor.py
├── tests/                      # Test files
│   ├── __init__.py
│   ├── test_count_manager.py
│   ├── test_direction_detector.py
│   ├── test_data_logger.py
│   ├── test_integration.py     # End-to-end motion event tests
│   └── conftest.py            # Pytest configuration & fixtures
├── data/                       # Runtime data directory
│   ├── counts.json            # Persistent count storage
│   └── events.csv             # Event log file
├── docs/                       # Documentation
│   └── algorithm_notes.md     # Technical notes
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── .gitignore
├── README.md
└── setup.py                    # Package setup
```

## Development Workflow

### Milestone Tracking

**Week 1-2: Core Modules**
- [ ] config.py
- [ ] count_manager.py with tests
- [ ] direction_detector.py with tests

**Week 3-4: Supporting Modules**
- [ ] data_logger.py with tests (enhanced with motion events)

**Week 5: Integration**
- [ ] End-to-end simulation testing

**Week 6-7: Testing & Polish**
- [ ] Comprehensive test coverage
- [ ] Documentation complete
- [ ] Code review ready

### Testing Guidelines

1. **Write tests first** (TDD approach encouraged)
2. **Test edge cases:** Zero counts, negative scenarios, data corruption
3. **Test persistence:** Verify data survives restarts
4. **Mock hardware:** Use fixtures to simulate RFID/PIR responses
5. **Aim for >80% coverage**

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public methods
- Keep functions small and focused
- Comment complex algorithms

## Module Responsibilities

### Your Responsibility (Software Logic)

✅ `config.py` - All configuration constants    
✅ `count_manager.py` - Count logic, persistence, tag occurrence tracking  
✅ `direction_detector.py` - RSSI-based direction algorithm (multi-tag support)  
✅ `data_logger.py` - CSV event logging (with motion context)  
✅ All unit and integration tests

### Connor's Responsibility (Hardware Integration)

🔧 `hardware/rfid_reader.py` - RFID hardware interface with MOSFET power control
🔧 `hardware/motion_sensor.py` - PIR sensor GPIO
🔧 `hardware/battery_monitor.py` - Battery voltage reading
🔧 Hardware testing and deployment

## Key Algorithms

### Direction Detection

Uses RSSI (signal strength) trend analysis:
- **ENTRY:** RSSI increases (cattle approaching)
- **EXIT:** RSSI decreases (cattle departing)
- Requires multiple samples for confidence

See `docs/algorithm_notes.md` for detailed explanation.

### Count Persistence

- JSON file storage for reliability
- Survives power cycles
- Daily auto-reset at midnight
- Manual reset via button

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock all external dependencies
- Focus on business logic correctness

### Integration Tests
- Test module interactions
- Simulate complete cattle passage scenarios
- Verify data flow through system

### Simulation Mode
- Run entire system without hardware
- Test with fake RFID data
- Validate display output to console

## Common Tasks

### Add a new configuration parameter

1. Add to `src/config.py`
2. Document with comment
3. Update tests if needed

### Modify count logic

1. Edit `src/count_manager.py`
2. Update tests in `tests/test_count_manager.py`
3. Run tests: `pytest tests/test_count_manager.py`

### Change direction detection algorithm

1. Edit `src/direction_detector.py`
2. Update algorithm notes in `docs/algorithm_notes.md`
3. Update tests to reflect new behavior
4. Discuss with Connor if hardware implications

## Troubleshooting

### Tests failing after changes
```bash
# Run specific test with verbose output
pytest tests/test_count_manager.py -v

# Check what changed
git diff
```

### Import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Data directory issues
```bash
# Create data directory if missing
mkdir -p data

# Check permissions (Linux/Mac)
ls -la data/
```

## Communication

### Weekly Check-ins with Teanm

Share in each check-in:
1. ✅ Completed milestones
2. 🔄 Current work in progress
3. ❓ Questions or blockers
4. 📊 Test results

### Getting Help

- **Technical questions:** Connor
- **Hardware specs:** Connor will provide documentation
- **Algorithm questions:** Discuss and document decisions

## Implementation Guide

## Resources

### Python Testing
- [pytest documentation](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)

### RFID Technology
- EPC Gen2 UHF RFID Protocol
- [RFID basics](https://www.rfidjournal.com/what-is-rfid)

### Best Practices
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
