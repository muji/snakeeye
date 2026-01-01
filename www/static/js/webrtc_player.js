
const streamUrl = "http://192.168.100.51:8889/cam1/whep";
const video = document.getElementById("videoElement");
const fallbackGif = document.getElementById("fallbackGif");

let pc = null;
let lastTime = 0;
let freezeCounter = 0;
let reconnecting = false;

function log(msg) {
  console.log(`[WebRTC] ${msg}`);
}

function startWatchdog() {
  setInterval(() => {
    if (video.readyState >= 2 && !reconnecting) {
      const nowTime = video.currentTime;
      if (nowTime === lastTime) {
        freezeCounter++;
        if (freezeCounter >= 3) {
          log("⚠️ Video frozen, switching to GIF and reconnecting...");
          fallbackGif.style.display = "block";
          video.style.display = "none";
          reconnect();
        }
      } else {
        freezeCounter = 0;
        fallbackGif.style.display = "none";
        video.style.display = "block";
      }
      lastTime = nowTime;
    }
  }, 2000);
}

function setupPeerConnection() {
  reconnecting = false;
  pc = new RTCPeerConnection({
    iceServers: [{ urls: ["stun:stun.l.google.com:19302"] }]
  });

  pc.addTransceiver("video", { direction: "recvonly" });

  pc.ontrack = (event) => {
    log("✅ Video track received");
    video.srcObject = event.streams[0];
    video.play();
    fallbackGif.style.display = "none";
    video.style.display = "block";
  };

  pc.createOffer()
    .then(offer => pc.setLocalDescription(offer))
    .then(() => fetch(streamUrl, {
      method: "POST",
      headers: { "Content-Type": "application/sdp" },
      body: pc.localDescription.sdp
    }))
    .then(res => res.text())
    .then(sdp => {
      const answer = new RTCSessionDescription({ type: "answer", sdp });
      return pc.setRemoteDescription(answer);
    })
    .catch(err => {
      log("❌ Setup failed: " + err);
      fallbackGif.style.display = "block";
      video.style.display = "none";
      reconnect();  // Retry on failure
    });
}

function reconnect() {
  if (reconnecting) return;
  reconnecting = true;
  if (pc) {
    pc.close();
    pc = null;
  }
  setTimeout(() => {
    log("🔁 Attempting reconnection...");
    setupPeerConnection();
  }, 5000);
}

// Button loggers
const buttonIds = [
  'btn-help', 'btn-brightness', 'btn-camera', 'btn-fullscreen',
  'btn-image', 'btn-play', 'btn-record', 'btn-audio',
  'btn-reset-distance', 'btn-depth-edit',
  'btn-satellite', 'btn-usb', 'btn-device', 'btn-wifi', 'btn-bluetooth'
];

buttonIds.forEach(id => {
  const btn = document.getElementById(id);
  if (btn) {
    btn.addEventListener('click', () => {
      console.log(`Button clicked: ${id}`);
    });
  }
});

setupPeerConnection();
startWatchdog();
