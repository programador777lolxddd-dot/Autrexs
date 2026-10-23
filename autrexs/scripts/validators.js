export function isValidDuration(value) {
  return Number.isFinite(value) && value >= 0;
}

export function clampDuration(value, maximum = 24 * 60 * 60 * 1000) {
  if (!isValidDuration(value)) throw new TypeError("La duración debe ser un número finito no negativo.");
  return Math.min(value, maximum);
}
