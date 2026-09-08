const submit = document.getElementById("submit")
const errorBox = document.getElementById("error")
let flag = true;

async function submitPressed(event) {
    event.preventDefault()
    if (flag) {
        flag = false
        const response = await fetch("http://localhost:8080/login", {
            "method": "POST",
            "headers": {
                "X-Username": document.getElementById("username").value,
                "X-Password": document.getElementById("password").value
            }
        })
        if (response.status == 401) {
            errorBox.innerText = "Incorrect username or password"
            // errorBox.innerText += await response.json()
        }
        else if (response.status == 200) {
            const reply = await response.json()
            // TODO: STORE REPLY AUTH TOKEN
            window.location.replace("/ws_chat.html")
        } else {
            errorBox.innerText = "Unknown server error. Please try again after a few minutes."
        }
        flag = true
    }
}

submit.addEventListener("click", submitPressed)

// TODO: Check if auth token exists, then validate, then redirect if necessary.