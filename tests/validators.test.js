import test from "node:test";
import assert from "node:assert/strict";
import {isValidDuration,clampDuration} from "../autrexs/scripts/validators.js";
test("accepts zero and positive durations",()=>{assert.equal(isValidDuration(0),true);assert.equal(isValidDuration(1500),true);});
test("rejects invalid durations",()=>{assert.equal(isValidDuration(-1),false);assert.equal(isValidDuration(Infinity),false);assert.equal(isValidDuration(NaN),false);});
test("caps durations",()=>assert.equal(clampDuration(1000,500),500));
test("throws for invalid values",()=>assert.throws(()=>clampDuration(-1),TypeError));
