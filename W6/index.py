import numpy as np
import time
from datetime import datetime
from threading import Thread
import os
import subprocess
import platform
import pandas as pd

def multiply_matrices(A, B):
    """
    Divides the matrix A into chunks and multiplies each chunk by matrix B in serial.

    Args:
        A (numpy.ndarray): The first matrix.
        B (numpy.ndarray): The second matrix.

    Returns:
        numpy.ndarray: The result of multiplying matrices A and B.
    """
    num_chunks = os.cpu_count()
    size = A.shape[0]
    result = np.zeros((size, B.shape[1]))
    chunk_size = size // num_chunks
    
    for i in range(num_chunks):
        row_start = i * chunk_size
        if i != num_chunks - 1:
            row_end = (i + 1) * chunk_size
        else:
            row_end = size
        
        subA = A[row_start:row_end, :]
        
        for j in range(subA.shape[0]):
            result[row_start + j, :] = np.dot(subA[j, :], B)

    return result


def parallel_worker(subA, B, result, row_start):
    """
    Multiplies rows of matrix A with matrix B and stores the results in the corresponding
    part of the 'result' matrix.
    
    Args:
        subA (numpy.ndarray): A subset of matrix A.
        B (numpy.ndarray): Matrix B.
        result (numpy.ndarray): The matrix where the results are stored.
        row_start (int): The row index where the results should be stored.
    
    """
    sub_result = np.dot(subA, B)
    
    #? Store the results in the corresponding part of the 'result' matrix
    #? Example: If sub_result.shape = (2, 10) and row_start = 0, then the results should be stored in result[0:2, :], it means from row 0 to row 1. and all columns.
    result[row_start:row_start + sub_result.shape[0], :] = sub_result



def parallel_matrix_without_join(A, B, num_threads):
    """
    Divide la matriz A en submatrices y multiplica cada submatriz por la matriz B en paralelo sin usar join.

    Args:
        A (numpy.ndarray): The first matrix.
        B (numpy.ndarray): The second matrix.
        num_threads (int): The number of threads to use.

    Returns:
        numpy.ndarray: The result of multiplying matrices A and B.
    """
    
    size = A.shape[0]
    result = np.zeros((size, size))
    chunk_size = size // num_threads

    threads = []
    for i in range(num_threads):
        
        row_start = i * chunk_size
        
        #? The last thread should multiply the remaining rows
        if i != num_threads - 1:
            row_end = (i + 1) * chunk_size
        else:
            row_end = size
        
        subA = A[row_start:row_end, :]

        thread = Thread(target=parallel_worker, args=(subA, B, result, row_start))
        threads.append(thread)
        thread.start()

    return result

def parallel_matrix_multiply(A, B, num_threads):
    """
    Release multiples threads to multiply rows of matrix A with matrix B and store the results in "results matrix".

    Args:
        A (numpy.ndarray): The first matrix.
        B (numpy.ndarray): The second matrix.
        num_threads (int): The number of threads to use.

    Returns:
        numpy.ndarray: The result of multiplying matrices A and B.
    """
    
    size = A.shape[0]
    result = np.zeros((size, size))
    chunk_size = size // num_threads

    threads = []
    for i in range(num_threads):
        
        row_start = i * chunk_size
        
        #? The last thread should multiply the remaining rows
        if i != num_threads - 1:
            row_end = (i + 1) * chunk_size
        else:
            row_end = size
        
        subA = A[row_start:row_end, :]

        thread = Thread(target=parallel_worker, args=(subA, B, result, row_start))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        
    return result

