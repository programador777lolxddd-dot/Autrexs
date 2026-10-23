import test from "node:test";
import assert from "node:assert/strict";
import {formatStopwatch} from "../autrexs/scripts/format.js";
test("starts at zero",()=>assert.equal(formatStopwatch(0),"00:00.00"));
test("formats seconds and centiseconds",()=>assert.equal(formatStopwatch(1234),"00:01.23"));
test("formats minutes",()=>assert.equal(formatStopwatch(61000),"01:01.00"));
test("clamps negative values",()=>assert.equal(formatStopwatch(-100),"00:00.00"));
