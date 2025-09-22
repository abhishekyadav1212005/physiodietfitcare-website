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

