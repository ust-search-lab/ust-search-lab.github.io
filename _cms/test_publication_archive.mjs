import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

function archive() {
  const registered = {};
  const context = {
    CMS: {
      registerCustomFormat: (_name, _extension, format) => { registered.format = format; },
      registerWidget: (_name, widget) => { registered.widget = widget; },
    },
    // Parsing is delegated to the pinned js-yaml library. These tests exercise
    // the read-only adapter and rendering policy with already parsed fixtures.
    jsyaml: { JSON_SCHEMA: {}, load: JSON.parse },
    h: (tag, props, ...children) => ({ tag, props, children }),
    createClass: (definition) => definition,
  };
  context.window = context;
  vm.runInNewContext(readFileSync(new URL("../admin/publication-archive.js", import.meta.url), "utf8"), context);
  context.registerPublicationArchive({ hidden_first_authors: ["Young-Joo Song", "송영주"] });
  return registered;
}

test("archive displays first-author matches but preserves every source record", () => {
  const { format, widget } = archive();
  const source = [
    { title: "English hidden", authors: ["YOUNG–JOO SONG", "Park"], year: 2021 },
    { title: "Korean hidden", authors: ["송영주", "박재익"], year: 2020 },
    { title: "Visible coauthorship", authors: ["Park", "Young-Joo Song"] },
    { title: "Already excluded", authors: ["송영주"], exclude: true },
  ];
  const data = format.fromFile(JSON.stringify(source));
  const original = JSON.stringify(data);
  const rendered = widget.render.call({ props: { value: { toJS: () => data.records } } });
  const output = JSON.stringify(rendered);
  assert.match(output, /숨긴 실적 2건/);
  assert.match(output, /English hidden/);
  assert.match(output, /Korean hidden/);
  assert.doesNotMatch(output, /Visible coauthorship|Already excluded/);
  assert.equal(JSON.stringify(data), original);
  assert.throws(() => format.toFile(data), /조회 전용/);
  assert.throws(() => format.fromFile("{}"), /형식/);
});

test("archive renders names as text and never creates an unsafe source link", () => {
  const { widget } = archive();
  const result = widget.render.call({ props: { value: { toJS: () => [
    { title: "<script>unsafe()</script>", authors: ["송영주"], link: "javascript:unsafe()" },
  ] } } });
  const output = JSON.stringify(result);
  assert.doesNotMatch(output, /dangerouslySetInnerHTML|javascript:|onChange/);
  assert.match(output, /<script>unsafe\(\)<\/script>/);
});
