import tkinter as tk
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.smart_alarm_clock import SmartAlarmClock
from src.ui.modern_ui import ModernAlarmClockUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartAlarmClock(root)
    ui = ModernAlarmClockUI(root, app)
    app.set_ui(ui)  # Connect the UI to the core application
    root.mainloop()