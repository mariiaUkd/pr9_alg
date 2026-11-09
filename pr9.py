import random
import sys
import time
from array import array

K = 6 
RUNS = 3 
SIZES = [10_000, 100_000, 1_000_000, 10_000_000, 100_000_000]
LOW, HIGH = -10_000, 10_000
NEG_INF = LOW - 1 


def generate(n):
    """Масив з n випадкових цілих у діапазоні [-10000; 10000]."""
    try:
        import numpy as np  # швидка генерація для великих n
        src = np.random.randint(LOW, HIGH + 1, size=n, dtype=np.int32)
        arr = array('i')
        arr.frombytes(src.tobytes())
        return arr
    except ImportError:
        return array('i', (random.randint(LOW, HIGH) for _ in range(n)))


def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    res, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res


def method_sort(data):
    sorted_data = merge_sort(list(data))
    return sorted_data[-K]


def method_top_array(data):
    top = sorted(data[:K], reverse=True)
    for x in data[K:]:
        if x > top[-1]: 
            i = K - 1
            while i > 0 and top[i - 1] < x: 
                top[i] = top[i - 1]
                i -= 1
            top[i] = x
    return top[-1]


def method_max_k_times(data):
    work = list(data) 
    n = len(work)
    result = None
    for _ in range(K):
        max_val, max_idx = work[0], 0
        for i in range(1, n):
            if work[i] > max_val:
                max_val, max_idx = work[i], i
        result = max_val
        work[max_idx] = NEG_INF 
    return result


def measure(func, data):
    start = time.perf_counter()
    res = func(data)
    ms = (time.perf_counter() - start) * 1000
    return res, ms


def fmt(times):
    avg = round(sum(times) / len(times))
    return f"{avg}({' '.join(str(round(t)) for t in times)})"


def main():
    sizes = [int(s) for s in sys.argv[1:]] or SIZES
    methods = [("Спосіб 1 (Сортування)", method_sort),
               ("Спосіб 2 (Масив)", method_top_array),
               ("Спосіб 3 (Максимальні елементи)", method_max_k_times)]

    test = generate(1000)
    expected = sorted(test)[-K]
    for name, f in methods:
        assert f(test) == expected, f"Помилка в алгоритмі: {name}"
    print("Перевірка коректності пройдена.\n")

    rows = []
    for n in sizes:
        print(f"Розмір {n:,} ...", flush=True)
        times = {name: [] for name, _ in methods}
        for run in range(RUNS):
            data = generate(n) 
            results = set()
            for name, f in methods:
                res, ms = measure(f, data)
                times[name].append(ms)
                results.add(res)
            assert len(results) == 1, "Способи дали різні результати!"
            print(f"  запуск {run + 1}: 6-й елемент = {results.pop()}")
        rows.append((n, [fmt(times[name]) for name, _ in methods]))

    print("\nЧас роботи, мс: середнє(запуск1 запуск2 запуск3)")
    header = ["Розмір"] + [name for name, _ in methods]
    print(" | ".join(header))
    for n, cells in rows:
        print(" | ".join([f"{n:,}"] + cells))


if __name__ == "__main__":
    main()