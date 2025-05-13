# Sleep
A system tray application for Windows that lets you manage sleep and delayed sleep timers with real-time countdown display.

## Features

- Put your computer to sleep instantly via tray menu
- Set a **delayed sleep timer** (e.g., 30 minutes)
- Tray icon dynamically updates with time remaining
- Tooltip shows real-time countdown (e.g., "Shutting down in 12 min 45 sec")
- Cancel delayed sleep anytime
- Prevents multiple timers from running at once (only one tray icon is shown)

## How It Works

When you launch the program, a tray icon will appear with a right-click menu:
- Sleep
- Delayed sleep
- Cancel delayed sleep
- Exit

## Requirements

- Python 3.7+
- Windows OS
- `PySimpleGUIQt`
- `Pillow`

Install dependencies using:

```bash
pip install PySimpleGUIQt pillow
```

## Running the App
Simply run the main script:

```bash
python sleep.py
```
The tray icon should appear immediately. No GUI window will open by default.

## Notes
- Tray icons are limited in size and shape by Windows, so wide icons are not supported.

- Only one active delayed sleep countdown is allowed at a time.
