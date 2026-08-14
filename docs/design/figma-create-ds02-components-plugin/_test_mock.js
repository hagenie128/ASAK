/**
 * Mock test — verifies DS-02 plugin builds 40+ components / 25+ variant sets
 * Run: node docs/design/figma-create-ds02-components-plugin/_test_mock.js
 */
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
    opacity: 1,
    children: [],
    parent: null,
    visible: true,
    removed: false,
    appendChild(child) {
      if (child.parent && child.parent !== this) {
        const i = child.parent.children.indexOf(child);
        if (i >= 0) child.parent.children.splice(i, 1);
      }
      if (!this.children.includes(child)) this.children.push(child);
      child.parent = this;
      child.removed = false;
    },
    resize(w, h) {
      this.width = w;
      this.height = h;
    },
    rescale(s) {
      this.width *= s;
      this.height *= s;
      for (const child of this.children) {
        if (child.rescale) child.rescale(s);
        else {
          child.width *= s;
          child.height *= s;
          child.x *= s;
          child.y *= s;
        }
      }
    },
    remove() {
      for (const child of [...this.children]) child.remove();
      if (this.parent) {
        const i = this.parent.children.indexOf(this);
        if (i >= 0) this.parent.children.splice(i, 1);
      }
      this.removed = true;
    },
  };
  if (type === "TEXT") {
    node.characters = "";
    node.fontSize = 12;
    node.fontName = { family: "Inter", style: "Regular" };
    node.textAlignHorizontal = "LEFT";
    node.textAlignVertical = "TOP";
    node.textDecoration = "NONE";
  }
  if (type === "COMPONENT") node.type = "COMPONENT";
  if (type === "COMPONENT_SET") node.type = "COMPONENT_SET";
  if (type === "COMPONENT") {
    node.createInstance = function () {
      const inst = makeNode("INSTANCE");
      inst.width = this.width;
      inst.height = this.height;
      inst.name = this.name + " (instance)";
      return inst;
    };
  }
  return node;
}

let componentCount = 0;
let variantSetCount = 0;
const topLevelNodes = [];

