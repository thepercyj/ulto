<?php
// Initialize counters for assignments and evaluations
$assignments = 0;
$evaluations = 0;

// Start measuring time and memory
$startTime = microtime(true);
$startMemory = memory_get_usage();

// Initialize variables
$x = 10;
$y = 20;
$assignments += 2; // Initial assignments of $x and $y

// Number of iterations
$n = 1000;
$i = 0;
$assignments += 2; // Assigning $n and $i

// Perform the loop for accumulation
while ($i < $n) {
    // Assign new values by adding two-digit numbers
    $x += 15;
    $assignments += 1; // Assignment of $x += 15
    $evaluations += 1; // Evaluation of $x + 15
    echo "Iteration " . ($i + 1) . " - Step 1: x = $x\n";

    $x += 20;
    $assignments += 1; // Assignment of $x += 20
    $evaluations += 1; // Evaluation of $x + 20
    echo "Iteration " . ($i + 1) . " - Step 2: x = $x\n";

    $y += 25;
    $assignments += 1; // Assignment of $y += 25
    $evaluations += 1; // Evaluation of $y + 25
    echo "Iteration " . ($i + 1) . " - Step 1: y = $y\n";

    $y += 30;
    $assignments += 1; // Assignment of $y += 20
    $evaluations += 1; // Evaluation of $y + 20
    echo "Iteration " . ($i + 1) . " - Step 2: y = $y\n";

    // Increment the iterator
    $i++;
    $assignments += 1; // Assignment of $i += 1
    $evaluations += 1; // Evaluation of $i + 1
}

// Reset the iterator
$i = 0;
$assignments += 1; // Reassigning $i to 0

// Perform the loop for reversal
while ($i < $n) {
    // Reverse the state to the previous value
    $x -= 15;
    $assignments += 1; // Assignment of $x -= 20
    $evaluations += 1; // Evaluation of $x - 20
    echo "Reverse Iteration " . ($i + 1) . " - Step 1: x = $x\n";

    $x -= 20;
    $assignments += 1; // Assignment of $x -= 15
    $evaluations += 1; // Evaluation of $x - 15
    echo "Reverse Iteration " . ($i + 1) . " - Step 2: x = $x\n";

    $y -= 25;
    $assignments += 1; // Assignment of $y -= 20
    $evaluations += 1; // Evaluation of $y - 20
    echo "Reverse Iteration " . ($i + 1) . " - Step 1: y = $y\n";

    $y -= 30;
    $assignments += 1; // Assignment of $y -= 25
    $evaluations += 1; // Evaluation of $y - 25
    echo "Reverse Iteration " . ($i + 1) . " - Step 2: y = $y\n";

    // Increment the iterator
    $i++;
    $assignments += 1; // Assignment of $i += 1
    $evaluations += 1; // Evaluation of $i + 1
}

// Stop measuring time and memory
$endTime = microtime(true);
$endMemory = memory_get_usage();

// Calculate execution time in seconds
$executionTime = $endTime - $startTime;

// Calculate memory usage in megabytes
$memoryUsed = ($endMemory - $startMemory) / (1024 * 1024);

// Print final values of $x and $y
echo "Final x: $x\n";
echo "Final y: $y\n";

// Display the execution time, memory usage, assignments, and evaluations
echo "\nExecution Time: " . $executionTime . " seconds\n";
echo "Memory Used: " . number_format($memoryUsed, 6) . " MB\n";
echo "Total Assignments: " . $assignments . "\n";
echo "Total Evaluations: " . $evaluations . "\n";
?>
