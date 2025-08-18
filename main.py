import json
from openai import OpenAI
from midiutil import MIDIFile
import re
import os

# API key to access OpenAI 
API_KEY = os.getenv("OPENAI_API_KEY") # put your own api key


# Creates the OpenAI client using the key
client = OpenAI(api_key = API_KEY)

#                                                    === Dictionaries ===

# Dictionary: translation from notes(C4) to pich(60)
note_to_midi = {
    # Octave 0
    "C0": 12, "C#0": 13, "Db0": 13,
    "D0": 14, "D#0": 15, "Eb0": 15,
    "E0": 16,
    "F0": 17, "F#0": 18, "Gb0": 18,
    "G0": 19, "G#0": 20, "Ab0": 20,
    "A0": 21, "A#0": 22, "Bb0": 22,
    "B0": 23,

    # Octave 1
    "C1": 24, "C#1": 25, "Db1": 25,
    "D1": 26, "D#1": 27, "Eb1": 27,
    "E1": 28,
    "F1": 29, "F#1": 30, "Gb1": 30,
    "G1": 31, "G#1": 32, "Ab1": 32,
    "A1": 33, "A#1": 34, "Bb1": 34,
    "B1": 35,

    # Octave 2
    "C2": 36, "C#2": 37, "Db2": 37,
    "D2": 38, "D#2": 39, "Eb2": 39,
    "E2": 40,
    "F2": 41, "F#2": 42, "Gb2": 42,
    "G2": 43, "G#2": 44, "Ab2": 44,
    "A2": 45, "A#2": 46, "Bb2": 46,
    "B2": 47,

    # Octave 3
    "C3": 48, "C#3": 49, "Db3": 49,
    "D3": 50, "D#3": 51, "Eb3": 51,
    "E3": 52,
    "F3": 53, "F#3": 54, "Gb3": 54,
    "G3": 55, "G#3": 56, "Ab3": 56,
    "A3": 57, "A#3": 58, "Bb3": 58,
    "B3": 59,

    # Octave 4
    "C4": 60, "C#4": 61, "Db4": 61,
    "D4": 62, "D#4": 63, "Eb4": 63,
    "E4": 64,
    "F4": 65, "F#4": 66, "Gb4": 66,
    "G4": 67, "G#4": 68, "Ab4": 68,
    "A4": 69, "A#4": 70, "Bb4": 70,
    "B4": 71,

    # Octave 5
    "C5": 72, "C#5": 73, "Db5": 73,
    "D5": 74, "D#5": 75, "Eb5": 75,
    "E5": 76,
    "F5": 77, "F#5": 78, "Gb5": 78,
    "G5": 79, "G#5": 80, "Ab5": 80,
    "A5": 81, "A#5": 82, "Bb5": 82,
    "B5": 83,

    # Octave 6
    "C6": 84, "C#6": 85, "Db6": 85,
    "D6": 86, "D#6": 87, "Eb6": 87,
    "E6": 88,
    "F6": 89, "F#6": 90, "Gb6": 90,
    "G6": 91, "G#6": 92, "Ab6": 92,
    "A6": 93, "A#6": 94, "Bb6": 94,
    "B6": 95,

    # Octave 7
    "C7": 96, "C#7": 97, "Db7": 97,
    "D7": 98, "D#7": 99, "Eb7": 99,
    "E7": 100,
    "F7": 101, "F#7": 102, "Gb7": 102,
    "G7": 103, "G#7": 104, "Ab7": 104,
    "A7": 105, "A#7": 106, "Bb7": 106,
    "B7": 107,

    # Octave 8
    "C8": 108, "C#8": 109, "Db8": 109,
    "D8": 110, "D#8": 111, "Eb8": 111,
    "E8": 112,
    "F8": 113, "F#8": 114, "Gb8": 114,
    "G8": 115, "G#8": 116, "Ab8": 116,
    "A8": 117, "A#8": 118, "Bb8": 118,
    "B8": 119,
}


