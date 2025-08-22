// Enhanced Modal functionality with animations
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Add entrance animation
    const content = modal.querySelector('.modal-content');
    if (content) {
      content.style.transform = 'scale(0.8) translateY(-50px)';
      content.style.opacity = '0';
      
      requestAnimationFrame(() => {
        content.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        content.style.transform = 'scale(1) translateY(0)';
        content.style.opacity = '1';
      });
    }
  }
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    const content = modal.querySelector('.modal-content');
    if (content) {
      content.style.transform = 'scale(0.8) translateY(-50px)';
      content.style.opacity = '0';
    }
    
    setTimeout(() => {
      modal.classList.remove('active');
      document.body.style.overflow = 'auto';
    }, 300);
  }
}

// Enhanced Toast notifications with modern design
function showToast(msg, type = 'info') {
  const toast = document.createElement('div');
  toast.className = 'modern-toast';
  
  let icon = 'fas fa-info-circle';
  let bg = 'rgba(99, 102, 241, 0.95)';
  
  if (type.includes('success')) {
    icon = 'fas fa-check-circle';
    bg = 'rgba(16, 185, 129, 0.95)';
  } else if (type.includes('error')) {
    icon = 'fas fa-exclamation-circle';
    bg = 'rgba(239, 68, 68, 0.95)';
  } else if (type.includes('warning')) {
    icon = 'fas fa-exclamation-triangle';
    bg = 'rgba(245, 158, 11, 0.95)';
  }
  
  toast.innerHTML = `
    <div style="display: flex; align-items: center; gap: 0.75rem;">
      <i class="${icon}" style="font-size: 1.2rem;"></i>
      <span>${msg}</span>
    </div>
  `;
  
  Object.assign(toast.style, {
    position: 'fixed',
    top: '2rem',
    right: '2rem',
    background: bg,
    backdropFilter: 'blur(20px)',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    color: '#fff',
    padding: '1.25rem 1.75rem',
    borderRadius: '1.5rem',
    boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
    fontWeight: '600',
    fontSize: '1rem',
    zIndex: '3000',
    opacity: '0',
    transform: 'translateX(100%) scale(0.8)',
    transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)',
    maxWidth: '400px',
    wordWrap: 'break-word',
    cursor: 'pointer'
  });
  
  document.body.appendChild(toast);
  
  // Animate in
  setTimeout(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(0) scale(1)';
  }, 100);
  
  // Animate out
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%) scale(0.8)';
    setTimeout(() => toast.remove(), 500);
  }, 4000);
  
  // Click to dismiss with animation
  toast.addEventListener('click', () => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%) scale(0.8)';
    setTimeout(() => toast.remove(), 500);
  });
}

// Modern loading spinner with glassmorphism
function showLoading(text = 'Loading...') {
  const loader = document.createElement('div');
  loader.id = 'global-loader';
  loader.innerHTML = `
    <div style="
      background: rgba(255, 255, 255, 0.25);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 2rem;
      padding: 3rem;
      text-align: center;
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
      transform: scale(0.9);
      transition: transform 0.3s ease-out;
    ">
      <div style="
        width: 60px;
        height: 60px;
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-top: 4px solid #ffffff;
        border-radius: 50%;
        animation: modernSpin 1.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
        margin: 0 auto 1.5rem;
      "></div>
      <div style="
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
      ">${text}</div>
    </div>
  `;
  
  Object.assign(loader.style, {
    position: 'fixed',
    top: '0',
    left: '0',
    width: '100vw',
    height: '100vh',
    background: 'rgba(0, 0, 0, 0.8)',
    backdropFilter: 'blur(10px)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: '9999',
    opacity: '0',
    transition: 'opacity 0.4s ease-out'
  });
  
  document.body.appendChild(loader);
  
  requestAnimationFrame(() => {
    loader.style.opacity = '1';
    const content = loader.querySelector('div');
    content.style.transform = 'scale(1)';
  });
  
  // Add modern spinner animation
  if (!document.getElementById('modern-spinner-styles')) {
    const style = document.createElement('style');
    style.id = 'modern-spinner-styles';
    style.textContent = `
      @keyframes modernSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `;
    document.head.appendChild(style);
  }
}

