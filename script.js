const BIO_PAGE = "https://wwp.shizuoka.ac.jp/vision-i/%E6%83%85%E5%A0%B1%E5%AD%A6%E3%81%AE%E5%81%89%E4%BA%BA/";

const FIGURES = [
  {
    id: "grace-hopper",
    name: "Grace Hopper（グレイス・ホッパー）",
    qrMatch: "gratefigures_01",
    stampImg: "assets/grace-hopper-stamp.png",
    bio: "1906–1992。アメリカ海軍少将であり計算機科学者。プログラミング言語を人間にとって読みやすいものにしようと、世界最初期のコンパイラを開発しました。その成果は後にCOBOLの誕生へとつながり、今日の情報システムの基盤を築いたことから「コンピュータプログラミングの母」とも呼ばれています。",
    bioLink: BIO_PAGE + "#gratefigures_01",
  },
  {
    id: "tim-berners-lee",
    name: "Tim Berners-Lee（ティム・バーナーズ＝リー）",
    qrMatch: "gratefigures_02",
    stampImg: "assets/tim-berners-lee-stamp.png",
    bio: "1955–。英国出身の計算機科学者。CERN在籍中の1990年、研究成果を共有する仕組みとしてワールド・ワイド・ウェブ（WWW）を考案し、世界初のウェブサイトとブラウザを開発しました。現代のインターネット社会の土台を築いた人物です。",
    bioLink: BIO_PAGE + "#gratefigures_02",
  },
  {
    id: "marvin-minsky",
    name: "Marvin Minsky（マーヴィン・ミンスキー）",
    qrMatch: "greatfigures_03",
    stampImg: "assets/marvin-minsky-stamp.png",
    bio: "1927–2016。アメリカの認知科学者・AI研究者。1959年にMITで人工知能研究所を共同設立し、「人工知能」という分野を切り拓いた第一人者の一人です。著書『The Society of Mind』では、心とは単純な仕組みが数多く協調して生まれるものだという理論を提唱しました。",
    bioLink: BIO_PAGE + "#greatfigures_03",
  },
  {
    id: "alan-turing",
    name: "Alan Turing（アラン・チューリング）",
    qrMatch: "greatfigures_04",
    stampImg: "assets/alan-turing-stamp.png",
    bio: "1912–1954。現代計算機科学の基礎を築いた数学者。1936年、抽象的な計算のしくみである「チューリングマシン」を考案し、「計算とは何か」を理論化しました。1950年には機械が思考しうるかを問う「チューリングテスト」を提示しています。",
    bioLink: BIO_PAGE + "#greatfigures_04",
  },
  {
    id: "claude-shannon",
    name: "Claude Shannon（クロード・シャノン）",
    qrMatch: "greatfigures_05",
    stampImg: "assets/claude-shannon-stamp.png",
    bio: "1916–2001。「情報理論」の生みの親。1948年の論文で情報量やビット、通信容量といった概念を数学的に定義し、雑音のある通信路でも誤り訂正しながら正確に情報を伝えられることを示しました。今日のデジタル通信・インターネットの理論的土台です。",
    bioLink: BIO_PAGE + "#greatfigures_05",
  },
  {
    id: "john-von-neumann",
    name: "John von Neumann（ジョン・フォン・ノイマン）",
    qrMatch: "greatfigures_06",
    stampImg: "assets/john-von-neumann-stamp.png",
    bio: "1903–1957。数学・物理・経済など複数分野にまたがる業績を残した学者。プログラムとデータを同じメモリに格納する「ノイマン型」のコンピュータ構造を提案し、今日のほぼすべてのコンピュータの基本設計として使われています。ゲーム理論の確立者でもあります。",
    bioLink: BIO_PAGE + "#greatfigures_06",
  },
  {
    id: "alan-kay",
    name: "Alan Kay（アラン・ケイ）",
    qrMatch: "greatfigures_07",
    stampImg: "assets/alan-kay-stamp.png",
    bio: "1940–。Xerox PARCで活躍した計算機科学者。開発した言語Smalltalkはオブジェクト指向プログラミングの先駆けとなり、後のJavaやPython、GUIの考え方に影響を与えました。1970年代には、誰もが使える携帯型の知的道具「Dynabook」を構想し、今日のタブレットやノートPCの原型となりました。",
    bioLink: BIO_PAGE + "#greatfigures_07",
  },
  {
    id: "jun-murai",
    name: "村井純（Jun Murai）",
    qrMatch: "greatfigures_08",
    stampImg: "assets/jun-murai-stamp.png",
    bio: "1955–。日本にインターネット技術を導入し、学術ネットワークから商用インターネットへの普及を主導した人物で、「日本のインターネットの父」と呼ばれています。1980年代にWIDEプロジェクトを立ち上げ、日本のネットワーク基盤づくりを牽引しました。",
    bioLink: BIO_PAGE + "#greatfigures_08",
  },
  {
    id: "herbert-simon",
    name: "Herbert A. Simon（ハーバート・サイモン）",
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

  // restart the fx animation each time
  const fx = document.getElementById("stamp-fx");
  document.querySelector(".stamp-image").src = figure.stampImg;
  fx.classList.remove("play");
  void fx.offsetWidth; // reflow to restart CSS animations
  fx.classList.add("play");

  renderPassport(alreadyHad ? null : id);
  setTimeout(playThunk, 350);
  setTimeout(() => showFigureBio(figure), 1250);
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
