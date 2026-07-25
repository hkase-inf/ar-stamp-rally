const FIGURES = [
  { id: "grace-hopper",     name: "Grace Hopper",      demo: true, qrMatch: "gratefigures_01" },
  { id: "tim-berners-lee",  name: "Tim Berners-Lee",   demo: false },
  { id: "marvin-minsky",    name: "Marvin Minsky",     demo: false },
  { id: "alan-turing",      name: "Alan Turing",       demo: false },
  { id: "claude-shannon",   name: "Claude Shannon",    demo: false },
  { id: "john-von-neumann", name: "John von Neumann",  demo: false },
  { id: "alan-kay",         name: "Alan Kay",          demo: false },
  { id: "jun-murai",        name: "村井純",             demo: false },
  { id: "herbert-simon",    name: "Herbert A. Simon",  demo: false },
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
      img.src = "assets/grace-hopper-stamp.png";
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

function triggerStamp() {
  if (!recognizedFigure) return;
  const collected = getCollected();
  const id = recognizedFigure.id;
  const alreadyHad = collected.includes(id);
  if (!alreadyHad) {
    collected.push(id);
    saveCollected(collected);
  }

  showScreen("screen-stamp");
  document.getElementById("screen-stamp").classList.add("active");

  // restart the fx animation each time
  const fx = document.getElementById("stamp-fx");
  fx.classList.remove("play");
  void fx.offsetWidth; // reflow to restart CSS animations
  fx.classList.add("play");

  renderPassport(alreadyHad ? null : id);
  setTimeout(playThunk, 350);
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

renderPassport(null);
