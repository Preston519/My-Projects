import scala.util.boundary, boundary.break

object Yahtzee {
    val totalRolls = 3
    val random = new scala.util.Random

    def main(args: Array[String]) : Unit = {
        val players = new scala.collection.mutable.Queue[Player]

        print("Enter player (blank to continue): ")
        var name = scala.io.StdIn.readLine()
        while (name != "") {
            players.enqueue(new Player(name))
            print("Enter player (blank to continue): ")
            name = scala.io.StdIn.readLine()
        }

        val rolls = new Array[Int](5)
        for (x <- 0 until players.length*13) { // 13 slots to fill for each player
            val player = players.dequeue()
            var rerolls = totalRolls-1
            for (x <- 0 until 5) rolls(x) = random.between(1, 7)
            var flag = true
            while (flag && rerolls > 0) {
                player.addScoreDisplay(rolls)
                println(s"\nRolls: ${rolls.mkString(" ")}")
                println(s"You have $rerolls roll${if (rerolls == 1) "" else "s"} left")
                var input: String = "a"
                while (flag && !parseReroll(rolls, input)) {
                    print(s"Enter indexes (starting 0) to reroll dice, or blank to accept: ")
                    input = scala.io.StdIn.readLine()
                    flag = input != ""
                }
                rerolls -= 1
            }

            player.addScoreDisplay(rolls)
            println(s"\nRolls: ${rolls.mkString(" ")}")
            var input = ""
            while (!Player.section_names.contains(input) || player.isFilled(Player.boxNumber(input))) {
                print("Choose a box to fill: ")
                input = scala.io.StdIn.readLine()
            }

            player.setScore(rolls, Player.boxNumber(input))
            players.enqueue(player)
        }

        if (!players.isEmpty) {
            val rankings = new Array[Player](players.length)
            for (length <- 0 until players.length) insert(rankings, length, players.dequeue())

            println("\n\nFinal Sheets:")
            for (player <- rankings) {
                println("\n--------------------------------------------------")
                player.displaySheet()
            }
            println("\n--------------------------------------------------")

            println("\nRankings:")
            var rank = 0
            val padding = rankings.maxBy(_.name.length()).name.length() + 4
            for (x <- 0 until rankings.length) {
                if (x == 0 || rankings(x-1).getTotal(3) > rankings(x).getTotal(3)) rank += 1
                println(s"$rank. ${rankings(x).name}${" "*(padding-rankings(x).name.length())}${rankings(x).getTotal(3)}")
            }
        }
    }

    def insert(array: Array[Player], len: Int, player: Player): Unit = {
        require(array.length > len)
        var p = 0; var q = len
        while (q-p > 0) {
            val m = (p+q)/2
            if (array(m).getTotal(3) == player.getTotal(3)) {q = m; p = m}
            else if (array(m).getTotal(3) > player.getTotal(3)) p = m+1
            else q = m
        }
        for (x <- len until q by -1) {array(x) = array(x-1)}
        array(q) = player
    }

    def parseReroll(rolls: Array[Int], input: String): Boolean = {
        require(rolls.length == 5)
        boundary {
            for (x <- input.split(" ")) {
                if (x.forall(_.isDigit) && (0 to 4).contains(x.toInt)) rolls(x.toInt) = random.between(1, 7)
                else break(false)
            }
            true
        }
    }
}

class Player(val name: String) {
    private val scores = new Array[Int](13)
    private val scoresFilled = new Array[Boolean](13)
    private val totals = new Array[Int](4)
    private var bonus = false
    private var yahtzeeBonus = 0

    def isFilled(slot: Int) = scoresFilled(slot)

    def setScore(rolls: Array[Int], slot: Int): Boolean = {
        require((0 until 13).contains(slot))
        if (!scoresFilled(slot)) {
            val score = scoreForSlot(rolls, slot)
            scores(slot) = score
            if (slot < 6) {
                totals(0) += score
                totals(1) += score
                if (!bonus && totals(0) >= 63) {
                    bonus = true
                    totals(1) += 35
                    totals(3) += 35
                }
            }
            else {
                totals(2) += score
            }
            totals(3) += score
            scoresFilled(slot) = true
            yahtzeeBonus(rolls)
            true
        }
        else false
    }

    private def yahtzeeBonus(rolls: Array[Int]): Boolean = {
        if (scores(11) == 50 && rolls.count(_ == rolls(0)) == 5) {
            scores(13) += 1
            true
        }
        else false
    }

    // def getScore(slot: Int) = scores(slot)

    def getTotal(slot: Int) = totals(slot)

