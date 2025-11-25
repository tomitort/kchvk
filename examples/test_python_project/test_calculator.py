"""
Тесты для модуля калькулятора
"""

import pytest
from calculator import Calculator


class TestCalculator:
    """Тестовый класс для калькулятора"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.calculator = Calculator()

    def test_add(self):
        """Тестирование сложения"""
        assert self.calculator.add(5, 3) == 8
        assert self.calculator.add(0, 0) == 0
        assert self.calculator.add(-2, -3) == -5
        assert self.calculator.add(5, -3) == 2

    def test_subtract(self):
        """Тестирование вычитания"""
        assert self.calculator.subtract(5, 3) == 2
        assert self.calculator.subtract(0, 0) == 0
        assert self.calculator.subtract(-2, -3) == 1
        assert self.calculator.subtract(5, -3) == 8

    def test_multiply(self):
        """Тестирование умножения"""
        assert self.calculator.multiply(5, 3) == 15
        assert self.calculator.multiply(0, 5) == 0
        assert self.calculator.multiply(-2, -3) == 6
        assert self.calculator.multiply(5, -3) == -15

    def test_divide(self):
        """Тестирование деления"""
        assert self.calculator.divide(10, 2) == 5
        assert self.calculator.divide(5, 2) == 2.5
        assert self.calculator.divide(-6, 3) == -2

    def test_divide_by_zero(self):
        """Тестирование деления на ноль"""
        with pytest.raises(ValueError, match="Деление на ноль невозможно"):
            self.calculator.divide(5, 0)


def test_calculator_integration():
    """Интеграционный тест калькулятора"""
    calc = Calculator()
    
    # Проверяем последовательность операций
    result = calc.add(10, 5)  # 15
    result = calc.subtract(result, 3)  # 12
    result = calc.multiply(result, 2)  # 24
    result = calc.divide(result, 4)  # 6
    
    assert result == 6