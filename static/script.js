function detectBark() {
    const result = document.getElementById("result");
    result.textContent = "🎙️ Listening...";

    fetch('/detect-bark')
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            result.textContent = data.message;
        })
        .catch(error => {
            console.error("Error during fetch:", error);
            result.textContent = "❌ Error: Could not reach the server.";
        });
}
