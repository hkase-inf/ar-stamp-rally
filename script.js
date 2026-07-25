const BIO_PAGE = "https://wwp.shizuoka.ac.jp/vision-i/%E6%83%85%E5%A0%B1%E5%AD%A6%E3%81%AE%E5%81%89%E4%BA%BA/";

const FIGURES = [
  {
    id: "grace-hopper",
    name: "Grace Hopper",
    qrMatch: "gratefigures_01",
    stampImg: "assets/grace-hopper-stamp.png",
    bio: "1906–1992。アメリカ海軍少将であり計算機科学者。プログラミング言語を人間にとって読みやすいものにしようと、世界最初期のコンパイラを開発しました。その成果は後にCOBOLの誕生へとつながり、今日の情報システムの基盤を築いたことから「コンピュータプログラミングの母」とも呼ばれています。",
    bioLink: BIO_PAGE + "#gratefigures_01",
  },
  {
    id: "tim-berners-lee",
    name: "Tim Berners-Lee",
    qrMatch: "gratefigures_02",
    stampImg: "assets/tim-berners-lee-stamp.png",
    bio: "1955–。英国出身の計算機科学者。CERN在籍中の1990年、研究成果を共有する仕組みとしてワールド・ワイド・ウェブ（WWW）を考案し、世界初のウェブサイトとブラウザを開発しました。現代のインターネット社会の土台を築いた人物です。",
    bioLink: BIO_PAGE + "#gratefigures_02",
  },
  {
    id: "marvin-minsky",
    name: "Marvin Minsky",
    qrMatch: "greatfigures_03",
    stampImg: "assets/marvin-minsky-stamp.png",
    bio: "1927–2016。アメリカの認知科学者・AI研究者。1959年にMITで人工知能研究所を共同設立し、「人工知能」という分野を切り拓いた第一人者の一人です。著書『The Society of Mind』では、心とは単純な仕組みが数多く協調して生まれるものだという理論を提唱しました。",
    bioLink: BIO_PAGE + "#greatfigures_03",
  },
  {
    id: "alan-turing",
    name: "Alan Turing",
    qrMatch: "greatfigures_04",
    stampImg: "assets/alan-turing-stamp.png",
    bio: "1912–1954。現代計算機科学の基礎を築いた数学者。1936年、抽象的な計算のしくみである「チューリングマシン」を考案し、「計算とは何か」を理論化しました。1950年には機械が思考しうるかを問う「チューリングテスト」を提示しています。",
    bioLink: BIO_PAGE + "#greatfigures_04",
  },
  {
    id: "claude-shannon",
    name: "Claude Shannon",
    qrMatch: "greatfigures_05",
    stampImg: "assets/claude-shannon-stamp.png",
    bio: "1916–2001。「情報理論」の生みの親。1948年の論文で情報量やビット、通信容量といった概念を数学的に定義し、雑音のある通信路でも誤り訂正しながら正確に情報を伝えられることを示しました。今日のデジタル通信・インターネットの理論的土台です。",
    bioLink: BIO_PAGE + "#greatfigures_05",
  },
  {
    id: "john-von-neumann",
    name: "John von Neumann",
    qrMatch: "greatfigures_06",
    stampImg: "assets/john-von-neumann-stamp.png",
    bio: "1903–1957。数学・物理・経済など複数分野にまたがる業績を残した学者。プログラムとデータを同じメモリに格納する「ノイマン型」のコンピュータ構造を提案し、今日のほぼすべてのコンピュータの基本設計として使われています。ゲーム理論の確立者でもあります。",
    bioLink: BIO_PAGE + "#greatfigures_06",
  },
  {
    id: "alan-kay",
    name: "Alan Kay",
    qrMatch: "greatfigures_07",
    stampImg: "assets/alan-kay-stamp.png",
    bio: "1940–。Xerox PARCで活躍した計算機科学者。開発した言語Smalltalkはオブジェクト指向プログラミングの先駆けとなり、後のJavaやPython、GUIの考え方に影響を与えました。1970年代には、誰もが使える携帯型の知的道具「Dynabook」を構想し、今日のタブレットやノートPCの原型となりました。",
    bioLink: BIO_PAGE + "#greatfigures_07",
  },
  {
    id: "jun-murai",
    name: "村井純",
    qrMatch: "greatfigures_08",
    stampImg: "assets/jun-murai-stamp.png",
    bio: "1955–。日本にインターネット技術を導入し、学術ネットワークから商用インターネットへの普及を主導した人物で、「日本のインターネットの父」と呼ばれています。1980年代にWIDEプロジェクトを立ち上げ、日本のネットワーク基盤づくりを牽引しました。",
    bioLink: BIO_PAGE + "#greatfigures_08",
  },
  {
    id: "herbert-simon",
    name: "Herbert A. Simon",
    qrMatch: "greatfigures_09",
    stampImg: "assets/herbert-simon-stamp.png",
    bio: "1916–2001。認知科学・経済学など幅広い分野で革新的理論を残した学者。人工知能の草創期には知能をシンボル操作として捉える理論を提唱し、経済学では人間の意思決定を現実的にとらえる「限定合理性」の概念を導入しました。1978年にノーベル経済学賞を受賞しています。",
    bioLink: BIO_PAGE + "#greatfigures_09",
  },
];