function hideLoading() {
  const loader = document.getElementById('global-loader');
  if (loader) {
    const content = loader.querySelector('div');
    content.style.transform = 'scale(0.9)';
    loader.style.opacity = '0';
    setTimeout(() => loader.remove(), 400);
  }
}

// Enhanced form validation with modern animations
function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return false;
  
  const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
  let isValid = true;
  
  inputs.forEach(input => {
    const errorMsg = input.parentNode.querySelector('.error-message');
    if (errorMsg) {
      errorMsg.style.animation = 'fadeOut 0.3s ease-out';
      setTimeout(() => errorMsg.remove(), 300);
    }
    
    if (!input.value.trim()) {
      isValid = false;
      
      // Create modern error message
      const error = document.createElement('div');
      error.className = 'error-message';
      error.style.cssText = `
        color: #ef4444;
        font-size: 0.875rem;
        margin-top: 0.5rem;
        font-weight: 500;
        padding: 0.5rem 1rem;
        background: rgba(239, 68, 68, 0.1);
        border-radius: 0.75rem;
        border-left: 3px solid #ef4444;
        animation: slideInDown 0.3s ease-out;
        display: flex;
        align-items: center;
        gap: 0.5rem;
      `;
      
      error.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        ${input.placeholder || input.name || 'This field'} is required
      `;
      
      input.parentNode.appendChild(error);
      input.style.borderColor = '#ef4444';
      input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
      
      // Shake animation for input
      input.style.animation = 'shake 0.5s ease-in-out';
      setTimeout(() => input.style.animation = '', 500);
      
    } else {
      input.style.borderColor = '#10b981';
      input.style.boxShadow = '0 0 0 3px rgba(16, 185, 129, 0.1)';
    }
  });
  
  return isValid;
}

// Add validation animations CSS
const validationCSS = `
  @keyframes slideInDown {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes fadeOut {
    from {
      opacity: 1;
      transform: translateY(0);
    }
    to {
      opacity: 0;
      transform: translateY(-10px);
    }
  }
  
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
  }
`;

const validationStyle = document.createElement('style');
validationStyle.textContent = validationCSS;
document.head.appendChild(validationStyle);

// Enhanced smooth scroll with offset for fixed headers
function smoothScrollTo(elementId, offset = 100) {
  const element = document.getElementById(elementId);
  if (element) {
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - offset;
    
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}

// Parallax effect for hero sections
function initParallax() {
  window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.parallax');
    
    parallaxElements.forEach(element => {
      const speed = element.dataset.speed || 0.5;
      const yPos = -(scrolled * speed);
      element.style.transform = `translateY(${yPos}px)`;
    });
  });
}

// Initialize parallax on load
document.addEventListener('DOMContentLoaded', initParallax);

// Enhanced image modal with modern design
function openImageModal(imageSrc) {
  const modal = document.createElement('div');
  modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.95);
    backdrop-filter: blur(20px);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  `;
  
  const img = document.createElement('img');
  img.src = imageSrc;
  img.style.cssText = `
    max-width: 90vw;
    max-height: 90vh;
    object-fit: contain;
    border-radius: 1.5rem;
    box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    transform: scale(0.8) translateY(50px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid rgba(255,255,255,0.1);
  `;
  
  const closeBtn = document.createElement('button');
  closeBtn.innerHTML = '<i class="fas fa-times"></i>';
  closeBtn.style.cssText = `
    position: absolute;
    top: 2rem;
    right: 2rem;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    color: white;
    font-size: 1.2rem;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
  `;
  
  closeBtn.addEventListener('mouseenter', () => {
    closeBtn.style.background = 'rgba(239, 68, 68, 0.8)';
    closeBtn.style.transform = 'scale(1.1)';
  });
  
  closeBtn.addEventListener('mouseleave', () => {
    closeBtn.style.background = 'rgba(255,255,255,0.15)';
    closeBtn.style.transform = 'scale(1)';
  });
  
  modal.appendChild(img);
  modal.appendChild(closeBtn);
  document.body.appendChild(modal);
  
  // Animate in
  requestAnimationFrame(() => {
    modal.style.opacity = '1';
    img.style.transform = 'scale(1) translateY(0)';
  });
  
  const closeModal = () => {
    modal.style.opacity = '0';
    img.style.transform = 'scale(0.8) translateY(50px)';
    setTimeout(() => {
      modal.remove();
      document.body.style.overflow = 'auto';
    }, 400);
  };
  
  modal.onclick = closeModal;
  closeBtn.onclick = closeModal;
  img.onclick = (e) => e.stopPropagation();
  
  document.body.style.overflow = 'hidden';
}

// Notification system
function createNotification(type, title, message, time = 'now') {
  return {
    type,
    title,
    message,
    time,
    id: Date.now() + Math.random()
  };
}

function addNotification(notification) {
  // Show notification dot
  const notificationDot = document.getElementById('notificationDot');
  if (notificationDot) {
    notificationDot.style.display = 'block';
  }
  
  // Store in localStorage for persistence
  const notifications = JSON.parse(localStorage.getItem('notifications') || '[]');
  notifications.unshift(notification);
  localStorage.setItem('notifications', JSON.stringify(notifications.slice(0, 50))); // Keep only 50 latest
}

// Modern notification system with better UX
function simulateNotifications() {
  // Stagger notifications for better UX
  const notifications = [
    { type: 'job', title: 'New Job Posted', message: 'Software Engineer at TechCorp', delay: 3000 },
    { type: 'event', title: 'Upcoming Event', message: 'Tech Meetup this Friday', delay: 8000 },
    { type: 'message', title: 'New Message', message: 'You have 2 unread messages', delay: 15000 }
  ];
  
  notifications.forEach(notif => {
    setTimeout(() => {
      addNotification(createNotification(
        notif.type,
        notif.title,
        notif.message,
        'just now'
      ));
    }, notif.delay);
  });
}

// Modern page transitions and interactions
function initModernUI() {
  // Animate elements on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade-in');
      }
    });
  }, observerOptions);
  
  // Observe all cards and interactive elements
  document.querySelectorAll('.card, .interactive-hover').forEach(el => {
    observer.observe(el);
  });
  
  // Enhanced button interactions
  document.querySelectorAll('.btn, button').forEach(btn => {
    btn.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-3px) scale(1.02)';
    });
    btn.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });
  
