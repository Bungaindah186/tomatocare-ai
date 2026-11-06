
from ultralytics import YOLO
import cv2

# =====================================
# 1. MEMUAT MODEL YOLOv8n
# =====================================
model = YOLO("weights/best.pt")

# =====================================
# 2. MENGAKTIFKAN WEBCAM
# =====================================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam tidak ditemukan!")
    exit()

# =====================================
# 3. PENGATURAN DETEKSI
# =====================================
CONFIDENCE = 0.60
IMG_SIZE = 640

# =====================================
# 4. PENGATURAN JENDELA KAMERA
# =====================================
window_name = "YOLOv8n - Tomato Leaf Detection"

# Membuat jendela yang bisa diubah ukurannya
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# Ukuran awal jendela
cv2.resizeWindow(window_name, 800, 600)

print("=====================================")
print(" YOLOv8n TOMATO LEAF DETECTION")
print("=====================================")
print("Real-time detection aktif.")
print("Tekan Q untuk keluar.")
print("Gunakan tombol maximize untuk memperbesar jendela.")

# =====================================
# 5. PROSES DETEKSI REAL-TIME
# =====================================
while True:

    ret, frame = cap.read()

    if not ret:
        print("Gagal membaca frame dari webcam!")
        break

    # Melakukan prediksi menggunakan YOLO
    results = model.predict(
        source=frame,
        conf=CONFIDENCE,
        imgsz=IMG_SIZE,
        verbose=False
    )

    result = results[0]

    # Menampilkan hasil deteksi
    if len(result.boxes) > 0:
        annotated_frame = result.plot()
    else:
        annotated_frame = frame.copy()

        cv2.putText(
            annotated_frame,
            "Tidak ada daun terdeteksi",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    # Menampilkan video pada jendela
    cv2.imshow(window_name, annotated_frame)

    # Tekan Q untuk menghentikan program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# =====================================
# 6. MENUTUP WEBCAM
# =====================================
cap.release()
cv2.destroyAllWindows()

print("Program deteksi berhasil dihentikan.")