const STORAGE_KEY = "arRallyStamps";

function getCollected() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveCollected(list) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
}

function showScreen(id) {
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}

/* ---------------- QR marker recognition ---------------- */
/* The posters already carry a citation QR code (e.g. .../情報学の偉人/#gratefigures_01).
   Each figure's QR encodes a unique #gratefigures_NN anchor, so we reuse it as the
   AR recognition trigger instead of asking for a new dedicated code. */

const video = document.getElementById("camera-feed");
const qrCanvas = document.getElementById("qr-canvas");
const qrCtx = qrCanvas.getContext("2d", { willReadFrequently: true });
const hudText = document.getElementById("hud-text");
const btnScan = document.getElementById("btn-scan");
const cameraFallback = document.getElementById("camera-fallback");

const HUD_DEFAULT = "ポスターのQRコードを\n枠の中に収めてね";
const HUD_FOUND = "認識しました！\nボタンをタップしてスタンプGET";

const LOST_GRACE_MS = 800;
const SCAN_INTERVAL_MS = 250;

let mediaStream = null;
let scanTimer = null;
let recognizedFigure = null;
let lastMatchAt = 0;

function setHud(text) {
  hudText.innerHTML = text.replace(/\n/g, "<br>");
}

function matchFigureFromQr(data) {
  return FIGURES.find(fig => fig.qrMatch && data.includes(fig.qrMatch)) || null;
}

function setRecognized(figure) {
  recognizedFigure = figure;
  if (figure) {
    setHud(HUD_FOUND);
    btnScan.classList.remove("hidden");
  } else {
    setHud(HUD_DEFAULT);
    btnScan.classList.add("hidden");
  }
}

function scanFrame() {
  if (!video.videoWidth) return;
  qrCanvas.width = video.videoWidth;
  qrCanvas.height = video.videoHeight;
  qrCtx.drawImage(video, 0, 0, qrCanvas.width, qrCanvas.height);

  const imageData = qrCtx.getImageData(0, 0, qrCanvas.width, qrCanvas.height);
  const code = jsQR(imageData.data, imageData.width, imageData.height, {
    inversionAttempts: "dontInvert",
  });

  const now = Date.now();
  const matched = code && code.data ? matchFigureFromQr(code.data) : null;

  if (matched) {
    lastMatchAt = now;
    if (!recognizedFigure || recognizedFigure.id !== matched.id) setRecognized(matched);
  } else if (recognizedFigure && now - lastMatchAt > LOST_GRACE_MS) {
    setRecognized(null);
  }
}

async function startAR() {
  cameraFallback.classList.add("hidden");
  setRecognized(null);

  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
      audio: false,
    });
    video.srcObject = mediaStream;
    scanTimer = setInterval(scanFrame, SCAN_INTERVAL_MS);
  } catch (err) {
    console.warn("camera unavailable", err);
    cameraFallback.classList.remove("hidden");
  }
}

function stopAR() {
  if (scanTimer) {
    clearInterval(scanTimer);
    scanTimer = null;
  }
  if (mediaStream) {
    mediaStream.getTracks().forEach(t => t.stop());
    mediaStream = null;
  }
  setRecognized(null);
}

