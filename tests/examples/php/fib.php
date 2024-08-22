<?php

class Fibonacci {

    public function main() {
        // Initialize counters for assignments and evaluations
        $assignments = 0;
        $evaluations = 0;

        // Start measuring time and memory
        $startTime = microtime(true);
        gc_collect_cycles(); // Suggest garbage collection to minimize memory usage at the start
        $startMemory = memory_get_usage();

        // Initialize the first two Fibonacci numbers using BCMath
        $a = '0';
        $b = '1';
        $assignments += 2; // Assigning initial values to a and b

        $fib = $a;
        $assignments += 1; // Assigning fib to a

        $fibList = [];
        $assignments += 1; // Initializing fibList

        $n = 1000;
        $i = 2;
        $assignments += 2; // Assigning n and i

        // Generate Fibonacci sequence
        while ($i < $n) {
            $fib = bcadd($a, $b);
            $evaluations += 1; // a + b evaluation
            $assignments += 1; // Assigning fib

            echo $fib . "\n";
            $evaluations += 1; // Printing is considered an evaluation

            $a = $b;
            $b = $fib;
            $assignments += 2; // Reassigning a and b

            $fibList[] = $b;
            $evaluations += 1; // Adding to list is an evaluation
            $assignments += 1; // Adding new element to fibList

            $i += 1;
            $assignments += 1; // Incrementing i
        }

        // Reverse and print all values of a until the initial state is reached
        while ($i == 1000) {
            while (count($fibList) > 0) {
                $evaluations += 1; // Checking list size is an evaluation

                $b = array_pop($fibList); // Remove the last element from the list (b)
                $evaluations += 1; // Remove operation is an evaluation
                $assignments += 1; // Assigning removed value to b

                $a = bcsub($b, $a); // Reverse the calculation of 'a' using bcsub for precision
                $evaluations += 1; // b - a evaluation
                $assignments += 1; // Assigning reversed value to a

                echo "Reversed value of a: $a\n";
                $evaluations += 1; // Printing is considered an evaluation
                echo "Reversed value of b: $b\n";
                $evaluations += 1; // Printing is considered an evaluation

                if ($a == '0') {
                    $evaluations += 1; // Evaluation of condition
                    break;
                }
            }
            break;
        }

        // Stop measuring time and memory
        $endTime = microtime(true);
        $endMemory = memory_get_usage();

        // Calculate execution time in seconds
        $executionTime = $endTime - $startTime;

        // Calculate memory usage in megabytes
        $memoryUsed = ($endMemory - $startMemory) / (1024 * 1024);

        // Display the execution time, memory usage, assignments, and evaluations
        echo "\nExecution Time: $executionTime seconds\n";
        echo "Memory Used: $memoryUsed MB\n";
        echo "Total Assignments: $assignments\n";
        echo "Total Evaluations: $evaluations\n";
    }
}

// Create a new Fibonacci instance and run the main function
$fibonacci = new Fibonacci();
$fibonacci->main();

?>
