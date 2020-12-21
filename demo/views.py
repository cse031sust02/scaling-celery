import time

from django.http import HttpResponse

from .tasks import long_a, medium_b, short_c


def index(request):    
    t = time.strftime("%H:%M:%S", time.localtime())
    print("-----------PROCESS STARTED on {}---------------".format(t))
    for i in range(20):
        long_a.delay(i)
        medium_b.delay(i)
        short_c.delay(i)
    return HttpResponse("Hello, world. The Demo is running!")