/* ---------------- stamp passport ---------------- */

function renderPassport(justFilledId) {
  const grid = document.getElementById("passport-grid");
  const collected = getCollected();
  grid.innerHTML = "";

  FIGURES.forEach(fig => {
    const slot = document.createElement("div");
    const isFilled = collected.includes(fig.id);
    slot.className = "stamp-slot" + (isFilled ? " filled" : "");
    if (fig.id === justFilledId) slot.classList.add("just-filled");

    if (isFilled) {
      const img = document.createElement("img");
      img.src = fig.stampImg;
      img.alt = fig.name;
      slot.appendChild(img);
    } else {
      const q = document.createElement("span");
      q.className = "slot-q";
      q.textContent = "?";
      slot.appendChild(q);
    }

    const label = document.createElement("span");
    label.className = "slot-label";
    label.textContent = fig.name;
    slot.appendChild(label);

    grid.appendChild(slot);
  });

  document.getElementById("stamp-count").textContent = collected.length;
  const showBonus = collected.length >= FIGURES.length;
  document.getElementById("btn-bonus-enter").classList.toggle("hidden", !showBonus);
  document.getElementById("bonus-enter-hint").classList.toggle("hidden", !showBonus);
}

/* ---------------- little synth "thunk" sound ---------------- */

function playThunk() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(180, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(70, ctx.currentTime + 0.18);
    gain.gain.setValueAtTime(0.35, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.22);
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.22);
  } catch {
    /* audio not available, ignore */
  }
}

function showFigureBio(figure) {
  const bio = document.getElementById("figure-bio");
  document.getElementById("figure-bio-name").textContent = figure.name;
  document.getElementById("figure-bio-text").textContent = figure.bio || "";
  const link = document.getElementById("figure-bio-link");
  if (figure.bioLink) {
    link.href = figure.bioLink;
    link.classList.remove("hidden");
  } else {
    link.classList.add("hidden");
  }
  bio.classList.remove("hidden");
}

function triggerStamp() {
  if (!recognizedFigure) return;
  const figure = recognizedFigure;
  const collected = getCollected();
  const id = figure.id;
  const alreadyHad = collected.includes(id);
  if (!alreadyHad) {
    collected.push(id);
    saveCollected(collected);
  }

  showScreen("screen-stamp");
  document.getElementById("screen-stamp").classList.add("active");
  document.getElementById("figure-bio").classList.add("hidden");

  // restart the fx animations every time, even if the stamp screen was
  // already visible (CSS animations only auto-replay on a display:none -> block
  // transition, so force it explicitly via the animation:none reflow trick)
  document.querySelector(".stamp-image").src = figure.stampImg;
  document.querySelectorAll(".stamp-image, .ink-ring, .get-label").forEach(el => {
    el.style.animation = "none";
    void el.offsetWidth;
    el.style.animation = "";
  });

  renderPassport(alreadyHad ? null : id);
  setTimeout(playThunk, 350);
  setTimeout(() => showFigureBio(figure), 1950);
}

/* ---------------- bonus stage (shizuppi photo booth) ---------------- */
/* Three.js + the mascot model are only fetched the first time a visitor
   actually reaches this screen (9/9 stamps) -- never on initial page load. */

let threeModules = null; // cached after first dynamic import
let bonusStream = null;
let bonusFacingMode = "environment"; // default to the rear camera; flip button switches to selfie
let bonusRenderer, bonusScene, bonusCamera, bonusMixer, bonusClock, bonusRAF;
let bonusModel = null;
let bonusClips = {};
let bonusActiveAction = null;

// the model faces the camera at a fixed small scale (its low-poly mesh
// looks rough up close); drag repositions it around the frame instead
const BONUS_FRONT_ROTATION_Y = -Math.PI / 2; // rotates the model's front to face the camera
const BONUS_FIXED_SCALE = 0.4;
let bonusModelSize = null; // THREE.Vector3, set at load time, used to clamp drag bounds
let bonusModelBaseX = 0;
let bonusModelBaseY = 0;
let bonusOffsetX = 0;
let bonusOffsetY = 0;

