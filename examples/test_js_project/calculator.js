/**
 * Класс калькулятора для выполнения математических операций
 */
class Calculator {
    /**
     * Сложение двух чисел
     * @param {number} a первое число
     * @param {number} b второе число
     * @returns {number} сумма чисел
     */
    add(a, b) {
        return a + b;
    }

    /**
     * Вычитание двух чисел
     * @param {number} a первое число
     * @param {number} b второе число
     * @returns {number} разность чисел
     */
    subtract(a, b) {
        return a - b;
    }

    /**
     * Умножение двух чисел
     * @param {number} a первое число
     * @param {number} b второе число
     * @returns {number} произведение чисел
     */
    multiply(a, b) {
        return a * b;
    }

    /**
     * Деление двух чисел
     * @param {number} a делимое
     * @param {number} b делитель
     * @returns {number} частное
     * @throws {Error} если делитель равен нулю
     */
    divide(a, b) {
        if (b === 0) {
            throw new Error('Деление на ноль невозможно');
        }
        return a / b;
    }
}

module.exports = Calculator;