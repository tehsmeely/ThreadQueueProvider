# Threaded Queue Provider

A threaded class that can be spawned to provide a specific value threadsafe via a queue

Subclass ThreadQueueProvider to set the `_getVal()` method and control the values that will be pushed into the Queue

Queuesize defaults to 1, so whenever a requetor takes from the queue it is repopulated. this can be increased for more rapid requests if the `_getVal()` method doesnt need to be as up-to-date

see example.py for an example where a separate thread pulls the value


## Usage

1)

Instance ThreadQueueProvider and set a function to return the set of values:

```python
import random
from threadQueueProvider import ThreadQueueProvider
random.seed()

def myGetVal():
    return random.randint(1, 100)

provider = ThreadQueueProvider(valueFunction=myGetVal)
provider.start()

provider.getVal()
```


2)

SubClass ThreadQueueProvider and override the function to return the set of values - plus the other stuff you need since you chose to subclass!:

```python
import random
from threadQueueProvider import ThreadQueueProvider
random.seed()

class MyProvider(ThreadQueueProvider)
    def __init__(self, min, max):
        ThreadQueueProvider.__init__(self)
        self.min = min
        self.max = max

    def _getVal(self):
        #This is the overridden method from ThreadQueueProvider
        return self.getARandomNumber(self.min, self.max)

    def getARandomNumber(self, a, b)
        return random.randint(a, b)

provider = myProvider(0, 100)
provider.start()

provider.getVal()
```