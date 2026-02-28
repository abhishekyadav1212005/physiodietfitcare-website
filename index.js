// ================= FAQ ACCORDION =================
document.querySelectorAll('.faq-question').forEach(item => {
  item.addEventListener('click', () => {
    const parent = item.parentElement;
    const isActive = parent.classList.contains('active');

    // Close all other FAQs
    document.querySelectorAll('.faq-item').forEach(faq => {
      faq.classList.remove('active');
    });

    // Toggle current FAQ
    if (!isActive) {
      parent.classList.add('active');
    }
  });
});

// ================= STATS COUNTER ANIMATION =================
const counters = document.querySelectorAll('.count');
const speed = 50;

const runCounter = () => {
  counters.forEach(counter => {
    const updateCount = () => {
      const target = +counter.getAttribute('data-target') || parseInt(counter.innerText);
      if (!counter.getAttribute('data-target')) {
        counter.setAttribute('data-target', target);
        counter.innerText = '0';
      }

      const count = +counter.innerText;
      const inc = target / speed;

      if (count < target) {
        counter.innerText = Math.ceil(count + inc);
        setTimeout(updateCount, 25);
      } else {
        counter.innerText = target;
      }
    };
    updateCount();
  });
};

// Intersection Observer to trigger counter when visible
const statsSection = document.querySelector('.stats-strip');
if (statsSection) {
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        runCounter();
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  observer.observe(statsSection);
}

// ================= SET CURRENT YEAR =================
const yearSpan = document.getElementById('year');
if (yearSpan) {
  yearSpan.innerText = new Date().getFullYear();
}

// ================= BOOKING FORM HANDLER =================
document.querySelectorAll('.booking-form').forEach(form => {
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const name = this.querySelector('input[type="text"]')?.value || '';
    const phone = this.querySelector('input[type="tel"]')?.value || '';
    const service = this.querySelectorAll('select')[0]?.value || '';
    const time = this.querySelectorAll('select')[1]?.value || '';
    const message = this.querySelector('textarea')?.value || '';

    // Build WhatsApp message
    const waText = `Hi! I would like to book a consultation.%0A` +
      `Name: ${name}%0A` +
      `Phone: ${phone}%0A` +
      `Service: ${service}%0A` +
      `Time: ${time}%0A` +
      (message ? `Message: ${message}` : '');

    // Show success message
    const container = this.closest('.form-container');
    if (container) {
      const oldContent = container.innerHTML;
      container.innerHTML = `
        <div style="text-align:center;padding:40px 20px;">
          <i class="fas fa-check-circle" style="font-size:4rem;color:#0E7490;margin-bottom:20px;"></i>
          <h2 style="color:#131D4F;margin-bottom:10px;">Thank You, ${name}!</h2>
          <p style="color:#666;font-size:1.1rem;margin-bottom:25px;">Your booking request has been received.<br>We will call you within 2 hours.</p>
          <a href="https://wa.me/917611155249?text=${waText}" target="_blank" class="btn-primary" style="display:inline-flex;align-items:center;gap:8px;">
            <i class="fab fa-whatsapp" style="font-size:1.2rem;"></i> Confirm on WhatsApp
          </a>
        </div>
      `;
    }
  });
});
