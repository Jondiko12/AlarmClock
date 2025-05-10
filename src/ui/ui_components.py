import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os

def setup_alarm_interface(app, parent, colors, is_dark_mode):
    """Setup the alarm interface components"""
    parent.grid_rowconfigure(4, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)

    # Time picker frame
    time_frame = ttk.Frame(parent)
    time_frame.grid(row=0, column=0, columnspan=2, pady=5)

    ttk.Label(time_frame, text="Hour:").pack(side=tk.LEFT, padx=5)
    app.hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, width=3, format="%02.0f")
    app.hour_spinbox.pack(side=tk.LEFT, padx=5)

    ttk.Label(time_frame, text="Minute:").pack(side=tk.LEFT, padx=5)
    app.minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, width=3, format="%02.0f")
    app.minute_spinbox.pack(side=tk.LEFT, padx=5)

    # Sound selection
    ttk.Label(parent, text="Select Sound").grid(row=1, column=0, pady=5, sticky="e")
    sound_frame = ttk.Frame(parent)
    sound_frame.grid(row=1, column=1, pady=5, sticky="w")
    app.sound_path = tk.StringVar(value="default_alarm.wav")
    browse_button = ttk.Button(sound_frame, text="Browse", command=lambda: browse_sound(app))
    browse_button.pack(side=tk.LEFT, padx=5)
    # Add a label to show selected file
    app.sound_label = ttk.Label(sound_frame, textvariable=app.sound_path, wraplength=300)
    app.sound_label.pack(side=tk.LEFT, padx=5)

    # Note input
    ttk.Label(parent, text="Note (Optional)").grid(row=2, column=0, pady=5, sticky="e")
    app.note_entry = ttk.Entry(parent)
    app.note_entry.grid(row=2, column=1, pady=5, sticky="ew")

    # Set alarm button
    ttk.Button(parent, text="Set Alarm", command=lambda: set_alarm(app)).grid(row=3, column=0, columnspan=2, pady=10)

    # Alarm list
    app.alarm_listbox = tk.Listbox(
        parent,
        height=10,
        width=50,
        bg=colors['light' if not is_dark_mode else 'dark']['listbox_bg'],
        fg=colors['light' if not is_dark_mode else 'dark']['listbox_fg'],
        selectmode=tk.SINGLE
    )
    app.alarm_listbox.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")
    app.update_alarm_listbox = lambda: update_alarm_listbox(app)
    app.update_alarm_listbox()

    # Delete alarm button
    ttk.Button(parent, text="Delete Selected Alarm", command=lambda: delete_alarm(app)).grid(row=5, column=0, columnspan=2, pady=5)

def setup_timer_interface(app, parent):
    """Setup the timer interface components"""
    ttk.Label(parent, text="Set Timer (minutes)").grid(row=0, column=0, pady=5)
    app.timer_entry = ttk.Entry(parent)
    app.timer_entry.grid(row=0, column=1, pady=5)

    app.timer_display = ttk.Label(parent, text="00:00:00", font=("Arial", 24))
    app.timer_display.grid(row=1, column=0, columnspan=2, pady=10)

    app.timer_start_button = ttk.Button(parent, text="Start", command=lambda: start_timer(app))
    app.timer_start_button.grid(row=2, column=0, pady=5)
    app.timer_stop_button = ttk.Button(parent, text="Stop", command=app.stop_timer, state=tk.DISABLED)
    app.timer_stop_button.grid(row=2, column=1, pady=5)

def setup_stopwatch_interface(app, parent):
    """Setup the stopwatch interface components"""
    app.stopwatch_display = ttk.Label(parent, text="00:00:00", font=("Arial", 24))
    app.stopwatch_display.grid(row=0, column=0, columnspan=2, pady=10)

    app.stopwatch_start_button = ttk.Button(parent, text="Start", command=lambda: start_stopwatch(app))
    app.stopwatch_start_button.grid(row=1, column=0, pady=5)
    app.stopwatch_stop_button = ttk.Button(parent, text="Stop", command=app.stop_stopwatch, state=tk.DISABLED)
    app.stopwatch_stop_button.grid(row=1, column=1, pady=5)
    app.stopwatch_reset_button = ttk.Button(parent, text="Reset", command=lambda: reset_stopwatch(app))
    app.stopwatch_reset_button.grid(row=2, column=0, columnspan=2, pady=5)

def apply_theme(style, root, main_frame, alarm_listbox, colors, is_dark_mode):
    """Apply the current theme to all widgets"""
    theme = 'dark' if is_dark_mode else 'light'
    theme_colors = colors[theme]

    style.configure('TFrame', background=theme_colors['bg'])
    style.configure('TLabel', background=theme_colors['bg'], foreground=theme_colors['fg'])
    style.configure('TButton', background=theme_colors['button_bg'], foreground=theme_colors['button_fg'])
    style.configure('TEntry', fieldbackground=theme_colors['entry_bg'], foreground=theme_colors['entry_fg'])
    style.configure('TNotebook', background=theme_colors['tab_bg'])
    style.configure('TNotebook.Tab', background=theme_colors['tab_bg'], foreground='#000000')

    root.configure(bg=theme_colors['bg'])
    main_frame.configure(style='TFrame')

    if alarm_listbox:
        alarm_listbox.configure(
            bg=theme_colors['listbox_bg'],
            fg=theme_colors['listbox_fg'],
            selectbackground=theme_colors['selected_bg'],
            selectforeground=theme_colors['selected_fg']
        )

