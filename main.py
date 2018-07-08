from collections import defaultdict
from collections import Counter
import os

from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(10)

import requests



def inline_future(gen):
    #wrap that generator in future
    def wrapper(*args, **kwargs):
        task = Task(gen(*args, **kwargs))
        task.step()
        return task.result()
    return wrapper


class Task(Future):
    
    def __init__(self, gen):
        self.gen = gen
        super().__init__()
    
    def step(self, value=None, error = None):
        try:
            future = self.gen.send(value)
            if isinstance(future, Future):
                future.add_done_callback(self._feed)
        except StopIteration  as e:
            self.set_result(e.value)


    def _feed(self, future):
        self.step(future.result())
        


@inline_future
def get(url):
    result = yield pool.submit(requests.get, url)
    return result

def main():
    url = 'http://upwork.com'
    g = get(url)
    print(g)
if __name__ == '__main__':
    main()
