# Challenge: Parallel Image Processing with Thread-Shared Memory

## Description 

In this challenge, students will implement parallel image processing using thread-shared memory. Image processing tasks often involve manipulating large amounts of data, and by using multiple threads, students can explore how to speed up the processing time.

### Instructions for Students
- Provide a large image (e.g., a high-resolution photograph).
- Implement a sequential image processing function that applies a specific effect or transformation to the image (e.g., grayscale conversion, edge detection, blurring).
- Implement a parallel image processing function using thread-shared memory. Divide the image into equal-sized sub-images and assign each sub-image processing task to a separate thread. Ensure proper synchronization and memory sharing between threads.
- Compare the execution time of the sequential and parallel implementations for different image sizes. Analyze the speedup achieved using multiple threads.
- Discuss the challenges and potential issues with memory sharing between threads, such as race conditions and synchronization. Propose solutions or optimizations to address these issues.

### Guidelines
- Students should use `Python's threading module` to create and manage threads.
- Encourage students to use locks or other synchronization primitives to ensure proper memory sharing between threads.
- Students can use the `PIL` or `OpenCV` library to load and manipulate images.
- Experiment with different image sizes to observe the impact on speedup and efficiency.
- Discuss the trade-offs between the number of threads and the overhead of thread management.
- Students can use the time module to measure execution time accurately.

### Evaluation Criteria

- Correctness of the sequential and parallel image processing implementations.
- Efficient utilization of thread-shared memory for parallel image processing.
- Analysis of speedup and efficiency achieved using multiple threads.
- Discussion of memory sharing challenges and proposed solutions or optimizations.

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