package main

import (
	"fmt"
	"math/big"
	"runtime"
	"time"
)

func main() {
	// Initialize counters for assignments and evaluations
	assignments := 0
	evaluations := 0

	// Start measuring time and memory
	startTime := time.Now()
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	startMemory := m.Alloc

	// Initialize the first two Fibonacci numbers using big.Int for large numbers
	a := big.NewInt(0)
	b := big.NewInt(1)
	assignments += 2 // Assigning initial values to a and b

	fib := new(big.Int).Set(a)
	assignments += 1 // Assigning fib to a

	fibList := []*big.Int{}
	assignments += 1 // Initializing fibList

	n := 1000
	i := 2
	assignments += 2 // Assigning n and i

	// Generate Fibonacci sequence
	for i < n {
		fib.Add(a, b)
		evaluations += 1 // a + b evaluation
		assignments += 1 // Assigning fib

		fmt.Println(fib)
		evaluations += 1 // Printing is considered an evaluation

		a.Set(b)
		b.Set(fib)
		assignments += 2 // Reassigning a and b

		fibList = append(fibList, new(big.Int).Set(b))
		evaluations += 1 // Adding to list is an evaluation
		assignments += 1 // Adding new element to fibList

		i += 1
		assignments += 1 // Incrementing i
	}

	// Reverse and print all values of a until the initial state is reached
	for i == 1000 {
		for len(fibList) > 0 {
			evaluations += 1 // Checking list size is an evaluation

			b.Set(fibList[len(fibList)-1])     // Get the last element from the list (b)
			fibList = fibList[:len(fibList)-1] // Remove the last element from the list
			evaluations += 1                   // Remove operation is an evaluation
			assignments += 1                   // Assigning removed value to b

			a.Sub(b, a)      // Reverse the calculation of 'a'
			evaluations += 1 // b - a evaluation
			assignments += 1 // Assigning reversed value to a

			fmt.Printf("Reversed value of a: %v\n", a)
			evaluations += 1 // Printing is considered an evaluation
			fmt.Printf("Reversed value of b: %v\n", b)
			evaluations += 1 // Printing is considered an evaluation

			if a.Cmp(big.NewInt(0)) == 0 {
				evaluations += 1 // Evaluation of condition
				break
			}
		}
		break
	}

	// Stop measuring time and memory
	runtime.ReadMemStats(&m)
	endMemory := m.Alloc
	endTime := time.Now()

	// Calculate execution time in seconds
	executionTime := endTime.Sub(startTime).Seconds()

	// Calculate memory usage in megabytes
	memoryUsed := float64(endMemory-startMemory) / (1024 * 1024)

	// Display the execution time, memory usage, assignments, and evaluations
	fmt.Printf("\nExecution Time: %.6f seconds\n", executionTime)
	fmt.Printf("Memory Used: %.6f MB\n", memoryUsed)
	fmt.Printf("Total Assignments: %d\n", assignments)
	fmt.Printf("Total Evaluations: %d\n", evaluations)
}
