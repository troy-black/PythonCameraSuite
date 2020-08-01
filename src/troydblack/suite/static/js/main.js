// Set 404.png image on error
document.addEventListener("DOMContentLoaded", function (event) {
    document.querySelectorAll('img').forEach(function (img) {
        img.onerror = function () {
            this.src = '../static/img/404.png';
        }
    })
})
