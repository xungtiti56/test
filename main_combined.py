# import multiprocessing
# import time
# from videzz_video import run_main_selenium
# from earn import run_earn_parallel

# if __name__ == "__main__":
#     p1 = multiprocessing.Process(target=run_main_selenium)
#     p2 = multiprocessing.Process(target=run_earn_parallel)

#     p1.start()
#     p2.start()

#     p1.join()
#     p2.join()

#     print("All tasks completed.")
import multiprocessing
from videzz_video import run_main_selenium
from earn import run_earn_parallel
from streamhg import run_streamhg_parallel

if __name__ == "__main__":
    processes = [
        multiprocessing.Process(target=run_main_selenium),
        multiprocessing.Process(target=run_earn_parallel),
        multiprocessing.Process(target=run_streamhg_parallel),
    ]
    # processes = [
    #     multiprocessing.Process(target=run_main_selenium),
    #     multiprocessing.Process(target=run_earn_parallel),
    # ]


    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print("✅ All jobs completed.")
