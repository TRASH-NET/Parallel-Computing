# Challenge

Producer-Consumer Problem with Condition Variables

# Description 

In this challenge, students will implement the producer-consumer problem using condition variables. The producer will generate data items, and the consumer will consume and process those items. Students will need to use condition variables to synchronize the producer and consumer threads, ensuring that data is produced and consumed in a controlled manner.

# Instructions for Students

- Implement a producer thread that generates data items and adds them to a shared queue.
- Implement a consumer thread that consumes data items from the shared queue and processes them.
- Use condition variables to synchronize the producer and consumer threads. The producer should wait if the queue is full, and the consumer should wait if the queue is empty.
- Implement proper signaling mechanisms between the producer and consumer threads using condition variables.
- Discuss the challenges and importance of using condition variables for synchronization in this scenario.

# Guidelines

- Students should use Python's threading module to create and manage threads.
- Encourage students to use the Condition class from the threading module to implement condition variables.
- The shared queue should be implemented using a suitable data structure, such as a list or collections.deque.
- Discuss the trade-offs between using condition variables and other synchronization primitives like locks.
- Students can use the time module to introduce artificial delays in the producer and consumer threads to simulate different processing speeds.

# Evaluation Criteria

- Correctness of the producer and consumer thread implementations.
- Efficient utilization of condition variables to synchronize the producer and consumer threads.
- Proper signaling mechanisms between the producer and consumer threads.
- Discussion of the challenges and importance of using condition variables for synchronization.