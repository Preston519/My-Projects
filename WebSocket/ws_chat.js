// TODO: Usernames, backend server

let wss = new WebSocket("ws://localhost:8080")
let connected = false

document.getElementById("form").addEventListener('submit', sendMessage)

document.getElementById("form").addEventListener('keydown', function(event) {
    if (event.key == 'Enter' && !event.shiftKey) sendMessage(event)
})

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

// TODO: Fit msg {user: XXX, content: XXX, time: XXX} format
function connMessage(msg) {
    document.getElementById("text").innerText += "\n"+msg.data
}


wss.onmessage = connMessage
wss.onclose = connClosed
wss.onerror = connClosed
wss.onopen = connOpened