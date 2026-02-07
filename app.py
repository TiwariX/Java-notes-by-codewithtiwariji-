 import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

# Route for the Home Page
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error: Templates folder or index.html not found! {str(e)}", 500

# Route for Download Logic
@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({"status": "error", "message": "URL missing!"}), 400

    # yt-dlp configuration
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_link = info.get('url')
            title = info.get('title', 'video')
            
            return jsonify({
                "status": "success",
                "title": title,
                "download_url": download_link
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Critical for Deployment (Render/Heroku/Vercel)
if __name__ == '__main__':
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
