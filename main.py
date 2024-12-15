import json
import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Path to the uploads directory
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'Missing location data'}), 400

    # Save the file
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Save metadata (e.g., latitude and longitude)
    metadata_file = os.path.join(UPLOAD_FOLDER, 'photos.json')
    metadata = []
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

    metadata.append({'filename': filename, 'latitude': latitude, 'longitude': longitude})

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f)

    return jsonify({'message': 'Photo uploaded successfully!'})

@app.route('/photos', methods=['GET'])
def get_photos():
    # Load photo metadata
    metadata_file = os.path.join(UPLOAD_FOLDER, 'photos.json')
    if not os.path.exists(metadata_file):
        return jsonify([])  # Return an empty list if no data is found

    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    return jsonify(metadata)

@app.route('/uploads/<path:filename>', methods=['GET'])
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