// Enhanced form handling with modern loading states
function initFormHandling() {
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
      const submitBtn = this.querySelector('button[type="submit"], input[type="submit"]');
      if (submitBtn && !submitBtn.disabled) {
        submitBtn.disabled = true;
        const originalText = submitBtn.innerHTML;
        
        // Modern loading animation
        submitBtn.innerHTML = `
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top: 2px solid white; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            Processing...
          </div>
        `;
        
        // Add loading styles
        submitBtn.style.opacity = '0.8';
        submitBtn.style.cursor = 'not-allowed';
        
        // Reset after timeout
        setTimeout(() => {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
          }
        }, 5000);
      }
    });
  });
}

// Add spin animation for loading
const spinCSS = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;
const spinStyle = document.createElement('style');
spinStyle.textContent = spinCSS;
document.head.appendChild(spinStyle);

// Initialize form handling
document.addEventListener('DOMContentLoaded', initFormHandling);
  
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // Add ripple effect to buttons
  document.querySelectorAll('.btn, button').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
      `;
      
      this.style.position = 'relative';
      this.style.overflow = 'hidden';
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });
  
  // Initialize notification system
  simulateNotifications();
}

// Add ripple animation CSS
const rippleCSS = `
  @keyframes ripple {
    to {
      transform: scale(4);
      opacity: 0;
    }
  }
`;
const style = document.createElement('style');
style.textContent = rippleCSS;
document.head.appendChild(style);

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initModernUI);
