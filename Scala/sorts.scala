object Sorts {
    def main(args: Array[String]): Unit = {
        val a = Array(197, 241, 809, 121, 92, 616, 177, 584, 402, 329, 397, 683, 40, 895, 174, 659, 21, 684, 786, 378)
        // println(mergesort(a).mkString(", "))
        // println(select(a, a.size/2))
        quicksort(a, 0, a.size)
        // println(partition(a, 0, a.size, 378))
        println(a.mkString(", "))
        println(isSorted(a))
        println(isSortedRecursive(a, a.size))
    }
}

def isSorted(arr: Array[Int]): Boolean = {
    var i = 1
    while (i < arr.size && arr(i-1) <= arr(i)) i += 1
    i >= arr.size
}

def isSortedRecursive(arr: Array[Int], n: Int): Boolean = n <= 1 || (arr(n-1) >= arr(n-2) && isSortedRecursive(arr, n-1))

def mergesort(arr: Array[Int]): Array[Int] = {
    if (arr.size > 1) {
        val (left, right) = arr.splitAt(arr.size / 2)
        val ls = mergesort(left)
        val rs = mergesort(right)
        val res = new Array[Int](arr.size)
        var l = 0
        var r = 0
        while (l < ls.size || r < rs.size) {
            if (r >= rs.size || (l < ls.size && ls(l) <= rs(r))) {
                res(l+r) = ls(l)
                l += 1
            }
            else {
                res(l+r) = rs(r)
                r += 1
            }
        }
        res
    }
    else arr
}

// In situ
def quicksort(arr: Array[Int], l: Int, r: Int): Unit = {
    if (r > l+1) {
        val median = select(arr, (l+r)/2)
        val k = partition(arr, l, r, median)
        var m = 0
        while (arr(m) != median) m += 1
        if (m < k) {
            arr(m) = arr(k-1)
            arr(k-1) = median
        }
        else {
            arr(m) = arr(k)
            arr(k) = median
        }
        quicksort(arr, l, k)
        quicksort(arr, k+1, r)
    }
}

def partition(arr: Array[Int], l: Int, r: Int, k: Int): Int = {
    var i = l
    var j = r
    while (i < j) {
        if (arr(i) < k) i += 1
        else {
            val t = arr(i)
            arr(i) = arr(j-1)
            arr(j-1) = t
            j -= 1
        }
    }
    i
}

def select(arr: Array[Int], k: Int): Int = {
    if (arr.size == 0) throw new IllegalArgumentException("Empty array")
    else if (arr.size == 1) arr(0)
    else {
        val len = arr.size / 5
        val extra = if arr.size % 5 > 0 then 1 else 0
        val a = new Array[Int](len + extra)
        for (i <- 0 until len) {
            val xs = new Array[Int](5)
            for (j <- 0 until 5) xs(j) = arr(i*5+j)
            a(i) = mergesort(xs)(2)
        }
        if (extra == 1) {
            val xs = new Array[Int](arr.size % 5)
            for (j <- 0 until (arr.size % 5)) xs(j) = arr(j+len*5)
            a(len) = mergesort(xs)(xs.size / 2)
        }
        val m = select(a, a.size/2)
        val arr2 = new Array[Int](arr.size)
        for (x <- 0 until arr.size) arr2(x) = arr(x)
        val y = partition(arr2, 0, arr.size, m)
        if (y >= k) {
            val arr3 = new Array[Int](y)
            for (x <- 0 until y) arr3(x) = arr2(x)
            select(arr3, k)
        }
        else {
            val arr3 = new Array[Int](arr.size - y)
            for (x <- 0 until (arr.size - y)) arr3(x) = arr2(x+y)
            select(arr3, k-y)
        }
    }
}