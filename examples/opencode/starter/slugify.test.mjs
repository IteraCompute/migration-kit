import assert from "node:assert/strict";
import test from "node:test";
import { slugify } from "./slugify.mjs";

test("lowercases and joins words", () => {
  assert.equal(slugify("Hello World"), "hello-world");
});
test("trims whitespace and collapses punctuation", () => {
  assert.equal(slugify("  Hello,   World!  "), "hello-world");
});
test("collapses repeated separators", () => {
  assert.equal(slugify("API___  migration---kit"), "api-migration-kit");
});
test("keeps digits and returns empty for punctuation only", () => {
  assert.equal(slugify("Version 42"), "version-42");
  assert.equal(slugify(" !!! "), "");
});
