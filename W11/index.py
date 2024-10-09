import multiprocessing
import random
import time

def producer(queue, pipe, producer_id, total_numbers, group_size):
    # Asegúrate de que total_numbers sea un múltiplo de group_size
    num_groups = total_numbers // group_size if total_numbers % group_size == 0 else total_numbers // group_size + 1
    for _ in range(num_groups):
        numbers = [random.randint(1, 100) for _ in range(group_size)]
        queue.put(numbers)
        pipe.send(f"Producer {producer_id} produced: {numbers}")
        time.sleep(random.uniform(0.1, 0.5))
    queue.put(None)  # Indica el final de la producción
    pipe.send(f"Producer {producer_id} finished")
    pipe.close()

def consumer(queue, pipe, consumer_id, sum_list):
    while True:
        numbers = queue.get()
        if numbers is None:  # Salir con la señal de fin
            break
        sum_list.extend(numbers)
        total_sum = sum(sum_list)
        pipe.send(f"Consumer {consumer_id} consumed: {numbers}, Total Sum: {total_sum}")
        time.sleep(random.uniform(0.1, 0.5))
    pipe.send(f"Consumer {consumer_id} finished")
    pipe.close()

def test(total_numbers, group_size, num_producers, num_consumers):
    shared_queue = multiprocessing.Queue()
    manager = multiprocessing.Manager()
    sum_list = manager.list()

    main_process_sum = 0

    producer_pipes = []
    consumer_pipes = []

    for _ in range(num_producers + num_consumers):
        producer_conn, consumer_conn = multiprocessing.Pipe()
        producer_pipes.append(producer_conn)
        consumer_pipes.append(consumer_conn)

    producers = []
    for i in range(num_producers):
        p = multiprocessing.Process(target=producer, args=(shared_queue, consumer_pipes[i], i + 1, total_numbers // num_producers, group_size))
        producers.append(p)
        p.start()

    consumers = []
    for i in range(num_consumers):
        c = multiprocessing.Process(target=consumer, args=(shared_queue, consumer_pipes[num_producers + i], i + 1, sum_list))
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
                        produced_numbers = eval(produced_numbers_str)
                        if isinstance(produced_numbers, list):
                            main_process_sum += sum(produced_numbers)
                    if "finished" in message:
                        finished_processes += 1
    except KeyboardInterrupt:
        print("Terminating processes...")

    for p in producers:
        p.join()

    for c in consumers:
        c.join()

    consumer_final_sum = sum(sum_list)
    
    return main_process_sum, consumer_final_sum

def run_experiment(total_numbers, group_size):
    results = []
    num_cores = multiprocessing.cpu_count()

    # Configuración 1: Más productores que consumidores
    num_producers = min(2 * (num_cores // 3), num_cores)
    num_consumers = max(1, num_cores - num_producers)
    start_time = time.time()
    print(f"Running experiment: {num_producers} producers & {num_consumers} consumers")
    main_process_sum, consumer_final_sum = test(total_numbers, group_size, num_producers, num_consumers)
    elapsed_time = time.time() - start_time
    results.append((f"{num_producers} producers & {num_consumers} consumers", total_numbers, main_process_sum, consumer_final_sum, main_process_sum == consumer_final_sum, elapsed_time))

    # Configuración 2: Menos productores que consumidores
    num_consumers = min(2 * (num_cores // 3), num_cores)
    num_producers = max(1, num_cores - num_consumers)
    start_time = time.time()
    print(f"Running experiment: {num_producers} producers & {num_consumers} consumers")
    main_process_sum, consumer_final_sum = test(total_numbers, group_size, num_producers, num_consumers)
    elapsed_time = time.time() - start_time
    results.append((f"{num_producers} producers & {num_consumers} consumers", total_numbers, main_process_sum, consumer_final_sum, main_process_sum == consumer_final_sum, elapsed_time))

    # Configuración 3: Igual número de productores que consumidores
    num_producers = num_cores // 2
    num_consumers = num_producers
    start_time = time.time()
    print(f"Running experiment: {num_producers} producers & {num_consumers} consumers")
    main_process_sum, consumer_final_sum = test(total_numbers, group_size, num_producers, num_consumers)
    elapsed_time = time.time() - start_time
    results.append((f"{num_producers} producers & {num_consumers} consumers", total_numbers, main_process_sum, consumer_final_sum, main_process_sum == consumer_final_sum, elapsed_time))

    print("\nResults:")
    print("| Configuración                 | Total de Números | Suma por Productores | Suma por Consumidores | Coinciden | Tiempo (s) |")
    print("|-------------------------------|------------------|----------------------|-----------------------|-----------|------------|")
    for result in results:
        print(f"| {result[0]:<30}| {result[1]:<17}| {result[2]:<20} | {result[3]:<21} | {'Sí' if result[4] else 'No':<9} | {result[5]:<10.4f} |")

if __name__ == "__main__":
    while True:
        total_numbers = int(input("Ingrese el total de numeros a sumar (mayor que 1): "))
        if total_numbers > 1:
            run_experiment(total_numbers, group_size=10)
            break
        else:
            print("ERROR: El total de números debe ser mayor que 1. Intente nuevamente.")
