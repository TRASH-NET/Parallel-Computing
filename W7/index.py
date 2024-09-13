from datetime import datetime
import os
import platform
import subprocess
import threading
import queue
import numpy as np
import time
import matplotlib.pyplot as plt

#? Variables globales
GLOBAL_QUEUE = queue.Queue(maxsize=10) #* global queue, used to store chunks of the matrix
condition = threading.Condition() #* condition variable, indicates when the queue is full or empty
stop_event = threading.Event() #* stop event, used to notify consumers to stop

result = None #* global variable to store the results of the matrix multiplication

producer_wait_times = [] #* list to store producer wait times
consumer_wait_times = [] #* list to store consumer wait times

fill_count = 0 #* counter to keep track of how many times the queue was full
empty_count = 0 #* counter to keep track of how many times the queue was empty

max_threads = os.cpu_count()
min_threads = 1

def serial_multiply_matrices(A, B, chunk_size):
    """
    Divides the matrix A into chunks and multiplies each chunk by matrix B in serial.

    Args:
        A (numpy.ndarray): The first matrix.
        B (numpy.ndarray): The second matrix.
        chunk_size (int): The size of each chunk to process.

    Returns:
        numpy.ndarray: The result of multiplying matrices A and B.
    """
    print("Multiplicación en serie...")

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


def split_matrix(A, chunk_size):
    """
    Divide the matrix A into chunks of size chunk_size.
    """
    size = A.shape[0]
    chunks = []
    for start_row in range(0, size, chunk_size):
        end_row = min(start_row + chunk_size, size)
        subA = A[start_row:end_row, :]
        chunks.append((subA, start_row))
    
    return chunks

def producer(A, num_threads):
    """
    Producer adds the chunks of matrix A to the global queue.
    """
    global GLOBAL_QUEUE, fill_count

    size = A.shape[0]
    chunk_size = size // num_threads
    chunks = split_matrix(A, chunk_size)

    for subA, start_row in chunks:
        with condition:
            while GLOBAL_QUEUE.full():
                start_time = time.time()
                print("Cola llena, productor esperando...")
                fill_count += 1
                condition.wait()
                producer_wait_times.append(time.time() - start_time)
            GLOBAL_QUEUE.put((subA, start_row))
            print(f"Se ha agregado el chunk de filas: {start_row} a {start_row + subA.shape[0] - 1} a la cola")
            condition.notify()
    stop_event.set()
    with condition:
        condition.notify_all()

def consumer(B):
    """
    Consumer takes chunks from the global queue and multiplies them by matrix B.
    """
    global GLOBAL_QUEUE, result, empty_count
    
    while True:
        with condition:
            while GLOBAL_QUEUE.empty():
                
                if stop_event.is_set():
                    return
                
                start_time = time.time()
                print("Cola vacía, consumidor esperando...")
                empty_count += 1
                condition.wait()
                consumer_wait_times.append(time.time() - start_time)

            subA, row_start = GLOBAL_QUEUE.get()

            print(f"Consumidor procesa chunk de filas {row_start} a {row_start + subA.shape[0] - 1}")
            result_chunk = np.dot(subA, B)

            result[row_start:row_start + subA.shape[0], :] = result_chunk
            condition.notify()

def test():
    """
    Measures the execution time for parallel matrix multiplication.
    """
    while True:
        try:
            size = int(input("Ingrese el tamaño de la matriz: "))
            if size < 1 or size > 10_000:
                print("Tamaño de matriz inválido. Por favor, ingrese un número entre 1 y 10000.")
            else:
                break
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

    global result

    num_threads = os.cpu_count()
    
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    result = np.zeros((size, size))

    # ? Testing serial matrix multiplication
    start_time = time.time()
    serial_result= serial_multiply_matrices(A, B, size // num_threads)
    end_time = time.time()
    serial_elapsed_time = end_time - start_time

    print("Tiempo en la version serial: ", serial_elapsed_time)

    #? Testing parallel matrix multiplication

    start_time = time.time()
    producer_thread = threading.Thread(target=producer, args=(A, num_threads))
    producer_thread.start()

    consumer_threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=consumer, args=(B,))
        thread.start()
        consumer_threads.append(thread)

    producer_thread.join()
    stop_event.set()

    for thread in consumer_threads:
        thread.join()
    end_time = time.time()
    parallel_elapsed_time = end_time - start_time

    print("Tiempo en la version paralela: ", parallel_elapsed_time)

    print("Speedup: ", serial_elapsed_time / parallel_elapsed_time, "X")

    isCorrect = np.allclose(serial_result, result)

    if isCorrect:
        print("El resultado de las operaciones entre las matrices es correcto.")
    else:
        print("El resultado de las operaciones entre las matrices es incorrecto.")

    #? Report execution times
    avg_producer_wait_time = sum(producer_wait_times) / len(producer_wait_times) if producer_wait_times else 0
    avg_consumer_wait_time = sum(consumer_wait_times) / len(consumer_wait_times) if consumer_wait_times else 0

    print(f"Tiempo de ejecución secuencial: {serial_elapsed_time:.4f} segundos")
    print(f"Tiempo de ejecución paralelo: {parallel_elapsed_time:.4f} segundos")
    print(f"Tiempo de espera promedio del productor: {avg_producer_wait_time:.4f} segundos")
    print(f"Tiempo de espera promedio del consumidor: {avg_consumer_wait_time:.4f} segundos")
    print(f"Cola llena {fill_count} veces")
    print(f"Cola vacía {empty_count} veces")

    result = [
        A,
        B,
        size,
        serial_elapsed_time,
        parallel_elapsed_time,
        serial_elapsed_time / parallel_elapsed_time,
        avg_producer_wait_time,
        avg_consumer_wait_time,
        fill_count,
        empty_count,
        isCorrect
    ]

    return result