function applyBonusTransform() {
  if (!bonusModel) return;
  bonusModel.rotation.y = BONUS_FRONT_ROTATION_Y;
  bonusModel.scale.setScalar(BONUS_FIXED_SCALE);
  bonusModel.position.x = bonusModelBaseX + bonusOffsetX;
  bonusModel.position.y = bonusModelBaseY + bonusOffsetY;
}

async function loadThreeModules() {
  if (threeModules) return threeModules;
  const [THREE, { GLTFLoader }, { DRACOLoader }] = await Promise.all([
    import("three"),
    import("three/addons/loaders/GLTFLoader.js"),
    import("three/addons/loaders/DRACOLoader.js"),
  ]);
  threeModules = { THREE, GLTFLoader, DRACOLoader };
  return threeModules;
}

function setupBonusScene(THREE, canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.set(0, 0.2, 5.2);
  camera.lookAt(0, -0.2, 0);

  scene.add(new THREE.AmbientLight(0xffffff, 1.2));
  const key = new THREE.DirectionalLight(0xffffff, 1.8);
  key.position.set(2, 3, 4);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xffffff, 0.6);
  fill.position.set(-3, 1, 2);
  scene.add(fill);

  return { renderer, scene, camera };
}

function resizeBonusRenderer() {
  if (!bonusRenderer) return;
  const el = document.getElementById("screen-bonus");
  const w = el.clientWidth, h = el.clientHeight;
  bonusRenderer.setSize(w, h, false);
  bonusCamera.aspect = w / h;
  bonusCamera.updateProjectionMatrix();
}

async function initBonusThree() {
  const { THREE, GLTFLoader, DRACOLoader } = await loadThreeModules();
  const canvas = document.getElementById("bonus-three-canvas");
  const built = setupBonusScene(THREE, canvas);
  bonusRenderer = built.renderer;
  bonusScene = built.scene;
  bonusCamera = built.camera;
  resizeBonusRenderer();

  const dracoLoader = new DRACOLoader();
  dracoLoader.setDecoderPath("https://unpkg.com/three@0.160.0/examples/jsm/libs/draco/");
  const gltfLoader = new GLTFLoader();
  gltfLoader.setDRACOLoader(dracoLoader);

  const gltf = await new Promise((resolve, reject) => {
    gltfLoader.load("assets/shizuppi.glb", resolve, undefined, reject);
  });

  const model = gltf.scene;
  model.rotation.y = BONUS_FRONT_ROTATION_Y; // face the model's front toward the camera
  bonusScene.add(model);
  bonusModel = model;

  // these props were exported as static children instead of following their
  // bone's pose animation -- re-parent them onto the actual joint node
  // (.attach keeps their current world position/rotation while doing so)

  // Debug: dump all object names to help diagnose reparenting issues
  console.log("=== GLB object names ===");
  model.traverse(node => {
    if (node.name) console.log(`  [${node.type}] "${node.name}"`);
  });

  // Fuzzy-match helper: NFC-normalize both sides to handle encoding differences
  // that can occur when Japanese names are stored in GLB files
  function findNodeFuzzy(root, name) {
    const normName = name.normalize("NFC");
    let found = null;
    root.traverse(node => {
      if (found) return;
      if (node.name.normalize("NFC") === normName) found = node;
    });
    return found;
  }

  const REPARENT_MAP = { "帽子": "Head", "右目": "Head", "左目": "Head", "鼻": "Head", "揺れもの": "Head", "足": "Hip" };
  Object.entries(REPARENT_MAP).forEach(([objName, boneName]) => {
    const obj = findNodeFuzzy(model, objName);
    const bone = findNodeFuzzy(model, boneName);
    console.log(`Reparent "${objName}" → "${boneName}": obj=${!!obj}, bone=${!!bone}`);
    if (obj && bone && obj.parent !== bone) bone.attach(obj);
  });

  // flat/unlit-style shading: hides low-poly faceting that directional
  // lighting would otherwise reveal as visible shaded facets.
  // NOTE: For GLTF MASK alpha mode, Three.js sets transparent=false + alphaTest=cutoff;
  // MeshBasicMaterial handles this correctly without forcing transparent=true.
  model.traverse(node => {
    if (!node.isMesh || !node.material) return;
    const toBasic = mat => new THREE.MeshBasicMaterial({
      map: mat.map || null,
      color: mat.map ? 0xffffff : mat.color,
      transparent: mat.transparent,
      alphaTest: mat.alphaTest,
      side: mat.side,
    });
    node.material = Array.isArray(node.material)
      ? node.material.map(toBasic)
      : toBasic(node.material);
    // Alpha-test cutout meshes (eyes, nose, etc.) must render after opaque geometry
    const hasAlphaTest = Array.isArray(node.material)
      ? node.material.some(m => m.alphaTest > 0)
      : node.material.alphaTest > 0;
    if (hasAlphaTest) node.renderOrder = 1;
  });

  // frame the camera for the model's full (unscaled) size -- this leaves
  // visible room around the smaller, fixed-scale model for repositioning
  const fullBox = new THREE.Box3().setFromObject(model);
  const fullSize = new THREE.Vector3();
  fullBox.getSize(fullSize);

  const JUMP_EXTRA = 1.5;
  const halfHeight = (fullSize.y + JUMP_EXTRA) / 2 * 1.15;
  const dist = halfHeight / Math.tan((bonusCamera.fov / 2) * Math.PI / 180);
  bonusCamera.position.set(0, fullSize.y * 0.45, dist);
  bonusCamera.lookAt(0, fullSize.y * 0.45, 0);

  // now apply the fixed display scale and re-center/floor at that size
  model.scale.setScalar(BONUS_FIXED_SCALE);
  const box = new THREE.Box3().setFromObject(model);
  const size = new THREE.Vector3();
  box.getSize(size);
  const center = new THREE.Vector3();
  box.getCenter(center);
  model.position.x -= center.x;
  model.position.z -= center.z;
  model.position.y -= box.min.y;

  bonusModelBaseX = model.position.x;
  bonusModelBaseY = model.position.y;
  bonusModelSize = size;
  bonusOffsetX = 0;
  bonusOffsetY = 0;
  applyBonusTransform();

  bonusMixer = new THREE.AnimationMixer(model);
  bonusClips = {};
  gltf.animations.forEach(clip => { bonusClips[clip.name] = clip; });
  playBonusMotion("Wave");

  bonusClock = new THREE.Clock();
  startBonusRenderLoop();
}

