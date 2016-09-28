## Threaded Queue Provider

A threaded class that can be spawned to provide a specific value threadsafe via a queue

Subclass ThreadQueueProvider to set the getVal method and control the values that will be pushed into the Queue

Queuesize defaults to 1, so whenever a requetor takes from the queue it is repopulated. this can be increased for more rapid requests if the getVal method doesnt need to be as up-to-date

see example.py for an example where a separate thread pulls the value every 5 seconds