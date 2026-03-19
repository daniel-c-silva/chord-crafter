# chord-crafter

**Prompt and Create, Stop and listen**

![A GIF of the real-time C-nebot dashboard in action](https://github.com/daniel-c-silva/chord-crafter/blob/main/Assets/chordcraft.gif?raw=true)

## **DISCLAIMER** There's a Demo Version, How ever my API token's have ran out.

## Overview

**chord-crafter** lets you compose music by typing chord progressions or melody instructions in natural language. It interprets input and converts it into MIDI files you can download or play.


## Features

- Generate chord progressions and melodies from text input
- Converts instructions into structured chord and note data
- Creates MIDI files with specified tempo, chords, and melodies
- Web app interface with chat for input and download

  
## How to Run Locally

### Prerequisites

- Python 3.x
- OpenAI API key with access to GPT-4o-mini
- Install dependencies:


## Backend Setup
```
Prerequisites: Python 3.x, OpenAI API key

cd chord-crafter
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your_api_key_here'

# Run the Flask app
python main.py
```

## Using the CLI
```
python cli.py
```
Follow the prompts to input your chord progressions and generate MIDI files.


## Web App

Open your browser and navigate to `http://localhost:5000` after running the Flask app.

## Audio & MIDI Samples

Chord-Crafter generates MIDI files that you can download or play. Some sample files included in this repo:

- [Sample MIDI](https://github.com/daniel-c-silva/chord-crafter/raw/main/Assets/generated-3.mid)

## Conclusion

Chord-crafter was my first full-stack project, as a musician I always thought of how useful an automated music generation midi app would be, so I decided that if I can't find one I might aswell build it. It was also my first time integrating AI and midi into any project, and while I found OpenAI's api syntax very simple and easy to work with using midi although "intuitive" proved difficult, specially because I had never had to deal with a dictionary function this complex. Being my first real project It really made me understand frontend to backend connection a little bit better.


## License

MIT License

**Acknowledgments:**
Powered by OpenAI GPT-4o-mini
MIDI file creation via MIDIUtil

