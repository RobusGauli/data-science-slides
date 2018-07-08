# from collections import defaultdict
# from collections import Counter
# import os

# from concurrent.futures import Future
# from concurrent.futures import ThreadPoolExecutor

# pool = ThreadPoolExecutor(10)

# import requests



# def inline_future(gen):
#     #wrap that generator in future
#     def wrapper(*args, **kwargs):
#         task = Task(gen(*args, **kwargs))
#         task.step()
#         return task.result()
#     return wrapper


# class Task(Future):
    
#     def __init__(self, gen):
#         self.gen = gen
#         super().__init__()
    
#     def step(self, value=None, error = None):
#         try:
#             future = self.gen.send(value)
#             if isinstance(future, Future):
#                 future.add_done_callback(self._feed)
#         except StopIteration  as e:
#             self.set_result(e.value)


#     def _feed(self, future):
#         self.step(future.result())
        


# @inline_future
# def get(url):
#     result = yield pool.submit(requests.get, url)
#     return result

# def main():
#     url = 'http://upwork.com'
#     g = get(url)
#     print(g)
# if __name__ == '__main__':
#     main()


import os

def file_runner(txt_files):
    current_index = 0
    
    while True:
        next_index = yield current_index
        
        current_index = next_index
        print(open(txt_files[current_index]).read())
        yield



sorted_txt_files = sorted([file for file in os.listdir() if file.endswith('.txt')], key=lambda file: int(file.split('.')[0]))

f = file_runner(sorted_txt_files)

def left(delta = 1):
    #get current_index
    current = f.send(None)
    f.send(((current - delta) + len(sorted_txt_files)) % len(sorted_txt_files))
    
def right(delta = 1):
    current = f.send(None)
    next_idx = ((current + delta) + len(sorted_txt_files)) % len(sorted_txt_files)
    print(next_idx, len(sorted_txt_files))
    f.send(next_idx)

def show():
    current = f.send(None)
    f.send(current)