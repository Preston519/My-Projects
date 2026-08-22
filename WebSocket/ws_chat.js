// TODO: multiple chats

let wss = null
let connected = false
let loggedin = false
let username = ""
let colour = ""

document.getElementById("form").addEventListener('submit', sendMessage)
document.getElementById("form").addEventListener('keydown', function(event) {
    if (event.key == 'Enter' && !event.shiftKey) sendMessage(event)
})
document.getElementById("login").addEventListener('submit', login)
document.getElementById("reconnect").addEventListener("click", setup)

function setup() {
    document.getElementById("connecting").style.color = "darkviolet"
    document.getElementById("connText").innerText = "Connecting..."
    document.getElementById("reconnect").style.visibility = "hidden"
    wss = new WebSocket("ws://localhost:8080")
    wss.onmessage = connMessage
    wss.onclose = connClosed
    wss.onerror = connClosed
    wss.onopen = connOpened
}

function login(event) {
    event.preventDefault()
    if (document.getElementById("username").value) {
        username = document.getElementById("username").value
        colour = document.getElementById("colourpicker").value
        loggedin = true
        if (connected) wss.send(JSON.stringify({"username": username, "colour": colour}))
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
    document.getElementById("reconnect").style.visibility = "visible"
}

function connOpened() {
    document.getElementById("connecting").style.color = "lawngreen"
    document.getElementById("connText").innerText = "Connected"
    connected = true
    if (loggedin) wss.send(JSON.stringify({"username": username, "colour": colour}))
}

function connMessage(msg) {
    const data = JSON.parse(msg.data)
    const t = document.getElementById("text")
    const gap = t.scrollHeight - t.scrollTop - t.clientHeight
    t.innerHTML += `<span style="color: ${data.colour}">${data.username}</span><br>${data.message}<br><span style="color: dimgrey; font-size: 0.6em">${epochToString(data.time)}</span><br><br>`
    if (gap <= 10) {
        // If at bottom, autoscroll to keep new message in view
        t.scrollTop = t.scrollHeight
    }
}

function epochToString(secEpoch) {
    return (new Date(secEpoch * 1000)).toLocaleString()
}

setup()