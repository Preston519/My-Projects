object TryThis {
    def main(args: Array[String]): Unit = {
        val queue = scala.collection.mutable.Queue(0, 1, 2, 3, 4)
        println(queue)
        for (x <- 0 until queue.length){
            println(x)
            println(queue.length)
            queue.dequeue()
        }
    }
}

// trait Tester {
//     def test(): Int = 3
// }