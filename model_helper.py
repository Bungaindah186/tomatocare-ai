"""
TomatoCare AI - Modul Pembantu Inferensi Model YOLOv8n (CPU Mode)
Memuat model weights/best.pt secara efisien (singleton) dan memproses prediksi gambar/frame.
"""

import os
import time
import base64
import cv2
import numpy as np
from ultralytics import YOLO
from disease_data import get_disease_info

# Inisialisasi variabel global singleton
_MODEL = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_PATH = os.path.join(BASE_DIR, "weights", "best.pt")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
RESULT_FOLDER = os.path.join(BASE_DIR, "static", "results")

# Pastikan folder penyimpanan tersedia
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


def get_yolo_model():
    """Mengambil atau menginisialisasi model YOLOv8n secara singleton di CPU."""
    global _MODEL
    if _MODEL is None:
        if not os.path.exists(WEIGHTS_PATH):
            raise FileNotFoundError(f"File model tidak ditemukan di: {WEIGHTS_PATH}")
        print(f"[TomatoCare AI] Memuat model YOLOv8n dari {WEIGHTS_PATH} ke CPU...")
        _MODEL = YOLO(WEIGHTS_PATH)
        print("[TomatoCare AI] Model berhasil dimuat.")
    return _MODEL


def predict_image_file(image_path: str, conf_threshold: float = 0.30):
    """
    Melakukan inferensi pada file gambar yang diunggah.
    Menyimpan hasil visualisasi anotasi ke folder static/results/.
    Mengembalikan data deteksi, ringkasan diagnosis, dan URL gambar hasil.
    """
    model = get_yolo_model()
    
    # Jalankan prediksi dengan mode CPU
    results = model.predict(
        source=image_path,
        conf=conf_threshold,
        imgsz=640,
        device='cpu',
        verbose=False
    )
    
    result = results[0]
    detections = []
    
    # Nama file unik untuk output visualisasi
    timestamp = int(time.time() * 1000)
    result_filename = f"pred_{timestamp}.jpg"
    result_filepath = os.path.join(RESULT_FOLDER, result_filename)
    
    # Simpan gambar teranotasi jika ada deteksi atau gambar asli berlabel
    if len(result.boxes) > 0:
        # Gunakan plotting ultralytics dengan visualisasi jelas
        annotated_img = result.plot(line_width=3, font_size=1.2)
        cv2.imwrite(result_filepath, annotated_img)
    else:
        # Jika tidak ada bounding box, beri label ramah di gambar
        img = cv2.imread(image_path)
        if img is not None:
            cv2.putText(
                img,
                "Tidak ada penyakit terdeteksi",
                (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (46, 196, 182), # Hijau cerah
                3,
                cv2.LINE_AA
            )
            cv2.imwrite(result_filepath, img)
        else:
            result_filename = os.path.basename(image_path)

    # Ekstraksi informasi bounding box dan confidence
    for box in result.boxes:
        cls_id = int(box.cls[0].item())
        cls_name = model.names.get(cls_id, f"Class_{cls_id}")
        confidence = float(box.conf[0].item())
        coords = [round(float(c), 1) for c in box.xyxy[0].tolist()]
        
        info = get_disease_info(cls_name)
        detections.append({
            "class_id": cls_id,
            "class_name": cls_name,
            "name_id": info["name_id"],
            "confidence": round(confidence, 4),
            "confidence_pct": round(confidence * 100, 1),
            "severity": info["severity"],
            "badge_color": info["badge_color"],
            "box": coords,
            "disease_info": info
        })

    # Urutkan berdasarkan confidence tertinggi
    detections.sort(key=lambda x: x["confidence"], reverse=True)

    # Tentukan diagnosis utama
    if len(detections) > 0:
        top_detection = detections[0]
        # Himpun ringkasan kelas unik yang terdeteksi
        unique_classes = {}
        for d in detections:
            cname = d["class_name"]
            if cname not in unique_classes or d["confidence"] > unique_classes[cname]["confidence"]:
                unique_classes[cname] = d
        summary_list = list(unique_classes.values())
    else:
        top_detection = None
        summary_list = []

    return {
        "success": True,
        "total_detections": len(detections),
        "detections": detections,
        "summary": summary_list,
        "top_diagnosis": top_detection,
        "result_image_url": f"/static/results/{result_filename}",
        "has_detections": len(detections) > 0
    }


def predict_base64_frame(base64_str: str, conf_threshold: float = 0.35):
    """
    Melakukan inferensi kilat pada frame base64 dari kamera browser.
    Tidak menyimpan gambar ke disk untuk kecepatan responsivitas real-time maksimal.
    """
    try:
        model = get_yolo_model()
        
        # Bersihkan header base64 jika ada
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]
            
        img_bytes = base64.b64decode(base64_str)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return {"success": False, "error": "Gagal mendekode frame kamera."}
        
        h, w = frame.shape[:2]
        
        # Prediksi frame
        results = model.predict(
            source=frame,
            conf=conf_threshold,
            imgsz=480, # Ukuran lebih kompak untuk inferensi CPU real-time cepat
            device='cpu',
            verbose=False
        )
        
        result = results[0]
        boxes_out = []
        
        for box in result.boxes:
            cls_id = int(box.cls[0].item())
            cls_name = model.names.get(cls_id, f"Class_{cls_id}")
            confidence = float(box.conf[0].item())
            xyxy = [float(c) for c in box.xyxy[0].tolist()]
            
            info = get_disease_info(cls_name)
            boxes_out.append({
                "class_id": cls_id,
                "class_name": cls_name,
                "name_id": info["name_id"],
                "confidence_pct": round(confidence * 100, 1),
                "severity": info["severity"],
                "badge_color": info["badge_color"],
                "box": [
                    round(xyxy[0]), round(xyxy[1]), 
                    round(xyxy[2]), round(xyxy[3])
                ]
            })
            
        # Diagnosis teratas
        top_diag = None
        if boxes_out:
            boxes_out.sort(key=lambda x: x["confidence_pct"], reverse=True)
            top_diag = boxes_out[0]
            
        return {
            "success": True,
            "frame_width": w,
            "frame_height": h,
            "detections": boxes_out,
            "total_detections": len(boxes_out),
            "top_diagnosis": top_diag
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}