def generate_report():

    global result
    date = datetime.now().strftime("%Y-%m-%d")
    
    test_results = test()
    A, B, size, serial_time, parallel_time, speedup, producer_wait_time, consumer_wait_time, fill_count, empty_count, isCorrect = test_results

    np.set_printoptions(precision=3, suppress=True, linewidth=150)

    fig, ax1 = plt.subplots()
    ax1.bar(['Serial', 'Parallel'], [serial_time, parallel_time], color=['blue', 'green'])
    ax1.set_title('Execution Time: Serial vs Parallel')
    ax1.set_ylabel('Time (seconds)')
    plt.savefig('speedup_comparison.png')

    qmd_content = f"""
---
title: "Producer-Consumer Problem with Condition Variables"
author: "Emmanuel Silva Diaz"
date: {date}
format: pdf
jupyter: python3
---

# Introduction

This report describes the implementation of a matrix multiplication algorithm using the producer-consumer pattern in a multithreaded environment. 
multithreaded environment. The main objective is to divide the multiplication job into smaller parts (chunks) that are processed in parallel, 
using threads to maximize efficiency and reduce computation time. Producer threads are implemented, in charge of dividing a matrix “A” into 
subMatrices and distributing them in parallel. into subMatrices and distribute them to a shared queue, and consumer threads, which multiply 
each of the subMatrices with a matrix B, and insert the partial results into a global matrix. the partial results into a resulting global matrix.


# Objectives

- Implementing a parallel solution for matrix multiplication using a producer-consumer pattern.
- Measuring the performance of the parallel solution compared to a sequential version.
- Analyze producer and consumer waiting times, queue filling and synchronization between threads.
- Verify queue fill and empty frequency to measure producer and consumer load.
- Verification of results to ensure that the parallel operation generates correct results.


# Description of the system

1. **Producer**: The producer is responsible for splitting the A array into chunks and placing them in the shared queue for consumers to process. 
It is designed so that, in case the queue is full, it waits until space is available.

2. **Consumer**: The consumer extracts the chunks from the queue, multiplies each by the B matrix, and stores the partial result in a global result matrix. 
global result matrix.

# Methodology

For the implementation of this study the following functions were carried out:

- **serial_multiply_matrices()**: This function divides matrix A into chunks and multiplies each chunk by matrix B serially.
- **split_matrix(A, chunk_size)**: This function splits matrix A into chunks of specified size and returns them as a list of submatrices.
- producer(A, num_threads)**: This function takes care of adding chunks of matrix A to the shared queue using the split_matrix() function 
to split the matrix.
- consumer(B)**: This function extracts chunks from the shared queue, multiplies each one by the matrix B and stores the result in the global 
result matrix. of results.
- **test()**: This function measures the execution time of parallel and serial matrix multiplication, and reports the producer and consumer 
wait times, as well as queue fill and empty.

# Test Results:

The test was executed with matrix **A** of size **{size} x {size}** and matrix **B** of size **{size} x {size}** to compare the 
processing time between serial and parallel multiplication.

- **Matrix A**:

{A}

- **Matrix B**:

{B}

- To verify the result of the operations, the result of the serial multiplication was compared with the result of the parallel 
multiplication using the **np.allclose(**) function. The result was (correct = true or incorrect = false): **{isCorrect}**

The test results show the following data:

| **Matrix Size** | **Serial** | **Parallel** | **Avg. Producer** | **Avg. Consume**r | **Queue Full** | **Queue Empty** | **Speedup** |
|-------------|--------|----------|---------------|---------------|------------|-------------|---------|
""".format(test_results)

    qmd_content += f"| {size} | {serial_time:.4f} | {parallel_time:.4f} | {producer_wait_time:.4f} | {consumer_wait_time:.4f} | {fill_count} | {empty_count} | {speedup:.2f}x |\n"
    
    qmd_content += """

# Performance graph

![Speedup Comparison](speedup_comparison.png)


# Analysis and Discussion

During the implementation of matrix multiplication using the threaded producer-consumer problem, several key points emerged 
related to system efficiency, synchronization between threads, and proper shared queue management. The most important aspects 
are discussed in detail below:

1. **Single Producing Thread and Multiple Consuming Threads**:
A notable aspect of the implementation is that only one producing thread was necessary, while multiple consuming threads 
were used. This is because the produce operation (chunks from matrix A) is relatively fast compared to the consume operation 
(multiply chunks with matrix B). Therefore, the producer quickly fills the queue with chunks, while consumers take more time 
to process them, justifying the need for several consumer threads.

2. **Blocking with Condition Variables:
The use of a condition variable (condition) was critical to ensure proper synchronization between the producing and consumers. In 
a multithreaded environment, access to shared resources such as the queue must be carefully managed to avoid race conditions or data 
corruption. The mechanisms implemented are detailed below:
    - Protection with Locks: The condition variable is used in conjunction with a lock, which ensures that only one thread at a time can 
    modify or access the shared queue. When the producer attempts to add a new chunk to the queue and the queue is full, or when a consumer 
    attempts to extract a chunk from an empty queue, both must wait for the queue to have space or work available.
        - Blocking on the Producer**: If the queue is full, the producer enters an active wait with condition.wait(), preventing more items 
        from being added to the queue until the queue is full. If the queue is full, the producer enters an active wait with condition.wait(), 
        preventing more items from being added to the queue until a consumer removes an item.
        - Consumer Lockout**: If the queue is empty, consumers also enter a wait with condition.wait(), until the producer adds a new chunk. 
        producer adds a new chunk.
    - **Avoid Data Corruption**: The condition variable ensures that when the producer or consumer accesses the queue, they do so in an orderly 
    fashion. By using explicit locks before adding or removing items from the queue, data corruption that could occur if multiple threads attempted 
    to read or modify the queue simultaneously without synchronization is avoided.
    - Notifications and Synchronization**: The producer uses condition.notify() to notify consumers that they can pull data. Similarly, when a 
    consumer pulls a chunk, it notifies the producer with condition.notify() that it can add more data to the queue. This notification mechanism 
    ensures that threads are always synchronized, preventing the producer from working when the queue is full. producer from working when the queue 
    is full or consumers from trying to work when the queue is empty.

3. **Use of the 'stop_event'** Event: The stop_event event plays an important role in the controlled termination of the consuming threads.
    - **Stop Consumers**: When the producer has finished processing all chunks, it calls stop_event.set() to signal to the consumers that no more 
    work will be available. If a consumer attempts to extract a chunk from an empty queue and detects that the stop_event event has been triggered, 
    it terminates its execution safely.
    - Avoiding Unnecessary Waiting**: Without the use of stop_event, consumers could continue to wait indefinitely if the queue is empty and the 
    producer has finished its work. The use of this event provides a clear mechanism to stop all consumer threads in a controlled manner, avoiding 
    deadlocks or infinite loops.


# Conclusions

The implementation of the producer-consumer system for matrix multiplication achieved effective synchronization between the producer and 
the consumers through the use of condition variables, the shared queue and the stop event. consumers through the use of condition variables, 
the shared queue and the stop event. The condition variable was used to coordinate queue access, avoiding race conditions and ensuring that 
consumers wait when the queue is empty and that the producer waits when the queue is full. producer waits when the queue is full. This 
prevented data corruption and ensured proper interaction between threads, allowing for efficient parallel execution.

The stop event (stop_event) was instrumental in telling consumers when to finish their work once the producer completed all tasks, which 
prevented threads from waiting indefinitely.

An important point that was observed was that only one producer thread was necessary to keep up with multiple consumer threads. 
This is because the producing operation (splitting the matrix into chunks) is much faster compared to the consuming operation 
(multiplying sub-matrices), which caused the producer to manage to keep the queue full several times without the need for support from more threads.

However, an important area of improvement would be the implementation of a dynamic adjustment of the number of consuming threads. 
Although it was not applied in this implementation, adjusting the number of threads based on the queue load could further improve 
efficiency. For example, increasing the number of consumers when the queue is consistently full and reducing it when the queue is empty 
would help optimize the load balance and avoid bottlenecks in scenarios where the consumers are slower than the producer.
   
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