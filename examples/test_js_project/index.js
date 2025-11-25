/**
 * Главный файл приложения для тестирования Self-Deploy CI/CD
 */

const Calculator = require('./calculator');

console.log('🚀 Запуск тестового JavaScript приложения');

const calculator = new Calculator();

const result = calculator.add(5, 3);
console.log(`Результат сложения 5 + 3 = ${result}`);

const divResult = calculator.divide(10, 2);
console.log(`Результат деления 10 / 2 = ${divResult}`);

console.log('✅ Приложение успешно запущено!');

// Экспортируем для использования в тестах
module.exports = { Calculator };