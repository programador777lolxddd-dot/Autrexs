export function formatClockTime(date) {
  return new Intl.DateTimeFormat("es-BO", {
    hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false
  }).format(date);
}

export function formatDate(date) {
  return new Intl.DateTimeFormat("es-BO", {
    weekday: "long", day: "numeric", month: "long", year: "numeric"
  }).format(date);
}

export function formatStopwatch(milliseconds) {
  const centiseconds = Math.floor(Math.max(0, milliseconds) / 10);
  const minutes = Math.floor(centiseconds / 6000);
  const seconds = Math.floor((centiseconds % 6000) / 100);
  const hundredths = centiseconds % 100;
  return [minutes, seconds].map(value => String(value).padStart(2, "0")).join(":") + "." + String(hundredths).padStart(2, "0");
}
