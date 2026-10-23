// Modelo de datos; no programa notificaciones del sistema.
export function createAlarm({id,hour,minute,enabled=true}) {
  if (!Number.isInteger(hour) || hour < 0 || hour > 23) throw new RangeError("Hora fuera de rango");
  if (!Number.isInteger(minute) || minute < 0 || minute > 59) throw new RangeError("Minuto fuera de rango");
  return {id:String(id),hour,minute,enabled:Boolean(enabled)};
}
