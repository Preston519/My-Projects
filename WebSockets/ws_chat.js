// const ws = require("ws")
// import ws from "ws"

const wss = new WebSocket("ws://localhost:8080")

document.getElementById("text").innerText = "wahs"
// document.getElementById("textbox").addEventListener('click', function () {
//     document.getElementById("text").innerText = "Clicked!"
// })
document.getElementById("form").addEventListener('submit', function (event) {
    event.preventDefault()
    const msg = document.getElementById("textbox").value
    wss.send(msg)
})
// document.getElementById("submit").addEventListener('click', function () {
//     const msg = document.getElementById("textbox").value
//     wss.send(msg)
// })


wss.onmessage = (msg) => {
    document.getElementById("text").innerText += "\n"+msg.data
}