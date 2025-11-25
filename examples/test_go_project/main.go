package main

import (
	"fmt"
	"log"
)

// Calculator представляет калькулятор для выполнения математических операций
type Calculator struct{}

// Add выполняет сложение двух чисел
func (c *Calculator) Add(a, b int) int {
	return a + b
}

// Subtract выполняет вычитание двух чисел
func (c *Calculator) Subtract(a, b int) int {
	return a - b
}

// Multiply выполняет умножение двух чисел
func (c *Calculator) Multiply(a, b int) int {
	return a * b
}

// Divide выполняет деление двух чисел
func (c *Calculator) Divide(a, b int) (float64, error) {
	if b == 0 {
		return 0, fmt.Errorf("деление на ноль невозможно")
	}
	return float64(a) / float64(b), nil
}

func main() {
	fmt.Println("🚀 Запуск тестового Go приложения")
	
	calc := &Calculator{}
	
	result := calc.Add(5, 3)
	fmt.Printf("Результат сложения 5 + 3 = %d\n", result)
	
	divResult, err := calc.Divide(10, 2)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Результат деления 10 / 2 = %.1f\n", divResult)
	
	fmt.Println("✅ Приложение успешно запущено!")
}