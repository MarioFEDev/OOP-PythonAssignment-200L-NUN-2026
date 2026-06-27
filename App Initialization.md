# App Initialization Steps

Follow these steps to set up and run the Reflex app from scratch in PowerShell.

**1. Navigate into the Project directory**
First, move into the `Project` directory where your app and virtual environment are located:
```powershell
cd Project
```

**2. Activate the Virtual Environment**
Activate your existing Python virtual environment using the correct PowerShell syntax:
```powershell
.\venv\Scripts\Activate.ps1
```
*(Note: If you get a "running scripts is disabled on this system" error, you can use the batch file instead by running: `venv\Scripts\activate.bat`)*

**3. Install the dependencies (if you haven't already)**
Make sure all required packages (including Reflex) are installed:
```powershell
pip install -r requirements.txt
```

**4. Run the Reflex app**
Once the environment is active (you should see `(venv)` at the beginning of your prompt) and the dependencies are installed, you can start the development server:
```powershell
reflex run
```

This will compile your app and make it available at `http://localhost:3000`.
