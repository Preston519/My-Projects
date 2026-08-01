function foo(a, b) {
    return a * b
}

function dispFoo(a, b) {
    console.log(foo(a,b))
}

console.log("Hello World")
console.log(foo(2,4,2020,330))
// dispFoo.bind(this,2,3)()
setTimeout(console.log.bind(this, foo(2,3)), 5000)

// console.log.bind(6)()
new Promise().then
