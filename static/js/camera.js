/**
 * TomatoCare AI - Script Kamera Real-Time WebRTC (camera.js)
 * Mengakses webcam/kamera HP, mengirim frame snapshot secara berkala ke API,
 * dan menggambar bounding box 2D di atas canvas overlay.
 */

document.addEventListener('DOMContentLoaded', () => {
  const video = document.getElementById('cameraVideo');
  const overlayCanvas = document.getElementById('cameraOverlayCanvas');
  const cameraPlaceholder = document.getElementById('cameraPlaceholder');
  
  const btnStartCamera = document.getElementById('btnStartCamera');
  const btnStopCamera = document.getElementById('btnStopCamera');
  const btnSwitchCamera = document.getElementById('btnSwitchCamera');
  const liveStatusText = document.getElementById('liveStatusText');
  const confSlider = document.getElementById('camConfSlider');
  const confValDisplay = document.getElementById('camConfValDisplay');

  // Diagnosis Card Live
  const liveDiagCard = document.getElementById('liveDiagnosisCard');
  const liveDiagName = document.getElementById('liveDiagName');
  const liveDiagBadge = document.getElementById('liveDiagBadge');
  const liveDiagConf = document.getElementById('liveDiagConf');

  let mediaStream = null;
  let currentFacingMode = 'environment'; // Default kamera belakang di smartphone
  let isScanning = false;
  let scanIntervalId = null;
  const SCAN_INTERVAL_MS = 350; // Inferensi setiap 350ms (~3 FPS) untuk efisiensi CPU

  // Off-screen canvas untuk frame capture
  const captureCanvas = document.createElement('canvas');
  const captureCtx = captureCanvas.getContext('2d');

  // Sinkronisasi slider
  if (confSlider && confValDisplay) {
    confSlider.addEventListener('input', (e) => {
      confValDisplay.textContent = `${Math.round(e.target.value * 100)}%`;
    });
  }

  // Tombol Mulai
  if (btnStartCamera) {
    btnStartCamera.addEventListener('click', () => startCamera());
  }

  // Tombol Berhenti
  if (btnStopCamera) {
    btnStopCamera.addEventListener('click', () => stopCamera());
  }

  // Tombol Ganti Kamera
  if (btnSwitchCamera) {
    btnSwitchCamera.addEventListener('click', () => {
      currentFacingMode = (currentFacingMode === 'environment') ? 'user' : 'environment';
      if (isScanning) {
        stopCamera();
        setTimeout(() => startCamera(), 400);
      }
    });
  }

  /**
   * Menjalankan stream kamera via WebRTC
   */
  async function startCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      showToast('Browser Anda tidak mendukung akses kamera WebRTC atau koneksi belum diizinkan.', 'danger');
      openModal('cameraHelpModal');
      return;
    }

    try {
      if (liveStatusText) liveStatusText.textContent = 'Menghubungkan kamera...';

      const constraints = {
        video: {
          facingMode: { ideal: currentFacingMode },
          width: { ideal: 640 },
          height: { ideal: 480 }
        },
        audio: false
      };

      mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      video.srcObject = mediaStream;

      video.onloadedmetadata = () => {
        video.play();
        cameraPlaceholder.style.display = 'none';
        btnStartCamera.style.display = 'none';
        btnStopCamera.style.display = 'inline-flex';
        btnSwitchCamera.style.display = 'inline-flex';
        
        // Sesuaikan ukuran overlay canvas dengan ukuran video riil
        resizeCanvas();

        isScanning = true;
        if (liveStatusText) liveStatusText.textContent = 'Kamera Aktif: Memindai...';
        showToast('Kamera aktif! Arahkan ke daun tomat.', 'success');

        // Mulai loop inferensi
        startInferenceLoop();
      };

    } catch (err) {
      console.error('[Webcam Error]', err);
      if (liveStatusText) liveStatusText.textContent = 'Kamera Gagal Dimuat';
      
      let errMsg = 'Tidak dapat mengakses kamera.';
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        errMsg = 'Izin kamera ditolak. Harap izinkan akses kamera di pengaturan browser.';
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        errMsg = 'Perangkat kamera tidak ditemukan di laptop/ponsel Anda.';
      }
      
      showToast(errMsg, 'danger');
      openModal('cameraHelpModal');
    }
  }

  /**
   * Menghentikan kamera dan loop inferensi
   */
  function stopCamera() {
    isScanning = false;
    if (scanIntervalId) {
      clearInterval(scanIntervalId);
      scanIntervalId = null;
    }

    if (mediaStream) {
      mediaStream.getTracks().forEach(track => track.stop());
      mediaStream = null;
    }

    if (video) {
      video.srcObject = null;
    }

    // Bersihkan overlay canvas
    const ctx = overlayCanvas.getContext('2d');
    ctx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

    cameraPlaceholder.style.display = 'flex';
    btnStartCamera.style.display = 'inline-flex';
    btnStopCamera.style.display = 'none';
    btnSwitchCamera.style.display = 'none';
    if (liveStatusText) liveStatusText.textContent = 'Kamera Dimatikan';

    if (liveDiagCard) liveDiagCard.style.display = 'none';
  }

  /**
   * Menyesuaikan ukuran overlay canvas agar tepat 1:1 di atas video
   */
  function resizeCanvas() {
    if (!video.videoWidth || !video.videoHeight) return;
    overlayCanvas.width = video.videoWidth;
    overlayCanvas.height = video.videoHeight;
    captureCanvas.width = video.videoWidth;
    captureCanvas.height = video.videoHeight;
  }

  window.addEventListener('resize', resizeCanvas);

  /**
   * Loop inferensi periodik
   */
  function startInferenceLoop() {
    if (scanIntervalId) clearInterval(scanIntervalId);

    let isRequestBusy = false;

    scanIntervalId = setInterval(async () => {
      if (!isScanning || isRequestBusy || video.readyState < 2) return;

      isRequestBusy = true;

      try {
        // Ambil frame dari video ke off-screen canvas
        captureCtx.drawImage(video, 0, 0, captureCanvas.width, captureCanvas.height);
        const base64Data = captureCanvas.toDataURL('image/jpeg', 0.65); // Kompresi JPEG ringan

        const confVal = confSlider ? parseFloat(confSlider.value) : 0.35;

        // Kirim ke backend Flask
        const res = await fetch('/api/predict-frame', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            frame: base64Data,
            confidence: confVal
          })
        });

        const data = await res.json();

        if (data.success && isScanning) {
          drawBoundingBoxes(data.detections);
          updateLiveDiagnosis(data.top_diagnosis);
        }

      } catch (err) {
        console.warn('[Frame Loop Warning]', err);
      } finally {
        isRequestBusy = false;
      }
    }, SCAN_INTERVAL_MS);
  }

  /**
   * Menggambar bounding box playful 2D pada canvas overlay
   */
  function drawBoundingBoxes(detections) {
    const ctx = overlayCanvas.getContext('2d');
    ctx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

    if (!detections || detections.length === 0) return;

    detections.forEach(det => {
      const [x1, y1, x2, y2] = det.box;
      const boxW = x2 - x1;
      const boxH = y2 - y1;
      const themeColor = det.badge_color || '#2EC4B6';

      // Gambar Bounding Box 2D Neo-flat
      ctx.lineWidth = 4;
      ctx.strokeStyle = themeColor;
      ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';

      // Kotak Bounding Box dengan sudut membulat
      ctx.beginPath();
      ctx.roundRect(x1, y1, boxW, boxH, 8);
      ctx.stroke();
      ctx.fill();

      // Border outline gelap untuk efek 2D kartun
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = '#2B2D42';
      ctx.stroke();

      // Label Pill Tag di Atas Box
      const labelText = `${det.name_id} (${det.confidence_pct}%)`;
      ctx.font = 'bold 15px "Fredoka", "Quicksand", sans-serif';
      const textWidth = ctx.measureText(labelText).width;
      const tagH = 26;
      const tagW = textWidth + 18;
      const tagY = Math.max(0, y1 - tagH - 4);

      // Background Tag
      ctx.fillStyle = themeColor;
      ctx.beginPath();
      ctx.roundRect(x1, tagY, tagW, tagH, 6);
      ctx.fill();

      // Outline Tag
      ctx.strokeStyle = '#2B2D42';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Teks Label Putih / Kontras
      ctx.fillStyle = '#FFFFFF';
      ctx.fillText(labelText, x1 + 9, tagY + 18);
    });
  }

  /**
   * Memperbarui kartu diagnosis langsung di bawah video
   */
  function updateLiveDiagnosis(top) {
    if (!liveDiagCard) return;

    if (!top) {
      liveDiagCard.style.display = 'none';
      return;
    }

    liveDiagCard.style.display = 'block';
    if (liveDiagName) liveDiagName.textContent = top.name_id;
    if (liveDiagConf) liveDiagConf.textContent = `${top.confidence_pct}%`;
    if (liveDiagBadge) {
      liveDiagBadge.textContent = top.severity;
      liveDiagBadge.style.backgroundColor = top.badge_color;
    }
  }

  // Hentikan kamera otomatis jika user berpindah halaman
  window.addEventListener('beforeunload', () => stopCamera());
});
