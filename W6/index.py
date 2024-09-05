import numpy as np
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import os

def multiply_matrices(A, B):
    """
    Multiplies two matrices using the numpy library.

    Args:
        A (numpy.ndarray): The first matrix.
        B (numpy.ndarray): The second matrix.

    Returns:
        numpy.ndarray: The result of multiplying matrices A and B.
    """
    
    return np.dot(A, B)


def parallel_worker(A, B, result, row_start, row_end):
    """Multiplies rows of matrix A with matrix B and stores results in 'result'."""
    for i in range(row_start, row_end):
        result[i, :] = multiply_matrices(A[i, :], B)

def parallel_matrix_multiply(A, B, num_threads):
    """Performs parallel matrix multiplication using threads."""
    
    size = A.shape[0]
    result = np.zeros((size, size))
    chunk_size = size // num_threads

    # Create and start threads
    threads = []
    for i in range(num_threads):
        row_start = i * chunk_size
        row_end = (i + 1) * chunk_size if i != num_threads - 1 else size
        thread = Thread(target=parallel_worker, args=(A, B, result, row_start, row_end))
        threads.append(thread)
        thread.start()

    # Wait for threads to finish
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

    #? Parallel multiplication
    parallel_start_time = time.time()
    result_parallel = parallel_matrix_multiply(A, B, num_threads)
    parallel_end_time = time.time()
    
    parallel_time = parallel_end_time - parallel_start_time
    print(f"Multiplicación en paralelo completada en {parallel_time:.4f} segundos.")

    #? Check correctness
    if np.allclose(result_serial, result_parallel):
        print("Los resultados son correctos.")
    else:
        print("Los resultados son incorrectos.")

    #? Speedup analysis
    speedup = serial_time / parallel_time
    print(speedup, serial_time, parallel_time)
    print(f"Speedup con {num_threads} hilos: {speedup:.2f}x")

if __name__ == "__main__":
    
    test()