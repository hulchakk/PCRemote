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
            console.error(error);
        }
    }

    document.addEventListener("click", async (event) => {
        const button = event.target.closest(".remote-btn");
        if (!button) return;

        const keyName = button.getAttribute("data-key");
        if (!keyName) return;

        try {
            await fetch("/api/keyboard", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ key: keyName })
            });
        } catch (error) {
            console.error(error);
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

    sleepBtn.addEventListener("click", async () => {
        if (!confirm("Do you want to sleep?")) return;
        try {
            await fetch("/api/system_sleep", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "sleep" })
            });
        } catch (error) {
            console.error(error);
        }
    });

    loadRemote("media");
});