def test():

    num_threads = os.cpu_count()

    while True:
        try:
            size = int(input("Ingrese el tamaño de la matriz: "))
            if size < 1 or size > 10000:
                print("Tamaño de matriz inválido. Por favor, ingrese un número entre 1 y 10000.")
            else:
                break
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

    A = np.random.rand(size, size)
    B = np.random.rand(size, size)

    #? Serial multiplication
    serial_start_time = time.time()
    result_serial = multiply_matrices(A,B)
    serial_end_time = time.time()
    
    serial_time = serial_end_time - serial_start_time
    print(f"Multiplicación en serie completada en {serial_time:.4f} segundos.")

    #? Parallel multiplication with join
    parallel_start_time = time.time()
    result_parallel = parallel_matrix_multiply(A, B, num_threads)
    parallel_end_time = time.time()
    
    parallel_time = parallel_end_time - parallel_start_time
    print(f"Multiplicación en paralelo usando join completada en {parallel_time:.4f} segundos.")

     #? Parallel multiplication without join
    parallel_without_join_start_time = time.time()
    result_parallel_without_join = parallel_matrix_without_join(A, B, num_threads)
    parallel_without_join_end_time = time.time()
    
    parallel_without_join_time = parallel_without_join_end_time - parallel_without_join_start_time
    print(f"Multiplicación en paralelo sin join completada en {parallel_without_join_time:.4f} segundos.")

    #? Check between parallel with join
    is_correct_with_join = np.allclose(result_serial, result_parallel)
    is_correct_without_join = np.allclose(result_serial, result_parallel_without_join)

    #? Speedup analysis
    speedup_with_join = serial_time / parallel_time
    speedup_without_join = serial_time / parallel_without_join_time

    results = {
        "**Matrix Size**": [size],
        "**Number of Threads**": [num_threads],
        "**Serial Time (s)**": [round(serial_time, 3)],
        "**Parallel Time with Join (s)**": [round(parallel_time, 3)],
        "**Parallel Time without Join (s)**": [round(parallel_without_join_time, 3)],
        "**Is Correct with Join**": [str(is_correct_with_join)],
        "**Is Correct without Join**": [str(is_correct_without_join)],
        "**Speedup with Join**": [speedup_with_join],
        "**Speedup without Join**": [speedup_without_join]
    }

    df = pd.DataFrame(results)

    return df


def generate_report():
    
    date = datetime.now().strftime("%Y-%m-%d")

    results = test()
    
    qmd_content = f"""
---
title: "Parallel Matrix Multiplication with Task Joins"
author: "Emmanuel Silva Diaz"
date: {date}
format: pdf
jupyter: python3
---

# Introduction

In this challenge, we will implement parallel matrix multiplication using task joins. Matrix multiplication is a computationally 
intensive task, and by using multiple threads, we can explore how to speed up the computation. Students will need to create threads, 
perform matrix multiplication in parallel, and use the join() method to wait for all threads to complete their tasks.

# Objective

The goal of this challenge is to implement a parallelized version of matrix multiplication using threads in Python and to 
explore how to improve the performance of the operation by using multiple threads and synchronization with and without 'join()' method.

# Metodology

The following methodology was used to carry out this analysis:

- **multiply_matrices()**: It uses the numpy library to multiply two matrices.
- **parallel_worker()**: Multiplies rows of matrix A with matrix B and stores the results in the corresponding part of the 'result' matrix.
- **parallel_matrix_without_join()**: It divides matrix A into submatrices and multiplies each submatrix by matrix B in parallel without using the 'join()' synchronization.
- **parallel_matrix_multiply()**: It divides matrix A into submatrices and multiplies each submatrix by matrix B in parallel using the 'join()' synchronization.
- **test()**: It performs the tests and prints the results.

# Test Results

{results.to_markdown(index=False)}

# Analysis and Discussion

- Performance of Matrix Multiplication: The comparison between serial and parallel matrix multiplication shows significant 
performance improvements with parallelization.  The parallel execution with join() demonstrates a reduction in processing time 
compared to the serial method. Specifically, the observed speedup aligns with the expected benefits of utilizing multiple 
threads to perform computations simultaneously. However, the actual speedup achieved is also dependent on the number of threads 
and the overhead associated with thread management.

- Thread Efficiency: The use of join() ensures that the main thread waits for all worker threads to complete their execution 
before proceeding. This synchronization is crucial to maintain the correctness of the results. Without join(), there is a risk 
of data corruption, as threads may overwrite parts of the result matrix before all computations are complete. This lack of 
synchronization leads to incorrect results, highlighting the importance of proper thread management.

- Impact on Results: The results indicate that parallel matrix multiplication without join() produces incorrect results, as 
verified by the np.allclose() function. This discrepancy underscores the necessity of using join() to ensure that all threads 
have completed their tasks and that results are correctly aggregated into the final matrix.

# Conclusion

While parallel processing offers performance gains, it also introduces overhead from thread 
creation and synchronization. The optimal number of threads should balance the benefits of parallelism against the costs of 
thread management. Excessive threading may lead to diminishing returns, where the overhead negates the advantages of parallel 

   
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