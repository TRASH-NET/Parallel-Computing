# Challenge

Implement a parallel program that simulates a producer-consumer system with multiple producers and multiple consumers. The program should have the following components:

- Multiple producers: a set of processes that generate random numbers and send them to a shared queue.
- Multiple consumers: a set of processes that receive numbers from the shared queue and calculate their sum.
- Main process: a process that creates the producers and consumers processes and coordinates their communication using pipes.

# Requirements

- Use the multiprocessing module to create the producers and consumers processes.
- Use a shared queue to communicate between the producers and consumers processes.
- Use pipes to communicate between the main process and the producers and consumers processes.
- Each producer process should generate 10 random numbers and send them to the shared queue.
- Each consumer process should receive numbers from the shared queue and calculate their sum.
- The main process should receive the sums from the consumer processes and print the total sum.
- The program should handle the case where a producer process finishes sending numbers to the queue before a consumer process has finished receiving numbers from the queue.

# Grading Criteria

- Correctness: Does the program correctly implement the producer-consumer system with multiple producers and multiple consumers?
- Performance: Does the program take advantage of multiple CPU cores to perform the calculations concurrently?
- Code quality: Is the code well-organized, readable, and maintainable?

# Tips and Hints

- Use the multiprocessing.Queue class to create a shared queue for communication between the producers and consumers processes.
- Use the multiprocessing.Pipe class to create pipes for communication between the main process and the producers and consumers processes.
- Use the multiprocessing.Process class to create the producers and consumers processes.
- Use the random module to generate random numbers in the producer processes.
- Use a synchronization primitive (such as a Lock or a Condition) to ensure that the producers and consumers processes access the shared queue safely.