# Challenge: Parallel Sum of Squares

# Description: 

In this challenge, students will implement a parallel algorithm to calculate the sum of squares of numbers in a given range using thread synchronization with mutexes.


# Instructions for Students:

- Implement a sequential function to calculate the sum of squares of numbers in a given range.
- Implement a parallel function using thread synchronization with mutexes to calculate the sum of squares in parallel. Divide the range of numbers into equal-sized sub-ranges and assign each sub-range calculation to a separate thread. Ensure proper synchronization using a mutex to avoid race conditions.
- Compare the execution time of the sequential and parallel implementations for different ranges and numbers of threads. Analyze the speedup achieved using multiple threads.
- Discuss the challenges and importance of thread synchronization, especially when multiple threads access and modify shared data concurrently.

# Guidelines:

- Students should use Python's threading module to create and manage threads.
- Encourage students to use a Lock object from the threading module as a mutex for synchronization.
- The sum variable should be shared between threads, and proper locking and unlocking of the mutex should be implemented.
- Experiment with different ranges of numbers and numbers of threads to observe the impact on speedup and efficiency.
- Discuss the trade-offs between the number of threads and the overhead of thread management and synchronization.
- Students can use the time module to measure execution time accurately.

# Evaluation Criteria:

- - Correctness of the sequential and parallel sum of squares implementations.
- - Efficient utilization of thread synchronization with mutexes to ensure correct and consistent updates to the shared sum variable.
- - Analysis of speedup and efficiency achieved using multiple threads.
- - Discussion of thread synchronization challenges and the importance of using mutexes to avoid race conditions.



## Setup Instructions

To set up your environment and run the code, follow these steps:

1. **Create a Virtual Environment**:

   Open your terminal and navigate to the project directory. Run the following command to create a virtual environment:

   ```bash
   python -m venv env
   ```
2. **Activate the Virtual Environment**:

   - On Windows, run:

     ```bash
     .\env\Scripts\activate
     ```

   - On macOS and Linux, run:

     ```bash
     source env/bin/activate
     ```
3. **Install the required libraries**:

     ```bash
        pip freeze > requirements.txt
     ```
     ```bash
        pip install -r requirements.txt
     ```
4. **Run the Code**:

   You can now run the Python script using the following command:

   ```bash
   python index.py
   ```