import pathlib
import os
from threading import Thread, Lock
import time

def read_file_content(path):
    """Open a file and return the file content.

    Args:
        path (str): Path to the file.

    Returns:
        str: File content or None if file can't be read.
    """

    file = pathlib.Path(path)

    if not file.exists():
        print(f"El archivo {path} no existe.")
        return None

    if file.suffix not in ('.txt', '.csv', '.log'):
        print(f"Formato de archivo no soportado: {path}")
        return None

    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except UnicodeDecodeError:
        print(f"No se pudo leer el archivo {path} debido a un problema de codificación.")
        return None

def word_counter(lines, word):
    """Counts the number of times a word appears in a list of lines.

    Args:
        lines (list): A list of lines.
        word (str): The word to count.

    Returns:
        int: The number of times the word appears in the list of lines.
    """

    count = 0
    word = word.lower()

    for line in lines:
        for line_word in line.split():
            if line_word.lower() == word:
                count += 1

    return count

def parallel_worker(lines, word, lock, total_count):
    """Counts the number of times a word appears in a list of lines and updates the total count.

    Args:
        lines (list): A list of lines.
        word (str): The word to count.
        lock (Lock): A threading lock to synchronize access to shared resources.
        total_count (list): A list containing a single element to hold the total count.
    """
    count = word_counter(lines, word)
    
    with lock:
        total_count[0] += count

def parallel_word_counter(path, word):
    """Divides the work equally and launches threads based on the number of cores.

    Args:
        word (str): The word to count.
        path (str): The path to the file.

    Returns:
        int: The number of times the word appears in the file.
    """ 
    cores = os.cpu_count()
    content = read_file_content(path)

    if content is None:
        print(f"No se pudo contar la palabra {word} en el archivo {path}.")
        return None
    
    with open(path, 'r') as f:
        lines = f.readlines()
        num_lines = len(lines)

        chunk_size = num_lines // cores
        range_start = 0
        range_end = num_lines - 1

        threads = []
        lock = Lock()
        total_count = [0]  

        for i in range(cores):
            start = range_start + i * chunk_size
            end = start + chunk_size

            if i == cores - 1:
                end = range_end + 1

            thread = Thread(target=parallel_worker, args=(lines[start:end], word, lock, total_count))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return total_count[0]


if __name__ == '__main__':
    path = 'registros.txt'
    word = 'python'

    # Serial execution
    with open(path, 'r') as f:
        lines = f.readlines()

    start_time = time.time()
    serial_times_word_appear = word_counter(lines, word)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Numero de veces que aparece la palabra '{word}' en el archivo {path}: {serial_times_word_appear}")
    print(f"Tiempo de ejecución en serie: {elapsed_time} segundos.")

    # Parallel execution
    start_time = time.time()
    parallel_times_word_appear = parallel_word_counter(path, word)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Numero de veces que aparece la palabra '{word}' en el archivo {path}: {parallel_times_word_appear}")
    print(f"Tiempo de ejecución en paralelo: {elapsed_time} segundos.")