const figma = {
  mixed: Symbol("mixed"),
  root: {
    children: [
      {
        type: "PAGE",
        name: "02. User Flow",
        children: [],
        appendChild(child) {
          if (child.parent && child.parent !== this) {
            const i = child.parent.children.indexOf(child);
            if (i >= 0) child.parent.children.splice(i, 1);
          }
          if (!this.children.includes(child)) this.children.push(child);
          child.parent = this;
          child.removed = false;
        },
      },
    ],
  },
  get currentPage() {
    return this.root.children[0];
  },
  createFrame() {
    return makeNode("FRAME");
  },
  createComponent() {
    componentCount++;
    return makeNode("COMPONENT");
  },
  combineAsVariants(parts, parent) {
    variantSetCount++;
    const set = makeNode("COMPONENT_SET");
    set.name = parts[0] ? parts[0].name.split(",")[0] : "Set";
    set.children = parts;
    parts.forEach((p) => {
      p.parent = set;
    });
    if (parent) parent.appendChild(set);
    return set;
  },
  createEllipse() {
    const n = makeNode("ELLIPSE");
    return n;
  },
  createRectangle() {
    return makeNode("RECTANGLE");
  },
  createPolygon() {
    return makeNode("POLYGON");
  },
  createText() {
    return makeNode("TEXT");
  },
  createImage(data) {
    if (!(data instanceof Uint8Array)) {
      throw new Error("createImage: Expected Uint8Array, received " + typeof data);
    }
    return { hash: "mock-kiosk-" + data.length };
  },
  createNodeFromSvg(svgString) {
    const frame = makeNode("FRAME");
    frame.resize(24, 24);
    frame.name = "svg-import";
    const v = makeNode("VECTOR");
    v.resize(20, 20);
    v.strokes = [{ type: "SOLID", color: { r: 0.1, g: 0.11, b: 0.13 } }];
    v.x = 2;
    v.y = 2;
    frame.appendChild(v);
    return frame;
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
  on() {},
};

const sandbox = {
  figma,
  console,
  globalThis: { __DS02_TEST__: true },
  Uint8Array,
  atob(s) {
    return Buffer.from(s, "base64").toString("binary");
  },
  Math,
  Object,
  Array,
  String,
  Number,
  Error,
  Symbol,
  Promise,
};

const codePath = __dirname + "/code.js";
const code = fs.readFileSync(codePath, "utf8");
vm.createContext(sandbox);
vm.runInContext(code, sandbox);

async function test() {
  const exp = sandbox.globalThis.__DS02_EXPORTS__;
  if (!exp) throw new Error("Missing __DS02_EXPORTS__");

  await exp.loadFonts();
  await exp.loadKioskIconSheet();
  exp.INVENTORY.variantSets = [];
  exp.INVENTORY.components = [];
  exp.INVENTORY.totalVariants = 0;
  componentCount = 0;
  variantSetCount = 0;

  const items = exp.buildAllComponents();
  const page = figma.root.children[0];
  const library = exp.layoutComponentLibrary(page, items);
  const summary = exp.getInventorySummary();

  let plainFramesInLibrary = 0;
  for (const child of library.children) {
    if (child.type === "FRAME" && child.name !== LIB_FRAME_EXEMPT(child.name)) {
      plainFramesInLibrary++;
    }
  }

  console.log("=== DS-02 Component Plugin Mock Test ===");
  console.log(`createComponent calls: ${componentCount}`);
  console.log(`combineAsVariants calls: ${variantSetCount}`);
  console.log(`Variant sets: ${summary.variantSets} (target ≥25)`);
  console.log(`Single components: ${summary.singleComponents}`);
  console.log(`Total component nodes: ${summary.totalComponentNodes} (target ≥40)`);
  console.log(`Library items placed: ${items.length}`);
  console.log(`Library frame children: ${library.children.length}`);

  const failures = [];
  if (summary.variantSets < 25) failures.push(`variant sets ${summary.variantSets} < 25`);
  if (summary.totalComponentNodes < 70) failures.push(`component nodes ${summary.totalComponentNodes} < 70`);
  if (variantSetCount < 25) failures.push(`combineAsVariants ${variantSetCount} < 25`);
  if (items.length < 70) failures.push(`library items ${items.length} < 70`);

  const uiItems = items.filter((i) => i.category === "IconUI");
  if (uiItems.length !== exp.MAGNIFIC_UI_ICON_SPECS.length) {
    failures.push(`IconUI items ${uiItems.length} !== ${exp.MAGNIFIC_UI_ICON_SPECS.length}`);
  }
  for (const item of uiItems) {
    if (!item.node.name.startsWith("DS-02 / Icon / UI /")) {
      failures.push(`IconUI bad name: ${item.node.name}`);
    }
    const svgChild = item.node.children.find((c) => c.name === "svg-import" || c.type === "FRAME");
    if (!svgChild) failures.push(`IconUI missing SVG child: ${item.node.name}`);
  }

  const sheetItems = items.filter((i) => i.category === "IconSheet");
  if (sheetItems.length !== 16) failures.push(`IconSheet items ${sheetItems.length} !== 16`);
  const specByName = Object.fromEntries(exp.KIOSK_ICON_SPECS.map((s) => [s.name, s]));
  for (const item of sheetItems) {
    const imgChild = item.node.children.find((c) => c.fills && c.fills[0] && c.fills[0].type === "IMAGE");
    if (!imgChild) {
      failures.push(`IconSheet missing IMAGE fill: ${item.node.name}`);
      continue;
    }
    const fill = imgChild.fills[0];
    const label = item.node.name.replace("DS-02 / Icon / ", "");
    const spec = specByName[label];
    if (!spec) {
      failures.push(`IconSheet unknown spec: ${label}`);
      continue;
    }
    if (fill.scaleMode === "FILL") {
      if (imgChild.width !== 64 || imgChild.height !== 64) {
        failures.push(`IconSheet rect not 64×64: ${item.node.name}`);
      }
      continue;
    }
    if (fill.scaleMode !== "CROP") {
      failures.push(`IconSheet scaleMode must be CROP or FILL: ${item.node.name} (${fill.scaleMode})`);
    }
    const m = fill.imageTransform;
    const expected = exp.kioskIconTransform(spec.col, spec.row);
    const same =
      m &&
      m.length === 2 &&
      m[0][0] === expected[0][0] &&
      m[0][2] === expected[0][2] &&
      m[1][1] === expected[1][1] &&
      m[1][2] === expected[1][2];
    if (!same) {
      const got =
        m && m[0] && m[1] ? `[${m[0][2]},${m[1][2]}]` : String(m);
      failures.push(
        `IconSheet imageTransform mismatch ${label}: got ${got} want [${expected[0][2]},${expected[1][2]}]`
      );
    }
    if (imgChild.width !== 64 || imgChild.height !== 64) {
      failures.push(`IconSheet rect not 64×64: ${item.node.name}`);
    }
  }

  for (const item of items) {
    const t = item.node.type;
    if (item.node.removed) {
      failures.push(`removed node in items: ${item.category}`);
      continue;
    }
    if (t !== "COMPONENT" && t !== "COMPONENT_SET") {
      failures.push(`non-component output: ${item.category} (${t})`);
    }
  }

  if (exp.T.radiusSm !== 10) failures.push(`radiusSm ${exp.T.radiusSm} !== 10`);
  if (exp.T.radiusMd !== 12) failures.push(`radiusMd ${exp.T.radiusMd} !== 12`);
  if (exp.T.radiusLg !== 16) failures.push(`radiusLg ${exp.T.radiusLg} !== 16`);
  if (exp.T.stroke !== 2) failures.push(`stroke ${exp.T.stroke} !== 2`);
  if (/#3B82F6|#4B96E7/i.test(exp.T.info || "")) failures.push(`blue info token ${exp.T.info}`);

  const chipItem = items.find((i) => i.category === "Chip");
  if (!chipItem) {
    failures.push("Chip variant set missing");
  } else if (chipItem.node.children) {
    for (const want of ["State=Default", "State=Selected", "State=Disabled"]) {
      if (!chipItem.node.children.some((c) => c.name.includes(want))) failures.push(`chip missing ${want}`);
    }
    for (const child of chipItem.node.children) {
      if (child.strokeWeight !== exp.T.stroke) failures.push(`chip strokeWeight ${child.strokeWeight}`);
      if (child.cornerRadius !== exp.T.radiusSm) failures.push(`chip radius ${child.cornerRadius}`);
    }
  }

  const buttonItem = items.find((i) => i.category === "Button");
  if (!buttonItem) {
    failures.push("Button variant set missing");
  } else {
    const buttonVariants = buttonItem.node.children ? buttonItem.node.children.length : 0;
    const expectedButtonVariants = exp.BUTTON_STYLE_DEFS.length * exp.BUTTON_SIZE_DEFS.length;
    console.log(`Button variants: ${buttonVariants} (target ≥10, full matrix ${expectedButtonVariants})`);
    if (buttonVariants < 10) failures.push(`button variants ${buttonVariants} < 10`);
    if (buttonVariants !== expectedButtonVariants) {
      failures.push(`button variants ${buttonVariants} !== ${expectedButtonVariants}`);
    }
    for (const child of buttonItem.node.children || []) {
      if (child.cornerRadius !== exp.T.radiusBtn) {
        failures.push(`button cornerRadius ${child.cornerRadius} !== ${exp.T.radiusBtn}`);
        break;
      }
    }
  }

  if (failures.length) {
    console.error("FAIL:", failures.join("; "));
    process.exitCode = 1;
  } else {
    console.log("OK — all targets met");
    console.log("\nVariant sets:");
    summary.sets.forEach((s) => console.log("  ·", s));
    console.log(`\nSingle components (${summary.singles.length}):`);
    summary.singles.forEach((s) => console.log("  ·", s));
  }

  // ─── Full UI Kit mock test ───
  console.log("\n=== DS-02 Full UI Kit Mock Test ===");
  exp.resetFullKitInventory();
  exp.INVENTORY.variantSets = [];
  exp.INVENTORY.components = [];
  exp.INVENTORY.totalVariants = 0;
  componentCount = 0;
  variantSetCount = 0;

  const kitPage = figma.root.children[0];
  const kitFrame = exp.buildY2KStyleFullKit(kitPage);
  const kitSummary = exp.getFullKitSummary();

  console.log(`Kit frame: ${kitFrame.name}`);
  console.log(`Sections: ${kitSummary.sections} (target ≥20)`);
  console.log(`Component nodes in kit: ${kitSummary.componentNodes} (target ≥150)`);
  console.log(`Section titles: ${kitSummary.sectionTitles.length}`);

  const kitFailures = [];
  if (kitSummary.sections < 20) kitFailures.push(`sections ${kitSummary.sections} < 20`);
  if (kitSummary.componentNodes < 150) kitFailures.push(`components ${kitSummary.componentNodes} < 150`);
  if (kitSummary.sectionTitles.length !== exp.Y2K_KIT_SECTIONS.length) {
    kitFailures.push(`section count mismatch ${kitSummary.sectionTitles.length} !== ${exp.Y2K_KIT_SECTIONS.length}`);
  }
  if (kitFrame.name !== exp.FULL_KIT_FRAME_NAME) kitFailures.push(`frame name ${kitFrame.name}`);
  if (!kitSummary.sectionTitles.includes("Chip")) kitFailures.push("missing Chip section in full kit");

  for (const sec of kitFrame.children) {
    if (sec.type !== "FRAME" || sec.name === kitFrame.name) continue;
    let hasComp = false;
    function walk(n) {
      if (n.type === "COMPONENT" || n.type === "COMPONENT_SET") hasComp = true;
      if (n.children) n.children.forEach(walk);
    }
    walk(sec);
    if (!hasComp) kitFailures.push(`section empty of components: ${sec.name}`);
  }

  if (kitFailures.length) {
    console.error("KIT FAIL:", kitFailures.join("; "));
    process.exitCode = 1;
  } else {
    console.log("KIT OK — sections ≥20, components ≥150");
  }
}

function LIB_FRAME_EXEMPT(name) {
  return false;
}

test().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
