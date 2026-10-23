import {readPreference,writePreference} from "./storage.js";
export function getTheme(){return readPreference("theme","dark");}
export function setTheme(theme){
  if(!["dark","light","system"].includes(theme)) throw new TypeError("Tema no reconocido");
  return writePreference("theme",theme);
}