function startBonusRenderLoop() {
  if (bonusRAF) return; // already running
  bonusClock.getDelta(); // drop the idle gap since the last frame
  const tick = () => {
    bonusRAF = requestAnimationFrame(tick);
    if (bonusMixer) bonusMixer.update(bonusClock.getDelta());
    bonusRenderer.render(bonusScene, bonusCamera);
  };
  tick();
}

function stopBonusRenderLoop() {
  if (bonusRAF) cancelAnimationFrame(bonusRAF);
  bonusRAF = null;
}

function playBonusMotion(name) {
  const clip = bonusClips[name];
  if (!clip || !bonusMixer) return;
  const nextAction = bonusMixer.clipAction(clip);
  if (bonusActiveAction && bonusActiveAction !== nextAction) {
    bonusActiveAction.fadeOut(0.3);
  }
  nextAction.reset().fadeIn(0.3).play();
  bonusActiveAction = nextAction;

  document.querySelectorAll(".btn-motion").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.motion === name);
  });
}

/* --- drag to reposition the (fixed-scale) model around the frame --- */
const bonusPointers = new Map();
let bonusDragLastX = null;
let bonusDragLastY = null;

function bonusDragBounds() {
  // base the draggable range on what's actually visible in the camera
  // frustum at the model's depth, so landscape (much wider) gets a wider
  // range instead of being limited by the model's own fixed size
  const depth = Math.abs(bonusCamera.position.z - (bonusModel ? bonusModel.position.z : 0));
  const vFov = (bonusCamera.fov * Math.PI) / 180;
  const visibleHeight = 2 * Math.tan(vFov / 2) * depth;
  const visibleWidth = visibleHeight * bonusCamera.aspect;
  const s = bonusModelSize || { y: 4 };
  return {
    maxX: (visibleWidth / 2) * 0.42,
    minY: -s.y * 0.15,
    maxY: visibleHeight * 0.42,
  };
}

function bonusPointerDown(e) {
  if (bonusPointers.size === 0) {
    bonusDragLastX = e.clientX;
    bonusDragLastY = e.clientY;
  }
  bonusPointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
}

