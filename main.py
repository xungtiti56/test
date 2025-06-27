# main.py
import multiprocessing
import random
import time
from streamhg_worker import run_browser_instance

# Danh sách các link
link_list = [
    "https://gradehgplus.com/nqtgnz8x2dx9",
    "https://gradehgplus.com/hfip1hmdbutz",
    "https://gradehgplus.com/gd466mm36ade",
    "https://gradehgplus.com/86pbb3fb14i2",
    "https://gradehgplus.com/j8edjxkcfz7y",
    "https://gradehgplus.com/f0bm2v25r7jl",
    "https://gradehgplus.com/gd7t22p8s8jb",
]

def run_all():
    selected_links = random.sample(link_list, 3)
    processes = []

    for i, url in enumerate(selected_links):
        p = multiprocessing.Process(target=run_browser_instance, args=(i, url))
        processes.append(p)
        p.start()

    for p in processes:
        p.join(timeout=350)  # 7 phút

        if p.is_alive():
            print(f"[Main] Timeout reached. Killing process {p.pid}")
            p.terminate()
            p.join()

    print("All processes finished or were terminated.")

if __name__ == "__main__":
    run_all()
