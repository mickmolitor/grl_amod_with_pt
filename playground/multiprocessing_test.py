import time
from multiprocessing import Pool

# Fibonacci-Funktion
def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

def sequential_execution(numbers):
    start_time = time.time()
    results = [fib(n) for n in numbers]
    end_time = time.time()
    print(f"Sequentielle Ausführung: {end_time - start_time:.2f} Sekunden")
    return results

def parallel_execution(numbers):
    start_time = time.time()
    with Pool(processes=8) as pool:  # adjust the amount of processes to available cores
        results = pool.map(fib, numbers)
    end_time = time.time()
    print(f"Parallele Ausführung: {end_time - start_time:.2f} Sekunden")
    return results

def test_parallel_execution():
    # main program
    if __name__ == "__main__":
        numbers = [30, 31, 32, 33, 34, 35, 36, 37]
        
        sequential_results = sequential_execution(numbers)
        
        parallel_results = parallel_execution(numbers)
        
        assert sequential_results == parallel_results, "Die Ergebnisse der sequentiellen und parallelen Ausführung stimmen nicht überein!"
        print("Ergebnisse stimmen überein.")
