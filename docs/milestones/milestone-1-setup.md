# Milestone 1: Setup

## Objective
Set up the repository and get the simulation running.

## Steps

### 1. Clone the Repository
Open your terminal and run the following command to clone the repository:
```bash
git clone <repository-url>
cd critter-counter
```

### 2. Create a Virtual Environment
Create a virtual environment to manage dependencies:
```bash
make setup
# or
python -m venv venv
```

Activate the virtual environment:
- On Linux/Mac:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

### 3. Install Dependencies
Install the required dependencies for the project:
```bash
make install
# or 
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Run the Visual Simulation
Start the visual simulation to test your setup:
```bash
make simulate
# or
python3 simulator/simulate_web.py
```
Then, open your browser and navigate to `http://localhost:5000` to access the interactive simulation interface.

## Expected Outcome
You should see the visual simulation running in your browser, with the ability to interact with the interface and view real-time event logs. If you encounter any issues, refer to the troubleshooting section in the README.md for guidance.