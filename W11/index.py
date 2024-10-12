"""
    Emmanuel Silva Diaz

    Challenge 11: Implementacion de un sistema de productores y consumidores con multiprocesamiento usando colas y pipes

    Objetivos:
        - Crear un proceso principal que administre la creación de productores y consumidores.
        - Crear productores que generen números aleatorios y los envíen a una cola compartida con los consumidores.
        - Crear consumidores que obtengan los números de la cola compartida y realicen la suma de los números.
        - Crear un sistema de pipes para la comunicación entre los procesos y el proceso principal y los consumidores con el proceso principal.
        - Implementar un sistema de parada para los procesos.
        - Implementar un sistema de configuración de experimentos para determinar el número de productores y consumidores a crear.

    Metodologia:
        - para cumplir con los objetivos se llevo a cabo la siguiente metodologia:
            -  Se diseñaron 5 experimentos con diferentes cantidades de números a sumar donde la funcion principal
               llamada test() se encarga de distribuir los numeros antes de enviarlos al productor, con el objetivo
               de que el productor se encarge de generar paquetes de 10 numeros aleatorios y enviarlos mediante una cola
               al consumidor.
            - Se realizo la validacion para cuando no es posible empaquetar los numeros en grupos de 10, se envian los
              numeros restantes al ultimo grupo.
            - Se implemento un sistema de configuracion de experimentos para determinar el numero de productores y consumidores
              a crear, donde se calcula el numero de grupos y el tamaño de los grupos a enviar.
            - El productor envia los paquetes generados al consumidor mediante una cola y se tambien se envian esos numeros al
              proceso principal mediante un pipe.
            - El consumidor recibe los paquetes de numeros de la cola y realiza la suma de los numeros, luego envia el resultado
              al proceso principal mediante un pipe.
            - Se implemento un sistema de parada para los procesos, donde se utiliza un evento para detener los procesos cuando
              se ha completado la tarea.
            - Se implemento una simulacion de trabajo añadiendo time.sleep() en los procesos para simular la carga de trabajo.
            - Se valido realizo una comparacion entre los resultados de la suma de los productores y consumidores para verificar
              la integradad de los datos mediante el envio de mensajes a traves de los pipes.
            - Se utilizo un timeout en el get() de la cola para evitar que el proceso se quede esperando indefinidamente.

"""


import multiprocessing
import random
import time
import ast
from colorama import Fore, init

init(autoreset=True)

def producer(queue, pipe, producer_id, group_size, remaining, stop_event):
    produced_numbers = []
    for _ in range(group_size):
        num = random.randint(1, 100)
        produced_numbers.append(num)
        time.sleep(random.uniform(0.1, 0.5))
    if remaining > 0:
        for _ in range(remaining):
            num = random.randint(1, 100)
            produced_numbers.append(num)
            time.sleep(random.uniform(0.1, 0.5))

    queue.put(produced_numbers)
    pipe.send(f"Producer {producer_id} produced: {produced_numbers}")
    pipe.send(f"Producer {producer_id} finished")
    stop_event.set()

def consumer(queue, pipe, consumer_id, stop_event):
    while True:
        try:
            numbers = queue.get(timeout=1)
            total_sum = sum(numbers)
            pipe.send(f"Consumer {consumer_id} consumed: {numbers}, Total Sum: {total_sum}")
            time.sleep(random.uniform(0.1, 0.5))
        except Exception:
            if stop_event.is_set():
                break
    pipe.send(f"Consumer {consumer_id} finished")

def test(group_size, remaining, num_producers, num_consumers):
    shared_queue = multiprocessing.Queue()
    stop_event = multiprocessing.Event()

    producer_sum = 0
    consumer_sum = 0

    producer_pipes = []
    consumer_pipes = []

    for _ in range(num_producers + num_consumers):
        producer_conn, consumer_conn = multiprocessing.Pipe()
        producer_pipes.append(producer_conn)
        consumer_pipes.append(consumer_conn)

    producers = []
    for i in range(num_producers):
        if i == num_producers - 1 and remaining > 0:
            p = multiprocessing.Process(target=producer, args=(shared_queue, consumer_pipes[i], i + 1, group_size, remaining, stop_event))
            producers.append(p)
            p.start()
        else:
            p = multiprocessing.Process(target=producer, args=(shared_queue, consumer_pipes[i], i + 1, group_size, 0, stop_event))
            producers.append(p)
            p.start()

    consumers = []
    for i in range(num_consumers):
        c = multiprocessing.Process(target=consumer, args=(shared_queue, consumer_pipes[num_producers + i], i + 1, stop_event))
        consumers.append(c)
        c.start()

    finished_processes = 0
    total_processes = num_producers + num_consumers
    try:
        while finished_processes < total_processes:
            for i, pipe in enumerate(producer_pipes):
                if pipe.poll():
                    message = pipe.recv()
                    if "produced" in message:
                        produced_numbers_str = message.split(": ")[1]
                        produced_numbers = ast.literal_eval(produced_numbers_str)
                        if isinstance(produced_numbers, list):
                            producer_sum += sum(produced_numbers)
                    if "consumed" in message:
                        total_sum_str = message.split(", Total Sum: ")[1]
                        consumer_partial_sum = int(total_sum_str)
                        consumer_sum += consumer_partial_sum
                    if "finished" in message:
                        finished_processes += 1
    except KeyboardInterrupt:
        print("Terminating processes...")

    for p in producers:
        p.join()

    for c in consumers:
        c.join()

    for pipe in producer_pipes + consumer_pipes:
        pipe.close()

    return producer_sum, consumer_sum

