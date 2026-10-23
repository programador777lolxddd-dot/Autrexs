export function getLocalTimeZone() {
  return Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
}
export function formatInTimeZone(date, timeZone, locale = "es-BO") {
  return new Intl.DateTimeFormat(locale, {timeZone,hour:"2-digit",minute:"2-digit",second:"2-digit",hour12:false}).format(date);
}
