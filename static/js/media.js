document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll(".remote-btn");

    buttons.forEach(button => {
        button.addEventListener("click", async (event) => {
            const keyName = event.currentTarget.getAttribute("data-key");

            const requestData = { key: keyName };

            try {
                const response = await fetch("/api/keyboard", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(requestData)
                });
            } catch (error) {
                console.error("Error", error);
            }
        });
    });
});
