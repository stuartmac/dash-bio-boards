function adjustComponents() {
    // Get the 3D viewer
    var mol3dViewer = document.getElementById("zooming-specific-molecule3d-zoomto");

    // Get the DataTable card body
    var dataTableCard = document.querySelector('.data-table-card-body');

    if(mol3dViewer && dataTableCard) {
        // Get the parent card body of the 3D viewer
        var mol3dCardBody = mol3dViewer.closest('.card-body');
        var mol3dContainerDiv = mol3dViewer.querySelector(".molecule-3d");

        if (mol3dCardBody) {
            // Calculate new dimensions based on the parent container of the 3D viewer
            var parentWidth = mol3dViewer.parentElement.clientWidth - 20;  // 20 for 10px padding on each side
            var parentHeight = parentWidth;  // Make it square

            // Set new dimensions for the 3D viewer, accounting for padding
            var adjustedWidth = parentWidth - 20;  // Adjust for padding: 10px on each side
            var adjustedHeight = parentHeight - 20;  // Adjust for padding: 10px on each side

            mol3dContainerDiv.style.width = adjustedWidth + "px";
            mol3dContainerDiv.style.height = adjustedHeight + "px";

            // Set new height for the DataTable and Mol3D card bodies to match the 3D viewer
            dataTableCard.style.height = parentHeight + "px";
            mol3dCardBody.style.height = parentHeight + "px";
            
            // TODO: Use Dash callbacks to dynamically adjust DataTable's page_size based on the new height
        }
    }
}

// Adjust dimensions on initial load
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(adjustComponents, 1000);  // Increased delay to 1000 milliseconds
});

// Adjust dimensions on window resize
window.addEventListener("resize", adjustComponents);
