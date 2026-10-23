import {formatInTimeZone} from "./timezone.js";
export function worldClockEntry(timeZone,date=new Date()) {
  return {timeZone,time:formatInTimeZone(date,timeZone),iso:date.toISOString()};
}
