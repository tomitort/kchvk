package com.example;

/**
 * Класс калькулятора для демонстрации функциональности
 */
public class Calculator {
    
    /**
     * Сложение двух чисел
     * @param a первое число
     * @param b второе число
     * @return сумма чисел
     */
    public int add(int a, int b) {
        return a + b;
    }
    
    /**
     * Вычитание двух чисел
     * @param a первое число
     * @param b второе число
     * @return разность чисел
     */
    public int subtract(int a, int b) {
        return a - b;
    }
    
    /**
     * Умножение двух чисел
     * @param a первое число
     * @param b второе число
     * @return произведение чисел
     */
    public int multiply(int a, int b) {
        return a * b;
    }
    
    /**
     * Деление двух чисел
     * @param a делимое
     * @param b делитель
     * @return частное
     * @throws ArithmeticException если делитель равен нулю
     */
    public double divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Деление на ноль невозможно");
        }
        return (double) a / b;
    }
}