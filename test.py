# Initialize variables
a = 0
b = 1
fib = a
rev_history = []

# Number of terms in the Fibonacci sequence
n = 500
i = 2

# Print the first two terms if n > 1
if n > 1:
    print(a)
if n > 2:
    print(b)

# Generate the Fibonacci sequence and store the history
while i < n:
    fib = a + b
    print(fib)
    a = b
    b = fib
    rev_history = [b] + rev_history  # Prepend b to rev_history
    i += 1