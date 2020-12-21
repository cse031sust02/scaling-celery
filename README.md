## Overview

This is a personal repository to get my hands on Celery (with Django).

## Tasks setup

There are few tasks with below naming and time to complete :
- LONG_A : 3 seconds to complete
- LONG_A_inner_short_1 : 1 seconds to complete
- LONG_A_inner_long_1 : 4 seconds to complete
- MEDIUM_B : 2 seconds to complete
- SHORT_C : 1 seconds to complete

When we call the endpoint `localhost:8000/demo`, It will run
- 20 LONG_A tasks (each of which will run 10 inner short tasks and 10 inner long tasks)
- 20 MEDIUM_B tasks
- 20 SHORT_C tasks

---

### Experiment #1 : Basic Setup

With Celery's default setup, it comes with a default Queue where all the tasks will end up in that Queue.
	
Setup :
- 1 Broker (Redis)
- 1 Queue
- 1 Result Backend*

> *We should keep track of results only if we really need them. We can set CELERY_TASK_IGNORE_RESULT = True in config to discard the results for [all tasks](https://docs.celeryproject.org/en/stable/userguide/configuration.html#std-setting-task_ignore_result). Or we can [ignore results for individual tasks](https://docs.celeryproject.org/en/stable/userguide/tasks.html#ignore-results-you-don-t-want).


#### Demo 1 : running with 1 worker processes (concurrency)

```bash
$ celery -A celery_demo worker -l INFO -n DEMO_1 -c 1
```

Observation : As there is only one worker process, it is completing tasks serially.

```
start LONG TASK #1
end LONG TASK #1
start MEDIUM TASK #1
end MEDIUM TASK #1
start SHORT TASK #1
end SHORT TASK #1
....
....
start LONG TASK #20
end LONG TASK #20
start MEDIUM TASK #20
end MEDIUM TASK #20
start SHORT TASK #20
end SHORT TASK #20 (after approx 2 minutes)
....
....
start INNER LONG TASK #1
end  INNER LONG TASK #1
start INNER SHORT TASK #1
end  INNER SHORT TASK #1
```

- time to complete the whole process : 20 min (approx)
- last short task (#20) was completed after 2 minutes (approx)

#### Demo 2 : running with 10 worker processes (concurrency)

```bash
$ celery -A celery_demo worker -l INFO -n DEMO_1 -c 10
```

Observation : As there are 10 worker, it is processing 10 tasks at a time..

```
start LONG TASK #1
start MEDIUM TASK #1
start SHORT TASK #1
start LONG TASK #2
start SHORT TASK #2
start MEDIUM TASK #2
start LONG TASK #3
start MEDIUM TASK #3
start SHORT TASK #3
start LONG TASK #4
...
end SHORT TASK #1
end SHORT TASK #2
end SHORT TASK #3
start MEDIUM TASK #4
start SHORT TASK #4
start LONG TASK #5
end MEDIUM TASK #1
...
```

- time to complete the whole process : 2 min (approx)
- last short task (#20) was completed after 12 seconds (approx)

#### reference
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html


