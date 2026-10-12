document.getElementById("login-form").addEventListener("submit", function (e) {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    const errEmail = document.getElementById("err-email");
    const errPassword = document.getElementById("err-password");

    errEmail.textContent = "";
    errPassword.textContent = "";

    let ok = true;
    if (!email) { errEmail.textContent = "Email is required"; ok = false; }
    if (!password) { errPassword.textContent = "Password is required"; ok = false; }

    if (!ok) e.preventDefault();
});