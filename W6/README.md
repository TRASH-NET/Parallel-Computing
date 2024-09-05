# Challenge

Parallel Matrix Multiplication with Task Joins

# Description 

In this challenge, students will implement parallel matrix multiplication using task joins. Matrix multiplication is a computationally intensive task, and by using multiple threads, students can explore how to speed up the computation. Students will need to create threads, perform matrix multiplication in parallel, and use the join() method to wait for all threads to complete their tasks.

# Instructions for Students

- Provide two square matrices, A and B, of the same size (e.g., 1000x1000).
- Implement a function to perform matrix multiplication in a separate thread. Each thread should multiply a sub-matrix of A and B and return the result.
- Create multiple threads to perform matrix multiplication in parallel. Use the join() method to wait for all threads to complete their tasks before proceeding.
- Combine the results from the threads to obtain the final matrix multiplication result.
- Compare the execution time of the parallel implementation with and without using join(). Analyze the speedup achieved using multiple threads.
- Discuss the importance of using join() to ensure that all threads complete their tasks before proceeding. Explain how join() helps synchronize the execution of threads.

# Guidelines

- Students should use Python's threading module to create and manage threads.
- Encourage students to divide the matrices into equal-sized sub-matrices and assign each sub-matrix multiplication task to a separate thread.
- Students can use the time module to measure execution time accurately.
- Discuss the trade-offs between the number of threads and the overhead of thread management and synchronization.

# Evaluation Criteria

- Correctness of the parallel matrix multiplication implementation using threads.
- Efficient utilization of join() to synchronize the completion of all threads.
- Analysis of speedup and efficiency achieved using multiple threads.
- Discussion of the importance of using join() for proper thread synchronization.