document.querySelectorAll(".sticky-note").forEach(note => {
    let isDragging = false;
    let isResizing = false;

    let offsetX, offsetY;
    let startWidth, startHeight;

    const handle = note.querySelector(".resize-handle");

    // DRAGGING ----------
    note.addEventListener("mousedown", e => {
        if (e.target === handle) return;

        isDragging = true;
        offsetX = e.clientX - note.offsetLeft;
        offsetY = e.clientY - note.offsetTop;
    });

    // RESIZING ----------
    handle.addEventListener("mousedown", e => {
        e.stopPropagation();
        isResizing = true;

        startWidth = note.offsetWidth;
        startHeight = note.offsetHeight;
    });

    document.addEventListener("mousemove", e => {
        if (isDragging) {
            note.style.left = (e.clientX - offsetX) + "px";
            note.style.top = (e.clientY - offsetY) + "px";
        }

        if (isResizing) {
            note.style.width = (startWidth + (e.clientX - note.offsetLeft)) + "px";
            note.style.height = (startHeight + (e.clientY - note.offsetTop)) + "px";
        }
    });

    document.addEventListener("mouseup", () => {
        if (isDragging || isResizing) {
            save(note);
        }
        isDragging = false;
        isResizing = false;
    });
});


// SAVE POSITION + SIZE --------------------------
function save(note) {
    const data = new FormData();
    data.append("id", note.dataset.id);
    data.append("x", parseFloat(note.style.left));
    data.append("y", parseFloat(note.style.top));
    data.append("width", parseFloat(note.style.width));
    data.append("height", parseFloat(note.style.height));

    fetch("/sticky/save-position/", {
        method: "POST",
        body: data,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    });
}
