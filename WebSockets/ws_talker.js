// const ws = require("ws")

const wss = new WebSocket("ws://localhost:8080")

// wss.onmessage(function )

// wss.onmessage(function (message) {
wss.on('message', function (message) {
    console.log(message.toString())
})

wss.on('close', function() {
    console.log("Out!")
})

console.log("Test")
// setTimeout(() => wss.send("Test message"), 1000)
function talk(msg) {
    wss.send(msg)
}