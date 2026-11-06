/**
 * TomatoCare AI - Script Utama (main.js)
 * Utilitas notifikasi toast, modal popup 2D, dan verifikasi status model.
 */

// Inisialisasi container toast otomatis
document.addEventListener('DOMContentLoaded', () => {
  if (!document.querySelector('.toast-container')) {
    const toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container';
    document.body.appendChild(toastContainer);
  }

  // Cek status model YOLO saat pertama kali halaman dimuat
  checkModelHealth();
});

/**
 * Menampilkan pesan toast playful 2D
 * @param {string} message - Pesan yang ingin ditampilkan
 * @param {string} type - 'success', 'warning', 'danger', atau 'info'
 */
function showToast(message, type = 'info') {
  const container = document.querySelector('.toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast-item toast-${type}`;

  const iconMap = {
    success: `<span class="icon-box icon-box-sm icon-box-leaf"><svg class="lucide-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg></span>`,
    warning: `<span class="icon-box icon-box-sm icon-box-yellow"><svg class="lucide-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></span>`,
    danger: `<span class="icon-box icon-box-sm icon-box-tomato"><svg class="lucide-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg></span>`,
    info: `<span class="icon-box icon-box-sm icon-box-blue"><svg class="lucide-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg></span>`
  };

  toast.innerHTML = `
    ${iconMap[type] || iconMap.info}
    <span>${message}</span>
  `;

  container.appendChild(toast);

  // Hilangkan setelah 3.5 detik
  setTimeout(() => {
    toast.style.transition = 'all 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(15px)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

/**
 * Membuka modal popup 2D
 * @param {string} modalId 
 */
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
}

/**
 * Menutup modal popup 2D
 * @param {string} modalId 
 */
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('show');
    document.body.style.overflow = '';
  }
}

// Menutup modal jika klik pada area backdrop luar
window.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-backdrop')) {
    e.target.classList.remove('show');
    document.body.style.overflow = '';
  }
});

/**
 * Memeriksa status kesehatan server dan kesiapan model YOLOv8n
 */
async function checkModelHealth() {
  try {
    const response = await fetch('/api/health');
    const data = await response.json();
    const statusPill = document.querySelector('.model-pill span:last-child');
    if (statusPill && data.status === 'healthy') {
      statusPill.textContent = `YOLOv8n Aktif (${data.classes_count} Kelas)`;
    }
  } catch (err) {
    console.warn('[TomatoCare AI] Menghubungi status model:', err);
  }
}