# Dictionary: grouping sets of already translated notes and making chords 
chords = {
    # Major Triads
    "C":  ["C4", "E4", "G4"],
    "C#": ["C#4", "F4", "G#4"],
    "D":  ["D4", "F#4", "A4"],
    "D#": ["D#4", "G4", "A#4"],
    "E":  ["E4", "G#4", "B4"],
    "F":  ["F4", "A4", "C5"],
    "F#": ["F#4", "A#4", "C#5"],
    "G":  ["G4", "B4", "D5"],
    "G#": ["G#4", "C5", "D#5"],
    "A":  ["A4", "C#5", "E5"],
    "A#": ["A#4", "D5", "F5"],
    "B":  ["B4", "D#5", "F#5"],

    # Minor Triads
    "Cm":  ["C4", "D#4", "G4"],
    "C#m": ["C#4", "E4", "G#4"],
    "Dm":  ["D4", "F4", "A4"],
    "D#m": ["D#4", "F#4", "A#4"],
    "Em":  ["E4", "G4", "B4"],
    "Fm":  ["F4", "G#4", "C5"],
    "F#m": ["F#4", "A4", "C#5"],
    "Gm":  ["G4", "A#4", "D5"],
    "G#m": ["G#4", "B4", "D#5"],
    "Am":  ["A4", "C5", "E5"],
    "A#m": ["A#4", "C#5", "F5"],
    "Bm":  ["B4", "D5", "F#5"],

    # Dominant 7th (7)
    "C7":  ["C4", "E4", "G4", "A#4"],
    "C#7": ["C#4", "F4", "G#4", "B4"],
    "D7":  ["D4", "F#4", "A4", "C5"],
    "D#7": ["D#4", "G4", "A#4", "C#5"],
    "E7":  ["E4", "G#4", "B4", "D5"],
    "F7":  ["F4", "A4", "C5", "D#5"],
    "F#7": ["F#4", "A#4", "C#5", "E5"],
    "G7":  ["G4", "B4", "D5", "F5"],
    "G#7": ["G#4", "C5", "D#5", "F#5"],
    "A7":  ["A4", "C#5", "E5", "G5"],
    "A#7": ["A#4", "D5", "F5", "G#5"],
    "B7":  ["B4", "D#5", "F#5", "A5"],

    # Major 7th (maj7)
    "Cmaj7": ["C4", "E4", "G4", "B4"],
    "C#maj7": ["C#4", "F4", "G#4", "C5"],
    "Dmaj7": ["D4", "F#4", "A4", "C#5"],
    "D#maj7": ["D#4", "G4", "A#4", "D5"],
    "Emaj7": ["E4", "G#4", "B4", "D#5"],
    "Fmaj7": ["F4", "A4", "C5", "E5"],
    "F#maj7": ["F#4", "A#4", "C#5", "F5"],
    "Gmaj7": ["G4", "B4", "D5", "F#5"],
    "G#maj7": ["G#4", "C5", "D#5", "G5"],
    "Amaj7": ["A4", "C#5", "E5", "G#5"],
    "A#maj7": ["A#4", "D5", "F5", "A5"],
    "Bmaj7": ["B4", "D#5", "F#5", "A#5"],

    # Minor 7th (m7)
    "Cm7":  ["C4", "D#4", "G4", "A#4"],
    "C#m7": ["C#4", "E4", "G#4", "B4"],
    "Dm7":  ["D4", "F4", "A4", "C5"],
    "D#m7": ["D#4", "F#4", "A#4", "C#5"],
    "Em7":  ["E4", "G4", "B4", "D5"],
    "Fm7":  ["F4", "G#4", "C5", "D#5"],
    "F#m7": ["F#4", "A4", "C#5", "E5"],
    "Gm7":  ["G4", "A#4", "D5", "F5"],
    "G#m7": ["G#4", "B4", "D#5", "F#5"],
    "Am7":  ["A4", "C5", "E5", "G5"],
    "A#m7": ["A#4", "C#5", "F5", "G#5"],
    "Bm7":  ["B4", "D5", "F#5", "A5"],

    # Diminished triads (dim)
    "Cdim": ["C4", "D#4", "F#4"],
    "C#dim": ["C#4", "E4", "G4"],
    "Ddim": ["D4", "F4", "G#4"],
    "D#dim": ["D#4", "F#4", "A4"],
    "Edim": ["E4", "G4", "A#4"],
    "Fdim": ["F4", "G#4", "B4"],
    "F#dim": ["F#4", "A4", "C5"],
    "Gdim": ["G4", "A#4", "C#5"],
    "G#dim": ["G#4", "B4", "D5"],
    "Adim": ["A4", "C5", "D#5"],
    "A#dim": ["A#4", "C#5", "E5"],
    "Bdim": ["B4", "D5", "F5"],

    # Half-diminished (m7b5)
    "Cm7b5": ["C4", "D#4", "F#4", "A#4"],
    "C#m7b5": ["C#4", "E4", "G4", "B4"],
    "Dm7b5": ["D4", "F4", "G#4", "C5"],
    "D#m7b5": ["D#4", "F#4", "A4", "C#5"],
    "Em7b5": ["E4", "G4", "A#4", "D5"],
    "Fm7b5": ["F4", "G#4", "B4", "D#5"],
    "F#m7b5": ["F#4", "A4", "C5", "E5"],
    "Gm7b5": ["G4", "A#4", "C#5", "F5"],
    "G#m7b5": ["G#4", "B4", "D5", "F#5"],
    "Am7b5": ["A4", "C5", "D#5", "G5"],
    "A#m7b5": ["A#4", "C#5", "E5", "G#5"],
    "Bm7b5": ["B4", "D5", "F5", "A5"],

    # Augmented (aug)
    "Caug": ["C4", "E4", "G#4"],
    "C#aug": ["C#4", "F4", "A4"],
    "Daug": ["D4", "F#4", "A#4"],
    "D#aug": ["D#4", "G4", "B4"],
    "Eaug": ["E4", "G#4", "C5"],
    "Faug": ["F4", "A4", "C#5"],
    "F#aug": ["F#4", "A#4", "D5"],
    "Gaug": ["G4", "B4", "D#5"],
    "G#aug": ["G#4", "C5", "E5"],
    "Aaug": ["A4", "C#5", "F5"],
    "A#aug": ["A#4", "D5", "F#5"],
    "Baug": ["B4", "D#5", "G5"],
    # Sixth chords
    "C6":      ["C4", "E4", "G4", "A4"],
    "Cm6":     ["C4", "D#4", "G4", "A4"],

    # Ninth chords
    "C9":      ["C4", "E4", "G4", "A#4", "D5"],
    "Cm9":     ["C4", "D#4", "G4", "A#4", "D5"],
    "Cmaj9":   ["C4", "E4", "G4", "B4", "D5"],

    # Eleventh chords
    "C11":     ["C4", "E4", "G4", "A#4", "D5", "F5"],
    "Cm11":    ["C4", "D#4", "G4", "A#4", "D5", "F5"],
    "Cmaj11":  ["C4", "E4", "G4", "B4", "D5", "F5"],

    # Thirteenth chords
    "C13":     ["C4", "E4", "G4", "A#4", "D5", "F5", "A5"],
    "Cm13":    ["C4", "D#4", "G4", "A#4", "D5", "F5", "A5"],
    "Cmaj13":  ["C4", "E4", "G4", "B4", "D5", "F5", "A5"],

    # Suspended chords
    "Csus2":   ["C4", "D4", "G4"],
    "Csus4":   ["C4", "F4", "G4"],

    # Add chords
    "Cadd9":   ["C4", "E4", "G4", "D5"],
    "Cmadd9":  ["C4", "D#4", "G4", "D5"],

    # Fully Diminished Seventh
    "Cdim7":   ["C4", "D#4", "F#4", "A4"],

    # Add9 chords 
    "C#add9": ["C#4", "F4", "G#4", "D#5"],
    "Dadd9":  ["D4", "F#4", "A4", "E5"],
    "D#add9": ["D#4", "G4", "A#4", "F5"],
    "Eadd9":  ["E4", "G#4", "B4", "F#5"],
    "Fadd9":  ["F4", "A4", "C5", "G5"],
    "F#add9": ["F#4", "A#4", "C#5", "G#5"],
    "Gadd9":  ["G4", "B4", "D5", "A5"],
    "G#add9": ["G#4", "C5", "D#5", "A#5"],
    "Aadd9":  ["A4", "C#5", "E5", "B5"],
    "A#add9": ["A#4", "D5", "F5", "C6"],
    "Badd9":  ["B4", "D#5", "F#5", "C#6"],

    #minor add9
        "C#madd9": ["C#4", "E4", "G#4", "D#5"],
    "Dmadd9":  ["D4", "F4", "A4", "E5"],
    "D#madd9": ["D#4", "F#4", "A#4", "F5"],
    "Emadd9":  ["E4", "G4", "B4", "F#5"],
    "Fmadd9":  ["F4", "G#4", "C5", "G5"],
    "F#madd9": ["F#4", "A4", "C#5", "G#5"],
    "Gmadd9":  ["G4", "A#4", "D5", "A5"],
    "G#madd9": ["G#4", "B4", "D#5", "A#5"],
    "Amadd9":  ["A4", "C5", "E5", "B5"],
    "A#madd9": ["A#4", "C#5", "F5", "C6"],
    "Bmadd9":  ["B4", "D5", "F#5", "C#6"],

    #maj9
    "C#maj9": ["C#4", "F4", "G#4", "C5", "D#5"],
    "Dmaj9":  ["D4", "F#4", "A4", "C#5", "E5"],
    "D#maj9": ["D#4", "G4", "A#4", "D5", "F5"],
    "Emaj9":  ["E4", "G#4", "B4", "D#5", "F#5"],
    "Fmaj9":  ["F4", "A4", "C5", "E5", "G5"],
    "F#maj9": ["F#4", "A#4", "C#5", "F5", "G#5"],
    "Gmaj9":  ["G4", "B4", "D5", "F#5", "A5"],
    "G#maj9": ["G#4", "C5", "D#5", "G5", "A#5"],
    "Amaj9":  ["A4", "C#5", "E5", "G#5", "B5"],
    "A#maj9": ["A#4", "D5", "F5", "A5", "C6"],
    "Bmaj9":  ["B4", "D#5", "F#5", "A#5", "C#6"],

        # D9 chord (D dominant 9)
    "D9": ["D4", "F#4", "A4", "C5", "E5"],

    # Ebm7 chord (E-flat minor 7) = D#m7
    "Ebm7": ["D#4", "F#4", "A#4", "C#5"],

    # Abmaj7 chord (A-flat major 7) = G#maj7
    "Abmaj7": ["G#4", "C5", "D#5", "G5"],

    # Db7 chord (D-flat dominant 7) = C#7
    "Db7": ["C#4", "F4", "G#4", "B4"]

}


