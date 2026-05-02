document.addEventListener("DOMContentLoaded", function () {
    const loader = document.createElement("div");
    loader.id = "global-loader";
    document.body.appendChild(loader);
});

window.addEventListener("load", function () {
    setTimeout(function() {
        const loader = document.getElementById("global-loader");
        if (loader) loader.remove();
    }, 1500);
});