    private def scoreForSlot(rolls: Array[Int], slot: Int): Int = {
        require(rolls.length == 5)
        require(slot >= 0 && slot < 13)
        if (slot < 6) {
            rolls.count(_ == slot+1)*(slot+1)
        }
        else if (slot < 8) {
            val occ = new Array[Int](6)
            rolls.foreach(x => occ(x-1) += 1)
            if (occ.max > slot-4) rolls.sum else 0
        }
        else if (slot == 8) {
            val occ = new Array[Int](6)
            rolls.foreach(x => occ(x-1) += 1)
            var flag = true
            occ.foreach(x => if (x == 1 || x >= 4) flag = false)
            if (flag) rolls.sum else 0
        }
        else if (slot < 11) {
            val occ = new Array[Int](6)
            rolls.foreach(x => occ(x-1) += 1)
            var flag = false
            var curlength = if (occ(0) > 0) 1 else 0
            for (x <- 1 to 5) {
                if (occ(x) > 0) curlength += 1 else curlength = 0
                if (curlength > slot-6) flag = true
            }
            if (flag) (slot-6)*10 else 0
        }
        else if (slot == 11) {
            if (rolls.count(_ == rolls(0)) == 5) 50 else 0
        }
        else rolls.sum
    }

    def addScoreDisplay(rolls: Array[Int]): Unit = {
        println(s"\n${name}'s Turn\n")
        println("Upper Section")
        for (x <- 0 to 5) {
            println(s"${Player.section_names(x)}${" "*(Player.padding - Player.section_names(x).length())}${if (scoresFilled(x)) scores(x) else s"-    <--    ${scoreForSlot(rolls, x)}"}")
        }
        println(s"${Player.totals_names(0)}${" "*(Player.padding - Player.totals_names(0).length())}${totals(0)}")
        println(s"Upper Section Bonus${" "*(Player.padding-19)}${if (bonus) 35 else 0}")
        println(s"${Player.totals_names(1)}${" "*(Player.padding-Player.totals_names(1).length())}${totals(1)}")
        println("\nLower Section")
        for (x <- 6 to 12) {
            println(s"${Player.section_names(x)}${" "*(Player.padding - Player.section_names(x).length())}${if (scoresFilled(x)) scores(x) else s"-    <--    ${scoreForSlot(rolls, x)}"}")
        }
        println(s"Yahtzee Bonus${" "*(Player.padding - 13)}${yahtzeeBonus * 100}\n")
        println(s"${Player.totals_names(2)}${" "*(Player.padding - Player.totals_names(2).length())}${totals(2)}")
        println(s"${Player.totals_names(1)}${" "*(Player.padding - Player.totals_names(1).length())}${totals(1)}")
        println(s"${Player.totals_names(3)}${" "*(Player.padding - Player.totals_names(3).length())}${totals(3)}")
    }

    def displaySheet(): Unit = {
        println(s"\n${name}'s Sheet\n")
        println("Upper Section")
        for (x <- 0 to 5) {
            println(s"${Player.section_names(x)}${" "*(Player.padding - Player.section_names(x).length())}${if (scoresFilled(x)) scores(x) else "-"}")
        }
        println(s"${Player.totals_names(0)}${" "*(Player.padding - Player.totals_names(0).length())}${totals(0)}")
        println(s"Upper Section Bonus${" "*(Player.padding-19)}${if (bonus) 35 else 0}")
        println(s"${Player.totals_names(1)}${" "*(Player.padding-Player.totals_names(1).length())}${totals(1)}")
        println("\nLower Section")
        for (x <- 6 to 12) {
            println(s"${Player.section_names(x)}${" "*(Player.padding - Player.section_names(x).length())}${if (scoresFilled(x)) scores(x) else "-"}")
        }
        println(s"Yahtzee Bonus${" "*(Player.padding - 13)}${yahtzeeBonus*100}")
        println()
        println(s"${Player.totals_names(2)}${" "*(Player.padding - Player.totals_names(2).length())}${totals(2)}")
        println(s"${Player.totals_names(1)}${" "*(Player.padding - Player.totals_names(1).length())}${totals(1)}")
        println(s"${Player.totals_names(3)}${" "*(Player.padding - Player.totals_names(3).length())}${totals(3)}")
    }
}

object Player {
    val section_names = Array("Aces","Twos","Threes","Fours","Fives","Sixes","3 of a kind","4 of a kind","Full House","Small Straight","Large Straight","Yahtzee","Chance")
    val totals_names = Array("Total Score","Upper Section Total","Lower Section Total","Grand Total")
    val padding = totals_names.maxBy(_.length()).length() + 3

    def boxNumber(boxName: String): Int = {
        require(section_names.contains(boxName))
        var flag = false
        var index = -1
        while (!flag) {
            index += 1
            flag = Player.section_names(index) == boxName
        }
        index
    }
}