import {readFile} from "node:fs/promises";
const readme=await readFile(new URL("../README.md",import.meta.url),"utf8");
const required=["CONTRIBUTING.md","SECURITY.md","docs/ROADMAP.md"];
const missing=required.filter(path=>!readme.includes(path));
if(missing.length){console.error("Faltan referencias en README:",missing.join(", "));process.exitCode=1;}
else console.log("Referencias principales documentadas.");
