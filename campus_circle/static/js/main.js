// Modal functionality
function openModal(id) {
  document.getElementById(id).classList.add('active');
}
function closeModal(id) {
  document.getElementById(id).classList.remove('active');
}

// Toast notification with type (success, error, info, warning)
function showToast(msg, type) {
  const toast = document.createElement('div');
  toast.className = 'custom-toast';
  toast.innerText = msg;
  let bg = 'linear-gradient(90deg, #6366f1 0%, #06b6d4 100%)';
  if (type && type.includes('success')) bg = 'linear-gradient(90deg, #22c55e 0%, #06b6d4 100%)';
  if (type && type.includes('error')) bg = 'linear-gradient(90deg, #e11d48 0%, #f472b6 100%)';
  if (type && type.includes('warning')) bg = 'linear-gradient(90deg, #facc15 0%, #f472b6 100%)';
  toast.style.position = 'fixed';
  toast.style.top = '2rem';
  toast.style.right = '2rem';
  toast.style.background = bg;
  toast.style.color = '#fff';
  toast.style.padding = '1rem 2rem';
  toast.style.borderRadius = '0.7rem';
  toast.style.boxShadow = '0 4px 16px rgba(60,60,100,0.13)';
  toast.style.fontWeight = 'bold';
  toast.style.fontSize = '1.08rem';
  toast.style.zIndex = 3000;
  toast.style.opacity = 1;
  toast.style.transition = 'opacity 0.5s, top 0.5s';
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = 0; toast.style.top = '0rem'; setTimeout(() => toast.remove(), 500); }, 2500);
}