def configure_experiment(total_numbers, num_cores):
    group_size = 10
    num_groups = total_numbers // group_size
    remaining = total_numbers % group_size

    if num_groups == 0:
        num_groups = 1
        group_size = remaining
        remaining = 0
    if num_groups == 1:
        num_producers = 1
        num_consumers = 1
    elif num_groups <= num_cores // 2:
        num_producers = num_groups
        num_consumers = num_cores - num_producers
    else:
        num_producers = num_cores // 2
        num_consumers = num_cores - num_producers

    return group_size, num_groups, remaining, num_producers, num_consumers

def print_results(results):
    print("\nResults\n\n")
    print("|         Configuración            | Total de Números | Suma de Productores  | Suma de Consumidores  | Coinciden | Tiempo (s) |")
    print("|----------------------------------|------------------|----------------------|-----------------------|-----------|------------|")
    for result in results:
        print(f"| {result[0]:<30}   | {result[1]:<17}| {result[2]:<20} | {result[3]:<21} | {'Sí' if result[4] else 'No':<9} | {result[5]:<10.4f} |")

def run_experiment():
    results = []
    num_cores = multiprocessing.cpu_count()

    test_cases = [2, 10, 15, 135, 543]

    for total_numbers in test_cases:
        if total_numbers > 1:
            group_size, num_groups, remaining, num_producers, num_consumers = configure_experiment(total_numbers, num_cores)
            start_time = time.time()
            print(Fore.CYAN + f"\nEjecutando experimento con {total_numbers} numeros: {num_producers} productores & {num_consumers} consumidores\n")
            if remaining == 0:
                if num_groups == 1:
                    print(Fore.LIGHTBLACK_EX + f"\nSe ha creado {num_groups} grupo de tamaño {group_size}.")
                else:
                    print(Fore.LIGHTBLACK_EX + f"\nSe han creado {num_groups} grupos de tamaño {group_size}.")
            else:
                if num_groups == 1:
                    print(Fore.LIGHTBLACK_EX + f"\nSe ha creado {num_groups} grupo de tamaño {group_size} y los {remaining} números restantes se han agregado al último grupo.")
                else:
                    print(Fore.LIGHTBLACK_EX + f"\nSe han creado {num_groups} grupos de tamaño {group_size} y los {remaining} números restantes se han agregado al último grupo.")
            main_process_sum, consumer_final_sum = test(group_size, remaining, num_producers, num_consumers)
            elapsed_time = time.time() - start_time
            results.append((
                f"{num_producers} productores & {num_consumers} consumidores",
                total_numbers, main_process_sum, consumer_final_sum, main_process_sum == consumer_final_sum, elapsed_time))

    while True:
        total_numbers = int(input(Fore.LIGHTYELLOW_EX + "\n\nEjecute su propio experimento - Ingrese el total de numeros a sumar (mayor que 1): "))
        
        if total_numbers > 1:
            group_size, num_groups, remaining, num_producers, num_consumers = configure_experiment(total_numbers, num_cores)
            start_time = time.time()
            print(Fore.CYAN + f"\nEjecutando experimento con {total_numbers} numeros: {num_producers} productores & {num_consumers} consumidores\n")
            if remaining == 0:
                if num_groups == 1:
                    print(Fore.LIGHTBLACK_EX + f"\nSe ha creado {num_groups} grupo de tamaño {group_size}.")
                else:
                    print(Fore.LIGHTBLACK_EX + f"\nSe han creado {num_groups} grupos de tamaño {group_size}.")
            else:
                if num_groups == 1:
                    print(Fore.LIGHTBLACK_EX + f"\nSe ha creado {num_groups} grupo de tamaño {group_size} y los {remaining} números restantes se han agregado al último grupo.")
                else:
                    print(Fore.LIGHTBLACK_EX + f"\nSe han creado {num_groups} grupos de tamaño {group_size} y los {remaining} números restantes se han agregado al último grupo.")
            main_process_sum, consumer_final_sum = test(group_size, remaining, num_producers, num_consumers)
            elapsed_time = time.time() - start_time
            results.append((
                f"{num_producers} productores & {num_consumers} consumidores",
                total_numbers, main_process_sum, consumer_final_sum, main_process_sum == consumer_final_sum, elapsed_time))
            break
        else:
            print(Fore.RED + "\n\nERROR: El total de números debe ser mayor que 1. Intente nuevamente.")

    print_results(results)

if __name__ == "__main__":
    run_experiment()