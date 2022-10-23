$(document).ready(function() {
    const btn = document.getElementById("logout_submit")

    btn.addEventListener("click", async (e) => {
        e.preventDefault()
        console.log("WTF")
        let url = window.location.origin + "/api/logout"
        const api_response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: "{}",
        });
        console.log(await api_response.json())
        window.location.assign(window.location.origin)
    });
});

function bootstrap_alert_macro(message, type) {
    return `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `
}