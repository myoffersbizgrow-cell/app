import os
import time
import shutil
import sys
from pathlib import Path
from flask import Flask, request, render_template, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# ✅ Import converter
try:
    from converter import APKtoAABConverter
except Exception as e:
    print(f"❌ Failed to import converter: {e}")
    sys.exit(1)

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

BASE_DIR = Path(__file__).parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"

UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# ✅ Initialize converter
try:
    converter = APKtoAABConverter()
    print("✅ Converter initialized")
except Exception as e:
    print(f"❌ Converter init failed: {e}")
    sys.exit(1)

# ✅ Download tools if needed
try:
    if not (converter.tools_dir / "bundletool.jar").exists():
        print("📦 Downloading tools...")
        converter.download_tools()
        print("✅ Tools downloaded")
except Exception as e:
    print(f"❌ Tool download failed: {e}")

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"<h1>Error loading page</h1><p>{e}</p>", 500

@app.route('/health')
def health():
    try:
        return jsonify({
            'status': 'OK',
            'tools': {
                'apktool': converter.apktool.exists(),
                'aapt2': converter.aapt2.exists(),
                'bundletool': converter.bundletool.exists(),
                'android_jar': converter.android_jar.exists()
            }
        })
    except Exception as e:
        return jsonify({'status': 'ERROR', 'message': str(e)}), 500

@app.route('/api/convert', methods=['POST'])
def convert():
    try:
        # ✅ Check if file exists
        if 'apk' not in request.files:
            return jsonify({'error': 'No APK file uploaded'}), 400
        
        file = request.files['apk']
        if file.filename == '' or not file.filename.endswith('.apk'):
            return jsonify({'error': 'Invalid file type. Only APK allowed'}), 400
        
        # ✅ Save APK
        apk_name = f"{int(time.time())}_{secure_filename(file.filename)}"
        apk_path = UPLOADS_DIR / apk_name
        file.save(apk_path)
        print(f"✅ APK saved: {apk_path}")
        
        # ✅ Get SDK versions
        min_sdk = int(request.form.get('minSdk', 21))
        target_sdk = int(request.form.get('targetSdk', 33))
        print(f"📊 Min SDK: {min_sdk}, Target SDK: {target_sdk}")
        
        # ✅ Convert
        result = converter.convert(apk_path, min_sdk, target_sdk)
        
        # ✅ Clean up
        apk_path.unlink()
        
        if result and result.exists():
            return jsonify({
                'success': True,
                'aab': result.name,
                'download_url': f'/download/{result.name}',
                'size': result.stat().st_size
            })
        else:
            return jsonify({'error': 'Conversion failed - no output file'}), 500
            
    except Exception as e:
        print(f"❌ Conversion error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = OUTPUT_DIR / filename
        if file_path.exists():
            return send_file(file_path, as_attachment=True)
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)