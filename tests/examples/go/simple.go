package main

import (
	"fmt"
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

	// Initialize variables
	x := 10
	y := 20
	assignments += 2 // Initial assignments of x and y

	// Number of iterations
	n := 1000
	i := 0
	assignments += 2 // Assigning n and i

	// Perform the loop for accumulation
	for i < n {
		// Assign new values by adding two-digit numbers
		x += 15
		assignments += 1 // Assignment of x += 15
		evaluations += 1 // Evaluation of x + 15
		fmt.Printf("Iteration %d - Step 1: x = %d\n", i+1, x)

		x += 20
		assignments += 1 // Assignment of x += 20
		evaluations += 1 // Evaluation of x + 20
		fmt.Printf("Iteration %d - Step 2: x = %d\n", i+1, x)

		y += 25
		assignments += 1 // Assignment of y += 25
		evaluations += 1 // Evaluation of y + 25
		fmt.Printf("Iteration %d - Step 1: y = %d\n", i+1, y)

		y += 20
		assignments += 1 // Assignment of y += 20
		evaluations += 1 // Evaluation of y + 20
		fmt.Printf("Iteration %d - Step 2: y = %d\n", i+1, y)

		// Increment the iterator
		i++
		assignments += 1 // Assignment of i += 1
		evaluations += 1 // Evaluation of i + 1
	}

	// Reset the iterator
	i = 0
	assignments += 1 // Reassigning i to 0

	// Perform the loop for reversal
	for i < n {
		// Reverse the state to the previous value
		x -= 20
		assignments += 1 // Assignment of x -= 20
		evaluations += 1 // Evaluation of x - 20
		fmt.Printf("Reverse Iteration %d - Step 1: x = %d\n", i+1, x)

		x -= 15
		assignments += 1 // Assignment of x -= 15
		evaluations += 1 // Evaluation of x - 15
		fmt.Printf("Reverse Iteration %d - Step 2: x = %d\n", i+1, x)

		y -= 20
		assignments += 1 // Assignment of y -= 20
		evaluations += 1 // Evaluation of y - 20
		fmt.Printf("Reverse Iteration %d - Step 1: y = %d\n", i+1, y)

		y -= 25
		assignments += 1 // Assignment of y -= 25
		evaluations += 1 // Evaluation of y - 25
		fmt.Printf("Reverse Iteration %d - Step 2: y = %d\n", i+1, y)

		// Increment the iterator
		i++
		assignments += 1 // Assignment of i += 1
		evaluations += 1 // Evaluation of i + 1
	}

	// Stop measuring time and memory
	endTime := time.Now()
	runtime.ReadMemStats(&m)
	endMemory := m.Alloc

	// Calculate execution time in seconds
	executionTime := endTime.Sub(startTime).Seconds()

	// Calculate memory usage in megabytes
	memoryUsed := float64(endMemory-startMemory) / (1024 * 1024)

	// Print final values of x and y
	fmt.Printf("Final x: %d\n", x)
	fmt.Printf("Final y: %d\n", y)

	// Display the execution time, memory usage, assignments, and evaluations
	fmt.Printf("\nExecution Time: %.6f seconds\n", executionTime)
	fmt.Printf("Memory Used: %.6f MB\n", memoryUsed)
	fmt.Printf("Total Assignments: %d\n", assignments)
	fmt.Printf("Total Evaluations: %d\n", evaluations)
}
