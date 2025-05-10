# Smart Alarm Clock

A Python-based alarm clock application with a graphical user interface.

## Features
- Set multiple alarms with custom messages
- Choose custom alarm sounds (WAV or MP3)
- Snooze functionality (5 minutes)
- Dark/Light theme support

## Project Structure
```
AlarmClock/
├── src/
│   ├── core/         # Core functionality
│   ├── ui/           # User interface components
│   ├── utils/        # Utility functions
│   └── data/         # Data handling
├── sounds/           # Alarm sound files
└── requirements.txt  # Project dependencies
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
```
python main.py
```

## Requirements
- Python 3.6 or higher
- pygame 2.6.1
- tkinter (usually comes with Python) 