#                                               === OpenAI prompt analysing function ===

# Function sends a music-related message to GPT and returns a structured result using JSON
def analyse_music_instructions(user_text):
  
    # Keywords that trigger creative prompt generation
    generation_keywords = ["compose", "generate", "make me", "do me a", "create a"]

    if any(keyword in user_text.lower() for keyword in generation_keywords):
        print("Detected creative prompt. Generating structured music data...")
        
        # Creative music generation prompt
        prompt = f"""
You are a creative music composer assistant.

Based on the input: "{user_text}" 

Generate a music piece as structured JSON.

Only include the following fields:
- "chord_progression": a list of chords with durations (e.g. [{{"chord":"Am7", "duration":1}}, ...]) — use "Dm7" not "Dmin7", and "C" not "Cmaj". Use "Ddim" for diminished chords.
- "chord_loop": how many times to repeat the progression
- "melody": a list of notes with durations (e.g. [{{"note":"C#4", "duration":1}}, ...])
- "melody_loop": how many times to repeat the melody

Only return valid JSON — no extra commentary, no markdown.
"""
        temperature = 1.2 # Creativity is set

    else:
        # Try analysing direct JSON 
        try:
            return json.loads(user_text)
        except json.JSONDecodeError:
            print("Direct JSON analyse failed. Trying extraction with structured prompt...")

        # Extraction prompt if JSON analysing failed (if the key words failed to be found)
        prompt = f"""
You are a helpful assistant that extracts music information from user instructions.

Input: "{user_text}"

Extract:
- chord_progression: list of chords with optional durations (e.g. [{{"chord":"C", "duration":1}}, {{"chord":"Gm7", "duration":2}}])
- loop: number of repeats (default 1 if not mentioned)
- melody: list of notes with optional durations (e.g. [{{"note":"C#4", "duration":1}}])
ifUse "rest" with a duration to indicate silence, (e.g., [{{"note":"rest", "duration":1}}] for melody or [{{"chord":"rest","duration":1}}]) for chords.
Correct chord and note names if needed.

Output the extracted data in JSON format. No explanation, no comments.
"""
        temperature = 0
    # Ask Ai to reply using OpenAI chat completion, in this case gpt-4o-mini model.
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a music assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=1000
        )
      # Extract the AI’s reply text from the first choice.
      # This gets the actual message content "a string" from the response object
      # We use .strip() to remove any extra spaces or newlines around the JSON,
      # which helps prevent errors when analysing the JSON later,
      # even if the prompt asks for clean output with no extra text chat gpt might not always be obidiant.
        text_response = response.choices[0].message.content.strip()

        # Handle code block formatting (If the reply starts with ```json, remove those markers so we get clean JSON)
        if text_response.startswith("```json"):
            text_response = text_response.replace("```json", "").replace("```", "").strip()

        # Try to find JSON data inside the reply with re.search method
        json_match = re.search(r'\{.*\}', text_response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())  # Convert JSON text to a Python object (Dictionary Style) and return it
        else:  
            # If no JSON found, show the full reply so you can see what went wrong
            print("Failed to extract JSON from model output:")
            print(text_response)
            return None
        
  # If something goes wrong, print the error message
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

