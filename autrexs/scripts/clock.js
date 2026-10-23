import { formatClockTime, formatDate } from "./format.js";

export function renderClock(now, timeElement, dateElement) {
  timeElement.dateTime = now.toISOString();
  timeElement.textContent = formatClockTime(now);
  dateElement.textContent = formatDate(now);
}
