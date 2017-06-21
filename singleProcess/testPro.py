from multiprocessing import Process
from time import sleep

from multiprocessing import Queue


def run_proc(trees_part_1):
    trees_part_1.put(2)


if __name__ == '__main__':
    trees_part_1 = Queue()
    p = Process(target=run_proc, args=(trees_part_1,))
    p.start()
    p.join()

    trees_part_1.get()

