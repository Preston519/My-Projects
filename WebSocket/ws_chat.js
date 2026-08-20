// TODO: retry connection, timestamping

let wss = new WebSocket("ws://localhost:8080")
let connected = false

document.getElementById("form").addEventListener('submit', sendMessage)
document.getElementById("form").addEventListener('keydown', function(event) {
    if (event.key == 'Enter' && !event.shiftKey) sendMessage(event)
})
document.getElementById("login").addEventListener('submit', login)

function login(event) {
    event.preventDefault()
    if (document.getElementById("username").value) {
        wss.send(JSON.stringify({username: document.getElementById("username").value, colour: document.getElementById("colourpicker").value}))
        document.getElementById("popupBackground").style.display = "none"
    }
}

function sendMessage(event) {
    event.preventDefault()
    if (connected) {
        const msgbox = document.getElementById("textbox")
        const msg = msgbox.value.trim()
        if (msg) {
            wss.send(msgbox.value)
            msgbox.value = ""
        }
    }
}

function connClosed() {
    document.getElementById("connecting").style.color = "red"
    document.getElementById("connText").innerText = "Disconnected"
    connected = false
}

function connOpened() {
    document.getElementById("connecting").style.color = "lawngreen"
    document.getElementById("connText").innerText = "Connected"
    connected = true
}

function connMessage(msg) {
    // document.getElementById("text").innerText += "\n"+msg.data
    const data = JSON.parse(msg.data)
    // document.getElementById("text").innerText += data
    document.getElementById("text").innerHTML += `<p><span style="color: ${data.colour}">${data.username}</span><br>${data.message}</p>`
    // document.getElementById("text").innerText += "alkjslkjd"
}


wss.onmessage = connMessage
wss.onclose = connClosed
wss.onerror = connClosed
wss.onopen = connOpened