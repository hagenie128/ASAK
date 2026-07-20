/**
 * Injects full_kit.js into code.js before async function run().
 * Run: node docs/design/figma-create-ds02-components-plugin/bundle_plugin.js
 */
const fs = require("fs");
const path = require("path");

const dir = __dirname;
const codePath = path.join(dir, "code.js");
const kitPath = path.join(dir, "full_kit.js");
const marker = "async function run()";
const startMarker = "/* FULL_KIT_MODULE — auto-injected by bundle_plugin.js */\n";

let code = fs.readFileSync(codePath, "utf8");
const kit = fs.readFileSync(kitPath, "utf8");

const injectStart = code.indexOf(startMarker);
const runIdx = code.indexOf(marker);
if (runIdx < 0) throw new Error("run() anchor not found in code.js");

if (injectStart >= 0) {
  const endMarker = "\n/* END FULL_KIT_MODULE */\n";
  const endIdx = code.indexOf(endMarker, injectStart);
  if (endIdx < 0) throw new Error("END FULL_KIT_MODULE marker not found");
  code = code.slice(0, injectStart) + code.slice(endIdx + endMarker.length);
}

const endMarker = "\n/* END FULL_KIT_MODULE */\n";
const injection = startMarker + kit + endMarker;
const newRunIdx = code.indexOf(marker);
code = code.slice(0, newRunIdx) + injection + code.slice(newRunIdx);

// Update figma.on handler if not already patched
if (!code.includes('evt.command === "fullkit"')) {
  code = code.replace(
    'figma.on("run", (evt) => {\n    if (evt.command === "fullkit") runFullKit();
    else if (evt.command === "create" || !evt.command) run();\n  });',
    'figma.on("run", (evt) => {\n    if (evt.command === "fullkit") runFullKit();\n    else if (evt.command === "create" || !evt.command) run();\n  });'
  );
}

// Update exports block
if (!code.includes("buildY2KStyleFullKit")) {
  code = code.replace(
    "    kioskIconTransform,\n  };",
    "    kioskIconTransform,\n    buildY2KStyleFullKit,\n    runFullKit,\n    getFullKitSummary,\n    Y2K_KIT_SECTIONS,\n    FULL_KIT_FRAME_NAME,\n    resetFullKitInventory,\n  };"
  );
}

fs.writeFileSync(codePath, code, "utf8");
console.log("Bundled full_kit.js into code.js (" + kit.split("\n").length + " lines)");
