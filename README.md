## Overview

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
### Experiment #1 : Basic Setup (Without Result Backend)

With Celery's default setup, it comes with a default Queue where all the tasks will end up in that Queue.
	
Setup :
- 1 Broker (Redis)
- 1 Queue
- No Result Backend

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
- last short task ((#20)) was completed after 2 minutes (approx)

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

### reference
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html



Experiment #2 : Basic Setup (With Result Backend)
--------------------------------------------------
Intro :

No.6: Keep track of results only if you really need them (https://denibertovic.com/posts/celery-best-practices/)

CELERY_IGNORE_RESULT

Setup :
	- 1 Broker (Redis)
	- 1 Queue
	- 1 Result Backend
	- use 

Observation :

references :
- https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#keeping-results
- https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-result-backends 




Experiment #3 : Multiple Queue
--------------------------------

Intro : 
	By default everything goes into a default queue named celery and this is what celery worker will process if no queue is specified. But sometimes there may be situation where taskA and taskB might be doing totally different things, and perhaps one of them might be more important than the other. In this type of situation, we can use multiple queues. For example, taskA can go in one queue, and taskB in another queue.
	https://hackernoon.com/using-celery-with-multiple-queues-retries-and-scheduled-tasks-589fe9a4f9ba

Code :
	configuration :
		task_routes = {
			'myapp.tasks.taskA': {'queue': 'queue1'},
			'myapp.tasks.taskB': {'queue': 'queue2'},
		}

	shell :
		$ celery -A proj worker -Q queue1, queue2


Demo Setup :
	- 1 Broker (Redis)
	- 1 Worekr
		- 2 Queues
	- 1 Result Backend

Observation :


references : 
- https://docs.celeryproject.org/en/stable/userguide/routing.html



Experiment #4 : Multiple Worker with different setups
----------------------------------------------------------

Intro : The way to solve the issue above is to have taskA in one queue, and taskB in another and then assign x workers to process Q1 and all the other workers to process the more intensive Q2 as it has more tasks coming in
	

	shell :
		$ celery worker -A tasks -l INFO --concurrency=2 -n WokerWithTwoProcesses
		$ celery worker -A tasks -l INFO --concurrency=4 -n WokerWithFourProcesses -Q queue1, queue2



Note : Use priority workers (https://denibertovic.com/posts/celery-best-practices/)

Setup :
	- 1 Broker (Redis)
	- 2 Workers
		- worker1 = 1 Queue, concurrency 2
		- worker2 = 2 Queues, concurrency 4
	- 1 Result Backend

Observation :

- https://denibertovic.com/posts/celery-best-practices/



Experiment #4 : error handling mechanisms
- https://denibertovic.com/posts/celery-best-practices/



Experiment #5 : Sequential Tasks
- https://hackernoon.com/using-celery-with-multiple-queues-retries-and-scheduled-tasks-589fe9a4f9ba (Calling Sequential Tasks)