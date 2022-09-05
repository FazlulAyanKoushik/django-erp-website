const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector('.invalid_feedback');
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector('.emailFeedBackArea')

emailField.addEventListener('keyup', (e) => {
    const emailval = e.target.value;
    
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display='none';

    if(emailval.length>0){
        fetch('/authentication/validate-email',{
            body:JSON.stringify({email: emailval}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.email_error){
                emailField.classList.add("is-invalid");
                feedBackArea.style.display='block';
                feedBackArea.innerHTML = `<p>${data.email_error}</p>`
            }
        });
    }
})







usernameField.addEventListener("keyup", (e) => {

    const usernameval = e.target.value;
    
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display='none';

    if(usernameval.length>0){
        fetch('/authentication/validate-username',{
            body:JSON.stringify({username: usernameval}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.username_error){
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display='block';
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`
            }
        });
    }
})