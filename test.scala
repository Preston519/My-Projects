object Test {
    def main(args: Array[String]): Unit = {
        var a = Array(10, 23, 5, 77, 27, 2, 9, 4)
        println(qSort(a, 0, a.size))
        println(a.mkString(", "))
    }

    def partition(a: Array[Int], l: Int, r: Int, k: Int): Int = {
        require(l >= 0 && r <= a.size)
        var i = l
        var j = r
        while (j > i) {
            if (a(i) < k) i += 1
            else if (a(j-1) >= k) j -= 1
            else {
                val t = a(i)
                a(i) = a(j-1)
                a(j-1) = t
            }
        }
        j
    }

    def qSort(a: Array[Int], l: Int, r: Int): Unit = {
        require(l >= 0 && r <= a.size)
        if (r-l > 1) {
            val k = partition(a, l+1, r, a(l)) - 1
            val t = a(l)
            a(l) = a(k)
            a(k) = t
            qSort(a, l, k)
            qSort(a, k+1, r)
        }
    }
}