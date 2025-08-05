// Modal functionality
function openModal(id) {
  document.getElementById(id).classList.add('active');
}
function closeModal(id) {
  document.getElementById(id).classList.remove('active');
}

// Toast notification
function showToast(msg) {
  const toast = document.createElement('div');
  toast.style.position = 'fixed';
  toast.style.bottom = '2rem';
  toast.style.right = '2rem';
  toast.style.background = 'linear-gradient(90deg, #6366f1 0%, #f472b6 100%)';
  toast.style.color = '#fff';
  toast.style.padding = '1rem 2rem';
  toast.style.borderRadius = '0.5rem';
  toast.style.boxShadow = '0 2px 8px rgba(99,102,241,0.15)';
  toast.style.fontWeight = 'bold';
  toast.style.zIndex = 2000;
  toast.style.opacity = 1;
  toast.style.transition = 'opacity 0.5s';
  toast.innerText = msg;
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = 0; setTimeout(() => toast.remove(), 500); }, 2500);
}