function bonusPointerMove(e) {
  if (!bonusPointers.has(e.pointerId)) return;
  bonusPointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  if (bonusPointers.size !== 1 || bonusDragLastX === null || !bonusModel) return;

  const el = document.getElementById("screen-bonus");
  const depth = Math.abs(bonusCamera.position.z - bonusModel.position.z);
  const vFov = (bonusCamera.fov * Math.PI) / 180;
  const worldPerPixel = (2 * Math.tan(vFov / 2) * depth) / el.clientHeight;

  const dxPixels = e.clientX - bonusDragLastX;
  const dyPixels = e.clientY - bonusDragLastY;
  bonusDragLastX = e.clientX;
  bonusDragLastY = e.clientY;

  const bounds = bonusDragBounds();
  bonusOffsetX = Math.max(-bounds.maxX, Math.min(bounds.maxX, bonusOffsetX + dxPixels * worldPerPixel));
  const newBaseRelativeY = bonusOffsetY - dyPixels * worldPerPixel; // screen-down = world-down
  bonusOffsetY = Math.max(bounds.minY - bonusModelBaseY, Math.min(bounds.maxY - bonusModelBaseY, newBaseRelativeY));
  applyBonusTransform();
}

function bonusPointerUp(e) {
  bonusPointers.delete(e.pointerId);
  if (bonusPointers.size === 0) {
    bonusDragLastX = null;
    bonusDragLastY = null;
  }
}

async function startBonusCamera() {
  const video = document.getElementById("bonus-camera-feed");
  const fallback = document.getElementById("bonus-camera-fallback");
  fallback.classList.add("hidden");
  try {
    bonusStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: bonusFacingMode },
      audio: false,
    });
    video.srcObject = bonusStream;
    // インカメラのときは左右を鏡像にして自然に見えるようにする
    video.classList.toggle("mirrored", bonusFacingMode === "user");
  } catch (err) {
    console.warn("bonus camera unavailable", err);
    fallback.classList.remove("hidden");
  }
}

function stopBonusCamera() {
  if (bonusStream) {
    bonusStream.getTracks().forEach(t => t.stop());
    bonusStream = null;
  }
}

function onBonusOrientationChange() {
  // mobile browsers often report stale inner dimensions right at the event
  setTimeout(resizeBonusRenderer, 50);
  setTimeout(resizeBonusRenderer, 300);
}

async function enterBonusStage() {
  showScreen("screen-bonus");
  document.getElementById("bonus-result").classList.add("hidden");
  document.getElementById("btn-bonus-capture").classList.add("hidden");
  document.getElementById("bonus-loading").classList.remove("hidden");

  await startBonusCamera();
  try {
    if (!bonusRenderer) {
      await initBonusThree();
    } else {
      resizeBonusRenderer();
      startBonusRenderLoop();
    }
    window.addEventListener("resize", resizeBonusRenderer);
    window.addEventListener("orientationchange", onBonusOrientationChange);
    document.getElementById("btn-bonus-capture").classList.remove("hidden");
  } catch (err) {
    console.error("failed to load bonus stage 3D content", err);
  }
  document.getElementById("bonus-loading").classList.add("hidden");
}

function exitBonusStage() {
  stopBonusCamera();
  stopBonusRenderLoop();
  window.removeEventListener("resize", resizeBonusRenderer);
  window.removeEventListener("orientationchange", onBonusOrientationChange);
  showScreen("screen-stamp");
}

async function flipBonusCamera() {
  bonusFacingMode = bonusFacingMode === "user" ? "environment" : "user";
  stopBonusCamera();
  await startBonusCamera();
}

