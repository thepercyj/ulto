import java.util.ArrayList;
import java.util.List;

public class fib {

    public static void main(String[] args) {
        int assignments = 0;
        int evaluations = 0;

        long startTime = System.nanoTime();
        Runtime runtime = Runtime.getRuntime();
        runtime.gc();
        long startMemory = runtime.totalMemory() - runtime.freeMemory();

        int a = 0;
        int b = 1;
        assignments += 2;

        int fib = a;
        assignments += 1;

        List<Integer> fibList = new ArrayList<>();
        assignments += 1;

        int n = 1000;
        int i = 2;
        assignments += 2;

        // Generate Fibonacci sequence
        while (i < n) {
            fib = a + b;
            evaluations += 1;
            assignments += 1;

            System.out.println(fib);
            evaluations += 1;

            a = b;
            b = fib;
            assignments += 2;

            fibList.add(b);
            evaluations += 1;
            assignments += 1;

            i += 1;
            assignments += 1;
        }

        // Reverse and print all values of a until the initial state is reached
        while (i == 1000) {
            while (fibList.size() > 0) {
                evaluations += 1;

                b = fibList.remove(fibList.size() - 1);
                evaluations += 1;
                assignments += 1;

                a = b - a;
                evaluations += 1;
                assignments += 1;

                System.out.println("Reversed value of a: " + a);
                evaluations += 1;
                System.out.println("Reversed value of b: " + b);
                evaluations += 1;

                if (a == 0) {
                    evaluations += 1;
                    break;
                }
            }
            break;
        }

        long endTime = System.nanoTime();
        long endMemory = runtime.totalMemory() - runtime.freeMemory();

        double executionTime = (endTime - startTime) / 1_000_000_000.0;

        double memoryUsed = (endMemory - startMemory) / (1024.0 * 1024.0);

        System.out.println("\nExecution Time: " + executionTime + " seconds");
        System.out.println("Memory Used: " + memoryUsed + " MB");
        System.out.println("Total Assignments: " + assignments);
        System.out.println("Total Evaluations: " + evaluations);
    }
}
