import concurrent.futures
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

URLS = [
    'http://www.google.com',
    'http://www.bing.com',
    'http://www.yahoo.com',
    'http://www.duckduckgo.com',
    'http://www.example.com',
    'http://www.python.org',
    'http://www.github.com',
    'http://www.stackoverflow.com',
    'http://www.wikipedia.org',
    'http://www.reddit.com',
]

MAX_PROCESSES = 61

def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def fetch_with_workers(worker_type, max_workers, urls):
    if worker_type == "thread":
        executor_class = concurrent.futures.ThreadPoolExecutor
    elif worker_type == "process":
        if max_workers > MAX_PROCESSES:
            print(f"Can't run more than {MAX_PROCESSES} processes. Using {MAX_PROCESSES} processes instead.")
            max_workers = MAX_PROCESSES
        executor_class = concurrent.futures.ProcessPoolExecutor
    else:
        raise ValueError("Invalid worker_type. Use 'thread' or 'process'.")
    
    start_time = time.time()
    with executor_class(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_url, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error in future result: {e}")
    end_time = time.time()
    duration = end_time - start_time

    return worker_type, max_workers, duration

def plot_performance(df_threads, df_processes):
    workers_threads = np.array(df_threads['Workers'])
    thread_times = np.array(df_threads['Time (seconds)'])
    
    workers_processes = np.array(df_processes['Workers'])
    process_times = np.array(df_processes['Time (seconds)'])
    
    plt.figure(figsize=(12, 6))
    
    if len(workers_threads) > 0:
        plt.plot(workers_threads, thread_times, label='Threads', marker='o')
    if len(workers_processes) > 0:
        plt.plot(workers_processes, process_times, label='Processes', marker='o')
    
    plt.xscale('log', base=2)
    plt.yscale('linear')
    plt.xlabel('Number of Workers')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Comparison: Threads vs Processes')
    plt.legend()
    plt.grid(True)
    
    plt.ylim(bottom=0)
    plt.yticks(np.arange(0, 31, 1))
    
    plt.show()


def main():
    num_workers_options = [1, 2, 4, 8, 16, 32]
    urls = URLS * 4 
    
    t_results = []  #? Threads results
    p_results = []  #? Process results
    
    print("Number of URLs to fetch: ", len(urls))
    for workers in num_workers_options:
        print(f"\nTesting with Threads: {workers} workers")
        result = fetch_with_workers("thread", workers, urls)
        t_results.append(result)
    
    for workers in num_workers_options:
        if workers > MAX_PROCESSES:
            print(f"Skipping Processes test with {workers} workers. Exceeds maximum allowed processes.")
            continue
        print(f"\nTesting with Processes: {workers} workers")
        result = fetch_with_workers("process", workers, urls)
        p_results.append(result)
    
    df_threads = pd.DataFrame(t_results, columns=['Type', 'Workers', 'Time (seconds)'])
    df_processes = pd.DataFrame(p_results, columns=['Type', 'Workers', 'Time (seconds)'])
    
    print("\n\n------------------------RESULTS----------------------\n\n")
    print("\n\n")
    print("         ----------------")
    print("        |Threads Results:|")
    print("         ----------------")
    print(df_threads)
    print("\n\n")
    print("         ------------------")
    print("        |Processes Results:|")
    print("         ------------------")
    print(df_processes)
    
    plot_performance(df_threads, df_processes)

if __name__ == "__main__":
    main()
