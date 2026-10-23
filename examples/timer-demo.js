import {CountdownTimer} from "../autrexs/scripts/timer.js";
const timer=new CountdownTimer(10000);
timer.start(1000);
console.log("Milisegundos restantes:",timer.remaining(3500));
