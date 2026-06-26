document.addEventListener("DOMContentLoaded", () => {

    document.addEventListener("input", (event) => {
        const input = event.target;
        if (!input || input.id !== "text-input") return;

        if (!window.socket || !window.socket.connected) return;

        const inputType = event.inputType;

        if (inputType === "deleteContentBackward" || inputType === "deleteContentForward") {
            window.socket.emit("keyboard", { key: "delete" });
        }
        else if (event.data) {
            window.socket.emit("text", { text: event.data });
        }
    });
});
