import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import datetime
from src.data.database import Database
from src.ui.ui_components import setup_alarm_interface, setup_timer_interface, setup_stopwatch_interface, apply_theme
from src.utils.audio_manager import AudioManager
from src.utils.constants import COLORS

class SmartAlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Alarm Clock")

        # Make window fullscreen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Configure root window grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Initialize components
        self.db = Database()
        self.audio = AudioManager()
        self.colors = COLORS
        self.is_dark_mode = False

        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Initialize style
        self.style = ttk.Style()

        # Alarm settings
        self.alarms = self.db.load_alarms()

        # Create main interface
        self.setup_ui()

        # Apply theme after UI is set up
        self.apply_theme()

        # Start alarm checking thread
        self.running = True
        self.alarm_thread = threading.Thread(target=self.check_alarms)
        self.alarm_thread.daemon = True
        self.alarm_thread.start()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        """Setup the main user interface"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.grid_columnconfigure(0, weight=1)

        # Alarm tab
        self.alarm_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alarm_frame, text="Alarms")

        # Timer tab
        self.timer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.timer_frame, text="Timer")

        # Stopwatch tab
        self.stopwatch_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stopwatch_frame, text="Stopwatch")

        # Setup interfaces
        setup_alarm_interface(self, self.alarm_frame, self.colors, self.is_dark_mode)
        setup_timer_interface(self, self.timer_frame)
        setup_stopwatch_interface(self, self.stopwatch_frame)

        # Theme toggle button
        self.theme_button = ttk.Button(self.main_frame, text="Toggle Dark Mode", command=self.toggle_theme)
        self.theme_button.grid(row=1, column=0, pady=10)

    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme to all widgets"""
        apply_theme(self.style, self.root, self.main_frame, self.alarm_listbox, self.colors, self.is_dark_mode)

    def check_alarms(self):
        """Check for active alarms"""
        while self.running:
            current_time = datetime.datetime.now()
            for alarm in self.alarms:
                alarm_time = datetime.datetime.strptime(alarm["time"], "%H:%M").time()
                # Compare hours and minutes only
                if (current_time.hour == alarm_time.hour and 
                    current_time.minute == alarm_time.minute and 
                    not hasattr(self, "alarm_triggered")):
                    self.alarm_triggered = alarm
                    self.trigger_alarm(alarm)
            # Check every second instead of every 10 seconds
            time.sleep(1)

    def trigger_alarm(self, alarm):
        """Trigger an alarm"""
        self.root.deiconify()
        
        # Create alarm dialog
        self.alarm_dialog = tk.Toplevel(self.root)
        self.alarm_dialog.title("Alarm!")
        self.alarm_dialog.lift()  # Bring window to front
        self.alarm_dialog.focus_force()  # Force focus
        
        # Make dialog stay on top
        self.alarm_dialog.attributes('-topmost', True)
        
        # Center the dialog on screen
        window_width = 200  # Reduced width
        window_height = 100  # Reduced height
        screen_width = self.alarm_dialog.winfo_screenwidth()
        screen_height = self.alarm_dialog.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.alarm_dialog.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Configure grid
        self.alarm_dialog.grid_rowconfigure(0, weight=1)
        self.alarm_dialog.grid_rowconfigure(1, weight=0)
        self.alarm_dialog.grid_columnconfigure(0, weight=1)
        
        # Add message
        message = alarm['note'] if alarm['note'] else 'Time to wake up!'
        message_label = ttk.Label(
            self.alarm_dialog,
            text=message,
            wraplength=180,  # Adjusted for new width
            font=('Arial', 12),
            justify='center'
        )
        message_label.grid(row=0, column=0, pady=(5, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(self.alarm_dialog)
        button_frame.grid(row=1, column=0, pady=(0, 5))
        
        # Snooze button
        snooze_btn = ttk.Button(
            button_frame,
            text="Snooze (5 min)",
            command=lambda: [self.snooze_alarm(), self.alarm_dialog.destroy()]
        )
        snooze_btn.pack(side=tk.LEFT, padx=2)
        
        # Stop button
        stop_btn = ttk.Button(
            button_frame,
            text="Stop Alarm",
            command=lambda: [self.stop_alarm(), self.alarm_dialog.destroy()]
        )
        stop_btn.pack(side=tk.LEFT, padx=2)
        
        # Play alarm sound
        self.audio.play_alarm(alarm["sound_path"], gradual=True)
        
        # Prevent closing with Alt+F4
        self.alarm_dialog.protocol("WM_DELETE_WINDOW", lambda: None)

    def snooze_alarm(self):
        """Snooze the current alarm"""
        if hasattr(self, "alarm_triggered"):
            self.audio.stop_alarm()
            alarm = self.alarm_triggered

            # Calculate snooze time
            alarm_time = datetime.datetime.strptime(alarm["time"], "%H:%M")
            snooze_time = alarm_time + datetime.timedelta(minutes=5)
            new_time = snooze_time.strftime("%H:%M")

            # Update alarm in database
            self.db.update_alarm_time(alarm, new_time)
            alarm["time"] = new_time
            self.update_alarm_listbox()
            self.cleanup_alarm()

    def stop_alarm(self):
        """Stop the current alarm"""
        if hasattr(self, "alarm_triggered"):
            self.audio.stop_alarm()
            alarm = self.alarm_triggered
            self.db.deactivate_alarm(alarm)
            self.alarms.remove(alarm)
            self.update_alarm_listbox()
            self.cleanup_alarm()

    def cleanup_alarm(self):
        """Cleanup after alarm"""
        if hasattr(self, 'alarm_dialog') and self.alarm_dialog:
            self.alarm_dialog.destroy()
        delattr(self, "alarm_triggered")

    def on_closing(self):
        """Handle window closing"""
        self.running = False
        if hasattr(self, "alarm_triggered"):
            self.audio.stop_alarm()
            if hasattr(self, 'alarm_dialog') and self.alarm_dialog:
                self.alarm_dialog.destroy()
        self.db.close()
        self.audio.quit()
        self.root.destroy()

    def stop_timer(self):
        """Stop the timer"""
        if hasattr(self, 'timer_running'):
            self.timer_running = False
            self.timer_start_button.config(state=tk.NORMAL)
            self.timer_stop_button.config(state=tk.DISABLED)

    def stop_stopwatch(self):
        """Stop the stopwatch"""
        if hasattr(self, 'stopwatch_running'):
            self.stopwatch_running = False
            self.stopwatch_start_button.config(state=tk.NORMAL)
            self.stopwatch_stop_button.config(state=tk.DISABLED)