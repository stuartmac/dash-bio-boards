function resizeMol3dViewer() {
    var mol3dViewer = document.getElementById("zooming-specific-molecule3d-zoomto");
    if (mol3dViewer) {
        var containerDiv = mol3dViewer.querySelector(".molecule-3d");
        var parentElement = mol3dViewer.parentElement;
        if (containerDiv && parentElement) {
            var parentWidth = parentElement.clientWidth - 20;  // 20 for 10px padding on each side
            var parentHeight = parentElement.clientHeight - 20; // 20 for 10px padding on each side
            containerDiv.style.width = parentWidth + "px";
            containerDiv.style.height = parentHeight + "px";
        }
    }
}

// For initial load
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(resizeMol3dViewer, 500);  // Delay of 500 milliseconds
});

// For window resizes
window.addEventListener("resize", function() {
    resizeMol3dViewer();
});
