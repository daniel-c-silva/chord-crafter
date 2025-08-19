# Import necessary modules from Flask to create the web app and handle requests
from flask import Flask, render_template, request, jsonify

# Import functions and classes from your music processing module 'main.py'
from main import analyse_music_instructions, MIDIFile, add_chord, add_named_note

# Import modules to handle binary data and encoding
import base64
import io

from flask_cors import CORS

# Create an instance of the Flask class to start the web application
app = Flask(__name__)

CORS(app)  # allow frontend to talk to backend
# Define a route for the homepage ('/') using the HTTP GET method by default
@app.route('/')
def home():
    # Tells Flask to send the 'index.html' file to the user's browser when they visit the root URL
    return jsonify({"message": "API is running"}) # Potentially change this to "render_template("index.html")" if u want to run locally

# Define a route '/chat' that listens for POST requests from the client
@app.route('/chat', methods=['POST'])
def chat(): 
    # Tells Flask to extract the JSON data sent by the client and get the value of the 'message' key
    user_message = request.json.get('message')

    # Pass the user's text instructions to the 'analyse_music_instructions' function
    # This function tells the app how to interpret the music instructions into structured data
    music_data = analyse_music_instructions(user_message)

    # Check if the instructions were understood properly (if no data was returned)
    if not music_data:
        # Tells Flask to send back a JSON response with an error message if it couldn't understand the instructions
        return jsonify({'response': 'Sorry, I could not understand your music instructions.'})
    
    # Create a new MIDI file object with 2 tracks (one for chords, one for melody)
    midi = MIDIFile(2)

    # Tells each track to set the tempo to 120 beats per minute starting at time 0
    midi.addTempo(0, 0, 120)  # Track 0 (chords)
    midi.addTempo(1, 0, 120)  # Track 1 (melody)

    # Initialize the time cursor for chords to 0 beats
    time = 0

    # Loop through the chord progression as many times as specified by "chord_loop"
    for _ in range(music_data.get("chord_loop", 1)):
        # For each chord in the chord progression
        for chord in music_data.get("chord_progression", []):
            # Tells the MIDI file to add this chord at the current time on track 0
            # Duration of each chord is taken from the chord data, defaulting to 1 beat
            add_chord(midi, chord["chord"], time, chord.get("duration", 1), track=0)

            # Move the time cursor forward by the chord's duration for the next chord
            time += chord.get("duration", 1)

    # Reset the time cursor for the melody track back to 0 beats
    time = 0

    # Loop through the melody as many times as specified by "melody_loop"
    for _ in range(music_data.get("melody_loop", 1)):
        # For each note in the melody
        for note in music_data.get("melody", []):
            # Tells the MIDI file to add this named note at the current time on track 1
            # Duration of each note is taken from the note data, defaulting to 1 beat
            add_named_note(midi, note["note"], time, note.get("duration", 1), track=0)

            # Move the time cursor forward by the note's duration for the next note
            time += note.get("duration", 1)

    # Create an in-memory bytes buffer to store the MIDI file data
    output = io.BytesIO()

    # Tells the MIDI object to write the complete MIDI file data into the bytes buffer
    midi.writeFile(output)

    # Encode the MIDI data in base64 format so it can be safely sent over the internet as a string
    midi_data = base64.b64encode(output.getvalue()).decode("utf-8")

    # Tells Flask to send a JSON response back to the client containing:
    # - a message confirming the music was created
    # - the base64-encoded MIDI file data so it can be downloaded or played
    return jsonify({
        "response": "Here's your music!",
        "midi_b64": midi_data
    })

# This condition checks if this script is being run directly (not imported as a module)
if __name__ == '__main__':
    # Tells Flask to start the web server in debug mode, which shows errors and reloads automatically on code changes
    app.run(debug=True)
