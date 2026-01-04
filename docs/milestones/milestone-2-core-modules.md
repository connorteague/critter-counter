# Milestone 2: Core Modules Development

## Overview

In this milestone, we will focus on the development of the core modules for the Critter Counter project. This includes the following components:

- **Configuration File (`config.py`)**
- **Count Manager (`count_manager.py`)**
- **Direction Detector (`direction_detector.py`)**

The emphasis will be on implementing these modules using a Test-Driven Development (TDD) approach, ensuring that tests are written before the actual implementation.

## Steps

### 1. Configuration File (`config.py`)

- **Objective:** Define all configuration constants required for the application.
- **Tasks:**
  - Create a `config.py` file in the `src` directory.
  - Define constants such as RFID settings, logging paths, and any other necessary parameters.
  - Write unit tests to verify that the configuration values are correctly set.

### 2. Count Manager (`count_manager.py`)

- **Objective:** Implement the logic for counting cattle entries and exits, as well as tracking tag occurrences.
- **Tasks:**
  - Create a `count_manager.py` file in the `src` directory.
  - Implement methods for:
    - Counting entries and exits.
    - Tracking the number of times each tag is detected.
  - Write unit tests for each method to ensure correctness and reliability.

### 3. Direction Detector (`direction_detector.py`)

- **Objective:** Develop the logic to determine the direction of cattle movement based on RSSI (Received Signal Strength Indicator) values.
- **Tasks:**
  - Create a `direction_detector.py` file in the `src` directory.
  - Implement the algorithm to analyze RSSI trends and determine whether cattle are entering or exiting.
  - Write unit tests to validate the direction detection logic under various scenarios.

## Testing Approach

- Follow the TDD methodology:
  - Write tests for each module before implementing the functionality.
  - Use mock data where necessary to simulate hardware interactions.
  - Aim for high test coverage to ensure reliability.

## Documentation

- Update the project documentation to reflect the new modules and their functionalities.
- Ensure that all code is well-commented and adheres to PEP 8 style guidelines.

## Milestone Completion

- All core modules should be implemented and tested.
- Documentation should be updated to include details about the new modules.
- Prepare for the next milestone, which will focus on supporting modules.