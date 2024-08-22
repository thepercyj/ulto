import time
import tracemalloc

assignments = 0
evaluations = 0

start_time = time.time()
tracemalloc.start()

# Initialize the first two Fibonacci numbers
a = 0
b = 1
assignments += 2

fib = a
assignments += 1

fib_list = []
assignments += 1

n = 1000
i = 2
assignments += 2

# Generate Fibonacci sequence
while i < n:
    fib = a + b
    evaluations += 1
    assignments += 1

    print(fib)
    evaluations += 1

    a = b
    b = fib
    assignments += 2

    fib_list = fib_list + [b]
    evaluations += 1
    assignments += 1

    i += 1
    assignments += 1

# Reverse and print all values of a until the initial state is reached
while i == 1000:
    while len(fib_list) > 0:
        evaluations += 1

        b = fib_list.pop()
        evaluations += 1
        assignments += 1

        a = b - a  # Reverse the calculation of 'a'
        evaluations += 1
        assignments += 1

        print(f"Reversed value of a: {a}")
        evaluations += 1
        print(f"Reversed value of b: {b}")
        evaluations += 1

        if a == 0:
            evaluations += 1
            break
    break

# Stop measuring time and memory
end_time = time.time()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

execution_time = end_time - start_time
print(f"\nExecution Time: {execution_time} seconds")
print(f"Peak Memory Usage: {peak / 10**6} MB")
print(f"Total Assignments: {assignments}")
print(f"Total Evaluations: {evaluations}")
