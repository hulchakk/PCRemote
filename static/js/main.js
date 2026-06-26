window.socket = io();

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("remote-container");
    const tabs = document.querySelectorAll(".tab-btn");
    const sleepBtn = document.getElementById("sleep-btn");

    async function loadRemote(type) {
        try {
            const response = await fetch(`/partials/${type}`);
            if (response.ok) {
                container.innerHTML = await response.text();
            }
        } catch (error) {
            console.error("Load tab error:", error);
        }
    }

    document.addEventListener("click", (event) => {
        const button = event.target.closest(".remote-btn");
        if (!button) return;

        const keyName = button.getAttribute("data-key");
        if (!keyName) return;

        window.socket.emit("keyboard", { key: keyName });
        if (keyName === "clear") {
                document.getElementById("text-input").value = "";
        }
    });

    tabs.forEach(tab => {
        tab.addEventListener("click", (e) => {
            const currentTab = e.currentTarget;
            tabs.forEach(t => t.classList.remove("active"));
            currentTab.classList.add("active");

            const targetRemote = currentTab.getAttribute("data-target");
            loadRemote(targetRemote);
        });
    });

    if (sleepBtn) {
        sleepBtn.addEventListener("click", () => {
            if (!confirm("Do you want to sleep?")) return;
            window.socket.emit("system_sleep", { action: "sleep" });
        });
    }

    loadRemote("media");
});
