require 'objspace' # This is part of Ruby's standard library

# Initialize counters for assignments and evaluations
assignments = 0
evaluations = 0

# Start measuring time and memory
start_time = Time.now
start_memory = ObjectSpace.memsize_of_all

# Initialize the first two Fibonacci numbers
a = 0
b = 1
assignments += 2  # Assigning initial values to a and b

fib = a
assignments += 1  # Assigning fib to a

fib_list = []
assignments += 1  # Initializing fib_list

n = 1000
i = 2
assignments += 2  # Assigning n and i

# Generate Fibonacci sequence
while i < n
  fib = a + b
  evaluations += 1  # a + b evaluation
  assignments += 1  # Assigning fib

  puts fib
  evaluations += 1  # Printing is considered an evaluation

  a = b
  b = fib
  assignments += 2  # Reassigning a and b

  fib_list << b
  evaluations += 1  # Adding to list is an evaluation
  assignments += 1  # Adding new element to fib_list

  i += 1
  assignments += 1  # Incrementing i
end

# Reverse and print all values of a until the initial state is reached
while i == 1000
  while !fib_list.empty?
    evaluations += 1  # Checking list size is an evaluation

    b = fib_list.pop  # Remove the last element from the list (b)
    evaluations += 1  # Pop operation is an evaluation
    assignments += 1  # Assigning removed value to b

    a = b - a  # Reverse the calculation of 'a'
    evaluations += 1  # b - a evaluation
    assignments += 1  # Assigning reversed value to a

    puts "Reversed value of a: #{a}"
    evaluations += 1  # Printing is considered an evaluation
    puts "Reversed value of b: #{b}"
    evaluations += 1  # Printing is considered an evaluation

    break if a == 0
    evaluations += 1  # Evaluation of condition
  end
  break
end

# Stop measuring time and memory
end_time = Time.now
end_memory = ObjectSpace.memsize_of_all

# Calculate execution time in seconds
execution_time = end_time - start_time

# Calculate memory usage in megabytes
memory_used = (end_memory - start_memory) / 1024.0 / 1024.0

# Display the execution time, memory usage, assignments, and evaluations
puts "\nExecution Time: #{execution_time} seconds"
puts "Memory Used: #{'%.6f' % memory_used} MB"
puts "Total Assignments: #{assignments}"
puts "Total Evaluations: #{evaluations}"
