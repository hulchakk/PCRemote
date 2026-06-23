let holdTimeout = null;
let spamInterval = null;

function sendMediaKey(keyName) {
    if (window.socket && window.socket.connected) {
        window.socket.emit("keyboard", { key: keyName });
    }
}

function clearTimers() {
    if (holdTimeout) {
        clearTimeout(holdTimeout);
        holdTimeout = null;
    }
    if (spamInterval) {
        clearInterval(spamInterval);
        spamInterval = null;
    }
}

document.addEventListener("pointerdown", (event) => {
    const button = event.target.closest(".media-btn");
    if (!button) return;

    const keyName = button.getAttribute("data-key");
    if (!keyName) return;

    clearTimers();

    sendMediaKey(keyName);

    holdTimeout = setTimeout(() => {
        spamInterval = setInterval(() => {
            sendMediaKey(keyName);
        }, 100); 
    }, 500);
});

document.addEventListener("pointerup", clearTimers);
document.addEventListener("pointercancel", clearTimers);
document.addEventListener("pointerleave", (event) => {
    if (event.target.closest(".media-btn")) {
        clearTimers();
    }
}, true);
