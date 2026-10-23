import test from "node:test";
import assert from "node:assert/strict";
import {CountdownTimer} from "../autrexs/scripts/timer.js";
test("starts with full duration",()=>assert.equal(new CountdownTimer(5000).remaining(100),5000));
test("counts down against supplied time",()=>{const t=new CountdownTimer(5000);t.start(100);assert.equal(t.remaining(2100),3000);assert.equal(t.remaining(6000),0);});
test("stop resets deadline",()=>{const t=new CountdownTimer(5000);t.start(100);t.stop();assert.equal(t.remaining(500),5000);});
