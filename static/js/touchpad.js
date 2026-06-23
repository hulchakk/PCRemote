let lastX = 0;
let lastY = 0;
let startX = 0;
let startY = 0;
let startTime = 0;
let isTapping = false;
let maxTouches = 0;
let activeTouchpad = null;

document.addEventListener("touchstart", (e) => {
    const pad = e.target.closest("#touchpad-area");
    if (!pad) return;

    e.preventDefault();
    activeTouchpad = pad;

    if (e.touches.length > maxTouches) {
        maxTouches = e.touches.length;
    }

    if (e.touches.length > 0) {
        lastX = e.touches[0].clientX;
        lastY = e.touches[0].clientY;
        startX = lastX;
        startY = lastY;
        startTime = Date.now();
        isTapping = true;
    }
}, { passive: false });

document.addEventListener("touchmove", (e) => {
    if (!activeTouchpad) return;

    e.preventDefault();
    
    if (e.touches.length > 0) {
        const currentX = e.touches[0].clientX;
        const currentY = e.touches[0].clientY;
        
        const dx = Math.round(currentX - lastX);
        const dy = Math.round(currentY - lastY);

        if (Math.abs(currentX - startX) > 5 || Math.abs(currentY - startY) > 5) {
            isTapping = false;
        }

        if ((dx !== 0 || dy !== 0) && window.socket && window.socket.connected) {
            window.socket.emit("mouse_move", { dx: dx, dy: dy });
        }
        
        lastX = currentX;
        lastY = currentY;
    }
}, { passive: false });

document.addEventListener("touchend", (e) => {
    if (!activeTouchpad) return;
    
    e.preventDefault();
    
    if (isTapping && e.touches.length === 0) {
        const duration = Date.now() - startTime;
        
        if (duration < 300 && window.socket && window.socket.connected) {
            const buttonType = maxTouches >= 2 ? "right" : "left";
            window.socket.emit("mouse_click", { button: buttonType });
        }
    }

    if (e.touches.length === 0) {
        maxTouches = 0;
        activeTouchpad = null;
    } else {
        lastX = e.touches[0].clientX;
        lastY = e.touches[0].clientY;
    }
}, { passive: false });

document.addEventListener("touchcancel", () => {
    activeTouchpad = null;
    isTapping = false;
    maxTouches = 0;
});
