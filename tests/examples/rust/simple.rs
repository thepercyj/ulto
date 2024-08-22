use cfg_if::cfg_if;
use sysinfo::{Pid, ProcessExt, System, SystemExt};
use std::time::Instant;

fn main() {
    let mut assignments = 0;
    let mut evaluations = 0;

    let start_time = Instant::now();
    let start_memory = get_memory_usage();

    let mut x = 10;
    let mut y = 20;
    assignments += 2;

    let n = 1000;
    let mut i = 0;
    assignments += 2;

    while i < n {
        x += 15;
        assignments += 1;
        evaluations += 1;
        println!("Iteration {} - Step 1: x = {}", i + 1, x);

        x += 20;
        assignments += 1;
        evaluations += 1;
        println!("Iteration {} - Step 2: x = {}", i + 1, x);

        y += 25;
        assignments += 1;
        evaluations += 1;
        println!("Iteration {} - Step 1: y = {}", i + 1, y);

        y += 30;
        assignments += 1;
        evaluations += 1;
        println!("Iteration {} - Step 2: y = {}", i + 1, y);

        i += 1;
        assignments += 1;
        evaluations += 1;
    }

    i = 0;
    assignments += 1;

    while i < n {
        // Check to prevent underflow
        if x >= 15 {
            x -= 15;
            assignments += 1;
            evaluations += 1;
            println!("Reverse Iteration {} - Step 1: x = {}", i + 1, x);
        } else {
            println!("Reverse Iteration {} - Step 1: x cannot be reduced further", i + 1);
            break;
        }

        if x >= 20 {
            x -= 20;
            assignments += 1;
            evaluations += 1;
            println!("Reverse Iteration {} - Step 2: x = {}", i + 1, x);
        } else {
            println!("Reverse Iteration {} - Step 2: x cannot be reduced further", i + 1);
            break;
        }

        if y >= 25 {
            y -= 25;
            assignments += 1;
            evaluations += 1;
            println!("Reverse Iteration {} - Step 1: y = {}", i + 1, y);
        } else {
            println!("Reverse Iteration {} - Step 1: y cannot be reduced further", i + 1);
            break;
        }

        if y >= 30 {
            y -= 30;
            assignments += 1;
            evaluations += 1;
            println!("Reverse Iteration {} - Step 2: y = {}", i + 1, y);
        } else {
            println!("Reverse Iteration {} - Step 2: y cannot be reduced further", i + 1);
            break;
        }

        i += 1;
        assignments += 1;
        evaluations += 1;
    }

    let end_time = Instant::now();
    let end_memory = get_memory_usage();

    let execution_time = end_time.duration_since(start_time);
    let memory_used = (end_memory - start_memory) as f64 / (1024.0 * 1024.0);

    println!("Final x: {}", x);
    println!("Final y: {}", y);
    println!("\nExecution Time: {:.6} seconds", execution_time.as_secs_f64());
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
