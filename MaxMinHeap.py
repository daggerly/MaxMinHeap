#coding: utf-8

try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

def cmp_lt(item1, item2):
    return item1[1] < item2[1]

def cmp_gt(item1, item2):
    return item1[1] > item2[1]

class MaxMinHeap(object):
    """
    堆只保存前maxsize个最小的元素，但堆为大顶堆
    """
    def __init__(self, key, maxsize=0):
        self.maxsize = maxsize
        self._init(maxsize)
        # mutex must be held whenever the queue is mutating.  All methods
        # that acquire mutex must release it before returning.  mutex
        # is shared between the three conditions, so acquiring and
        # releasing the conditions also acquires and releases mutex.
        self.mutex = _threading.Lock()
        # Notify not_empty whenever an item is added to the queue; a
        # thread waiting to get is notified then.
        self.not_empty = _threading.Condition(self.mutex)
        # Notify not_full whenever an item is removed from the queue;
        # a thread waiting to put is notified then.
        self.not_full = _threading.Condition(self.mutex)
        # Notify all_tasks_done whenever the number of unfinished tasks
        # drops to zero; thread waiting to join() is notified to resume

        self.key = key

    def put(self, item):
        """Put an item into the queue.
        """
        self.not_full.acquire()
        try:
            # decorated = self.key(item), item
            # 如果堆满了，先判断丢掉最后一个
            if (self.maxsize > 0) and (self._qsize() >= self.maxsize):
                self.heappushpop(item)
            else:
                self.heappush(item)
            self.not_empty.notify()

        finally:
            self.not_full.release()

    def get(self):
        self.not_empty.acquire()
        try:
            item = self.heappop()
            self.not_full.notify()
            return item
        finally:
            self.not_empty.release()

    def qsize(self):
        """Return the approximate size of the queue (not reliable!)."""
        self.mutex.acquire()
        n = self._qsize()
        self.mutex.release()
        return n

    def heappush(self, item):
        """Push item onto heap, maintaining the heap invariant."""
        self.queue.append(item)
        self._siftdown(0, self._qsize() - 1)

    def heappop(self):
        """Pop the smallest item off the heap, maintaining the heap invariant."""
        lastelt = self.queue.pop()  # raises appropriate IndexError if heap is empty
        if self.queue:
            returnitem = self.queue[0]
            self.queue[0] = lastelt
            self._siftup(0)
        else:
            returnitem = lastelt
        return returnitem

    def heappushpop(self, item):
        if self.queue and self.key(item, self.queue[0]):
            item, self.queue[0] = self.queue[0], item
            self._siftup( 0)
        return item

    def _siftdown(self, startpos, pos):
        newitem = self.queue[pos]
        # Follow the path to the root, moving parents down until finding a place
        # newitem fits.
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = self.queue[parentpos]
            if self.key(parent, newitem):
                self.queue[pos] = parent
                pos = parentpos
                continue
            break
        self.queue[pos] = newitem

    def _siftup(self, pos):
        'Maxheap variant of _siftup'
        endpos = len(self.queue)
        startpos = pos
        newitem = self.queue[pos]
        # Bubble up the larger child until hitting a leaf.
        childpos = 2 * pos + 1  # leftmost child position
        while childpos < endpos:
            # Set childpos to index of larger child.
            rightpos = childpos + 1
            if rightpos < endpos and not self.key(self.queue[rightpos],  self.queue[childpos]):
                childpos = rightpos
            # Move the larger child up.
            self.queue[pos] = self.queue[childpos]
            pos = childpos
            childpos = 2 * pos + 1
        # The leaf at pos is empty now.  Put newitem there, and bubble it up
        # to its final resting place (by sifting its parents down).
        self.queue[pos] = newitem
        self._siftdown(startpos, pos)

    def _qsize(self, len=len):
        return len(self.queue)

    def _init(self, maxsize):
        self.queue = []

    def __len__(self):
        return len(self.queue)
