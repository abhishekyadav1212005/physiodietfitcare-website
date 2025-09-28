// ================= PARTNERS CAROUSEL =================
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

showClient(current);
setInterval(() => {
  current = (current + 1) % clients.length;
  showClient(current);
}, 10000);

document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".slide");
  const prevBtn = document.querySelector(".btn.prev");
  const nextBtn = document.querySelector(".btn.next");
  const dotsContainer = document.querySelector(".dots");

  let currentIndex = 0;

  // Create dots
  slides.forEach((_, i) => {
    const dot = document.createElement("button");
    if (i === 0) dot.classList.add("active");
    dot.addEventListener("click", () => goToSlide(i));
    dotsContainer.appendChild(dot);
  });
  const dots = dotsContainer.querySelectorAll("button");

  function updateSlider() {
    const offset = -currentIndex * 100;
    document.querySelector(".activities-slider").style.transform = `translateX(${offset}%)`;

    dots.forEach(dot => dot.classList.remove("active"));
    dots[currentIndex].classList.add("active");
  }

  function goToSlide(index) {
    currentIndex = (index + slides.length) % slides.length;
    updateSlider();
  }

  prevBtn.addEventListener("click", () => goToSlide(currentIndex - 1));
  nextBtn.addEventListener("click", () => goToSlide(currentIndex + 1));
});
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("mediaModal");
  const modalImg = document.getElementById("modalImage");
  const modalVideo = document.getElementById("modalVideo");
  const closeBtn = document.querySelector(".modal .close");

  // Add click event for each media
  document.querySelectorAll(".media-wrap img, .media-wrap video").forEach(media => {
    media.addEventListener("click", () => {
      modal.style.display = "block";

      if (media.tagName === "IMG") {
        modalImg.src = media.src;
        modalImg.style.display = "block";
        modalVideo.style.display = "none";
      } else if (media.tagName === "VIDEO") {
        modalVideo.src = media.currentSrc;
        modalVideo.style.display = "block";
        modalImg.style.display = "none";
      }
    });
  });

  // Close modal on click (X)
  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
    modalVideo.pause(); // stop video when closing
  });

  // Close modal on outside click
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
      modalVideo.pause();
    }
  });
});
