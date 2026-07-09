/**
 * Mock test — DS-02 color mapping & branding replacement
 * Run: node docs/design/figma-apply-ds02-theme-plugin/_test_mock.js
 */
const fs = require("fs");
const vm = require("vm");

const sandbox = {
  figma: { mixed: Symbol("mixed") },
  console,
  globalThis: { __APPLY_DS02_TEST__: true },
};

const code = fs.readFileSync(__dirname + "/code.js", "utf8");
vm.createContext(sandbox);
vm.runInContext(code, sandbox);

const exp = sandbox.globalThis.__APPLY_DS02_EXPORTS__;
if (!exp) {
  console.error("FAIL: missing __APPLY_DS02_EXPORTS__");
  process.exitCode = 1;
} else {
  const failures = [];

  const pinkCases = [
    ["#FF69B4", exp.DS02.accent],
    ["#E91E8C", exp.DS02.accent],
    ["#FF4D8D", exp.DS02.accent],
    ["#FFE8F0", exp.DS02.background],
    ["#9B59B6", exp.DS02.primary],
    ["#FFFFFF", exp.DS02.surface],
    ["#1A1C20", "#1A1C20"],
  ];
  pinkCases.forEach(function ([inHex, want]) {
    const got = exp.mapColorHex(inHex);
    if (got !== want) failures.push(`map ${inHex} → ${got} (want ${want})`);
  });

  const branded = exp.replaceBranding("Retro Bubblegum UI by Community");
  if (branded.indexOf("ASAK Salady · DS-02") < 0) {
    failures.push("branding replace failed: " + branded);
  }

  const ramp = exp.generateShadeRamp(exp.DS02.accent, 7);
  if (ramp.length !== 7 || ramp[0] === ramp[6]) {
    failures.push("shade ramp length or variation");
  }

  const paints = [{ type: "SOLID", color: { r: 1, g: 0.41, b: 0.71 }, visible: true }];
  const remapped = exp.remapPaints(paints);
  const outHex = exp.paintToHex(remapped[0]);
  if (outHex !== exp.DS02.accent) {
    failures.push(`remapPaints got ${outHex}`);
  }

  console.log("=== Apply DS-02 Theme Mock Test ===");
  if (failures.length) {
    console.error("FAIL:", failures.join("; "));
    process.exitCode = 1;
  } else {
    console.log("OK — color map, branding, ramp, paint remap");
    console.log("Sample ramp:", ramp.join(" → "));
  }
}
