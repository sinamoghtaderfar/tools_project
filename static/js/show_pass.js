function togglePasswords(icon) {

    const pass1 = document.getElementById("password");
    const pass2 = document.getElementById("password1");
    const pass3 = document.getElementById("password2");

    const fields = [pass1, pass2, pass3];

    fields.forEach(field => {
        if (field) {
            field.type = field.type === "password" ? "text" : "password";
        }
    });

}