document.addEventListener("DOMContentLoaded", function () {

    const logoutModal = document.getElementById("logoutModal");
    const stayBtn = document.getElementById("stayLoggedIn");
    const countdownText = document.getElementById("countdown");

    let warningTimer;
    let logoutTimer;
    let countdownInterval;

    const idleTime = 3 * 60 * 1000; // 3 minutes
    const warningTime = 30; // seconds

    function resetTimer() {
        clearTimeout(warningTimer);
        clearTimeout(logoutTimer);
        clearInterval(countdownInterval);
        
        if (logoutModal && !logoutModal.classList.contains("hidden")) {
            logoutModal.classList.add("hidden");
        }
        
        warningTimer = setTimeout(showWarning, idleTime);
    }

    function showWarning() {
        if (!logoutModal || !countdownText) return;

        logoutModal.classList.remove("hidden");

        let countdown = warningTime;
        countdownText.textContent = countdown;

        clearInterval(countdownInterval);
        
        countdownInterval = setInterval(function () {
            countdown--;
            countdownText.textContent = countdown;

            if (countdown <= 0) {
                clearInterval(countdownInterval);
                window.location.href = "/accounts/logout/";
            }
        }, 1000);
    }

    if (stayBtn) {
    stayBtn.addEventListener("click", function () {

        fetch("/accounts/keep-alive/", {
            method: "GET",
            credentials: "same-origin"
        })
        .then(res => res.json())
        .then(data => {

            console.log("Session extended");

            // stop countdown
            clearInterval(countdownInterval);

            // close
            logoutModal.classList.add("hidden");

            // reset
            resetTimer();

        })
        .catch(err => {
            console.error(err);
        });

    });
}

    
    document.addEventListener("mousemove", resetTimer);
    document.addEventListener("keydown", resetTimer);
    document.addEventListener("click", resetTimer);
    document.addEventListener("scroll", resetTimer); 

    // start
    resetTimer();

});