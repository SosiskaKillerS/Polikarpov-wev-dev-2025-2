document.addEventListener("DOMContentLoaded", () => {
            const statusElement = document.getElementById("cookie-status");
            const button = document.getElementById("toggle-cookie");

            async function checkCookie() {
                const response = await fetch("/check-cookie", { credentials: "include" });
                const data = await response.json();
                updateStatus(data.cookieSet);
            }

            async function toggleCookie() {
                const response = await fetch("/toggle-cookie", { method: "POST", credentials: "include" });
                const data = await response.json();
                updateStatus(data.cookieSet);
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