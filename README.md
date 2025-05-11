# Smart Alarm Clock ⏰

A modern, customizable smart alarm clock built with Python and Tkinter. Features include setting multiple alarms, browsing custom alarm sounds, dark mode toggle, and more.

---

## 🖼️ UI Preview

![UI Preview](path/to/screenshot.png) <!-- Replace with actual image link if hosted -->

---

## 🚀 Features

- ⏰ Set new alarms with hour, minute, optional note, and sound
- 🎵 Browse and assign custom alarm sounds
- 🌙 Toggle between light and dark mode
- 📝 View, delete, and manage active alarms
- 📁 Persistent alarm data using SQLite
- 🧭 Timer and Stopwatch functionality (tabbed UI)

---

## 📁 Project Structure


## Project Structure
```
AlarmClock/
├── src/
│ ├── core/ # Alarm logic and database interaction
│ ├── data/ # SQLite database file
│ ├── ui/ # User interface files (modern_ui.py, ui_components.py)
│ └── utils/ # Helpers: audio manager, constants, defaults
│
├── main.py # App entry point
├── requirements.txt # Project dependencies
├── README.md # Project description
├── alarms.db # Local SQLite database (auto-generated)
└── .gitignore

yaml

```

## Setup
1. Create a virtual environment:
   ```
   python -m venv .venv
   ```
   

2. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   

4. Add a default alarm sound:
   - Place a WAV file named `default_alarm.wav` in the `sounds` directory

## Usage
Run the application:
python main.py
```
python main.py
```

📌 Notes
Alarm sounds can be any compatible audio file (e.g., .mp3, .wav).

All alarms are stored locally in alarms.db.

## Requirements
- Python 3.6 or higher
- pygame 2.6.1
- tkinter (usually comes with Python) 
