// Add form
document.getElementById("add-form").addEventListener("submit", function (e) {
    const title = document.getElementById("title").value.trim();
    const err = document.getElementById("err-title");
    err.textContent = "";

    if (!title) {
        err.textContent = "Title is required";
        e.preventDefault();
    } else if (title.length > 200) {
        err.textContent = "Title is too long (200 characters at most)";
        e.preventDefault();
    }
});

// Edit forms
document.querySelectorAll(".edit-js").forEach(function (form) {
    form.addEventListener("submit", function (e) {
        const title = form.querySelector("input[name=title]").value.trim();
        if (!title) {
            alert("Title is required");
            e.preventDefault();
        } else if (title.length > 200) {
            alert("Title is too long (200 characters at most)");
            e.preventDefault();
        }
    });
});

