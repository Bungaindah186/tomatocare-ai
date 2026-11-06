/**
 * TomatoCare AI - Script Deteksi Gambar (upload.js)
 * Mengatur interaksi drag-and-drop, kamera HP, galeri, AJAX inferensi, dan render hasil deteksi.
 */

document.addEventListener('DOMContentLoaded', () => {
  const dropzone = document.getElementById('uploadDropzone');
  const fileInput = document.getElementById('mainFileInput');
  const cameraInput = document.getElementById('cameraCaptureInput');
  const btnChooseFile = document.getElementById('btnChooseFile');
  const btnTriggerCamera = document.getElementById('btnTriggerCamera');
  
  const uploadFormArea = document.getElementById('uploadFormArea');
  const loadingArea = document.getElementById('loadingArea');
  const previewArea = document.getElementById('previewContainer');
  const btnResetDetect = document.getElementById('btnResetDetect');

  const confSlider = document.getElementById('confidenceSlider');
  const confValueDisplay = document.getElementById('confValueDisplay');

  let currentSelectedFile = null;

  // Sinkronisasi nilai slider confidence
  if (confSlider && confValueDisplay) {
    confSlider.addEventListener('input', (e) => {
      confValueDisplay.textContent = `${Math.round(e.target.value * 100)}%`;
    });
  }

  // Buka galeri/file explorer
  if (btnChooseFile && fileInput) {
    btnChooseFile.addEventListener('click', () => fileInput.click());
  }

  // Buka kamera HP langsung
  if (btnTriggerCamera && cameraInput) {
    btnTriggerCamera.addEventListener('click', () => cameraInput.click());
  }

  // Handle file input change
  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
      }
    });
  }

  if (cameraInput) {
    cameraInput.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
      }
    });
  }

  // Drag and drop event listener
  if (dropzone) {
    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove('dragover');
      });
    });

    dropzone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files.length > 0) {
        handleFileSelection(files[0]);
      }
    });

    dropzone.addEventListener('click', (e) => {
      // Hanya picu jika klik di luar tombol eksplisit
      if (!e.target.closest('.btn') && fileInput) {
        fileInput.click();
      }
    });
  }

  // Reset form deteksi
  if (btnResetDetect) {
    btnResetDetect.addEventListener('click', () => {
      currentSelectedFile = null;
      if (fileInput) fileInput.value = '';
      if (cameraInput) cameraInput.value = '';
      previewArea.style.display = 'none';
      uploadFormArea.style.display = 'block';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /**
   * Memvalidasi dan memproses file gambar yang dipilih
   */
  function handleFileSelection(file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      showToast('Format file tidak didukung! Harap unggah foto JPG, PNG, atau WEBP.', 'warning');
      return;
    }

    // Maksimal 16MB
    if (file.size > 16 * 1024 * 1024) {
      showToast('Ukuran file terlalu besar! Maksimum 16 MB.', 'warning');
      return;
    }

    currentSelectedFile = file;
    processDetection(file);
  }

  /**
   * Mengirim gambar ke backend Flask via AJAX fetch
   */
  async function processDetection(file) {
    try {
      uploadFormArea.style.display = 'none';
      loadingArea.style.display = 'block';
      previewArea.style.display = 'none';

      const formData = new FormData();
      formData.append('image', file);
      const confVal = confSlider ? confSlider.value : 0.30;
      formData.append('confidence', confVal);

      const response = await fetch('/api/predict-image', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      loadingArea.style.display = 'none';

      if (!response.ok || !data.success) {
        uploadFormArea.style.display = 'block';
        showToast(data.error || 'Gagal memproses gambar.', 'danger');
        return;
      }

      // Render hasil deteksi
      renderDetectionResults(data);

    } catch (err) {
      loadingArea.style.display = 'none';
      uploadFormArea.style.display = 'block';
      showToast('Koneksi terputus saat menganalisis gambar.', 'danger');
      console.error(err);
    }
  }

  /**
   * Merender data deteksi ke elemen DOM
   */
  function renderDetectionResults(data) {
    previewArea.style.display = 'block';

    const resultImg = document.getElementById('annotatedResultImg');
    const resultCountTag = document.getElementById('resultCountTag');
    const diagTitle = document.getElementById('diagTitle');
    const diagSciName = document.getElementById('diagSciName');
    const diagBadge = document.getElementById('diagBadge');
    const confScore = document.getElementById('confScore');
    const diagDesc = document.getElementById('diagDesc');
    const symptomsList = document.getElementById('symptomsList');
    const organicList = document.getElementById('organicList');
    const chemicalList = document.getElementById('chemicalList');
    const preventionList = document.getElementById('preventionList');
    const resultMascot = document.getElementById('resultMascot');

    // Tampilkan gambar hasil teranotasi
    if (resultImg) {
      resultImg.src = data.result_image_url;
    }

    if (resultCountTag) {
      if (data.has_detections) {
        resultCountTag.innerHTML = `
          <svg class="lucide-icon" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>
          </svg>
          <span>${data.total_detections} Objek Daun Terdeteksi</span>
        `;
      } else {
        resultCountTag.innerHTML = `
          <svg class="lucide-icon" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/>
          </svg>
          <span>Observasi Bersih</span>
        `;
      }
    }

    if (data.has_detections && data.top_diagnosis) {
      const top = data.top_diagnosis;
      const info = top.disease_info;

      if (diagTitle) diagTitle.textContent = top.name_id;
      if (diagSciName) diagSciName.textContent = info.scientific_name;
      if (confScore) confScore.textContent = `${top.confidence_pct}%`;
      if (diagDesc) diagDesc.textContent = info.description;

      // Status Badge
      if (diagBadge) {
        diagBadge.textContent = `Tingkat Bahaya: ${top.severity}`;
        diagBadge.style.backgroundColor = top.badge_color;
      }

      // Mascot ekspresi
      if (resultMascot) {
        if (top.class_name === 'Healthy') {
          resultMascot.src = '/static/img/mascot/tomy-happy.svg';
        } else if (top.severity === 'Kritis' || top.severity === 'Tinggi') {
          resultMascot.src = '/static/img/mascot/tomy-sick.svg';
        } else {
          resultMascot.src = '/static/img/mascot/tomy-doctor.svg';
        }
      }

      // Daftar Gejala
      if (symptomsList) {
        symptomsList.innerHTML = info.visual_symptoms.map(s => `<li>${s}</li>`).join('');
      }

      // Penanganan Organik
      if (organicList) {
        organicList.innerHTML = info.organic_treatment.map(t => `<li>${t}</li>`).join('');
      }

      // Penanganan Kimiawi
      if (chemicalList) {
        chemicalList.innerHTML = info.chemical_treatment.map(c => `<li>${c}</li>`).join('');
      }

      // Pencegahan
      if (preventionList) {
        preventionList.innerHTML = info.prevention.map(p => `<li>${p}</li>`).join('');
      }

      showToast(`Pemeriksaan selesai: ${top.name_id} (${top.confidence_pct}%)`, 'success');

    } else {
      // Tidak ada penyakit terdeteksi
      if (diagTitle) diagTitle.textContent = "Tidak Ada Penyakit Terdeteksi";
      if (diagSciName) diagSciName.textContent = "Solanum lycopersicum (Observasi Bersih)";
      if (confScore) confScore.textContent = "0%";
      if (diagBadge) {
        diagBadge.textContent = "Status: Bersih / Tidak Dikenali";
        diagBadge.style.backgroundColor = "#2EC4B6";
      }
      if (diagDesc) {
        diagDesc.textContent = "Model tidak mendeteksi tanda-tanda dari 9 kelas penyakit daun tomat dengan ambang keyakinan saat ini. Pastikan foto daun cukup terang, fokus, dan tidak kabur.";
      }
      if (resultMascot) resultMascot.src = '/static/img/mascot/tomy-happy.svg';

      if (symptomsList) symptomsList.innerHTML = '<li>Daun tidak menunjukkan tanda kelainan dari 9 kelas yang dilatihkan.</li>';
      if (organicList) organicList.innerHTML = '<li>Lanjutkan perawatan penyiraman dan pemupukan rutin seperti biasa.</li>';
      if (chemicalList) chemicalList.innerHTML = '<li>Tidak ada indikasi perlunya pestisida.</li>';
      if (preventionList) preventionList.innerHTML = '<li>Lakukan pemeriksaan visual berkala untuk pencegahan dini.</li>';

      showToast("Pemeriksaan selesai: Tidak ada daun berpenyakit terdeteksi.", 'info');
    }

    // Scroll halus ke area hasil
    previewArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});
