const FIGURES = [
  { id: "grace-hopper",     name: "Grace Hopper",      demo: true  },
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

/* ---------------- camera ---------------- */

let mediaStream = null;

async function startCamera() {
  const video = document.getElementById("camera-feed");
  const fallback = document.getElementById("camera-fallback");
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
      audio: false,
    });
    video.srcObject = mediaStream;
    fallback.classList.add("hidden");
  } catch (err) {
    console.warn("camera unavailable, using fallback", err);
    fallback.classList.remove("hidden");
  }
}

function stopCamera() {
  if (mediaStream) {
    mediaStream.getTracks().forEach(t => t.stop());
    mediaStream = null;
  }
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
  const collected = getCollected();
  const id = "grace-hopper";
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
  startCamera();
});

document.getElementById("btn-back-start").addEventListener("click", () => {
  stopCamera();
  showScreen("screen-start");
});

document.getElementById("btn-scan").addEventListener("click", triggerStamp);

document.getElementById("btn-continue").addEventListener("click", () => {
  showScreen("screen-camera");
});

renderPassport(null);
