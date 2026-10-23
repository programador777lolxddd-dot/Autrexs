import { renderClock } from "./clock.js";
import { Stopwatch } from "./stopwatch.js";
import { formatStopwatch } from "./format.js";

const clockElement = document.querySelector("#clock");
const dateElement = document.querySelector("#date");
const timezoneLabel = document.querySelector("#timezone-label");

function updateClock() {
  const now = new Date();
  renderClock(now, clockElement, dateElement);
}
timezoneLabel.textContent = Intl.DateTimeFormat().resolvedOptions().timeZone || "Zona horaria local";
updateClock();
setInterval(updateClock, 250);

const watch = new Stopwatch();
const output = document.querySelector("#stopwatch");
const startButton = document.querySelector("#start-stopwatch");
const lapButton = document.querySelector("#lap-stopwatch");
const resetButton = document.querySelector("#reset-stopwatch");
const lapsList = document.querySelector("#laps");
let animationFrame = null;

function drawStopwatch() {
  output.textContent = formatStopwatch(watch.elapsed());
  if (watch.running) animationFrame = requestAnimationFrame(drawStopwatch);
}
function syncButtons() {
  startButton.textContent = watch.running ? "Pausar" : (watch.elapsed() ? "Continuar" : "Iniciar");
  lapButton.disabled = !watch.running;
}
startButton.addEventListener("click", () => {
  if (watch.running) watch.pause();
  else watch.start();
  if (animationFrame !== null) cancelAnimationFrame(animationFrame);
  syncButtons();
  drawStopwatch();
});
lapButton.addEventListener("click", () => {
  const elapsed = watch.elapsed();
  const item = document.createElement("li");
  item.textContent = `Vuelta ${lapsList.children.length + 1}: ${formatStopwatch(elapsed)}`;
  lapsList.prepend(item);
});
resetButton.addEventListener("click", () => {
  watch.reset();
  if (animationFrame !== null) cancelAnimationFrame(animationFrame);
  lapsList.replaceChildren();
  output.textContent = "00:00.00";
  syncButtons();
});
syncButtons();
