"""
Модуль калькулятора для выполнения математических операций
"""


class Calculator:
    """Класс калькулятора для демонстрации функциональности"""
    
    def add(self, a: float, b: float) -> float:
        """
        Сложение двух чисел
        
        Args:
            a: первое число
            b: второе число
            
        Returns:
            сумма чисел
        """
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """
        Вычитание двух чисел
        
        Args:
            a: первое число
            b: второе число
            
        Returns:
            разность чисел
        """
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """
        Умножение двух чисел
        
        Args:
            a: первое число
            b: второе число
            
        Returns:
            произведение чисел
        """
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """
        Деление двух чисел
        
        Args:
            a: делимое
            b: делитель
            
        Returns:
            частное
            
        Raises:
            ValueError: если делитель равен нулю
        """
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        return a / b