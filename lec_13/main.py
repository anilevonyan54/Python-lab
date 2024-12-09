import string
import time
from collections import defaultdict
from threading import Thread, Lock
from multiprocessing import Process, Manager


def generate_large_file(filename, size_mb):
    with open(filename, "w") as file:
        words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
        sentences = [" ".join(words[i % len(words):] + words[:i % len(words)]) + ".\n" for i in range(100)]
        for _ in range(size_mb * 1024 * 1024 // 100):
            file.write(sentences[_ % len(sentences)])


def count_words_sequential(filename):
    word_count = defaultdict(int)
    with open(filename, "r") as file:
        for line in file:
            words = line.translate(str.maketrans("", "", string.punctuation)).lower().split()
            for word in words:
                word_count[word] += 1
    return word_count


def count_words_multithreading(filename, num_threads=4):
    def worker(chunk, local_count):
        for line in chunk:
            words = line.translate(str.maketrans("", "", string.punctuation)).lower().split()
            for word in words:
                with lock:
                    local_count[word] += 1

    with open(filename, "r") as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_threads
    threads = []
    lock = Lock()
    word_count = defaultdict(int)

    for i in range(num_threads):
        chunk = lines[i * chunk_size: (i + 1) * chunk_size]
        thread = Thread(target=worker, args=(chunk, word_count))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return word_count


def count_words_multiprocessing(filename, num_processes=4):
    def worker(chunk, shared_dict):
        local_count = defaultdict(int)
        for line in chunk:
            words = line.translate(str.maketrans("", "", string.punctuation)).lower().split()
            for word in words:
                local_count[word] += 1
        for word, count in local_count.items():
            shared_dict[word] += count

    with open(filename, "r") as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_processes
    processes = []
    manager = Manager()
    shared_dict = manager.defaultdict(int)

    for i in range(num_processes):
        chunk = lines[i * chunk_size: (i + 1) * chunk_size]
        process = Process(target=worker, args=(chunk, shared_dict))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return shared_dict


def compare_performance(filename):
    print(f"Comparing performance on file: {filename}")

    start_time = time.time()
    seq_result = count_words_sequential(filename)
    seq_time = time.time() - start_time
    print(f"Sequential time: {seq_time:.4f} seconds")

    start_time = time.time()
    mt_result = count_words_multithreading(filename)
    mt_time = time.time() - start_time
    print(f"Multithreading time: {mt_time:.4f} seconds")

    start_time = time.time()
    mp_result = count_words_multiprocessing(filename)
    mp_time = time.time() - start_time
    print(f"Multiprocessing time: {mp_time:.4f} seconds")

    assert seq_result == mt_result == mp_result, "Results mismatch between methods!"

    print(f"Speedup (Multithreading): {seq_time / mt_time:.2f}x")
    print(f"Speedup (Multiprocessing): {seq_time / mp_time:.2f}x")


if __name__ == "__main__":
    file_name = "large_text_file.txt"
    if not os.path.exists(file_name):
        print("Generating large file...")
        generate_large_file(file_name, size_mb=50)

    compare_performance(file_name)
