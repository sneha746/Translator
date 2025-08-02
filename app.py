from flask import Flask, jsonify, render_template
import numpy as np
import pyaudio
import random

app = Flask(__name__)

# Audio config
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1
THRESHOLD = 300

translations = [
    "The squirrels are plotting again. This is not a drill.",
    "I demand more snacks, or I shall revolt.",
    "I've seen things you wouldn't believe—vacuum cleaners with no mercy.",
    "Why do birds suddenly appear… every time I bark?",
    "I bark, therefore I am.",
    "Tell the humans: the cat knows something.",
    "Every time I bark, I feel alive.",
    "This bark was sponsored by Treats Unlimited™.",
    "Beware! The mailman returns at dawn.",
    "I had a dream… about the Big Bone again.",
]

p = pyaudio.PyAudio()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect-bark', methods=['GET'])
def detect_bark():
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    audio_data = b''.join(frames)
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    rms = np.sqrt(np.mean(audio_np.astype(np.float32)**2))

    if rms > THRESHOLD:
        translation = random.choice(translations)
        return jsonify({"bark": True, "message": "🐶 " + translation})
    else:
        return jsonify({"bark": False, "message": "No bark detected. Try again!"})

if __name__ == '__main__':
    app.run(debug=True)
