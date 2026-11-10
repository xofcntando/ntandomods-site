document.getElementById("yr").textContent = new Date().getFullYear();
document.querySelectorAll(".sw").forEach((b) => b.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(b.dataset.hex); } catch {}
  b.classList.add("copied");
  setTimeout(() => b.classList.remove("copied"), 1500);
}));
