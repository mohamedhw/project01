document.addEventListener("DOMContentLoaded", function () {
    const footer = document.getElementById("scroll-to-show");

    function checkFooterVisibility() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const windowHeight = window.innerHeight;
        const documentHeight = Math.max(
            document.body.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.clientHeight,
            document.documentElement.scrollHeight,
            document.documentElement.offsetHeight
        );

        if (scrollTop + windowHeight >= documentHeight) {
            footer.style.display = "block";
        } else {
            footer.style.display = "none";
        }
    }

    // Attach the event listener to the scroll event
    window.addEventListener("scroll", checkFooterVisibility);
});