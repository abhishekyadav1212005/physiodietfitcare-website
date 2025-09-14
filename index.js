
  const clients = document.querySelectorAll(".client");
  const prevBtn = document.getElementById("prev-client");
  const nextBtn = document.getElementById("next-client");
  let current = 0;

  function showClient(index) {
    clients.forEach(c => c.classList.remove("active"));
    clients[index].classList.add("active");
  }

  nextBtn.addEventListener("click", () => {
    current = (current + 1) % clients.length;
    showClient(current);
  });

  prevBtn.addEventListener("click", () => {
    current = (current - 1 + clients.length) % clients.length;
    showClient(current);
  });

  // Show first client on load
  showClient(current);

  // Auto-slide every 10s
  setInterval(() => {
    current = (current + 1) % clients.length;
    showClient(current);
  }, 10000);

const toggleBtn = document.getElementById("menu-toggle");
  const nav = document.getElementById("navbar");

  toggleBtn.addEventListener("click", () => {
    nav.classList.toggle("active");
  });

  // Auto-update footer year
document.getElementById("year").textContent = new Date().getFullYear();




// our activities
document.addEventListener('DOMContentLoaded', () => {
  const slider = document.getElementById('activitiesSlider');
  if (!slider) return;

  const slides = Array.from(slider.querySelectorAll('.slide'));
  const prevBtn = slider.querySelector('.btn.prev');
  const nextBtn = slider.querySelector('.btn.next');
  const dotsWrap = document.querySelector('#OurActivites .dots');

  let current = 0;

  // Build dots
  dotsWrap.innerHTML = '';
  slides.forEach((_, i) => {
    const d = document.createElement('button');
    d.type = 'button';
    d.className = 'dot' + (i === 0 ? ' active' : '');
    d.setAttribute('aria-label', `Go to slide ${i+1}`);
    d.addEventListener('click', () => show(i));
    dotsWrap.appendChild(d);
  });

  function pauseAllVideos() {
    slides.forEach(s => {
      const v = s.querySelector('video');
      if (v && !v.paused) v.pause();
    });
  }

  function show(n) {
    current = ((n % slides.length) + slides.length) % slides.length;
    slides.forEach((s, i) => s.classList.toggle('is-active', i === current));
    dotsWrap.querySelectorAll('.dot').forEach((dot, i) => dot.classList.toggle('active', i === current));
    pauseAllVideos();

    // Force layout update for images/videos that load slowly so container height adjusts:
    const active = slides[current];
    const img = active.querySelector('img');
    const vid = active.querySelector('video');

    if (img && !img.complete) {
      img.onload = () => { /* layout updates automatically */ };
    } else if (vid && vid.readyState < 2) {
      vid.onloadedmetadata = () => { /* layout updates automatically */ };
    }
  }

  // Prev / Next
  prevBtn.addEventListener('click', () => show(current - 1));
  nextBtn.addEventListener('click', () => show(current + 1));

  // Keyboard arrows for accessibility
  slider.tabIndex = 0;
  slider.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') show(current - 1);
    if (e.key === 'ArrowRight') show(current + 1);
  });

  // Touch swipe
  let startX = 0;
  slider.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, { passive: true });
  slider.addEventListener('touchend', (e) => {
    const diff = e.changedTouches[0].clientX - startX;
    if (Math.abs(diff) > 40) diff > 0 ? show(current - 1) : show(current + 1);
  });

  // Init
  show(0);
});