#                                                 === CHAT BOT === Function not yet implemented for optimization in testing purposes.


#                                                === MIDI utility functions ===

# Function to add a note by its name
def add_named_note(midi, note_name, start_time, duration, track=1):
    # Handle rest (pause) notes by skipping adding a note but advancing time (handled by caller)
    if note_name.lower() == "rest":
        # No note to add, just skip adding anything
        return

    pitch = note_to_midi.get(note_name)  # Calls the translated note from the dictionary and fills in the function's argument
    if pitch is None:
        print(f'Note "{note_name}" not found/ non existant !')
        return  # Exit early if the note is invalid
    
    # This only runs if the note is valid
    midi.addNote(track=track, channel=0, pitch=pitch, time=start_time, duration=duration, volume=100) # Take our midifile and use the built in add note funciton. replaces pitch with the pitch of the note the user chose.

# Function to add a chord by its name 
def add_chord(midi, chord_name, start_time, duration, track=0):
    # Handle rest (pause) chords by skipping note addition but advancing time
    if chord_name.lower() == "rest":
        # No notes to add, just skip chord insertion (time will be handled by caller)
        return
    
    notes = chords.get(chord_name)  # Calls the group of notes from the chord's dictionary and fills in the function's argument
    if notes is None:
        print(f'Chord "{chord_name}" not found/ non existent!')
        return  
        
    
    # This only runs if the chord is valid
    for note in notes: 
        # Go through each note in the chord : C (a list of note names : ["C4", "E4", "G4"])
        # and add it to the MIDI track one at a time
        add_named_note(midi, note, start_time, duration)



