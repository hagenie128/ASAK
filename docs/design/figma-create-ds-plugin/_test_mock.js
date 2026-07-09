const fs = require("fs");
const vm = require("vm");

function makeNode(type, w, h) {
  const node = {
    type,
    name: "",
    width: w || 100,
    height: h || 100,
    x: 0,
    y: 0,
    fills: [],
    strokes: [],
    strokeWeight: 0,
    cornerRadius: 0,
    effects: [],
    clipsContent: false,
    children: [],
    appendChild(child) {
      this.children.push(child);
      child.parent = this;
    },
    resize(w, h) {
      this.width = w;
      this.height = h;
    },
  };
  if (type === "TEXT") {
    node.characters = "";
    node.fontSize = 12;
    node.fontName = { family: "Inter", style: "Regular" };
    node.textAlignHorizontal = "LEFT";
    node.textAlignVertical = "TOP";
  }
  return node;
}

const figma = {
  mixed: Symbol("mixed"),
  root: { children: [{ type: "PAGE", name: "02. User Flow", children: [] }] },
  createFrame() {
    return makeNode("FRAME");
  },
  createEllipse() {
    const node = makeNode("ELLIPSE");
    delete node.appendChild;
    return node;
  },
  createRectangle() {
    const node = makeNode("RECTANGLE");
    delete node.appendChild;
    return node;
  },
  createText() {
    return makeNode("TEXT");
  },
  createImage(data) {
    if (!(data instanceof Uint8Array)) {
      throw new Error("createImage: Expected Uint8Array, received " + typeof data);
    }
    return { hash: "mock-hash-" + data.length };
  },
  createImageAsync(src) {
    if (typeof src !== "string") {
      throw new Error("createImageAsync: Expected string, received " + typeof src);
    }
    return Promise.resolve({ hash: "mock-async-" + src.length });
  },
  loadFontAsync() {
    return Promise.resolve();
  },
  loadAllPagesAsync() {
    return Promise.resolve();
  },
  setCurrentPageAsync() {
    return Promise.resolve();
  },
  notify() {},
  closePlugin() {},
  viewport: { scrollAndZoomIntoView() {} },
};

const sandbox = {
  figma,
  console,
  Uint8Array,
  atob(s) {
    return Buffer.from(s, "base64").toString("binary");
  },
  setTimeout,
  clearTimeout,
  Promise,
  Math,
  Object,
  Array,
  String,
  Number,
  Error,
  Symbol,
};

const code =
  fs.readFileSync(__dirname + "/code.js", "utf8").replace(/\nmain\(\);\s*$/, "") +
  "\n;globalThis.__test = { CANDIDATES, buildCandidateFrame, buildFullKitPreview, buildComponentsShowcase, loadMenuImages, loadFonts, menuImageCache, isDs02Candidate, getDs02SemanticSwatches };";
const ctx = vm.createContext(sandbox);
vm.runInContext(code, ctx);

async function test() {
  const t = sandbox.__test;
  await t.loadFonts();
  await t.loadMenuImages();
  let failed = 0;

  const ds02 = t.CANDIDATES.find(function (c) {
    return c.id === "b";
  });
  if (!ds02 || !t.isDs02Candidate(ds02)) {
    failed++;
    console.error("FAIL: DS-02 candidate (id=b) not found");
  } else {
    const swatches = t.getDs02SemanticSwatches(ds02);
    const roles = swatches.map(function (s) {
      return s.role;
    });
    const expected = ["Primary", "Accent", "Surface", "Background", "Text", "Border", "Success", "Warning"];
    const okRoles = expected.every(function (r) {
      return roles.indexOf(r) >= 0;
    });
    const hasPink = swatches.some(function (s) {
      return /FF5C7A|FF4D8D|FF6B9D|FFC2D9/i.test(s.hex);
    });
    if (!okRoles || hasPink || swatches.length !== 8) {
      failed++;
      console.error("FAIL DS-02 semantic swatches:", JSON.stringify(swatches));
    } else {
      console.log("OK DS-02 semantic palette —", swatches.length, "tokens, no pink");
    }
  }

  for (let i = 0; i < t.CANDIDATES.length; i++) {
    const candidate = t.CANDIDATES[i];
    try {
      const frame = t.buildCandidateFrame(candidate, i);
      const kit = frame.children.find(function (c) {
        return c.name === "Full kit preview";
      });
      if (candidate.id === "b" && kit) {
        const semantic = kit.children.filter(function (c) {
          return c.name && c.name.indexOf("semantic /") === 0;
        });
        const ramps = kit.children.filter(function (c) {
          return c.name && c.name.indexOf("ramp /") === 0;
        });
        if (semantic.length < 8 || ramps.length > 0) {
          failed++;
          console.error(
            `FAIL ${candidate.frameName}: expected semantic swatches, got semantic=${semantic.length} ramps=${ramps.length}`
          );
        }
        const chips = kit.children.filter(function (c) {
          return c.name && c.name.indexOf("chip /") === 0;
        });
        if (chips.length < 3) {
          failed++;
          console.error(`FAIL ${candidate.frameName}: DS-02 kit chip row expected ≥3, got ${chips.length}`);
        } else {
          console.log(`OK ${candidate.frameName} — kit chip row: ${chips.length}`);
        }
      }
      console.log(`OK ${candidate.frameName} — children: ${frame.children.length}`);
    } catch (e) {
      failed++;
      console.error(`FAIL ${candidate.frameName}:`, e.message);
      if (e.stack) console.error(e.stack);
    }
  }
  if (failed > 0) process.exitCode = 1;
  else console.log(`All ${t.CANDIDATES.length} candidates built successfully`);
}

test();
