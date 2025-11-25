package com.example;

/**
 * Главный класс приложения для тестирования Self-Deploy CI/CD
 */
public class Main {
    
    /**
     * Основной метод приложения
     * @param args аргументы командной строки
     */
    public static void main(String[] args) {
        System.out.println("🚀 Запуск тестового Java приложения");
        
        Calculator calculator = new Calculator();
        int result = calculator.add(5, 3);
        
        System.out.println("Результат сложения 5 + 3 = " + result);
        System.out.println("✅ Приложение успешно запущено!");
    }
}