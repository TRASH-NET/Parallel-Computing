# Challenge

Implement a parallel program in Python that simulates a team of workers performing a series of tasks. Each worker should perform a specific task, and once all workers have completed their tasks, they should synchronize at a barrier before proceeding to the next task.

# Task Description

You have a team of 5 workers, each responsible for performing a specific task:

- Worker 1: Calculates the sum of all numbers in a large list (e.g., 100,000 elements)
- Worker 2: Performs a matrix multiplication on two large matrices (e.g., 1000x1000)
- Worker 3: Searches for a specific pattern in a large text file (e.g., 100,000 lines)
- Worker 4: Simulates a random walk of 100,000 steps
- Worker 5: Calculates the maximum value in a large array (e.g., 100,000 elements)

Each worker should perform their task concurrently, and once all workers have completed their tasks, they should synchronize at a barrier. After the barrier, each worker should print a message indicating that they have completed their task and are ready to proceed.

- Requirements
- Use the threading module in Python to create and manage the worker threads.
- Use a barrier synchronization primitive (e.g., threading.Barrier) to ensure that all workers wait for each other to complete their tasks before proceeding.
- Use a shared data structure (e.g., a Queue or a Manager object from the multiprocessing module) to store the results of each worker's task.
- Write a main function that creates the worker threads, starts them, and waits for them to complete.

# Grading Criteria

- Correctness: Does the program correctly implement the barrier synchronization and ensure that all workers wait for each other to complete their tasks?
- Performance: Does the program take advantage of multiple CPU cores to perform the tasks concurrently?
- Code quality: Is the code well-organized, readable, and maintainable?

# Tips and Hints

- Use the threading.Barrier class to create a barrier synchronization primitive.
- Use the threading.Thread class to create and manage the worker threads.
- Use a shared data structure to store the results of each worker's task.
- Use the time module to measure the execution time of the program.