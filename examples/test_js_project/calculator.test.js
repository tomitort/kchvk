const Calculator = require('./calculator');

describe('Calculator', () => {
    let calculator;

    beforeEach(() => {
        calculator = new Calculator();
    });

    describe('add', () => {
        test('должен складывать положительные числа', () => {
            expect(calculator.add(5, 3)).toBe(8);
        });

        test('должен складывать нули', () => {
            expect(calculator.add(0, 0)).toBe(0);
        });

        test('должен складывать отрицательные числа', () => {
            expect(calculator.add(-2, -3)).toBe(-5);
        });

        test('должен складывать числа с разными знаками', () => {
            expect(calculator.add(5, -3)).toBe(2);
        });
    });

    describe('subtract', () => {
        test('должен вычитать положительные числа', () => {
            expect(calculator.subtract(5, 3)).toBe(2);
        });

        test('должен вычитать нули', () => {
            expect(calculator.subtract(0, 0)).toBe(0);
        });

        test('должен вычитать отрицательные числа', () => {
            expect(calculator.subtract(-2, -3)).toBe(1);
        });

        test('должен вычитать числа с разными знаками', () => {
            expect(calculator.subtract(5, -3)).toBe(8);
        });
    });

    describe('multiply', () => {
        test('должен умножать положительные числа', () => {
            expect(calculator.multiply(5, 3)).toBe(15);
        });

        test('должен умножать на ноль', () => {
            expect(calculator.multiply(0, 5)).toBe(0);
        });

        test('должен умножать отрицательные числа', () => {
            expect(calculator.multiply(-2, -3)).toBe(6);
        });

        test('должен умножать числа с разными знаками', () => {
            expect(calculator.multiply(5, -3)).toBe(-15);
        });
    });

    describe('divide', () => {
        test('должен делить положительные числа', () => {
            expect(calculator.divide(10, 2)).toBe(5);
        });

        test('должен делить числа с остатком', () => {
            expect(calculator.divide(5, 2)).toBe(2.5);
        });

        test('должен выбрасывать ошибку при делении на ноль', () => {
            expect(() => calculator.divide(5, 0)).toThrow('Деление на ноль невозможно');
        });

        test('должен делить отрицательные числа', () => {
            expect(calculator.divide(-6, 3)).toBe(-2);
        });
    });
});