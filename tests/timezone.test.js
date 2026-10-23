import test from "node:test";
import assert from "node:assert/strict";
import {formatInTimeZone,getLocalTimeZone} from "../autrexs/scripts/timezone.js";
test("local zone is a non-empty string",()=>{assert.equal(typeof getLocalTimeZone(),"string");assert.ok(getLocalTimeZone().length>0);});
test("formats known UTC time",()=>assert.equal(formatInTimeZone(new Date("2024-01-01T12:34:56Z"),"UTC","en-GB"),"12:34:56"));
