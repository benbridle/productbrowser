from threading import Thread
from ldproductbrowser.models import UniqueQueue

app_context = None
settings = None

task_queue = UniqueQueue()


def run_tasks(_task_queue):
    while True:
        task = _task_queue.get()
        task()
        _task_queue.task_done()


num_threads = 10
for i in range(num_threads):
    worker = Thread(target=run_tasks, args=(task_queue,))
    worker.setDaemon(True)
    worker.start()
