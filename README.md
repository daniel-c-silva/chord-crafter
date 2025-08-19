# chord-crafter

A Python tool that uses OpenAI's **gpt-4o-mini** model and **MIDIUtil** to generate MIDI files from text or structured music instructions. Comes with a Flask-based web interface and a CLI for easy interaction.

![A GIF of the real-time C-nebot dashboard in action](https://github.com/daniel-c-silva/chord-crafter/blob/main/Assets/chordcraft.gif?raw=true)

---

## Overview

**chord-crafter** lets you compose music by simply typing chord progressions or melody instructions in natural language or structured format. It uses OpenAI’s GPT model to interpret your input and converts it into MIDI files you can download or play.

---

## Features

- Generate chord progressions and melodies from text input
- Converts instructions into structured chord and note data
- Creates MIDI files with specified tempo, chords, and melodies
- Web app interface with chat-like experience for easy input and download
- CLI mode for quick command-line interaction

---

## How It Works

1. **Input:** Provide music instructions as text (e.g., “Play C major, then Am7 for 2 beats”).
2. **Processing:** The OpenAI GPT-4o-mini model analyzes the instructions and outputs structured music data.
3. **MIDI Generation:** MIDIUtil adds chords and notes to tracks with specified durations and tempo.
4. **Output:** MIDI file is created and encoded in base64 to be sent back to the web client or saved locally.

---

## Getting Started

### Prerequisites

- Python 3.x
- OpenAI API key with access to GPT-4o-mini
- Install dependencies:

```bash
pip install Flask MIDIUtil openai
Running the Web App
Set your OpenAI API key as an environment variable:

bash
export OPENAI_API_KEY='your_api_key_here'
Run the Flask app:

bash
python main.py
Open your browser and navigate to http://localhost:5000

Using the CLI
Run the CLI interface with:

bash
python cli.py
Follow the prompts to input your chord progressions and generate MIDI files from the terminal.

Project Structure
app.py — Flask web app to serve the chat interface and handle music generation requests.

cli.py — Command-line interface for generating music.

main.py — Core functions including music instruction analysis, chord/note adding, and MIDI file handling.

templates/index.html — HTML template for the web UI.

static/ — Optional folder for static files like CSS or JS (if you extend UI).

Example
python
# Example chord progression
chord_progression = [
    {"chord": "Cmaj7", "duration": 2},
    {"chord": "Am7", "duration": 1},
    {"chord": "Dm7", "duration": 1},
    {"chord": "G7", "duration": 2}
]

time = 0
for _ in range(2):  # repeat twice
    for chord_obj in chord_progression:
        add_chord(midi, chord_obj["chord"], time, chord_obj.get("duration", 1), track=0)
        time += chord_obj.get("duration", 1)
License
MIT License

Acknowledgments
Powered by OpenAI GPT-4o-mini

MIDI file creation via MIDIUtil
````

## Audio & MIDI Samples

Chord-Crafter generates MIDI files that you can download or play. Some sample files included in this repo:

- [Sample MIDI 1](https://github.com/daniel-c-silva/chord-crafter/blob/main/Assets/generated (3).mid?raw=true)

You can also listen directly in your browser:

### Play Sample 1
<audio controls>
  <source src="https://github.com/yourusername/chord-crafter/blob/main/Assets/Audio/sample1.mid?raw=true" type="audio/midi">
  Your browser does not support the audio element.
</audio>

```bash
## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```
