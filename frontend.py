#!/usr/bin/env python3
"""
Simple Docker Web App using existing TTS server
This approach uses your working tt4api.py as a backend service
"""

from flask import Flask, render_template, request, jsonify, send_file
import requests
import re
import tempfile
import time
from pydub import AudioSegment
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# TTS server URL
TTS_SERVER_URL = os.getenv('TTS_SERVER_URL', 'http://localhost:5000/synthesize')

def chunk_text(text):
    """Split text into chunks for processing"""
    text = re.sub(r'\s+', ' ', text.strip())
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    current_chunk = ""
    current_word_count = 0
    max_words = 30
    for sentence in sentences:
        words = sentence.split()
        sentence_word_count = len(words)
        if current_word_count + sentence_word_count > max_words and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_word_count = sentence_word_count
        else:
            if current_chunk:
                current_chunk += ". " + sentence
            else:
                current_chunk = sentence
            current_word_count += sentence_word_count
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    for i, chunk in enumerate(chunks):
        if not chunk.endswith(('.', '!', '?')):
            chunks[i] = chunk + "."
    
    return chunks

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', model_loaded=True)

@app.route('/status')
def status():
    """Check TTS server status"""
    try:
        response = requests.post(TTS_SERVER_URL, json={'text': 'test'}, timeout=5)
        return jsonify({
            'model_loaded': response.status_code == 200,
            'message': 'TTS server ready' if response.status_code == 200 else 'TTS server not ready'
        })
    except:
        return jsonify({
            'model_loaded': False,
            'message': 'TTS server not accessible'
        })

@app.route('/synthesize', methods=['POST'])
def synthesize():
    """Generate speech from long text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        logger.info(f"Processing text: {len(text)} characters, {len(text.split())} words")
        
        # Chunk the text
        chunks = chunk_text(text)
        logger.info(f"Split into {len(chunks)} chunks")
        
        # Generate audio for each chunk
        audio_segments = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Generating chunk {i+1}/{len(chunks)}")
            
            # Call TTS server
            response = requests.post(TTS_SERVER_URL, json={'text': chunk}, timeout=120)
            
            if response.status_code != 200:
                raise ValueError(f"TTS server error for chunk {i+1}")
            
            # Save chunk to temp file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name
            
            # Load as AudioSegment
            segment = AudioSegment.from_wav(temp_path)
            audio_segments.append(segment)
            os.unlink(temp_path)
        
        # Merge segments
        if len(audio_segments) == 1:
            final_audio = audio_segments[0]
        else:
            final_audio = audio_segments[0]
            pause = AudioSegment.silent(duration=200)
            
            for segment in audio_segments[1:]:
                final_audio = final_audio + pause + segment
        
        # Save final audio
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            final_audio.export(temp_file.name, format="wav")
            temp_file_path = temp_file.name
        
        logger.info(f"✅ Generated audio: {len(final_audio)/1000:.1f}s from {len(chunks)} chunks")
        
        return send_file(
            temp_file_path,
            as_attachment=True,
            download_name='long_text_audio.wav',
            mimetype='audio/wav'
        )
        
    except Exception as e:
        logger.error(f"Error in synthesis: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)