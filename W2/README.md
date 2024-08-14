# Homework Assignment: Exploring Concurrency with Threads and Processes in Python (I/O-bound Tasks)

## Objective:
To understand the impact of concurrency on the performance of I/O-bound tasks by
experimenting with different numbers of threads and processes. This exercise will demonstrate
how execution time changes with varying worker counts and highlight the practical limits of
concurrency for I/O-bound operations.
Task Description:
1. Task Overview:
- You will implement a Python script that fetches web pages using both threads and
processes.
- You will measure the execution time for varying numbers of workers (1, 2, 4, 8, 16, 32).
- You will analyze the results to understand how increasing the number of workers affects
performance and when the improvements become marginal.

2. Steps to Follow:

- Define the URL Fetching Function:
    - Implement a function that fetches the content of a URL. This function will serve as an
I/O-bound task.
- Create a Function to Fetch URLs with Concurrency:
    - Implement a function that accepts the worker type (thread or process), the number of
workers, and a list of URLs to fetch.
    - Use the `concurrent.futures.ThreadPoolExecutor` for threads and
`concurrent.futures.ProcessPoolExecutor` for processes to manage workers.
    - Measure and print the execution time for each configuration.

3. Run Experiments:
- Test your function with varying numbers of workers (1, 2, 4, 8, 16, 32).
- Use a sufficiently large list of URLs to fetch (e.g., a list of 10 different URLs) to ensure
there are more tasks than workers.

4. Summarize the Results:
- Record the execution times for each configuration (threads and processes with different
worker counts).
- Analyze and compare the results to understand how performance scales with the number
of workers and identify the point where improvements become marginal.

3. Deliverables:
- A Python script implementing the above steps.
- A brief report summarizing your findings, including:
    - The execution times for each configuration.
    - An analysis of how performance changes with increasing worker counts.
    - A discussion on when and why the improvements become marginal.
4. Submission:
- Submit your Python script and the report as a single ZIP file to the course's homework
submission portal.
Hints and Tips:
- Ensure that your script runs without errors before measuring execution times.
- Use print statements to track progress and debug any issues.
- Consider running your script on a machine with a stable internet connection to observe the
effects of parallelism more clearly.
Example Code Snippet:
Here is a small snippet to get you started with the `ThreadPoolExecutor` and
`ProcessPoolExecutor`:

```python
import concurrent.futures
import requests
import time

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
def fetch_url(url):
    response = requests.get(url)
    print(f"{url} fetched with {len(response.content)} bytes")
    return response.content
def fetch_with_workers(worker_type, max_workers, urls):
    if worker_type == "thread":
        executor_class = concurrent.futures.ThreadPoolExecutor
    else:
        executor_class = concurrent.futures.ProcessPoolExecutor
    
    start_time = time.time()
    with executor_class(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_url, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            future.result()
    end_time = time.time()
    duration = end_time - start_time
    print(f"{worker_type.capitalize()}s with {max_workers} workers took:", duration,"seconds")
    return duration
```
# Example of how to call the function
```python
urls = URLS * 2 # Increase the number of tasks by repeating the list
fetch_with_workers("thread", 4, urls)
```
Good luck, and have fun exploring the power of concurrency in Python!