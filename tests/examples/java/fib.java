import java.util.ArrayList;
import java.util.List;

public class fib {

    public static void main(String[] args) {
        // Initialize counters for assignments and evaluations
        int assignments = 0;
        int evaluations = 0;

        // Start measuring time and memory
        long startTime = System.nanoTime();
        Runtime runtime = Runtime.getRuntime();
        runtime.gc(); // Suggest garbage collection to minimize memory usage at the start
        long startMemory = runtime.totalMemory() - runtime.freeMemory();

        // Initialize the first two Fibonacci numbers
        int a = 0;
        int b = 1;
        assignments += 2; // Assigning initial values to a and b

        int fib = a;
        assignments += 1; // Assigning fib to a

        List<Integer> fibList = new ArrayList<>();
        assignments += 1; // Initializing fibList

        int n = 1000;
        int i = 2;
        assignments += 2; // Assigning n and i

        // Generate Fibonacci sequence
        while (i < n) {
            fib = a + b;
            evaluations += 1; // a + b evaluation
            assignments += 1; // Assigning fib

            System.out.println(fib);
            evaluations += 1; // Printing is considered an evaluation

            a = b;
            b = fib;
            assignments += 2; // Reassigning a and b

            fibList.add(b);
            evaluations += 1; // Adding to list is an evaluation
            assignments += 1; // Adding new element to fibList

            i += 1;
            assignments += 1; // Incrementing i
        }

        // Reverse and print all values of a until the initial state is reached
        while (i == 1000) {
            while (fibList.size() > 0) {
                evaluations += 1; // Checking list size is an evaluation

                b = fibList.remove(fibList.size() - 1); // Remove the last element from the list (b)
                evaluations += 1; // Remove operation is an evaluation
                assignments += 1; // Assigning removed value to b

                a = b - a; // Reverse the calculation of 'a'
                evaluations += 1; // b - a evaluation
                assignments += 1; // Assigning reversed value to a

                System.out.println("Reversed value of a: " + a);
                evaluations += 1; // Printing is considered an evaluation
                System.out.println("Reversed value of b: " + b);
                evaluations += 1; // Printing is considered an evaluation

                if (a == 0) {
                    evaluations += 1; // Evaluation of condition
                    break;
                }
            }
            break;
        }

        // Stop measuring time and memory
        long endTime = System.nanoTime();
        long endMemory = runtime.totalMemory() - runtime.freeMemory();

        // Calculate execution time in seconds
        double executionTime = (endTime - startTime) / 1_000_000_000.0;

        // Calculate memory usage in megabytes
        double memoryUsed = (endMemory - startMemory) / (1024.0 * 1024.0);

        // Display the execution time, memory usage, assignments, and evaluations
        System.out.println("\nExecution Time: " + executionTime + " seconds");
        System.out.println("Memory Used: " + memoryUsed + " MB");
        System.out.println("Total Assignments: " + assignments);
        System.out.println("Total Evaluations: " + evaluations);
    }
}
