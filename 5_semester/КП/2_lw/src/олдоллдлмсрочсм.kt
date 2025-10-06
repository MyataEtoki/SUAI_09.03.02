fun main() {
    val monitor = Object()
    var seconds = 0

    // Хронометр
    val timerThread = Thread {
        while (true) {
            Thread.sleep(1000)
            seconds++
            println("Прошло $seconds секунд(ы)")

        }
    }

    // Поток с сообщением раз в 5 секунд
    val fiveSecThread = Thread {
        var localSeconds = 0
        while (true) {
            Thread.sleep(1000)
            localSeconds++
            if (localSeconds % 5 == 0) {
                println(">>> Сообщение раз в 5 секунд")

            }
        }
    }

    // Поток с сообщением раз в 7 секунд
    val sevenSecThread = Thread {
        var localSeconds = 0
        while (true) {
            Thread.sleep(1000)
            localSeconds++
            if (localSeconds % 7 == 0) {
                println(">>> Сообщение раз в 7 секунд")

            }
        }
    }

    // Запуск
    timerThread.start()
    fiveSecThread.start()
    sevenSecThread.start()
}
