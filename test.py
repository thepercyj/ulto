a = 0
b = 1
fib = a
rev_history = []

n = 500
i = 2


if n > 1:
    print(a)
if n > 2:
    print(b)

while i < n:
    fib = a + b
    print(fib)
    a = b
    b = fib
    rev_history = [b] + rev_history
    i += 1