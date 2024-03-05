document.addEventListener("DOMContentLoaded", function () {
    const eyeButtons = document.querySelectorAll(".eye-button");

    eyeButtons.forEach(eyeButton => {
        const pwField = eyeButton.parentElement.querySelector(".password");

        // Check the initial state of the password field and update the eye icon accordingly
        if (pwField.type === "password") {
            eyeButton.querySelector(".eye-icon").classList.add("bx-hide");
        } else {
            eyeButton.querySelector(".eye-icon").classList.add("bx-show");
        }

        eyeButton.addEventListener("click", () => {
            if (pwField.type === "password") {
                pwField.type = "text";
                eyeButton.querySelector(".eye-icon").classList.replace("bx-hide", "bx-show");
            } else {
                pwField.type = "password";
                eyeButton.querySelector(".eye-icon").classList.replace("bx-show", "bx-hide");
            }
        });
    });
});