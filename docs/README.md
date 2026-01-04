# Critter Counter Project Milestones

This document outlines the milestones for the Critter Counter project, providing a structured approach to development and implementation.

## Milestone 1: Setup

- **Objective:** Set up the repository and get the simulation running.
- **Steps:**
  1. Clone the repository:
     ```bash
     git clone <repository-url>
     cd critter-counter
     ```
  2. Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use: venv\Scripts\activate
     ```
  3. Install dependencies:
     ```bash
     pip install -r requirements.txt
     pip install -r requirements-dev.txt
     ```
  4. Run the visual simulation:
     ```bash
     python3 simulator/simulate_web.py
     ```
     - Open your browser and navigate to `http://localhost:5000`.

## Milestone 2: Core Modules

- **Objective:** Develop core modules including configuration, count manager, and direction detector.
- **Steps:**
  1. Implement `config.py` for configuration constants.
  2. Develop `count_manager.py` for counting logic and persistence.
  3. Create `direction_detector.py` for RSSI-based direction detection.
  4. Write tests for each module before implementation.

## Milestone 3: Supporting Modules

- **Objective:** Develop supporting modules, specifically the data logger.
- **Steps:**
  1. Implement `data_logger.py` for event logging to CSV.
  2. Ensure integration with core modules.
  3. Write tests to validate functionality.

## Milestone 4: Integration

- **Objective:** Integrate all modules and test together.
- **Steps:**
  1. Combine core and supporting modules.
  2. Run end-to-end simulations to verify data flow.
  3. Address any integration issues.

## Milestone 5: Testing and Polish

- **Objective:** Finalize testing and polish the project.
- **Steps:**
  1. Achieve comprehensive test coverage (>80%).
  2. Conduct code quality checks using linters and type checkers.
  3. Complete documentation for all modules.

## Milestone 6: Deployment

- **Objective:** Prepare the project for deployment.
- **Steps:**
  1. Perform final testing to ensure stability.
  2. Package the project for deployment.
  3. Develop deployment strategies and documentation.

---

This README serves as a guide for the milestones in the Critter Counter project, ensuring a clear path from setup to deployment.