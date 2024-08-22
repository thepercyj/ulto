use std::time::Instant;
use num_bigint::BigInt;
use num_traits::{One, Zero};
use sysinfo::{Pid, ProcessExt, System, SystemExt};

fn main() {
    // Initialize counters for assignments and evaluations
    let mut assignments = 0;
    let mut evaluations = 0;

    // Start measuring time and memory
    let start_time = Instant::now();
    let start_memory = get_memory_usage();

    // Initialize the first two Fibonacci numbers using BigInt for large numbers
    let mut a = BigInt::zero();
    let mut b = BigInt::one();
    assignments += 2; // Assigning initial values to a and b

    let mut fib = a.clone();
    assignments += 1; // Assigning fib to a

    let mut fib_list: Vec<BigInt> = Vec::new();
    assignments += 1; // Initializing fib_list

    let n = 1000;
    let mut i = 2;
    assignments += 2; // Assigning n and i

    // Generate Fibonacci sequence
    while i < n {
        fib = &a + &b;
        evaluations += 1; // a + b evaluation
        assignments += 1; // Assigning fib

        println!("{}", fib);
        evaluations += 1; // Printing is considered an evaluation

        a = b.clone();
        b = fib.clone();
        assignments += 2; // Reassigning a and b

        fib_list.push(b.clone());
        evaluations += 1; // Adding to list is an evaluation
        assignments += 1; // Adding new element to fib_list

        i += 1;
        assignments += 1; // Incrementing i
    }

    // Reverse and print all values of a until the initial state is reached
    while i == 1000 {
        while !fib_list.is_empty() {
            evaluations += 1; // Checking list size is an evaluation

            b = fib_list.pop().unwrap(); // Remove the last element from the list (b)
            evaluations += 1; // Remove operation is an evaluation
            assignments += 1; // Assigning removed value to b

            a = &b - &a; // Reverse the calculation of 'a'
            evaluations += 1; // b - a evaluation
            assignments += 1; // Assigning reversed value to a

            println!("Reversed value of a: {}", a);
            evaluations += 1; // Printing is considered an evaluation
            println!("Reversed value of b: {}", b);
            evaluations += 1; // Printing is considered an evaluation

            if a.is_zero() {
                evaluations += 1; // Evaluation of condition
                break;
            }
        }
        break;
    }

    // Stop measuring time and memory
    let end_time = start_time.elapsed();
    let end_memory = get_memory_usage();

    // Calculate execution time in seconds
    let execution_time = end_time.as_secs_f64();

    // Calculate memory usage in bytes
    let memory_used = (end_memory - start_memory) as f64 / (1024.0 * 1024.0);

    // Display the execution time, memory usage, assignments, and evaluations
    println!("\nExecution Time: {:.6} seconds", execution_time);
    println!("Memory Used: {:.6} MB", memory_used);
    println!("Total Assignments: {}", assignments);
    println!("Total Evaluations: {}", evaluations);
}


fn get_memory_usage() -> usize {
    let mut system = System::new_all();
    system.refresh_all();

    let pid = Pid::from(std::process::id() as usize);
    if let Some(process) = system.process(pid) {
        process.memory() as usize
    } else {
        0
    }
}