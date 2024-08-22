public class simple {
    public static void main(String[] args) {
        // Initialize counters for assignments and evaluations
        int assignments = 0;
        int evaluations = 0;

        // Start measuring time and memory
        long startTime = System.nanoTime();
        Runtime runtime = Runtime.getRuntime();
        runtime.gc(); // Suggest garbage collection to minimize memory usage at the start
        long startMemory = runtime.totalMemory() - runtime.freeMemory();

        // Initialize variables
        int x = 10;
        int y = 20;
        assignments += 2; // Initial assignments of x and y

        // Number of iterations
        int n = 1000;
        int i = 0;
        assignments += 2; // Assigning n and i

        // Perform the loop for accumulation
        while (i < n) {
            // Assign new values by adding two-digit numbers
            x += 15;
            assignments += 1; // Assignment of x += 15
            evaluations += 1; // Evaluation of x + 15
            System.out.println("Iteration " + (i + 1) + " - Step 1: x = " + x);

            x += 20;
            assignments += 1; // Assignment of x += 20
            evaluations += 1; // Evaluation of x + 20
            System.out.println("Iteration " + (i + 1) + " - Step 2: x = " + x);

            y += 25;
            assignments += 1; // Assignment of y += 25
            evaluations += 1; // Evaluation of y + 25
            System.out.println("Iteration " + (i + 1) + " - Step 1: y = " + y);

            y += 30;
            assignments += 1; // Assignment of y += 20
            evaluations += 1; // Evaluation of y + 20
            System.out.println("Iteration " + (i + 1) + " - Step 2: y = " + y);

            // Increment the iterator
            i++;
            assignments += 1; // Assignment of i += 1
            evaluations += 1; // Evaluation of i + 1
        }

        // Reset the iterator
        i = 0;
        assignments += 1; // Reassigning i to 0

        // Perform the loop for reversal
        while (i < n) {
            // Reverse the state to the previous value
            x -= 15;
            assignments += 1; // Assignment of x -= 20
            evaluations += 1; // Evaluation of x - 20
            System.out.println("Reverse Iteration " + (i + 1) + " - Step 1: x = " + x);

            x -= 20;
            assignments += 1; // Assignment of x -= 15
            evaluations += 1; // Evaluation of x - 15
            System.out.println("Reverse Iteration " + (i + 1) + " - Step 2: x = " + x);

            y -= 25;
            assignments += 1; // Assignment of y -= 20
            evaluations += 1; // Evaluation of y - 20
            System.out.println("Reverse Iteration " + (i + 1) + " - Step 1: y = " + y);

            y -= 30;
            assignments += 1; // Assignment of y -= 25
            evaluations += 1; // Evaluation of y - 25
            System.out.println("Reverse Iteration " + (i + 1) + " - Step 2: y = " + y);

            // Increment the iterator
            i++;
            assignments += 1; // Assignment of i += 1
            evaluations += 1; // Evaluation of i + 1
        }

        // Stop measuring time and memory
        long endTime = System.nanoTime();
        long endMemory = runtime.totalMemory() - runtime.freeMemory();

        // Calculate execution time in seconds
        double executionTime = (endTime - startTime) / 1_000_000_000.0;

        // Calculate memory usage in megabytes
        double memoryUsed = (endMemory - startMemory) / (1024.0 * 1024.0);

        // Print final values of x and y
        System.out.println("Final x: " + x);
        System.out.println("Final y: " + y);

        // Display the execution time, memory usage, assignments, and evaluations
        System.out.println("\nExecution Time: " + executionTime + " seconds");
        System.out.println("Memory Used: " + memoryUsed + " MB");
        System.out.println("Total Assignments: " + assignments);
        System.out.println("Total Evaluations: " + evaluations);
    }
}
