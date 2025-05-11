import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os
from tkcalendar import Calendar
from PIL import Image, ImageTk
import customtkinter as ctk

class ModernAlarmClockUI:
    # Light and dark color palettes
    light_colors = {
        'bg': '#f0f0f0',
        'fg': '#333333',
        'button_bg': '#4a90e2',
        'button_fg': 'black',
        'entry_bg': '#ffffff',
        'entry_fg': '#333333',
        'tab_bg': '#f0f0f0',
        'listbox_bg': '#ffffff',
        'listbox_fg': '#333333',
        'selected_bg': '#4a90e2',
        'selected_fg': 'black'
    }
    dark_colors = {
        'bg': '#2d2d2d',
        'fg': '#ffffff',
        'button_bg': '#5a5a5a',
        'button_fg': '#ffffff',
        'entry_bg': '#3d3d3d',
        'entry_fg': '#ffffff',
        'tab_bg': '#2d2d2d',
        'listbox_bg': '#3d3d3d',
        'listbox_fg': '#ffffff',
        'selected_bg': '#5a5a5a',
        'selected_fg': '#ffffff'
    }

    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.is_dark_mode = False  # Default to light mode
        self.setup_window()
        self.create_styles()
        self.create_main_layout()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Smart Alarm Clock")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
    def create_styles(self):
        """Create custom styles for the UI"""
        self.style = ttk.Style()
        current_colors = self.dark_colors if self.is_dark_mode else self.light_colors
        self.style.configure("Modern.TFrame", background=current_colors['bg'])
        self.style.configure("Modern.TLabel", 
                           background=current_colors['bg'],
                           foreground=current_colors['fg'],
                           font=("Segoe UI", 12))
        # Use hardcoded colors for buttons with rounded corners
        self.style.configure("Modern.TButton",
                           background="#4a90e2",
                           foreground="black",
                           font=("Segoe UI", 12, "bold"),
                           borderwidth=0,
                           relief="flat")
        self.style.map("Modern.TButton",
                      background=[('active', '#3a80d2')],
                      relief=[('pressed', 'sunken')])
        self.style.configure("Title.TLabel",
                           background=current_colors['bg'],
                           foreground=current_colors['fg'],
                           font=("Segoe UI", 24, "bold"))
        # Use hardcoded colors for notebook and tabs
        self.style.configure("Modern.TNotebook",
                           background="#f0f0f0",
                           tabmargins=[2, 5, 2, 0])
        self.style.configure("Modern.TNotebook.Tab",
                           background="#f0f0f0",
                           foreground="#333333",
                           padding=[10, 5],
                           font=("Segoe UI", 11))
        self.style.map("Modern.TNotebook.Tab",
                      background=[('selected', '#4a90e2')],
                      foreground=[('selected', 'black')])
        self.style.configure("Modern.TEntry",
                           fieldbackground=current_colors['entry_bg'],
                           foreground=current_colors['entry_fg'],
                           padding=5,
                           font=("Segoe UI", 12))
        self.style.configure("Modern.TSpinbox",
                           fieldbackground=current_colors['entry_bg'],
                           foreground=current_colors['entry_fg'],
                           padding=5,
                           font=("Segoe UI", 12))
        self.style.configure("Modern.TListbox",
                           background=current_colors['listbox_bg'],
                           foreground=current_colors['listbox_fg'],
                           selectbackground=current_colors['selected_bg'],
                           selectforeground=current_colors['selected_fg'],
                           font=("Segoe UI", 12))
        
    def create_main_layout(self):
        """Create the main layout with tabs"""
        # Main container
        self.main_container = ttk.Frame(self.root, style="Modern.TFrame")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add dark mode toggle button
        toggle_button = ctk.CTkButton(self.main_container, text="Toggle Dark Mode", command=self.toggle_theme)
        toggle_button.pack(anchor=tk.NE, pady=5)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.alarm_tab = ttk.Frame(self.notebook)
        self.timer_tab = ttk.Frame(self.notebook)
        self.stopwatch_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.alarm_tab, text="Alarms")
        self.notebook.add(self.timer_tab, text="Timer")
        self.notebook.add(self.stopwatch_tab, text="Stopwatch")
        
        # Setup each tab
        self.setup_alarm_tab()
        self.setup_timer_tab()
        self.setup_stopwatch_tab()
        
    def setup_alarm_tab(self):
        """Setup the alarm tab with modern design"""
        # Left panel for setting new alarm
        left_panel = ttk.Frame(self.alarm_tab, style="Modern.TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(left_panel, 
                              text="Set New Alarm",
                              font=("Segoe UI", 16, "bold"),
                              style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Time selection
        time_frame = ttk.Frame(left_panel, style="Modern.TFrame")
        time_frame.pack(fill=tk.X, pady=10)
        
        # Hour selection
        hour_frame = ttk.Frame(time_frame, style="Modern.TFrame")
        hour_frame.pack(side=tk.LEFT, padx=5)
        ttk.Label(hour_frame, text="Hour", style="Modern.TLabel").pack()
        self.hour_spinbox = ttk.Spinbox(hour_frame, from_=0, to=23, width=3, format="%02.0f")
        self.hour_spinbox.pack()
        
        # Minute selection
        minute_frame = ttk.Frame(time_frame, style="Modern.TFrame")
        minute_frame.pack(side=tk.LEFT, padx=5)
        ttk.Label(minute_frame, text="Minute", style="Modern.TLabel").pack()
        self.minute_spinbox = ttk.Spinbox(minute_frame, from_=0, to=59, width=3, format="%02.0f")
        self.minute_spinbox.pack()
        
        # Sound selection
        sound_frame = ttk.Frame(left_panel, style="Modern.TFrame")
        sound_frame.pack(fill=tk.X, pady=10)
        ttk.Label(sound_frame, text="Alarm Sound", style="Modern.TLabel").pack(anchor=tk.W)
        
        sound_button_frame = ttk.Frame(sound_frame, style="Modern.TFrame")
        sound_button_frame.pack(fill=tk.X)
        
        self.sound_path = tk.StringVar(value="default_alarm.wav")
        browse_button = ctk.CTkButton(sound_button_frame, text="Browse Sound", command=self.browse_sound)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Note input
        note_frame = ttk.Frame(left_panel, style="Modern.TFrame")
        note_frame.pack(fill=tk.X, pady=10)
        ttk.Label(note_frame, text="Note (Optional)", style="Modern.TLabel").pack(anchor=tk.W)
        self.note_entry = ttk.Entry(note_frame, font=("Segoe UI", 12))
        self.note_entry.pack(fill=tk.X, pady=5)
        
        # Set alarm button
        set_alarm_button = ctk.CTkButton(left_panel, text="Set Alarm", command=self.set_alarm)
        set_alarm_button.pack(pady=20)
        
        # Right panel for alarm list
        right_panel = ttk.Frame(self.alarm_tab, style="Modern.TFrame")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Alarm list title
        ttk.Label(right_panel,
                 text="Active Alarms",
                 font=("Segoe UI", 16, "bold"),
                 style="Title.TLabel").pack(pady=(0, 10))
        
        # Alarm list
        self.alarm_listbox = tk.Listbox(
            right_panel,
            height=15,
            font=("Segoe UI", 12),
            bg="white",
            fg="#333333",
            selectbackground="#4a90e2",
            selectforeground="black"
        )
        self.alarm_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Delete button
        delete_button = ctk.CTkButton(right_panel, text="Delete Selected Alarm", command=self.delete_alarm)
        delete_button.pack(pady=10)
        
    def setup_timer_tab(self):
        """Setup the timer tab with modern design"""
        main_frame = ttk.Frame(self.timer_tab, style="Modern.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Timer display
        self.timer_display = ttk.Label(
            main_frame,
            text="00:00:00",
            font=("Segoe UI", 48, "bold"),
            style="Modern.TLabel"
        )
        self.timer_display.pack(pady=20)
        
        # Timer input (spinboxes)
        input_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        input_frame.pack(pady=20)
        
        ttk.Label(input_frame,
                 text="Set Timer:",
                 style="Modern.TLabel").pack(side=tk.LEFT, padx=5)
        
        self.timer_hour_spinbox = ttk.Spinbox(input_frame, from_=0, to=23, width=3, format="%02.0f")
        self.timer_hour_spinbox.pack(side=tk.LEFT, padx=2)
        ttk.Label(input_frame, text="h", style="Modern.TLabel").pack(side=tk.LEFT)
        self.timer_minute_spinbox = ttk.Spinbox(input_frame, from_=0, to=59, width=3, format="%02.0f")
        self.timer_minute_spinbox.pack(side=tk.LEFT, padx=2)
        ttk.Label(input_frame, text="m", style="Modern.TLabel").pack(side=tk.LEFT)
        self.timer_second_spinbox = ttk.Spinbox(input_frame, from_=0, to=59, width=3, format="%02.0f")
        self.timer_second_spinbox.pack(side=tk.LEFT, padx=2)
        ttk.Label(input_frame, text="s", style="Modern.TLabel").pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        button_frame.pack(pady=20)
        
        self.timer_start_button = ctk.CTkButton(button_frame, text="Start", command=self.start_timer)
        self.timer_start_button.pack(side=tk.LEFT, padx=5)
        
        self.timer_stop_button = ctk.CTkButton(button_frame, text="Stop", command=self.stop_timer_custom)
        self.timer_stop_button.pack(side=tk.LEFT, padx=5)
        
        self.timer_reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset_timer)
        self.timer_reset_button.pack(side=tk.LEFT, padx=5)
        
    def setup_stopwatch_tab(self):
        """Setup the stopwatch tab with modern design"""
        main_frame = ttk.Frame(self.stopwatch_tab, style="Modern.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Stopwatch display
        self.stopwatch_display = ttk.Label(
            main_frame,
            text="00:00:00",
            font=("Segoe UI", 48, "bold"),
            style="Modern.TLabel"
        )
        self.stopwatch_display.pack(pady=20)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        button_frame.pack(pady=20)
        
        self.stopwatch_start_button = ctk.CTkButton(button_frame, text="Start", command=self.start_stopwatch)
        self.stopwatch_start_button.pack(side=tk.LEFT, padx=5)
        
        self.stopwatch_stop_button = ctk.CTkButton(button_frame, text="Stop", command=self.stop_stopwatch_custom)
        self.stopwatch_stop_button.pack(side=tk.LEFT, padx=5)
        
        self.stopwatch_reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset_stopwatch)
        self.stopwatch_reset_button.pack(side=tk.LEFT, padx=5)
        
    def browse_sound(self):
        """Open file dialog to select alarm sound"""
        try:
            initial_dir = os.path.expanduser("~")
            file = filedialog.askopenfilename(
                parent=self.root,
                initialdir=initial_dir,
                title="Select Alarm Sound",
                filetypes=[
                    ("Audio Files", "*.wav *.mp3"),
                    ("WAV files", "*.wav"),
                    ("MP3 files", "*.mp3"),
                    ("All files", "*.*")
                ]
            )
            
            if file and os.path.exists(file):
                self.sound_path.set(file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file dialog: {str(e)}")
            
    def set_alarm(self):
        """Set a new alarm"""
        try:
            hour = int(self.hour_spinbox.get())
            minute = int(self.minute_spinbox.get())
            time_str = f"{hour:02d}:{minute:02d}"
            datetime.strptime(time_str, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Use 24-hour format (00-23:00-59).")
            return
            
        sound_path = self.sound_path.get()
        note = self.note_entry.get()
        
        self.app.db.save_alarm(time_str, sound_path, note)
        self.app.alarms.append({"time": time_str, "sound_path": sound_path, "note": note})
        self.update_alarm_listbox()
        
        # Reset inputs
        self.hour_spinbox.set("00")
        self.minute_spinbox.set("00")
        self.note_entry.delete(0, tk.END)
        self.sound_path.set("default_alarm.wav")
        
        messagebox.showinfo("Success", "Alarm set successfully!")
        
    def update_alarm_listbox(self):
        """Update the alarm list display"""
        self.alarm_listbox.delete(0, tk.END)
        for alarm in self.app.alarms:
            display_text = f"{alarm['time']} - {alarm['note']}" if alarm['note'] else f"{alarm['time']}"
            self.alarm_listbox.insert(tk.END, display_text)
            
    def delete_alarm(self):
        """Delete selected alarm"""
        selection = self.alarm_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Select an alarm to delete.")
            return
            
        index = selection[0]
        alarm = self.app.alarms[index]
        self.app.db.delete_alarm(alarm)
        self.app.alarms.pop(index)
        self.update_alarm_listbox()
        
    def start_timer(self):
        """Start the timer"""
        try:
            hours = int(self.timer_hour_spinbox.get())
            minutes = int(self.timer_minute_spinbox.get())
            seconds = int(self.timer_second_spinbox.get())
            self.app.timer_seconds = hours * 3600 + minutes * 60 + seconds
            self.app.timer_running = True
            self.timer_start_button.configure(state=tk.DISABLED)
            self.timer_stop_button.configure(text="Stop", command=self.stop_timer_custom, state=tk.NORMAL)
            self.timer_reset_button.configure(state=tk.NORMAL)
            self.update_timer()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for hours, minutes, and seconds.")
            
    def update_timer(self):
        """Update the timer display"""
        if hasattr(self.app, 'timer_running') and self.app.timer_running:
            if self.app.timer_seconds > 0:
                hours = self.app.timer_seconds // 3600
                minutes = (self.app.timer_seconds % 3600) // 60
                seconds = self.app.timer_seconds % 60
                self.timer_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
                self.app.timer_seconds -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.timer_complete()
                
    def timer_complete(self):
        """Handle timer completion"""
        self.app.timer_running = False
        self.timer_start_button.configure(state=tk.NORMAL)
        self.timer_stop_button.configure(text="Stop", command=self.stop_timer_custom, state=tk.DISABLED)
        self.timer_reset_button.configure(state=tk.NORMAL)
        messagebox.showinfo("Timer Complete", "Your timer has finished!")
        self.app.audio.play_alarm("default_alarm.wav")
        
    def start_stopwatch(self):
        """Start the stopwatch"""
        self.app.stopwatch_running = True
        self.stopwatch_start_button.configure(state=tk.DISABLED)
        self.stopwatch_stop_button.configure(state=tk.NORMAL)
        if not hasattr(self.app, 'stopwatch_seconds') or self.app.stopwatch_seconds == 0:
            self.app.stopwatch_seconds = 0
        self.update_stopwatch()
        
    def update_stopwatch(self):
        """Update the stopwatch display"""
        if hasattr(self.app, 'stopwatch_running') and self.app.stopwatch_running:
            hours = self.app.stopwatch_seconds // 3600
            minutes = (self.app.stopwatch_seconds % 3600) // 60
            seconds = self.app.stopwatch_seconds % 60
            self.stopwatch_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.app.stopwatch_seconds += 1
            self.root.after(1000, self.update_stopwatch)
            
    def stop_timer_custom(self):
        """Stop the timer and enable continue"""
        self.app.timer_running = False
        self.timer_start_button.configure(state=tk.DISABLED)
        self.timer_stop_button.configure(text="Continue", command=self.continue_timer)
        self.timer_stop_button.configure(state=tk.NORMAL)
        self.timer_reset_button.configure(state=tk.NORMAL)

    def continue_timer(self):
        """Continue the timer from where it stopped"""
        self.app.timer_running = True
        self.timer_start_button.configure(state=tk.DISABLED)
        self.timer_stop_button.configure(text="Stop", command=self.stop_timer_custom)
        self.timer_stop_button.configure(state=tk.NORMAL)
        self.timer_reset_button.configure(state=tk.NORMAL)
        self.update_timer()

    def reset_timer(self):
        """Reset the timer to 00:00:00 and enable start"""
        self.app.timer_running = False
        self.app.timer_seconds = 0
        self.timer_display.config(text="00:00:00")
        self.timer_start_button.configure(state=tk.NORMAL)
        self.timer_stop_button.configure(text="Stop", command=self.stop_timer_custom, state=tk.DISABLED)
        self.timer_reset_button.configure(state=tk.DISABLED)

    def stop_stopwatch_custom(self):
        """Stop the stopwatch and enable continue"""
        self.app.stopwatch_running = False
        self.stopwatch_start_button.configure(state=tk.DISABLED)
        self.stopwatch_stop_button.configure(text="Continue", command=self.continue_stopwatch)
        self.stopwatch_stop_button.configure(state=tk.NORMAL)
        self.stopwatch_reset_button.configure(state=tk.NORMAL)
        
    def continue_stopwatch(self):
        """Continue the stopwatch from where it stopped"""
        self.app.stopwatch_running = True
        self.stopwatch_start_button.configure(state=tk.DISABLED)
        self.stopwatch_stop_button.configure(text="Stop", command=self.stop_stopwatch_custom)
        self.stopwatch_stop_button.configure(state=tk.NORMAL)
        self.stopwatch_reset_button.configure(state=tk.DISABLED)
        self.update_stopwatch()
        
    def reset_stopwatch(self):
        """Reset the stopwatch"""
        self.app.stopwatch_running = False
        self.app.stopwatch_seconds = 0
        self.stopwatch_display.config(text="00:00:00")
        self.stopwatch_start_button.configure(state=tk.NORMAL)
        self.stopwatch_stop_button.configure(text="Stop", command=self.stop_stopwatch_custom, state=tk.DISABLED)
        self.stopwatch_reset_button.configure(state=tk.NORMAL)
        
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.create_styles()
        # Re-apply styles to all widgets
        self.root.update() 