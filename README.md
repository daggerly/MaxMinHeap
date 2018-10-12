# MaxMinHeap

用来计算最大或最小的n个元素的堆
模仿了python标准库的heapq, Queue.Queue
### usage:
```python
h = MaxMinHeap(cmp_lt, maxsize=3)
h.put(1)
h.put(2)
h.put(3)
h.put(4)
print h.queue
```
