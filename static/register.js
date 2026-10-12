document.getElementById("register-form").addEventListener("submit", function (e) {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirm = document.getElementById("confirm_password").value;

    const errName = document.getElementById("err-name");
    const errEmail = document.getElementById("err-email");
    const errPassword = document.getElementById("err-password");
    const errConfirm = document.getElementById("err-confirm");

    errName.textContent = "";
    errEmail.textContent = "";
    errPassword.textContent = "";
    errConfirm.textContent = "";

    let ok = true;

    if (!name) { errName.textContent = "Name is required"; ok = false; }
    if (!email) { errEmail.textContent = "Email is required"; ok = false; }
    if (!password) { errPassword.textContent = "Password is required"; ok = false; }

    if (!confirm) {
        errConfirm.textContent = "Confirm password is required";
        ok = false;
    } else if (password && password !== confirm) {
        errConfirm.textContent = "Passwords do not match";
        ok = false;
    }

    if (!ok) e.preventDefault();
});