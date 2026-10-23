export function announce(message, liveRegion) {
  if (!liveRegion) return;
  liveRegion.textContent = "";
  requestAnimationFrame(() => { liveRegion.textContent = String(message); });
}
