import tkinter as tk
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.smart_alarm_clock import SmartAlarmClock

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartAlarmClock(root)
    root.mainloop()