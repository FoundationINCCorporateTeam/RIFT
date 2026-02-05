"""
RIFT Standard Library - Collections Module

Advanced data structures: Stack, Queue, LinkedList, Set, OrderedDict, etc.
"""

from typing import Any, Dict, List, Optional, Callable, Union, Iterator
from collections import OrderedDict as PyOrderedDict


def create_collections_module(interpreter) -> Dict[str, Any]:
    """Create the collections module for RIFT."""
    
    # ========================================================================
    # Stack (LIFO)
    # ========================================================================
    
    class Stack:
        """Last-In-First-Out data structure."""
        
        def __init__(self, items: List[Any] = None):
            self._items = list(items) if items else []
        
        def push(self, *items) -> 'Stack':
            """Push items onto the stack."""
            self._items.extend(items)
            return self
        
        def pop(self) -> Any:
            """Pop and return top item."""
            if not self._items:
                return None
            return self._items.pop()
        
        def peek(self) -> Any:
            """Return top item without removing."""
            if not self._items:
                return None
            return self._items[-1]
        
        def size(self) -> int:
            """Return stack size."""
            return len(self._items)
        
        def isEmpty(self) -> bool:
            """Check if stack is empty."""
            return len(self._items) == 0
        
        def clear(self) -> 'Stack':
            """Clear the stack."""
            self._items = []
            return self
        
        def toList(self) -> List[Any]:
            """Convert to list (top to bottom)."""
            return list(reversed(self._items))
        
        def __repr__(self):
            return f"Stack({self._items})"
    
    # ========================================================================
    # Queue (FIFO)
    # ========================================================================
    
    class Queue:
        """First-In-First-Out data structure."""
        
        def __init__(self, items: List[Any] = None):
            self._items = list(items) if items else []
        
        def enqueue(self, *items) -> 'Queue':
            """Add items to the end."""
            self._items.extend(items)
            return self
        
        def dequeue(self) -> Any:
            """Remove and return first item."""
            if not self._items:
                return None
            return self._items.pop(0)
        
        def peek(self) -> Any:
            """Return first item without removing."""
            if not self._items:
                return None
            return self._items[0]
        
        def size(self) -> int:
            """Return queue size."""
            return len(self._items)
        
        def isEmpty(self) -> bool:
            """Check if queue is empty."""
            return len(self._items) == 0
        
        def clear(self) -> 'Queue':
            """Clear the queue."""
            self._items = []
            return self
        
        def toList(self) -> List[Any]:
            """Convert to list."""
            return list(self._items)
        
        def __repr__(self):
            return f"Queue({self._items})"
    
    # ========================================================================
    # Deque (Double-ended Queue)
    # ========================================================================
    
    class Deque:
        """Double-ended queue."""
        
        def __init__(self, items: List[Any] = None):
            self._items = list(items) if items else []
        
        def pushFront(self, item: Any) -> 'Deque':
            """Add item to front."""
            self._items.insert(0, item)
            return self
        
        def pushBack(self, item: Any) -> 'Deque':
            """Add item to back."""
            self._items.append(item)
            return self
        
        def popFront(self) -> Any:
            """Remove and return front item."""
            if not self._items:
                return None
            return self._items.pop(0)
        
        def popBack(self) -> Any:
            """Remove and return back item."""
            if not self._items:
                return None
            return self._items.pop()
        
        def peekFront(self) -> Any:
            """Return front item."""
            return self._items[0] if self._items else None
        
        def peekBack(self) -> Any:
            """Return back item."""
            return self._items[-1] if self._items else None
        
        def size(self) -> int:
            return len(self._items)
        
        def isEmpty(self) -> bool:
            return len(self._items) == 0
        
        def toList(self) -> List[Any]:
            return list(self._items)
        
        def __repr__(self):
            return f"Deque({self._items})"
    
    # ========================================================================
    # PriorityQueue
    # ========================================================================
    
    class PriorityQueue:
        """Priority queue (min-heap by default)."""
        
        def __init__(self, items: List[Any] = None, key: Callable = None, 
                     reverse: bool = False):
            import heapq
            self._heap = []
            self._key = key
            self._reverse = reverse
            self._counter = 0
            
            if items:
                for item in items:
                    self.push(item)
        
        def push(self, item: Any, priority: Any = None) -> 'PriorityQueue':
            """Add item with optional priority."""
            import heapq
            
            if priority is None:
                if self._key:
                    priority = interpreter._call(self._key, [item], None)
                else:
                    priority = item
            
            if self._reverse:
                priority = -priority if isinstance(priority, (int, float)) else priority
            
            heapq.heappush(self._heap, (priority, self._counter, item))
            self._counter += 1
            return self
        
        def pop(self) -> Any:
            """Remove and return highest priority item."""
            import heapq
            if not self._heap:
                return None
            return heapq.heappop(self._heap)[2]
        
        def peek(self) -> Any:
            """Return highest priority item."""
            if not self._heap:
                return None
            return self._heap[0][2]
        
        def size(self) -> int:
            return len(self._heap)
        
        def isEmpty(self) -> bool:
            return len(self._heap) == 0
        
        def __repr__(self):
            return f"PriorityQueue(size={len(self._heap)})"
    
    # ========================================================================
    # LinkedList
    # ========================================================================
    
    class LinkedListNode:
        def __init__(self, value):
            self.value = value
            self.next = None
            self.prev = None
    
    class LinkedList:
        """Doubly linked list."""
        
        def __init__(self, items: List[Any] = None):
            self._head = None
            self._tail = None
            self._size = 0
            
            if items:
                for item in items:
                    self.append(item)
        
        def append(self, value: Any) -> 'LinkedList':
            """Add item to end."""
            node = LinkedListNode(value)
            if not self._head:
                self._head = self._tail = node
            else:
                node.prev = self._tail
                self._tail.next = node
                self._tail = node
            self._size += 1
            return self
        
        def prepend(self, value: Any) -> 'LinkedList':
            """Add item to beginning."""
            node = LinkedListNode(value)
            if not self._head:
                self._head = self._tail = node
            else:
                node.next = self._head
                self._head.prev = node
                self._head = node
            self._size += 1
            return self
        
        def get(self, index: int) -> Any:
            """Get value at index."""
            node = self._getNode(index)
            return node.value if node else None
        
        def set(self, index: int, value: Any) -> bool:
            """Set value at index."""
            node = self._getNode(index)
            if node:
                node.value = value
                return True
            return False
        
        def insert(self, index: int, value: Any) -> bool:
            """Insert value at index."""
            if index <= 0:
                self.prepend(value)
                return True
            if index >= self._size:
                self.append(value)
                return True
            
            existing = self._getNode(index)
            if not existing:
                return False
            
            node = LinkedListNode(value)
            node.prev = existing.prev
            node.next = existing
            existing.prev.next = node
            existing.prev = node
            self._size += 1
            return True
        
        def remove(self, index: int) -> Any:
            """Remove and return value at index."""
            node = self._getNode(index)
            if not node:
                return None
            
            if node.prev:
                node.prev.next = node.next
            else:
                self._head = node.next
            
            if node.next:
                node.next.prev = node.prev
            else:
                self._tail = node.prev
            
            self._size -= 1
            return node.value
        
        def removeValue(self, value: Any) -> bool:
            """Remove first occurrence of value."""
            current = self._head
            while current:
                if current.value == value:
                    if current.prev:
                        current.prev.next = current.next
                    else:
                        self._head = current.next
                    
                    if current.next:
                        current.next.prev = current.prev
                    else:
                        self._tail = current.prev
                    
                    self._size -= 1
                    return True
                current = current.next
            return False
        
        def indexOf(self, value: Any) -> int:
            """Find index of value."""
            current = self._head
            index = 0
            while current:
                if current.value == value:
                    return index
                current = current.next
                index += 1
            return -1
        
        def contains(self, value: Any) -> bool:
            """Check if value exists."""
            return self.indexOf(value) != -1
        
        def head(self) -> Any:
            """Get first value."""
            return self._head.value if self._head else None
        
        def tail(self) -> Any:
            """Get last value."""
            return self._tail.value if self._tail else None
        
        def size(self) -> int:
            return self._size
        
        def isEmpty(self) -> bool:
            return self._size == 0
        
        def clear(self) -> 'LinkedList':
            """Clear the list."""
            self._head = self._tail = None
            self._size = 0
            return self
        
        def reverse(self) -> 'LinkedList':
            """Reverse the list in place."""
            current = self._head
            while current:
                current.prev, current.next = current.next, current.prev
                current = current.prev
            self._head, self._tail = self._tail, self._head
            return self
        
        def toList(self) -> List[Any]:
            """Convert to Python list."""
            result = []
            current = self._head
            while current:
                result.append(current.value)
                current = current.next
            return result
        
        def _getNode(self, index: int):
            """Get node at index."""
            if index < 0 or index >= self._size:
                return None
            
            if index < self._size // 2:
                current = self._head
                for _ in range(index):
                    current = current.next
            else:
                current = self._tail
                for _ in range(self._size - 1 - index):
                    current = current.prev
            
            return current
        
        def __repr__(self):
            return f"LinkedList({self.toList()})"
    
    # ========================================================================
    # Set
    # ========================================================================
    
    class RiftSet:
        """Ordered set implementation."""
        
        def __init__(self, items: List[Any] = None):
            self._items = PyOrderedDict()
            if items:
                for item in items:
                    self.add(item)
        
        def add(self, item: Any) -> 'RiftSet':
            """Add item to set."""
            self._items[item] = True
            return self
        
        def remove(self, item: Any) -> bool:
            """Remove item from set."""
            if item in self._items:
                del self._items[item]
                return True
            return False
        
        def has(self, item: Any) -> bool:
            """Check if item exists."""
            return item in self._items
        
        def size(self) -> int:
            return len(self._items)
        
        def isEmpty(self) -> bool:
            return len(self._items) == 0
        
        def clear(self) -> 'RiftSet':
            """Clear the set."""
            self._items = PyOrderedDict()
            return self
        
        def union(self, other: 'RiftSet') -> 'RiftSet':
            """Return union of sets."""
            result = RiftSet(self.toList())
            for item in other.toList():
                result.add(item)
            return result
        
        def intersection(self, other: 'RiftSet') -> 'RiftSet':
            """Return intersection of sets."""
            result = RiftSet()
            for item in self._items:
                if other.has(item):
                    result.add(item)
            return result
        
        def difference(self, other: 'RiftSet') -> 'RiftSet':
            """Return difference of sets."""
            result = RiftSet()
            for item in self._items:
                if not other.has(item):
                    result.add(item)
            return result
        
        def symmetricDifference(self, other: 'RiftSet') -> 'RiftSet':
            """Return symmetric difference."""
            return self.difference(other).union(other.difference(self))
        
        def isSubset(self, other: 'RiftSet') -> bool:
            """Check if this is subset of other."""
            for item in self._items:
                if not other.has(item):
                    return False
            return True
        
        def isSuperset(self, other: 'RiftSet') -> bool:
            """Check if this is superset of other."""
            return other.isSubset(self)
        
        def toList(self) -> List[Any]:
            return list(self._items.keys())
        
        def __repr__(self):
            return f"Set({self.toList()})"
    
    # ========================================================================
    # Map (OrderedDict-like)
    # ========================================================================
    
    class RiftMap:
        """Ordered map/dictionary."""
        
        def __init__(self, items: Dict[str, Any] = None):
            self._items = PyOrderedDict()
            if items:
                for key, value in items.items():
                    self._items[key] = value
        
        def set(self, key: Any, value: Any) -> 'RiftMap':
            """Set key-value pair."""
            self._items[key] = value
            return self
        
        def get(self, key: Any, default: Any = None) -> Any:
            """Get value by key."""
            return self._items.get(key, default)
        
        def has(self, key: Any) -> bool:
            """Check if key exists."""
            return key in self._items
        
        def remove(self, key: Any) -> bool:
            """Remove key."""
            if key in self._items:
                del self._items[key]
                return True
            return False
        
        def keys(self) -> List[Any]:
            """Get all keys."""
            return list(self._items.keys())
        
        def values(self) -> List[Any]:
            """Get all values."""
            return list(self._items.values())
        
        def entries(self) -> List[List[Any]]:
            """Get all entries as [key, value] pairs."""
            return [[k, v] for k, v in self._items.items()]
        
        def size(self) -> int:
            return len(self._items)
        
        def isEmpty(self) -> bool:
            return len(self._items) == 0
        
        def clear(self) -> 'RiftMap':
            """Clear the map."""
            self._items = PyOrderedDict()
            return self
        
        def forEach(self, callback: Callable) -> None:
            """Iterate over entries."""
            for key, value in self._items.items():
                interpreter._call(callback, [key, value], None)
        
        def map(self, mapper: Callable) -> 'RiftMap':
            """Map values."""
            result = RiftMap()
            for key, value in self._items.items():
                result.set(key, interpreter._call(mapper, [value, key], None))
            return result
        
        def filter(self, predicate: Callable) -> 'RiftMap':
            """Filter entries."""
            result = RiftMap()
            for key, value in self._items.items():
                if interpreter._call(predicate, [value, key], None):
                    result.set(key, value)
            return result
        
        def toDict(self) -> Dict[str, Any]:
            return dict(self._items)
        
        def __repr__(self):
            return f"Map({dict(self._items)})"
    
    # ========================================================================
    # Counter
    # ========================================================================
    
    class Counter:
        """Count occurrences of items."""
        
        def __init__(self, items: List[Any] = None):
            self._counts = {}
            if items:
                for item in items:
                    self.add(item)
        
        def add(self, item: Any, count: int = 1) -> 'Counter':
            """Add item with count."""
            self._counts[item] = self._counts.get(item, 0) + count
            return self
        
        def subtract(self, item: Any, count: int = 1) -> 'Counter':
            """Subtract count from item."""
            if item in self._counts:
                self._counts[item] = max(0, self._counts[item] - count)
                if self._counts[item] == 0:
                    del self._counts[item]
            return self
        
        def count(self, item: Any) -> int:
            """Get count of item."""
            return self._counts.get(item, 0)
        
        def mostCommon(self, n: int = None) -> List[List[Any]]:
            """Get n most common items."""
            sorted_items = sorted(self._counts.items(), key=lambda x: -x[1])
            if n:
                sorted_items = sorted_items[:n]
            return [[k, v] for k, v in sorted_items]
        
        def leastCommon(self, n: int = None) -> List[List[Any]]:
            """Get n least common items."""
            sorted_items = sorted(self._counts.items(), key=lambda x: x[1])
            if n:
                sorted_items = sorted_items[:n]
            return [[k, v] for k, v in sorted_items]
        
        def elements(self) -> List[Any]:
            """Return all elements repeated by count."""
            result = []
            for item, count in self._counts.items():
                result.extend([item] * count)
            return result
        
        def total(self) -> int:
            """Return total count."""
            return sum(self._counts.values())
        
        def toDict(self) -> Dict[Any, int]:
            return dict(self._counts)
        
        def __repr__(self):
            return f"Counter({self._counts})"
    
    # ========================================================================
    # DefaultDict
    # ========================================================================
    
    class DefaultDict:
        """Dictionary with default value factory."""
        
        def __init__(self, default_factory: Callable):
            self._items = {}
            self._factory = default_factory
        
        def get(self, key: Any) -> Any:
            """Get value, creating with factory if missing."""
            if key not in self._items:
                self._items[key] = interpreter._call(self._factory, [], None)
            return self._items[key]
        
        def set(self, key: Any, value: Any) -> 'DefaultDict':
            """Set value."""
            self._items[key] = value
            return self
        
        def has(self, key: Any) -> bool:
            return key in self._items
        
        def keys(self) -> List[Any]:
            return list(self._items.keys())
        
        def values(self) -> List[Any]:
            return list(self._items.values())
        
        def toDict(self) -> Dict[Any, Any]:
            return dict(self._items)
        
        def __repr__(self):
            return f"DefaultDict({self._items})"
    
    # ========================================================================
    # TreeNode (for Tree operations)
    # ========================================================================
    
    class TreeNode:
        """Tree node for hierarchical data."""
        
        def __init__(self, value: Any, children: List['TreeNode'] = None):
            self.value = value
            self.children = children or []
            self.parent = None
            
            for child in self.children:
                child.parent = self
        
        def addChild(self, value: Any) -> 'TreeNode':
            """Add child node."""
            child = TreeNode(value)
            child.parent = self
            self.children.append(child)
            return child
        
        def removeChild(self, child: 'TreeNode') -> bool:
            """Remove child node."""
            if child in self.children:
                child.parent = None
                self.children.remove(child)
                return True
            return False
        
        def isRoot(self) -> bool:
            """Check if node is root."""
            return self.parent is None
        
        def isLeaf(self) -> bool:
            """Check if node is leaf."""
            return len(self.children) == 0
        
        def depth(self) -> int:
            """Get depth from root."""
            d = 0
            node = self
            while node.parent:
                d += 1
                node = node.parent
            return d
        
        def height(self) -> int:
            """Get height of subtree."""
            if not self.children:
                return 0
            return 1 + max(child.height() for child in self.children)
        
        def traverse(self, order: str = 'pre') -> List[Any]:
            """Traverse tree (pre, post, breadth)."""
            result = []
            
            if order == 'pre':
                result.append(self.value)
                for child in self.children:
                    result.extend(child.traverse('pre'))
            elif order == 'post':
                for child in self.children:
                    result.extend(child.traverse('post'))
                result.append(self.value)
            elif order == 'breadth':
                queue = [self]
                while queue:
                    node = queue.pop(0)
                    result.append(node.value)
                    queue.extend(node.children)
            
            return result
        
        def find(self, value: Any) -> Optional['TreeNode']:
            """Find node with value."""
            if self.value == value:
                return self
            for child in self.children:
                found = child.find(value)
                if found:
                    return found
            return None
        
        def toDict(self) -> Dict[str, Any]:
            """Convert to dict representation."""
            return {
                'value': self.value,
                'children': [child.toDict() for child in self.children]
            }
        
        def __repr__(self):
            return f"TreeNode({self.value}, children={len(self.children)})"
    
    # ========================================================================
    # LRU Cache
    # ========================================================================
    
    class LRUCache:
        """Least Recently Used cache."""
        
        def __init__(self, capacity: int):
            self._capacity = capacity
            self._cache = PyOrderedDict()
        
        def get(self, key: Any) -> Any:
            """Get value (moves to end if found)."""
            if key not in self._cache:
                return None
            self._cache.move_to_end(key)
            return self._cache[key]
        
        def set(self, key: Any, value: Any) -> 'LRUCache':
            """Set value (evicts oldest if at capacity)."""
            if key in self._cache:
                self._cache.move_to_end(key)
            else:
                if len(self._cache) >= self._capacity:
                    self._cache.popitem(last=False)
            self._cache[key] = value
            return self
        
        def has(self, key: Any) -> bool:
            return key in self._cache
        
        def remove(self, key: Any) -> bool:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
        
        def size(self) -> int:
            return len(self._cache)
        
        def clear(self) -> 'LRUCache':
            self._cache = PyOrderedDict()
            return self
        
        def __repr__(self):
            return f"LRUCache(capacity={self._capacity}, size={len(self._cache)})"
    
    # ========================================================================
    # Module Exports
    # ========================================================================
    
    def create_stack(items: List[Any] = None) -> Stack:
        return Stack(items)
    
    def create_queue(items: List[Any] = None) -> Queue:
        return Queue(items)
    
    def create_deque(items: List[Any] = None) -> Deque:
        return Deque(items)
    
    def create_priority_queue(items: List[Any] = None, key: Callable = None,
                              reverse: bool = False) -> PriorityQueue:
        return PriorityQueue(items, key, reverse)
    
    def create_linked_list(items: List[Any] = None) -> LinkedList:
        return LinkedList(items)
    
    def create_set(items: List[Any] = None) -> RiftSet:
        return RiftSet(items)
    
    def create_map(items: Dict[str, Any] = None) -> RiftMap:
        return RiftMap(items)
    
    def create_counter(items: List[Any] = None) -> Counter:
        return Counter(items)
    
    def create_default_dict(factory: Callable) -> DefaultDict:
        return DefaultDict(factory)
    
    def create_tree(value: Any) -> TreeNode:
        return TreeNode(value)
    
    def create_lru_cache(capacity: int) -> LRUCache:
        return LRUCache(capacity)
    
    return {
        'Stack': create_stack,
        'Queue': create_queue,
        'Deque': create_deque,
        'PriorityQueue': create_priority_queue,
        'LinkedList': create_linked_list,
        'Set': create_set,
        'Map': create_map,
        'Counter': create_counter,
        'DefaultDict': create_default_dict,
        'Tree': create_tree,
        'LRUCache': create_lru_cache,
    }
