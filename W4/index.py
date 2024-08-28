import subprocess
import platform
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from threading import Thread, Lock
import time
import os


NUM_CORES = os.cpu_count()
SUM = 0
MUTEX = Lock()


def square_addition(range_start, range_end):
    """
    Calculates the sum of the squares of numbers in a given range.
    
    Args:
        range_start (int): The starting number of the range (inclusive).
        range_end (int): The ending number of the range (inclusive).

    Returns:
        int: The sum of the squares of the numbers in the range.
    """
    sum = 0
    for i in range(range_start, range_end + 1):
        sum += i ** 2
    return sum

def parallel_worker(range_start, range_end):
    """
    divides the job into sub-branches to be processed in parallel by multiple threads.

    Args:
        range_start (int): The starting number of the range (inclusive).
        range_end (int): The ending number of the range (inclusive).
    """
    partial_sum = square_addition(range_start, range_end)
    
    with MUTEX:
        global SUM
        SUM += partial_sum


def thread_square_addition(range_start, range_end, num_threads):
    """
    Calculates the sum of the squares of numbers in a given range using multiple threads.
    
    Args:
        start (int): The starting number of the range (inclusive).
        end (int): The ending number of the range (inclusive).
        num_threads (int): The number of threads to use for the calculation.

    Returns:
        int: The sum of the squares of the numbers in the range.
    """
    global SUM
    SUM = 0

    total_range = range_end - range_start + 1
    chunk_size = total_range // num_threads

    threads = []

    for i in range(num_threads):
        
        start = range_start + i * chunk_size
        end = start + chunk_size - 1
        
        if i == num_threads - 1:
            end = range_end

        thread = Thread(target=parallel_worker, args=(start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return SUM


def test_square_addition():
    """
    Runs tests on various ranges of numbers to calculate the sum of squares
    using both the sequential function and the parallel function with multiple threads.

    Measures and displays the execution time for each range and each method.
    """
    # ? Uncomment the ranges you want to test
    ranges = [
        (1, 1_000_000),
        (1, 5_000_000),
        (1, 10_000_000),
        (1, 20_000_000),
        # (1, 50_000_000),
        # (1, 100_000_000),
        # (1, 200_000_000),
        # (1, 300_000_000),
        # (1, 400_000_000),
        # (1, 500_000_000),
    ]

    num_threads_list = [
        NUM_CORES // 8,
        NUM_CORES // 4,
        NUM_CORES // 2,
        NUM_CORES // 1,
        NUM_CORES * 2,
    ]


    results = []

    for begin, end in ranges:
        
        # ? Serial method test
        start_time = time.time()
        results_serial = square_addition(begin, end)
        end_time = time.time()
        serial_execution_time = end_time - start_time
        
        results.append({
            'Range': f"{begin} - {end}",
            'Method': 'Serial',
            'Threads': 1,
            'Result': results_serial,
            'Time': serial_execution_time
        })
        
        # ? Parallel method test
        for num_threads in num_threads_list:
            start_time = time.time()
            parallel_result = thread_square_addition(begin, end, num_threads)
            end_time = time.time()
            parallel_execution_time = end_time - start_time
            
            results.append({
                'Range': f"{begin} - {end}",
                'Method': 'Parallel',
                'Threads': num_threads,
                'Result': parallel_result,
                'Time': parallel_execution_time
            })

    return results


def generate_report():
    
    date = datetime.now().strftime("%Y-%m-%d")

    results = test_square_addition()

    df = pd.DataFrame(results)

    table = df.to_markdown(index=False)

    plt.figure(figsize=(8, 4))
    for key, grp in df.groupby(['Range', 'Method']):
        plt.plot(grp['Threads'], grp['Time'], label=f"{key}", marker='o')
    plt.yscale('log')
    plt.xlabel("Number of Threads")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Comparison of execution times")
    plt.legend()
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    plt.savefig("grafica1.png")
    
    qmd_content = f"""
---
title: "Parallel Sum of Squares"
author: "Emmanuel Silva Diaz"
date: {date}
format: pdf
jupyter: python3
---

# Introduction

In this challenge, the concept of parallelism in computation will be explored by implementing a parallel algorithm to compute the sum of squares of 
numbers within a given range. The objective is to compare the efficiency between a sequential and a parallel implementation using multiple threads 
with synchronization via mutexes.

# Objective

The objective of this study is to analyze the performance of sequential versus parallel methods in computing the sum of squares over various ranges.

# Metodology

The following methodology was used to carry out this analysis:

- **square_addition()**: Calculates the sum of the squares of numbers in a given range.
- **parallel_worker**: divides the job into sub-branches to be processed in parallel by multiple threads.
- **thread_square_addition()**: Calculates the sum of the squares of numbers in a given range using multiple threads.
- **test_square_addition()**: Runs tests on various ranges of numbers to calculate the sum of squares using both the sequential function and the parallel function with multiple threads.

# Results

![Execution time graph](grafica1.png)

{table}

# Analysis and Discussion

1.) **Mutext usage**.

The use of a mutex ensures that only one thread at a time can modify the SUM variable. This guarantees that all partial results are summed correctly, 
preserving data integrity and ensuring that the final result is accurate. correctly, preserving the integrity of the data and ensuring that the final 
result is accurate. However, the use of locks may introduce some latency, as threads must wait their turn to access the critical section.

2.) **Execution time comparison**.

- **Longer Parallel Time**: In the tests performed, it is observed that parallel execution times are longer than sequential execution times. 
This may seem counterintuitive, since parallelism is expected to speed up processing. However, this result may be due to several factors:
    - **Thread creation and management overhead**: Creation, synchronization and termination of threads introduces significant overhead. 
    In tasks where the workload is relatively small, this overhead can outweigh the potential gains from parallelism.
    - **Mutex Contention**: The need to use a mutex to protect the SUM variable introduces additional waits, as threads must wait to access the 
    critical section. This can reduce the efficiency of parallelism, especially if threads spend a lot of time waiting.

# Conclusion

The analysis reveals that the use of parallelism in Python, despite its potential to improve computationally intensive performance, does not always 
translate into greater efficiency. One possible theory is that the Global Interpreter Lock (GIL) in Python could be limiting thread performance by 
allowing only one thread to execute Python code at a time. This restriction may exacerbate parallel performance problems, as the need for 
synchronization via locks to avoid race conditions introduces an additional cost that may offset the benefits of parallelism.

Although parallelization may be beneficial in contexts where GIL is not a limiting factor, in this specific case, the synchronization required to prevent race conditions and the constraints imposed by GIL in Python likely contributed to lower than expected performance.
   
   """
    with open("informe.qmd", "w", encoding="utf-8") as file:
        file.write(qmd_content)

    subprocess.run(["quarto", "render", "informe.qmd", "--to", "pdf"])

    pdf_file = "informe.pdf"
    if platform.system() == "Darwin":
        subprocess.run(["open", pdf_file])
    elif platform.system() == "Windows":
        subprocess.run(["start", pdf_file], shell=True)
    else:
        subprocess.run(["xdg-open", pdf_file])

if __name__ == "__main__":

    generate_report()