function captureBonusPhoto() {
  const video = document.getElementById("bonus-camera-feed");
  const threeCanvas = document.getElementById("bonus-three-canvas");
  const out = document.getElementById("bonus-capture-canvas");

  // 画面の表示サイズ（CSS pixels × devicePixelRatio）を基準にする。
  // カメラ映像の解像度を使うと、画面アスペクト比と食い違い
  // しずっぴーが引き伸ばされて見える問題が起きるため。
  const screenEl = document.getElementById("screen-bonus");
  const dpr = window.devicePixelRatio || 1;
  const w = screenEl.clientWidth * dpr;
  const h = screenEl.clientHeight * dpr;
  out.width = w;
  out.height = h;
  const ctx = out.getContext("2d");

  // カメラ映像を画面いっぱいに (object-fit: cover と同じ挙動) 描画
  const vw = video.videoWidth || 1;
  const vh = video.videoHeight || 1;
  const scale = Math.max(w / vw, h / vh);
  const dw = vw * scale;
  const dh = vh * scale;
  const dx = (w - dw) / 2;
  const dy = (h - dh) / 2;

  if (bonusFacingMode === "user") {
    // インカメラ：プレビューと同じ鏡像で合成する
    ctx.save();
    ctx.translate(w, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(video, dx, dy, dw, dh);
    ctx.restore();
  } else {
    ctx.drawImage(video, dx, dy, dw, dh);
  }

  // Three.js キャンバスをそのまま全面に重ねる（こちらはすでに画面比）
  ctx.drawImage(threeCanvas, 0, 0, w, h);

  out.toBlob(blob => {
    const url = URL.createObjectURL(blob);
    const img = document.getElementById("bonus-result-img");
    img.src = url;
    img.dataset.blobUrl = url;
    document.getElementById("bonus-result").classList.remove("hidden");
  }, "image/png");
}

async function saveBonusPhoto() {
  const img = document.getElementById("bonus-result-img");
  const resp = await fetch(img.src);
  const blob = await resp.blob();
  const file = new File([blob], "shizuppi.png", { type: "image/png" });

  if (navigator.canShare && navigator.canShare({ files: [file] })) {
    try {
      await navigator.share({ files: [file], title: "しずっぴーと記念写真" });
      return;
    } catch (err) {
      if (err.name === "AbortError") return;
      console.warn("share failed, falling back to download", err);
    }
  }

  const a = document.createElement("a");
  a.href = img.src;
  a.download = "shizuppi.png";
  document.body.appendChild(a);
  a.click();
  a.remove();
}

/* ---------------- wiring ---------------- */

document.getElementById("btn-open-camera").addEventListener("click", () => {
  showScreen("screen-camera");
  startAR();
});

document.getElementById("btn-back-start").addEventListener("click", () => {
  stopAR();
  showScreen("screen-start");
});

document.getElementById("btn-scan").addEventListener("click", triggerStamp);

document.getElementById("btn-continue").addEventListener("click", () => {
  showScreen("screen-camera");
});

document.getElementById("btn-bonus-enter").addEventListener("click", enterBonusStage);
document.getElementById("btn-bonus-back").addEventListener("click", exitBonusStage);
document.getElementById("btn-bonus-flip").addEventListener("click", flipBonusCamera);
document.getElementById("btn-bonus-capture").addEventListener("click", captureBonusPhoto);
document.getElementById("btn-bonus-save").addEventListener("click", saveBonusPhoto);
document.getElementById("btn-bonus-retake").addEventListener("click", () => {
  const img = document.getElementById("bonus-result-img");
  if (img.dataset.blobUrl) URL.revokeObjectURL(img.dataset.blobUrl);
  document.getElementById("bonus-result").classList.add("hidden");
});

document.querySelectorAll(".btn-motion").forEach(btn => {
  btn.addEventListener("click", () => playBonusMotion(btn.dataset.motion));
});

const bonusGestureSurface = document.getElementById("bonus-three-canvas");
bonusGestureSurface.addEventListener("pointerdown", bonusPointerDown);
bonusGestureSurface.addEventListener("pointermove", bonusPointerMove);
bonusGestureSurface.addEventListener("pointerup", bonusPointerUp);
bonusGestureSurface.addEventListener("pointercancel", bonusPointerUp);
bonusGestureSurface.addEventListener("pointerleave", bonusPointerUp);

// debug-only shortcut for testing: fills every stamp and jumps straight to
// the bonus stage so it doesn't need to be reached by scanning all 9 QR codes
document.getElementById("btn-debug-fill").addEventListener("click", () => {
  saveCollected(FIGURES.map(f => f.id));
  renderPassport(null);
  showScreen("screen-stamp");
  enterBonusStage();
});

renderPassport(null);
