import kotlin.math.pow

fun main() {
    println("ВЫЧИСЛЕНИЕ ФУНКЦИИ С ПОМОЩЬЮ РЯДА МАКЛОРЕНА")
    println("Функция: (1/(1+x)) = (1 - x + x^2 - x^3 + ...)")
    println("Ряд сходится при |x| < 1")
    println()

    // Ввод данных
    print("Введите x (дробное число, например 0.5): ")
    val x = readLine()!!.toDouble()

    print("Введите точность (маленькое число, например 0.001): ")
    val epsilon = readLine()!!.toDouble()

//    // Проверка условия сходимости
//    if (x >= 1 || x <= -1) {
//        println("Ошибка: x должен быть между -1 и 1")
//        return
//    }

    // Вычисление ряда Маклорена
    var sum = 0.0
    var n = 0
    var term: Double
    var lastTerm: Double

    println("\nВычисление ряда:")
    println("n\tЧлен ряда\tСумма")
    println("------------------------")

    do {
        // Вычисляем n-й член ряда: (-1)^(n-1) * x^n
        term = (-1.0).pow(n) * x.pow(n)
        sum += term
        lastTerm = term

        println("$n\t${"%.6f".format(term)}\t${"%.6f".format(sum)}")
        n++

    } while (Math.abs(lastTerm) > epsilon) // Продолжаем пока член ряда больше точности

    // Вычисление стандартной функции для сравнения
    val standard = (1.0 + x).pow(-1)

    // Вывод результатов
    println("\n" + "=".repeat(40))
    println("РЕЗУЛЬТАТЫ:")
    println("Значение x: $x")
    println("Точность: $epsilon")
    println("Количество членов ряда: ${n-1}")
    println("Сумма ряда: ${"%.8f".format(sum)}")
    println("Стандартная функция: ${"%.8f".format(standard)}")

    val difference = Math.abs(sum - standard)
    println("Разница: ${"%.8f".format(difference)}")
    println("=".repeat(40))
}