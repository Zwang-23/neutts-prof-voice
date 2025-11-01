import soundfile as sf
import numpy as np
from neuttsair.neutts import NeuTTSAir
from flask import Flask, request, jsonify, send_file
import io # Used to send file data from memory

print("--- TTS Server Starting Up ---")
ref_text_path = "samples/prof.txt"
ref_audio_path = "samples/prof.wav"
# --- ONE-TIME SETUP: Load model and cache when the server starts ---
print("Initializing TTS model...")
tts = NeuTTSAir(
    backbone_repo="neuphonic/neutts-air-q4-gguf",
    backbone_device="cpu",
    codec_repo="neuphonic/neucodec",
    codec_device="cpu"
)

print("Loading reference voice from cache...")
try:
    with open(ref_text_path, "r") as f:
        reference_text = f.read().strip()
    
    reference_codes = tts.encode_reference(ref_audio_path)
    print("✅ Model and reference cache are ready!")
except FileNotFoundError:
    print("❌ CRITICAL ERROR: Cache files (ref_codes.npy, ref_text_cache.txt) not found.")
    print("Please run the 'create_reference_cache.py' script first.")
    exit()

# --- Initialize Flask App ---
app = Flask(__name__)

# Define an endpoint to generate speech
@app.route('/synthesize', methods=['POST'])
def synthesize_speech():
    # Get text from the incoming request's JSON body
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    input_text = data['text']
    print(f"Received request to synthesize: '{input_text[:50]}...'")

    # --- INFERENCE: This is now very fast ---
    wav = tts.infer(input_text, reference_codes, reference_text)

    if wav is not None:
        # Save the WAV data to an in-memory buffer
        buffer = io.BytesIO()
        sf.write(buffer, wav, 24000, format='WAV')
        buffer.seek(0) # Rewind the buffer to the beginning

        print("✅ Synthesis successful. Sending audio file.")
        # Send the buffer as a file download
        return send_file(
            buffer,
            as_attachment=True,
            download_name='output.wav',
            mimetype='audio/wav'
        )
    else:
        print("❌ Synthesis failed.")
        return jsonify({"error": "Failed to generate audio"}), 500

# --- Start the Server ---
if __name__ == '__main__':
    # Use host='0.0.0.0' to make it accessible from Docker networks
    app.run(host='0.0.0.0', port=5000)