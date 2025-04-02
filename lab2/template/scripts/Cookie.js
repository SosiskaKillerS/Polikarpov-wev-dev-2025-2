document.addEventListener("DOMContentLoaded", function () {
    const statusElement = document.getElementById("cookie-status");
    const button = document.getElementById("toggle-cookie");

    function checkCookie() {
        fetch("/check-cookie", { credentials: "include" })
            .then(response => response.json())
            .then(function (data) {
                updateStatus(data.cookieSet);
            });
    }

    function toggleCookie() {
        fetch("/toggle-cookie", { method: "POST", credentials: "include" })
            .then(response => response.json())
            .then(function (data) {
                updateStatus(data.cookieSet);
            });
    }

    function updateStatus(cookieSet) {
        if (cookieSet) {
            statusElement.textContent = "Cookie установлено";
            button.textContent = "Удалить Cookie";
        } else {
            statusElement.textContent = "Cookie не установлено";
            button.textContent = "Установить Cookie";
        }
    }

    button.addEventListener("click", toggleCookie);
    checkCookie();
});
