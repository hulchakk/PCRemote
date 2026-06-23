document.addEventListener("click", async (event) => {
    const button = event.target.closest(".media-btn");
    if (!button) return;

    const keyName = button.getAttribute("data-key");
    if (!keyName) return;

    const requestData = { key: keyName };

    try {
        await fetch("/api/keyboard", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });
    } catch (error) {
        console.error("Media command error:", error);
    }
});
