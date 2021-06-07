import time

from celery.result import AsyncResult
from django.http import HttpResponse

from .tasks import long_a, medium_b, result_backend_task, short_c


def index(request):
    t = time.strftime("%H:%M:%S", time.localtime())
    print("-----------PROCESS STARTED on {}---------------".format(t))
    for i in range(2):
        long_a.delay(i)
        medium_b.delay(i)
        short_c.delay(i)
    return HttpResponse("Hello, world. The Demo is running!")


# If we want to keep track of the tasks’ states, Celery needs to store or send the states somewhere
# more : https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#keeping-results
def result_backend(request):
    print("testing result backend................")
    result = result_backend_task.delay()
    is_ready = result.ready()
    print(is_ready)
    r = result.get()  # will wait about 8 seconds here
    print(r)
    is_ready = result.ready()
    print(is_ready)
    return HttpResponse("The Result Backend Demo is running!")


def remove_task(request, task_id):
    print("ID===",task_id)
    AsyncResult(task_id).revoke(terminate=True)
    return HttpResponse("Removing the task!")
