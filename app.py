"""
TomatoCare AI - Server Backend Flask
Aplikasi web cerdas untuk deteksi 9 kelas penyakit daun tomat menggunakan YOLOv8n.
"""

import os
import tempfile

# Konfigurasi direktori cache matplotlib agar tidak memunculkan peringatan
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib_tomatocare")

import time
import glob
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

from disease_data import get_all_diseases, get_disease_info, EDUCATIONAL_DISCLAIMER
from model_helper import predict_image_file, predict_base64_frame, get_yolo_model

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get(
    "SECRET_KEY",
    "tomatocare-local-development-key"
)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maksimum ukuran upload 16 MB

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
RESULT_FOLDER = os.path.join(BASE_DIR, "static", "results")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Memeriksa apakah ekstensi file diizinkan."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_old_files(max_age_seconds: int = 7200):
    """Membersihkan file gambar sementara yang lebih lama dari 2 jam."""
    try:
        now = time.time()
        for folder in [UPLOAD_FOLDER, RESULT_FOLDER]:
            for filepath in glob.glob(os.path.join(folder, "*.*")):
                if os.path.isfile(filepath):
                    if now - os.path.getmtime(filepath) > max_age_seconds:
                        os.remove(filepath)
    except Exception as e:
        print(f"[Cleanup Warning] Gagal membersihkan file lama: {e}")


# ==========================================
# RUTE WEB UTAMA
# ==========================================

@app.route('/')
def index():
    """Halaman Beranda / Dashboard."""
    diseases = get_all_diseases()
    return render_template(
        'index.html',
        active_page='home',
        diseases=diseases,
        total_classes=len(diseases),
        disclaimer=EDUCATIONAL_DISCLAIMER
    )


@app.route('/detect')
def detect_page():
    """Halaman Deteksi Upload Gambar & Kamera HP."""
    return render_template(
        'detect.html',
        active_page='detect',
        disclaimer=EDUCATIONAL_DISCLAIMER
    )


@app.route('/realtime')
def realtime_page():
    """Halaman Deteksi Real-Time Kamera Browser."""
    return render_template(
        'realtime.html',
        active_page='realtime',
        disclaimer=EDUCATIONAL_DISCLAIMER
    )


@app.route('/encyclopedia')
def encyclopedia_page():
    """Halaman Ensiklopedia 9 Penyakit Daun Tomat."""
    diseases = get_all_diseases()
    return render_template(
        'encyclopedia.html',
        active_page='encyclopedia',
        diseases=diseases,
        disclaimer=EDUCATIONAL_DISCLAIMER
    )


@app.route('/about')
def about_page():
    """Halaman Informasi Proyek TomatoCare AI."""
    return render_template(
        'about.html',
        active_page='about',
        disclaimer=EDUCATIONAL_DISCLAIMER
    )


# ==========================================
# ENDPOINT REST API
# ==========================================

@app.route('/api/predict-image', methods=['POST'])
def api_predict_image():
    """Endpoint untuk inferensi file gambar dari upload drag-and-drop / kamera HP."""
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "Tidak ada file gambar yang dikirim."}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "error": "Nama file tidak valid."}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False, 
            "error": "Format file tidak didukung. Harap gunakan format JPG, JPEG, PNG, atau WEBP."
        }), 400

    try:
        # Pembersihan file lama di latar belakang
        cleanup_old_files()

        # Simpan file dengan nama unik
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"upload_{int(time.time() * 1000)}.{ext}"
        saved_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(saved_path)

        # Ambil threshold confidence opsional
        conf = float(request.form.get('confidence', 0.30))
        conf = max(0.1, min(conf, 0.95))

        # Lakukan inferensi
        result_data = predict_image_file(saved_path, conf_threshold=conf)
        result_data["original_image_url"] = f"/static/uploads/{filename}"
        result_data["disclaimer"] = EDUCATIONAL_DISCLAIMER

        return jsonify(result_data)

    except Exception as e:
        return jsonify({"success": False, "error": f"Terjadi kesalahan saat memproses gambar: {str(e)}"}), 500


@app.route('/api/predict-frame', methods=['POST'])
def api_predict_frame():
    """Endpoint untuk inferensi frame base64 dari kamera browser real-time."""
    try:
        data = request.get_json(silent=True)
        if not data or 'frame' not in data:
            return jsonify({"success": False, "error": "Data frame kamera tidak ditemukan."}), 400

        conf = float(data.get('confidence', 0.35))
        result_data = predict_base64_frame(data['frame'], conf_threshold=conf)
        return jsonify(result_data)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/diseases', methods=['GET'])
def api_diseases():
    """Mengembalikan katalog seluruh 9 penyakit daun tomat."""
    return jsonify({
        "success": True,
        "count": 9,
        "diseases": get_all_diseases(),
        "disclaimer": EDUCATIONAL_DISCLAIMER
    })


@app.route('/api/health', methods=['GET'])
def api_health():
    """Endpoint status server & model."""
    try:
        model = get_yolo_model()
        return jsonify({
            "status": "healthy",
            "model_loaded": True,
            "classes_count": len(model.names),
            "classes": model.names
        })
    except Exception as e:
        return jsonify({
            "status": "degraded",
            "error": str(e)
        }), 500


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', not_found=True), 404


@app.errorhandler(413)
def request_entity_too_large(e):
    return jsonify({"success": False, "error": "Ukuran file melebihi batas maksimal 16 MB."}), 413


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    print("======================================================")
    print("TOMATOCARE AI - FLASK SERVER BERJALAN")
    print(f"Server berjalan pada port: {port}")
    print("======================================================")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get("FLASK_DEBUG", "0") == "1"
    )