def browse_sound(app):
    """Open file dialog to select alarm sound"""
    try:
        # Get user's home directory as a starting point
        initial_dir = os.path.expanduser("~")
        
        file = filedialog.askopenfilename(
            parent=app.root,  # Set parent window
            initialdir=initial_dir,  # Start from user's home directory
            title="Select Alarm Sound",
            filetypes=[
                ("Audio Files", "*.wav *.mp3"),
                ("WAV files", "*.wav"),
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            ]
        )
        
        if file and os.path.exists(file):
            app.sound_path.set(file)
            print(f"Selected sound file: {file}")  # Debug print
    except Exception as e:
        print(f"Error in file dialog: {e}")
        messagebox.showerror("Error", f"Could not open file dialog: {str(e)}")

def set_alarm(app):
    """Set a new alarm"""
    try:
        hour = int(app.hour_spinbox.get())
        minute = int(app.minute_spinbox.get())
        time_str = f"{hour:02d}:{minute:02d}"
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        messagebox.showerror("Error", "Invalid time format. Use 24-hour format (00-23:00-59).")
        return

    sound_path = app.sound_path.get()
    note = app.note_entry.get()

    app.db.save_alarm(time_str, sound_path, note)
    app.alarms.append({"time": time_str, "sound_path": sound_path, "note": note})
    app.update_alarm_listbox()

    app.hour_spinbox.set("00")
    app.minute_spinbox.set("00")
    app.note_entry.delete(0, tk.END)
    app.sound_path.set("default_alarm.wav")

    messagebox.showinfo("Success", "Alarm set successfully!")

def update_alarm_listbox(app):
    """Update the alarm list display"""
    app.alarm_listbox.delete(0, tk.END)
    for alarm in app.alarms:
        # Only display time and note, omit sound path
        display_text = f"{alarm['time']} - {alarm['note']}" if alarm['note'] else f"{alarm['time']}"
        app.alarm_listbox.insert(tk.END, display_text)

def delete_alarm(app):
    """Delete selected alarm"""
    selection = app.alarm_listbox.curselection()
    if not selection:
        messagebox.showerror("Error", "Select an alarm to delete.")
        return

    index = selection[0]
    alarm = app.alarms[index]
    app.db.delete_alarm(alarm)
    app.alarms.pop(index)
    app.update_alarm_listbox()

def start_timer(app):
    """Start the timer"""
    try:
        minutes = int(app.timer_entry.get())
        app.timer_seconds = minutes * 60
        app.timer_running = True
        app.timer_start_button.config(state=tk.DISABLED)
        app.timer_stop_button.config(state=tk.NORMAL)
        update_timer(app)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of minutes.")

def update_timer(app):
    """Update the timer display"""
    if hasattr(app, 'timer_running') and app.timer_running:
        if app.timer_seconds > 0:
            hours = app.timer_seconds // 3600
            minutes = (app.timer_seconds % 3600) // 60
            seconds = app.timer_seconds % 60
            app.timer_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            app.timer_seconds -= 1
            app.root.after(1000, lambda: update_timer(app))
        else:
            timer_complete(app)

def timer_complete(app):
    """Handle timer completion"""
    app.timer_running = False
    app.timer_start_button.config(state=tk.NORMAL)
    app.timer_stop_button.config(state=tk.DISABLED)
    messagebox.showinfo("Timer Complete", "Your timer has finished!")
    app.audio.play_alarm("default_alarm.wav")

def start_stopwatch(app):
    """Start the stopwatch"""
    app.stopwatch_running = True
    app.stopwatch_start_button.config(state=tk.DISABLED)
    app.stopwatch_stop_button.config(state=tk.NORMAL)
    app.stopwatch_seconds = 0
    update_stopwatch(app)

def update_stopwatch(app):
    """Update the stopwatch display"""
    if hasattr(app, 'stopwatch_running') and app.stopwatch_running:
        hours = app.stopwatch_seconds // 3600
        minutes = (app.stopwatch_seconds % 3600) // 60
        seconds = app.stopwatch_seconds % 60
        app.stopwatch_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        app.stopwatch_seconds += 1
        app.root.after(1000, lambda: update_stopwatch(app))

def reset_stopwatch(app):
    """Reset the stopwatch"""
    app.stopwatch_running = False
    app.stopwatch_seconds = 0
    app.stopwatch_display.config(text="00:00:00")
    app.stopwatch_start_button.config(state=tk.NORMAL)
    app.stopwatch_stop_button.config(state=tk.DISABLED)