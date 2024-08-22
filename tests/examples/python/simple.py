import time
import tracemalloc

assignments = 0
evaluations = 0

# Start measuring time and memory
start_time = time.time()
tracemalloc.start()

x = 10
y = 20
assignments += 2

# Number of iterations
n = 1000
i = 0
assignments += 2

# Perform the loop for forward execution
while i < n:
    x += 15
    assignments += 1
    evaluations += 1
    print(f"Forward Iteration {i + 1} - Step 1: x = {x}")

    x += 20
    assignments += 1
    evaluations += 1
    print(f"Forward {i + 1} - Step 2: x = {x}")

    y += 25
    assignments += 1
    evaluations += 1
    print(f"Forward {i + 1} - Step 1: y = {y}")

    y += 30
    assignments += 1
    evaluations += 1
    print(f"Forward {i + 1} - Step 2: y = {y}")


    i += 1
    assignments += 1
    evaluations += 1


i = 0
assignments += 1

# Perform the loop for reversal
while i < n:
    # Reverse the state to the previous value
    x -= 15
    assignments += 1
    evaluations += 1
    print(f"Reverse Iteration {i + 1} - Step 1: x = {x}")

    x -= 20
    assignments += 1
    evaluations += 1
    print(f"Reverse Iteration {i + 1} - Step 2: x = {x}")

    y -= 25
    assignments += 1
    evaluations += 1
    print(f"Reverse Iteration {i + 1} - Step 1: y = {y}")

    y -= 30
    assignments += 1
    evaluations += 1
    print(f"Reverse Iteration {i + 1} - Step 2: y = {y}")

    i += 1
    assignments += 1
    evaluations += 1

# Stop measuring time and memory
end_time = time.time()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("Final x:", x)
print("Final y:", y)

# Display the execution time, memory usage, assignments, and evaluations
execution_time = end_time - start_time
print(f"\nExecution Time: {execution_time} seconds")
print(f"Peak Memory Usage: {peak / 10**6} MB")
print(f"Total Assignments: {assignments}")
print(f"Total Evaluations: {evaluations}")
