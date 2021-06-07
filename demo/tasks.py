from celery import shared_task
from time import sleep


@shared_task(name="LONG_A")
def long_a(id):
    print("START : LONG TASK : #COUNTER-{}".format(id))
    sleep(3)
    for i in range(10):
        long_a_inner_short.delay(id)
        long_a_inner_long.delay(id)
    print("END : LONG TASK : #COUNTER-{}".format(id))
    return 'Long-Task-{}'.format(id)


@shared_task(name="MEDIUM_B")
def medium_b(id):
    print("START : MEDIUM TASK : #COUNTER-{}".format(id))
    sleep(2)
    print("END : MEDIUM TASK : #COUNTER-{}".format(id))
    return 'Medium-Task-{}'.format(id)


@shared_task(name="SHORT_C")
def short_c(id):
    print("START : SHORT TASK : #COUNTER-{}".format(id))
    sleep(1)
    print("END : SHORT TASK : #COUNTER-{}".format(id))
    return 'Short-Task-{}'.format(id)


@shared_task(name="LONG_A_inner_short_1")
def long_a_inner_short(id):
    print("START : INNER SHORT TASK : #COUNTER-{}".format(id))
    sleep(1)
    print("END : INNER SHORT TASK : #COUNTER-{}".format(id))
    return 'Inner-Short-Task-{}'.format(id)


@shared_task(name="LONG_A_inner_long_1")
def long_a_inner_long(id):
    print("START : INNER LONG TASK : #COUNTER-{}".format(id))
    sleep(4)
    print("END : INNER LONG TASK : #COUNTER-{}".format(id))
    return 'Inner-Long-Task-{}'.format(id)


@shared_task(name="Result Backend Demo", ignore_result=False)
def result_backend_task():
    print("START : RESULT BACKEND")
    sleep(10)
    for i in range(1000000):
        print(i)
    print("END : RESULT BACKEND")
    return 'demo result'