#                                                     === Main Program === 
def main():
 if __name__ == "__main__":
    main()    
    user_prompt = (
  "🎶 Welcome to the Music Generator!\n\n"
    "Please enter your chord progression using chord names separated by spaces, for example: C Am F G\n"
    "To include a rest (silence), type 'rest' instead of a chord or note.\n\n"
    "Next, specify the duration (in beats) for each chord or note, also separated by spaces, like: 1 2 1 1.\n"
    "→ The number of durations must match the number of chords or notes.\n\n"
    "You may also enter a melody using note names with spaces, for example: C4 E4 G4 rest A4.\n"
    "'rest' will insert a silence in the melody.\n\n"
    "Then, provide melody durations in the same format: 1 1 1 2 1.\n\n"
    "Example input:\n"
    "chords: C Am rest F\n"
    "durations: 1 2 2 1\n"
    "melody: C4 E4 rest G4 A4\n"
    "melody durations: 1 1 1 2 1\n\n"
    "If you'd like to specify a genre or add specific instructions, feel free to mention them.\n"
    "When you're ready to generate the music, just type 'generate'.\n\n"
    "Let's create something amazing! 🎧\n"
)
    print(user_prompt)

    # Step 1: user gives natural language Instructions
    instruction = input("Enter your instructions: ")

    # Step 2: Get AI to extract the the structrued music info
    music_data = analyse_music_instructions(instruction)
    if not music_data:
        print("No music data received, exiting.")
        return

    
    chord_progression = music_data.get("chord_progression", []) 
    melody = music_data.get("melody", [])
    chord_loop = music_data.get("chord_loop", music_data.get("loop", 1))  # Fallback to loop if chord_loop missing
    melody_loop = music_data.get("melody_loop", 1)  # melody loop defaults to 1 if missing
    
    # Step 3: Create MIDI File
    midi = MIDIFile(2)  # One MIDI file with 2 tracks: 0 = Chords, 1 = Melody
    midi.addTempo(0, 0, 120)
    midi.addTempo(1, 0, 120)

    # Step 4: Add chords within looping                    === Add The Chords ===

    # Loops through the chord progression 'chord_loop' times.
    # Each chord is added to Track 0 with its specified duration.
    # The 'time' variable tracks the running start time of each chord.
    time = 0
    for _ in range(chord_loop):  # Repeat the chord progression 'chord_loop' times
         for chord_obj in chord_progression:  # Loop through each chord in the progression
            chord = chord_obj["chord"]  # Extract the chord from the current chord object(item) being analysed 
            dur = chord_obj.get("duration", 1)  # Get the chord's duration from the current(item), default to 1 if missing
            add_chord(midi, chord, time, dur, track=0)  # Add the chord to MIDI Track 0 at current time
            time += dur  # Advance the start time by the chord's duration for the next chord

    # Step 5: Add melody on top                             === Add melody ===

    # Adds each note from the melody list to Track 1.
    # The melody starts from time 0 and runs linearly.
    # Loops through the melody 'melody_loop' times.
    time = 0  # Initialize the starting time for the first note

    for _ in range(melody_loop):  # Repeat the melody 'melody_loop' times
        for note_obj in melody:  # Loop through each note object (item) in the melody list
            note = note_obj["note"]  # Extract the note name or pitch from the current note object
            dur = note_obj.get("duration", 1)  # Get the note duration, default to 1 if not specified
            add_named_note(midi, note, time, dur, track=0)  # Add the note to MIDI Track 0 at current time
            time += dur  # Advance the start time by the note's duration for the next note                                                 
    #                                         === Save the MIDI File === 


#   Write binary file to export into a midi file what we just wrote
    with open ("Named_notes.mid", "wb") as output_file:
        midi.writeFile(output_file)
        print("MIDI file created with named Notes")

        



# === Run the Program ===
main()
