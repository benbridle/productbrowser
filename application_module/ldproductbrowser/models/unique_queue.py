from queue import Queue
from collections import namedtuple, deque

KeyItemPair = namedtuple("KeyItemPair", "key item")


class UniqueQueue(Queue):
    def _init(self, maxsize):
        super()._init(maxsize)

    def put(self, key, item, block=True, timeout=None):
        super().put(KeyItemPair(key, item), block, timeout)

    def _put(self, key_item_pair):
        self._remove_key(key_item_pair.key)
        self.queue.append(key_item_pair)

    def _get(self):
        return self.queue.popleft().item

    def _remove_key(self, key):
        for element in self.queue.copy():
            if element.key == key:
                self.queue.remove(element)
