import test from "node:test";
import assert from "node:assert/strict";
import {createAlarm} from "../autrexs/scripts/alarms.js";
test("normalizes alarm fields",()=>assert.deepEqual(createAlarm({id:7,hour:8,minute:5}),{id:"7",hour:8,minute:5,enabled:true}));
test("rejects invalid hour or minute",()=>{assert.throws(()=>createAlarm({id:"x",hour:24,minute:0}),RangeError);assert.throws(()=>createAlarm({id:"x",hour:1,minute:60}),RangeError);});
