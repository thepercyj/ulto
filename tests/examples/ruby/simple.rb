require 'objspace' # This is part of Ruby's standard library

# Initialize counters for assignments and evaluations
assignments = 0
evaluations = 0

# Start measuring time and memory
start_time = Time.now
start_memory = ObjectSpace.memsize_of_all

# Initialize variables
x = 10
y = 20
assignments += 2 # Initial assignments of x and y

# Number of iterations
n = 1000
i = 0
assignments += 2 # Assigning n and i

# Perform the loop for accumulation
while i < n
  # Assign new values by adding two-digit numbers
  x += 15
  assignments += 1 # Assignment of x += 15
  evaluations += 1 # Evaluation of x + 15
  puts "Iteration #{i + 1} - Step 1: x = #{x}"

  x += 20
  assignments += 1 # Assignment of x += 20
  evaluations += 1 # Evaluation of x + 20
  puts "Iteration #{i + 1} - Step 2: x = #{x}"

  y += 25
  assignments += 1 # Assignment of y += 25
  evaluations += 1 # Evaluation of y + 25
  puts "Iteration #{i + 1} - Step 1: y = #{y}"

  y += 30
  assignments += 1 # Assignment of y += 20
  evaluations += 1 # Evaluation of y + 20
  puts "Iteration #{i + 1} - Step 2: y = #{y}"

  # Increment the iterator
  i += 1
  assignments += 1 # Assignment of i += 1
  evaluations += 1 # Evaluation of i + 1
end

# Reset the iterator
i = 0
assignments += 1 # Reassigning i to 0

# Perform the loop for reversal
while i < n
  # Reverse the state to the previous value
  x -= 15
  assignments += 1 # Assignment of x -= 20
  evaluations += 1 # Evaluation of x - 20
  puts "Reverse Iteration #{i + 1} - Step 1: x = #{x}"

  x -= 20
  assignments += 1 # Assignment of x -= 15
  evaluations += 1 # Evaluation of x - 15
  puts "Reverse Iteration #{i + 1} - Step 2: x = #{x}"

  y -= 25
  assignments += 1 # Assignment of y -= 20
  evaluations += 1 # Evaluation of y - 20
  puts "Reverse Iteration #{i + 1} - Step 1: y = #{y}"

  y -= 30
  assignments += 1 # Assignment of y -= 25
  evaluations += 1 # Evaluation of y - 25
  puts "Reverse Iteration #{i + 1} - Step 2: y = #{y}"

  # Increment the iterator
  i += 1
  assignments += 1 # Assignment of i += 1
  evaluations += 1 # Evaluation of i + 1
end

# Stop measuring time and memory
end_time = Time.now
end_memory = ObjectSpace.memsize_of_all

# Calculate execution time in seconds
execution_time = end_time - start_time

# Calculate memory usage in megabytes (MB)
memory_used = (end_memory - start_memory) / 1024.0 / 1024.0

# Print final values of x and y
puts "Final x: #{x}"
puts "Final y: #{y}"

# Display the execution time, memory usage, assignments, and evaluations
puts "\nExecution Time: #{execution_time} seconds"
puts "Memory Used: #{'%.6f' % memory_used} MB" # Limit to 6 decimal places
puts "Total Assignments: #{assignments}"
puts "Total Evaluations: #{evaluations}"
