#!/usr/bin/env python3
"""
Главный файл приложения для тестирования Self-Deploy CI/CD
"""

from calculator import Calculator


def main():
    print("🚀 Запуск тестового Python приложения")
    
    calculator = Calculator()
    
    result = calculator.add(5, 3)
    print(f"Результат сложения 5 + 3 = {result}")
    
    try:
        div_result = calculator.divide(10, 2)
        print(f"Результат деления 10 / 2 = {div_result}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    print("✅ Приложение успешно запущено!")


if __name__ == "__main__":
    main()