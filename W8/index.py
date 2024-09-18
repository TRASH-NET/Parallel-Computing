import threading
import random
import time
import numpy as np
import re

class Worker(threading.Thread):
    def __init__(self, barrier):
        super().__init__()
        self.barrier = barrier

    def run(self):
        raise NotImplementedError("Subclasses should implement this!")

    def wait_at_barrier(self):
        self.barrier.wait()

class WorkerSum(Worker):
    def __init__(self, numbers, barrier):
        super().__init__(barrier)
        self.numbers = numbers

    def run(self):
        print("Trabajador 1: Comenzando a calcular la suma.")
        
        start_time = time.time()
        
        total_sum = sum(self.numbers)
        
        end_time = time.time()
        
        duration = end_time - start_time
        
        print(f"Trabajador 1: Suma calculada = {total_sum}")
        print(f"Trabajador 1: Tiempo total en realizar la tarea = {duration:.4f} segundos")
        
        self.wait_at_barrier()
        print("Trabajador 1: Espera en la barrera finalizada.")

class WorkerMatrixMultiplication(Worker):
    def __init__(self, size, barrier):
        super().__init__(barrier)
        self.size = size

    def run(self):
        print("Trabajador 2: Comenzando la multiplicación de matrices.")
        
        matrix_a = np.random.randint(1, 10, size=(self.size, self.size))
        matrix_b = np.random.randint(1, 10, size=(self.size, self.size))
        
        start_time = time.time()
        
        result_matrix = np.dot(matrix_a, matrix_b)
        
        end_time = time.time()
        
        duration = end_time - start_time
        
        print(f"Trabajador 2: Multiplicación de matrices realizada.")
        print(f"Trabajador 2: Tiempo total en realizar la tarea = {duration:.4f} segundos")
        
        self.wait_at_barrier()
        print("Trabajador 2: Espera en la barrera finalizada.")

class WorkerPatternSearch(Worker):
    def __init__(self, filename, pattern, barrier):
        super().__init__(barrier)
        self.filename = filename
        self.pattern = pattern

    def run(self):
        print("Trabajador 3: Comenzando la búsqueda del patrón.")
        
        start_time = time.time()
        
        matches = 0
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    if re.search(self.pattern, line):
                        matches += 1
        
        except FileNotFoundError:
            print(f"Trabajador 3: El archivo {self.filename} no se encontró.")
            matches = 0
        
        end_time = time.time()
        
        duration = end_time - start_time
        
        print(f"Trabajador 3: Se encontraron {matches} coincidencias.")
        print(f"Trabajador 3: Tiempo total en realizar la tarea = {duration:.4f} segundos")
        
        self.wait_at_barrier()
        print("Trabajador 3: Espera en la barrera finalizada.")

class WorkerRandomWalk(Worker):
    def __init__(self, steps, barrier):
        super().__init__(barrier)
        self.steps = steps

    def run(self):
        print("Trabajador 4: Comenzando el paseo aleatorio.")
        
        start_time = time.time()
        
        position = [0, 0]
        for _ in range(self.steps):
            move = random.choice(['N', 'S', 'E', 'W'])
            if move == 'N':
                position[1] += 1
            elif move == 'S':
                position[1] -= 1
            elif move == 'E':
                position[0] += 1
            elif move == 'W':
                position[0] -= 1
        
        end_time = time.time()
        
        duration = end_time - start_time
        
        print(f"Trabajador 4: Paseo aleatorio terminado. Posición final = {position}")
        print(f"Trabajador 4: Tiempo total en realizar la tarea = {duration:.4f} segundos")
        
        self.wait_at_barrier()
        print("Trabajador 4: Espera en la barrera finalizada.")

class WorkerMaxValue(Worker):
    def __init__(self, size, barrier):
        super().__init__(barrier)
        self.size = size

    def run(self):
        print("Trabajador 5: Comenzando el cálculo del valor máximo.")
        
        start_time = time.time()
        
        array = [random.randint(1, 1000) for _ in range(self.size)]
        max_value = max(array)
        
        end_time = time.time()
        
        duration = end_time - start_time
        
        print(f"Trabajador 5: Valor máximo encontrado = {max_value}")
        print(f"Trabajador 5: Tiempo total en realizar la tarea = {duration:.4f} segundos")
        
        self.wait_at_barrier()
        print("Trabajador 5: Espera en la barrera finalizada.")

def coordinator():
    list_size = int(input("Ingrese el tamaño de la lista: "))
    matrix_size = int(input("Ingrese el tamaño de las matrices (por ejemplo, 1000 para matrices 1000x1000): "))
    
    while True:
        if list_size <= 0 or list_size > 100_000_000:
            print("Por favor, ingrese un tamaño de lista mayor que 0 y menor que 100.000.000")
            list_size = int(input("Ingrese el tamaño de la lista: "))
        elif matrix_size <= 0 or matrix_size > 50_000:
            print("Por favor, ingrese un tamaño de matriz mayor que 0 y menor que 50.000")
            matrix_size = int(input("Ingrese el tamaño de las matrices: "))
        else:
            break

    filename = input("Ingrese el nombre del archivo de texto para las búsquedas: ")
    pattern = input("Ingrese el patrón a buscar en el archivo: ")

    large_list = [random.randint(1, 100) for _ in range(list_size)]
    
    num_workers = 5
    barrier = threading.Barrier(num_workers + 1)
    
    workers = [
        WorkerSum(large_list, barrier),
        WorkerMatrixMultiplication(matrix_size, barrier),
        WorkerPatternSearch(filename, pattern, barrier),
        WorkerRandomWalk(100_000, barrier),
        WorkerMaxValue(100_000, barrier)
    ]
    
    for worker in workers:
        worker.start()
    
    barrier.wait()
    
    for worker in workers:
        worker.join()
    
    print("Todos los trabajadores han terminado.")

if __name__ == "__main__":
    coordinator()
