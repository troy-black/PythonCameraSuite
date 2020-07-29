// Set 404.png image on error
document.addEventListener("DOMContentLoaded", function (event) {
    document.querySelectorAll('img').forEach(function (img) {
        img.onerror = function () {
            this.src = '../static/img/404.png';
        }
    })
})

function getCameraStreamVideoModal(modalId) {
    const modal = document.getElementById(modalId);

    // Add window.onclick event on first modal pop
    if (modal.style.display === "") {
        window.onclick = function(event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        }
    }

    // Swap modal display
    if (modal.style.display === "block") {
        modal.style.display = "none"
    } else {
        modal.style.display = "block"
    }

}
