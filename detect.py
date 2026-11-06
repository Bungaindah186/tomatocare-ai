from ultralytics import YOLO

# Memuat model hasil training
model = YOLO("weights/best.pt")

# Melakukan deteksi gambar
results = model.predict(
    source="test_image1.jpg",
    conf=0.25,
    imgsz=640,
    save=True
)

# Menampilkan hasil deteksi
for result in results:
    result.show()