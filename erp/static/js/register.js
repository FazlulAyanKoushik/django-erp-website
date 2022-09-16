const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const passFeedBackArea = document.querySelector(".passFeedBackArea");
const passwordField = document.querySelector("#passwordField");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "SHOW") {
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
};

showPasswordToggle.addEventListener("click", handleToggleInput);



passwordField.addEventListener("keyup", (e) => {
    const passVal = e.target.value;

    // passwordField.classList.remove("is-invalid");
    // passFeedBackArea.style.display = "none";

    if (passVal.length > 0) {
        fetch("/authentication/validate-pass", {
            body: JSON.stringify({ password: passVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                if (data.pass_strength) {
                    // passwordField.classList.add("is-invalid");
                    if (data.pass_strength == 'Password too short'){
                        submitBtn.disabled = true;
                    }else{
                        submitBtn.removeAttribute("disabled");
                    }
                    passFeedBackArea.style.display = "block";
                    passFeedBackArea.innerHTML = `<p>${data.pass_strength}</p>`;
                } 
            });
    }
});


emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                if (data.email_error) {
                    submitBtn.disabled = true;
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
                } else {
                    submitBtn.removeAttribute("disabled");
                }
            });
    }
});

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;

    usernameSuccessOutput.style.display = "block";

    usernameSuccessOutput.textContent = `Checking  ${usernameVal}`;

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                usernameSuccessOutput.style.display = "none";
                if (data.username_error) {
                    usernameField.classList.add("is-invalid");
                    feedBackArea.style.display = "block";
                    feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                    submitBtn.disabled = true;
                } else {
                    submitBtn.removeAttribute("disabled");
                }
            });
    }
});