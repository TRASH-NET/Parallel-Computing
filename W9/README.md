# Challenge

Implement a parallel program in Python that uses shared memory to communicate between multiple processes. The program should simulate a bank account system where multiple processes can deposit and withdraw money concurrently.

# Task Description

Create a program that uses the multiprocessing module to create multiple processes that share a common memory space. The shared memory space should contain the following variables:

- balance: a floating-point number representing the current balance of the bank account
- lock: a lock object to synchronize access to the shared memory
- Each process should perform the following tasks:
- Deposit a random amount of money (between $1 and $100) into the account
- Withdraw a random amount of money (between $1 and $100) from the account
- Print the current balance after each transaction
- The program should ensure that the shared memory is accessed safely and efficiently by using the lock object to synchronize access.

# Requirements

- Use the multiprocessing module to create multiple processes
- Use the multiprocessing.Value and multiprocessing.Lock classes to create shared memory variables
- Use the lock object to synchronize access to the shared memory
- Use a loop to simulate multiple transactions in each process
- Print the final balance after all transactions have completed

# Grading Criteria

- Correctness: Does the program correctly implement shared memory and synchronization between processes?
- Performance: Does the program take advantage of multiple CPU cores to perform transactions concurrently?
- Code quality: Is the code well-organized, readable, and maintainable?

# Tips and Hints

- Use the multiprocessing.Value class to create a shared floating-point variable for the balance
- Use the multiprocessing.Lock class to create a shared lock object for synchronization
- Use the with statement to acquire and release the lock object
- Use a loop to simulate multiple transactions in each process
- Use the time module to measure the execution time of the program