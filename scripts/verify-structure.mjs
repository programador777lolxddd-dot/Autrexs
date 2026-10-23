import {access,readFile} from "node:fs/promises";
const paths=["README.md","autrexs/index.html","autrexs/styles/main.css","autrexs/scripts/app.js","docs/ROADMAP.md","tests/format.test.js"];
const missing=[];
for(const path of paths){try{await access(new URL("../"+path,import.meta.url));}catch{missing.push(path);}}
if(missing.length){console.error("Faltan archivos:",missing.join(", "));process.exitCode=1;}
else {const html=await readFile(new URL("../autrexs/index.html",import.meta.url),"utf8");if(!html.includes('id="clock"')){console.error("No se encontró el reloj en HTML");process.exitCode=1;}else console.log("Estructura base verificada.");}
