package main

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestCalculator_Add(t *testing.T) {
	calc := &Calculator{}
	
	tests := []struct {
		name     string
		a        int
		b        int
		expected int
	}{
		{"positive numbers", 5, 3, 8},
		{"zeros", 0, 0, 0},
		{"negative numbers", -2, -3, -5},
		{"mixed signs", 5, -3, 2},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Add(tt.a, tt.b)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCalculator_Subtract(t *testing.T) {
	calc := &Calculator{}
	
	tests := []struct {
		name     string
		a        int
		b        int
		expected int
	}{
		{"positive numbers", 5, 3, 2},
		{"zeros", 0, 0, 0},
		{"negative numbers", -2, -3, 1},
		{"mixed signs", 5, -3, 8},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Subtract(tt.a, tt.b)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCalculator_Multiply(t *testing.T) {
	calc := &Calculator{}
	
	tests := []struct {
		name     string
		a        int
		b        int
		expected int
	}{
		{"positive numbers", 5, 3, 15},
		{"with zero", 0, 5, 0},
		{"negative numbers", -2, -3, 6},
		{"mixed signs", 5, -3, -15},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Multiply(tt.a, tt.b)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCalculator_Divide(t *testing.T) {
	calc := &Calculator{}
	
	t.Run("successful division", func(t *testing.T) {
		result, err := calc.Divide(10, 2)
		assert.NoError(t, err)
		assert.Equal(t, 5.0, result)
	})
	
	t.Run("division by zero", func(t *testing.T) {
		result, err := calc.Divide(5, 0)
		assert.Error(t, err)
		assert.Equal(t, 0.0, result)
		assert.Equal(t, "деление на ноль невозможно", err.Error())
	})
	
	t.Run("division with remainder", func(t *testing.T) {
		result, err := calc.Divide(5, 2)
		assert.NoError(t, err)
		assert.Equal(t, 2.5, result)
	})
}