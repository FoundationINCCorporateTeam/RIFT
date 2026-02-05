"""
RIFT Standard Library - Array Module

Comprehensive array/list manipulation utilities.
"""

from typing import Any, Dict, List, Optional, Callable, Union
from functools import reduce as functools_reduce


def create_array_module(interpreter) -> Dict[str, Any]:
    """Create the array module for RIFT."""
    
    # ========================================================================
    # Creation
    # ========================================================================
    
    def arr_create(length: int, fill_value: Any = None) -> List[Any]:
        """Create array of specified length filled with value."""
        return [fill_value] * length
    
    def arr_range(start: int, end: int = None, step: int = 1) -> List[int]:
        """Create array from range."""
        if end is None:
            end = start
            start = 0
        return list(range(start, end, step))
    
    def arr_from_iterable(iterable) -> List[Any]:
        """Create array from any iterable."""
        return list(iterable)
    
    def arr_of(*items) -> List[Any]:
        """Create array from arguments."""
        return list(items)
    
    def arr_repeat(item: Any, count: int) -> List[Any]:
        """Create array by repeating item."""
        return [item] * count
    
    def arr_generate(length: int, generator: Callable) -> List[Any]:
        """Generate array using a function."""
        return [interpreter._call(generator, [i], None) for i in range(length)]
    
    # ========================================================================
    # Access
    # ========================================================================
    
    def arr_get(arr: List[Any], index: int, default: Any = None) -> Any:
        """Get item at index with optional default."""
        if 0 <= index < len(arr) or -len(arr) <= index < 0:
            return arr[index]
        return default
    
    def arr_first(arr: List[Any], default: Any = None) -> Any:
        """Get first item."""
        return arr[0] if arr else default
    
    def arr_last(arr: List[Any], default: Any = None) -> Any:
        """Get last item."""
        return arr[-1] if arr else default
    
    def arr_nth(arr: List[Any], n: int, default: Any = None) -> Any:
        """Get nth item (1-indexed)."""
        index = n - 1 if n > 0 else n
        if 0 <= index < len(arr) or -len(arr) <= index < 0:
            return arr[index]
        return default
    
    def arr_head(arr: List[Any], count: int = 1) -> List[Any]:
        """Get first n items."""
        return arr[:count]
    
    def arr_tail(arr: List[Any], count: int = 1) -> List[Any]:
        """Get last n items."""
        return arr[-count:] if count > 0 else []
    
    def arr_initial(arr: List[Any]) -> List[Any]:
        """Get all items except the last."""
        return arr[:-1] if arr else []
    
    def arr_rest(arr: List[Any]) -> List[Any]:
        """Get all items except the first."""
        return arr[1:] if arr else []
    
    # ========================================================================
    # Modification (returning new arrays)
    # ========================================================================
    
    def arr_push(arr: List[Any], *items) -> List[Any]:
        """Add items to end (returns new array)."""
        return arr + list(items)
    
    def arr_unshift(arr: List[Any], *items) -> List[Any]:
        """Add items to beginning (returns new array)."""
        return list(items) + arr
    
    def arr_insert(arr: List[Any], index: int, *items) -> List[Any]:
        """Insert items at index (returns new array)."""
        return arr[:index] + list(items) + arr[index:]
    
    def arr_remove_at(arr: List[Any], index: int) -> List[Any]:
        """Remove item at index (returns new array)."""
        return arr[:index] + arr[index + 1:]
    
    def arr_remove_item(arr: List[Any], item: Any) -> List[Any]:
        """Remove first occurrence of item (returns new array)."""
        result = arr.copy()
        try:
            result.remove(item)
        except ValueError:
            pass
        return result
    
    def arr_remove_all(arr: List[Any], item: Any) -> List[Any]:
        """Remove all occurrences of item."""
        return [x for x in arr if x != item]
    
    def arr_replace(arr: List[Any], index: int, item: Any) -> List[Any]:
        """Replace item at index (returns new array)."""
        result = arr.copy()
        if 0 <= index < len(result):
            result[index] = item
        return result
    
    def arr_swap(arr: List[Any], i: int, j: int) -> List[Any]:
        """Swap items at indices (returns new array)."""
        result = arr.copy()
        if 0 <= i < len(result) and 0 <= j < len(result):
            result[i], result[j] = result[j], result[i]
        return result
    
    def arr_move(arr: List[Any], from_index: int, to_index: int) -> List[Any]:
        """Move item from one index to another (returns new array)."""
        result = arr.copy()
        if 0 <= from_index < len(result):
            item = result.pop(from_index)
            result.insert(to_index, item)
        return result
    
    def arr_rotate(arr: List[Any], n: int = 1) -> List[Any]:
        """Rotate array by n positions."""
        if not arr:
            return arr
        n = n % len(arr)
        return arr[-n:] + arr[:-n]
    
    def arr_shuffle(arr: List[Any]) -> List[Any]:
        """Shuffle array randomly (returns new array)."""
        import random
        result = arr.copy()
        random.shuffle(result)
        return result
    
    # ========================================================================
    # Slicing
    # ========================================================================
    
    def arr_slice(arr: List[Any], start: int = 0, end: int = None) -> List[Any]:
        """Get slice of array."""
        if end is None:
            return arr[start:]
        return arr[start:end]
    
    def arr_splice(arr: List[Any], start: int, delete_count: int = 0, 
                   *items) -> Dict[str, List[Any]]:
        """Remove/replace items and return both removed items and new array."""
        removed = arr[start:start + delete_count]
        new_arr = arr[:start] + list(items) + arr[start + delete_count:]
        return {'removed': removed, 'array': new_arr}
    
    def arr_chunk(arr: List[Any], size: int) -> List[List[Any]]:
        """Split array into chunks of specified size."""
        return [arr[i:i + size] for i in range(0, len(arr), size)]
    
    def arr_partition(arr: List[Any], predicate: Callable) -> List[List[Any]]:
        """Split array into two arrays based on predicate."""
        truthy = []
        falsy = []
        for item in arr:
            if interpreter._call(predicate, [item], None):
                truthy.append(item)
            else:
                falsy.append(item)
        return [truthy, falsy]
    
    def arr_split_at(arr: List[Any], index: int) -> List[List[Any]]:
        """Split array at index."""
        return [arr[:index], arr[index:]]
    
    def arr_take_while(arr: List[Any], predicate: Callable) -> List[Any]:
        """Take items while predicate is true."""
        result = []
        for item in arr:
            if interpreter._call(predicate, [item], None):
                result.append(item)
            else:
                break
        return result
    
    def arr_drop_while(arr: List[Any], predicate: Callable) -> List[Any]:
        """Drop items while predicate is true."""
        for i, item in enumerate(arr):
            if not interpreter._call(predicate, [item], None):
                return arr[i:]
        return []
    
    # ========================================================================
    # Searching
    # ========================================================================
    
    def arr_index_of(arr: List[Any], item: Any, start: int = 0) -> int:
        """Find first index of item (-1 if not found)."""
        try:
            return arr.index(item, start)
        except ValueError:
            return -1
    
    def arr_last_index_of(arr: List[Any], item: Any) -> int:
        """Find last index of item (-1 if not found)."""
        for i in range(len(arr) - 1, -1, -1):
            if arr[i] == item:
                return i
        return -1
    
    def arr_find(arr: List[Any], predicate: Callable) -> Any:
        """Find first item matching predicate (None if not found)."""
        for item in arr:
            if interpreter._call(predicate, [item], None):
                return item
        return None
    
    def arr_find_last(arr: List[Any], predicate: Callable) -> Any:
        """Find last item matching predicate."""
        for item in reversed(arr):
            if interpreter._call(predicate, [item], None):
                return item
        return None
    
    def arr_find_index(arr: List[Any], predicate: Callable) -> int:
        """Find index of first item matching predicate."""
        for i, item in enumerate(arr):
            if interpreter._call(predicate, [item], None):
                return i
        return -1
    
    def arr_find_last_index(arr: List[Any], predicate: Callable) -> int:
        """Find index of last item matching predicate."""
        for i in range(len(arr) - 1, -1, -1):
            if interpreter._call(predicate, [arr[i]], None):
                return i
        return -1
    
    def arr_find_all(arr: List[Any], predicate: Callable) -> List[Any]:
        """Find all items matching predicate."""
        return [item for item in arr if interpreter._call(predicate, [item], None)]
    
    def arr_find_indices(arr: List[Any], predicate: Callable) -> List[int]:
        """Find all indices of items matching predicate."""
        return [i for i, item in enumerate(arr) 
                if interpreter._call(predicate, [item], None)]
    
    def arr_binary_search(arr: List[Any], item: Any) -> int:
        """Binary search in sorted array (returns index or -1)."""
        import bisect
        i = bisect.bisect_left(arr, item)
        if i != len(arr) and arr[i] == item:
            return i
        return -1
    
    # ========================================================================
    # Testing
    # ========================================================================
    
    def arr_includes(arr: List[Any], item: Any) -> bool:
        """Check if array contains item."""
        return item in arr
    
    def arr_includes_all(arr: List[Any], items: List[Any]) -> bool:
        """Check if array contains all items."""
        return all(item in arr for item in items)
    
    def arr_includes_any(arr: List[Any], items: List[Any]) -> bool:
        """Check if array contains any of the items."""
        return any(item in arr for item in items)
    
    def arr_every(arr: List[Any], predicate: Callable) -> bool:
        """Check if all items pass predicate."""
        return all(interpreter._call(predicate, [item], None) for item in arr)
    
    def arr_some(arr: List[Any], predicate: Callable) -> bool:
        """Check if any item passes predicate."""
        return any(interpreter._call(predicate, [item], None) for item in arr)
    
    def arr_none(arr: List[Any], predicate: Callable) -> bool:
        """Check if no items pass predicate."""
        return not any(interpreter._call(predicate, [item], None) for item in arr)
    
    def arr_is_empty(arr: List[Any]) -> bool:
        """Check if array is empty."""
        return len(arr) == 0
    
    def arr_is_sorted(arr: List[Any], key: Callable = None) -> bool:
        """Check if array is sorted."""
        if key:
            arr = [interpreter._call(key, [item], None) for item in arr]
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    
    def arr_is_unique(arr: List[Any]) -> bool:
        """Check if all items are unique."""
        try:
            return len(arr) == len(set(arr))
        except TypeError:
            # For unhashable items
            seen = []
            for item in arr:
                if item in seen:
                    return False
                seen.append(item)
            return True
    
    # ========================================================================
    # Transformation
    # ========================================================================
    
    def arr_map(arr: List[Any], mapper: Callable) -> List[Any]:
        """Map each item through function."""
        return [interpreter._call(mapper, [item], None) for item in arr]
    
    def arr_map_indexed(arr: List[Any], mapper: Callable) -> List[Any]:
        """Map with index: mapper(item, index)."""
        return [interpreter._call(mapper, [item, i], None) for i, item in enumerate(arr)]
    
    def arr_filter(arr: List[Any], predicate: Callable) -> List[Any]:
        """Filter items by predicate."""
        return [item for item in arr if interpreter._call(predicate, [item], None)]
    
    def arr_reject(arr: List[Any], predicate: Callable) -> List[Any]:
        """Reject items matching predicate."""
        return [item for item in arr if not interpreter._call(predicate, [item], None)]
    
    def arr_reduce(arr: List[Any], reducer: Callable, initial: Any = None) -> Any:
        """Reduce array to single value."""
        if not arr:
            return initial
        
        if initial is None:
            result = arr[0]
            items = arr[1:]
        else:
            result = initial
            items = arr
        
        for item in items:
            result = interpreter._call(reducer, [result, item], None)
        
        return result
    
    def arr_reduce_right(arr: List[Any], reducer: Callable, 
                         initial: Any = None) -> Any:
        """Reduce array from right."""
        return arr_reduce(list(reversed(arr)), reducer, initial)
    
    def arr_flat(arr: List[Any], depth: int = 1) -> List[Any]:
        """Flatten nested arrays to specified depth."""
        result = []
        for item in arr:
            if isinstance(item, list) and depth > 0:
                result.extend(arr_flat(item, depth - 1))
            else:
                result.append(item)
        return result
    
    def arr_flat_map(arr: List[Any], mapper: Callable) -> List[Any]:
        """Map then flatten by one level."""
        return arr_flat(arr_map(arr, mapper), 1)
    
    def arr_reverse(arr: List[Any]) -> List[Any]:
        """Reverse array."""
        return arr[::-1]
    
    def arr_sort(arr: List[Any], key: Callable = None, 
                 descending: bool = False) -> List[Any]:
        """Sort array."""
        if key:
            key_func = lambda x: interpreter._call(key, [x], None)
            return sorted(arr, key=key_func, reverse=descending)
        return sorted(arr, reverse=descending)
    
    def arr_sort_by(arr: List[Any], key: str, descending: bool = False) -> List[Any]:
        """Sort array of objects by key."""
        return sorted(arr, key=lambda x: x.get(key) if isinstance(x, dict) else getattr(x, key, None), 
                     reverse=descending)
    
    def arr_group_by(arr: List[Any], key: Union[str, Callable]) -> Dict[Any, List[Any]]:
        """Group array items by key."""
        groups = {}
        for item in arr:
            if callable(key) or hasattr(key, '__call__'):
                group_key = interpreter._call(key, [item], None)
            elif isinstance(item, dict):
                group_key = item.get(key)
            else:
                group_key = getattr(item, key, None)
            
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(item)
        return groups
    
    def arr_count_by(arr: List[Any], key: Union[str, Callable]) -> Dict[Any, int]:
        """Count items by key."""
        groups = arr_group_by(arr, key)
        return {k: len(v) for k, v in groups.items()}
    
    def arr_key_by(arr: List[Any], key: str) -> Dict[Any, Any]:
        """Create map from array using key."""
        result = {}
        for item in arr:
            if isinstance(item, dict):
                key_val = item.get(key)
            else:
                key_val = getattr(item, key, None)
            if key_val is not None:
                result[key_val] = item
        return result
    
    # ========================================================================
    # Aggregation
    # ========================================================================
    
    def arr_sum(arr: List[Union[int, float]]) -> Union[int, float]:
        """Sum all items."""
        return sum(arr)
    
    def arr_product(arr: List[Union[int, float]]) -> Union[int, float]:
        """Multiply all items."""
        result = 1
        for item in arr:
            result *= item
        return result
    
    def arr_min(arr: List[Any], key: Callable = None) -> Any:
        """Get minimum item."""
        if not arr:
            return None
        if key:
            return min(arr, key=lambda x: interpreter._call(key, [x], None))
        return min(arr)
    
    def arr_max(arr: List[Any], key: Callable = None) -> Any:
        """Get maximum item."""
        if not arr:
            return None
        if key:
            return max(arr, key=lambda x: interpreter._call(key, [x], None))
        return max(arr)
    
    def arr_mean(arr: List[Union[int, float]]) -> float:
        """Calculate mean."""
        if not arr:
            return 0.0
        return sum(arr) / len(arr)
    
    def arr_count(arr: List[Any], predicate: Callable = None) -> int:
        """Count items (optionally matching predicate)."""
        if predicate is None:
            return len(arr)
        return sum(1 for item in arr if interpreter._call(predicate, [item], None))
    
    # ========================================================================
    # Set Operations
    # ========================================================================
    
    def arr_unique(arr: List[Any]) -> List[Any]:
        """Get unique items (preserving order)."""
        seen = set()
        result = []
        for item in arr:
            try:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            except TypeError:
                # For unhashable items
                if item not in result:
                    result.append(item)
        return result
    
    def arr_unique_by(arr: List[Any], key: Union[str, Callable]) -> List[Any]:
        """Get unique items by key."""
        seen = set()
        result = []
        for item in arr:
            if callable(key) or hasattr(key, '__call__'):
                k = interpreter._call(key, [item], None)
            elif isinstance(item, dict):
                k = item.get(key)
            else:
                k = getattr(item, key, None)
            
            if k not in seen:
                seen.add(k)
                result.append(item)
        return result
    
    def arr_union(arr1: List[Any], arr2: List[Any]) -> List[Any]:
        """Union of two arrays."""
        return arr_unique(arr1 + arr2)
    
    def arr_intersection(arr1: List[Any], arr2: List[Any]) -> List[Any]:
        """Intersection of two arrays."""
        set2 = set(arr2)
        return [x for x in arr1 if x in set2]
    
    def arr_difference(arr1: List[Any], arr2: List[Any]) -> List[Any]:
        """Items in arr1 but not in arr2."""
        set2 = set(arr2)
        return [x for x in arr1 if x not in set2]
    
    def arr_symmetric_difference(arr1: List[Any], arr2: List[Any]) -> List[Any]:
        """Items in either but not both."""
        set1, set2 = set(arr1), set(arr2)
        return list((set1 - set2) | (set2 - set1))
    
    # ========================================================================
    # Combination
    # ========================================================================
    
    def arr_concat(*arrays) -> List[Any]:
        """Concatenate multiple arrays."""
        result = []
        for arr in arrays:
            result.extend(arr)
        return result
    
    def arr_zip(*arrays) -> List[List[Any]]:
        """Zip multiple arrays together."""
        return [list(t) for t in zip(*arrays)]
    
    def arr_zip_longest(*arrays, fill_value=None) -> List[List[Any]]:
        """Zip with fill for shorter arrays."""
        from itertools import zip_longest
        return [list(t) for t in zip_longest(*arrays, fillvalue=fill_value)]
    
    def arr_unzip(arr: List[List[Any]]) -> List[List[Any]]:
        """Unzip array of arrays."""
        if not arr:
            return []
        return [list(t) for t in zip(*arr)]
    
    def arr_cartesian(*arrays) -> List[List[Any]]:
        """Cartesian product of arrays."""
        from itertools import product
        return [list(t) for t in product(*arrays)]
    
    def arr_interleave(*arrays) -> List[Any]:
        """Interleave multiple arrays."""
        result = []
        max_len = max(len(arr) for arr in arrays) if arrays else 0
        for i in range(max_len):
            for arr in arrays:
                if i < len(arr):
                    result.append(arr[i])
        return result
    
    # ========================================================================
    # Iteration Utilities
    # ========================================================================
    
    def arr_for_each(arr: List[Any], callback: Callable) -> None:
        """Execute callback for each item."""
        for item in arr:
            interpreter._call(callback, [item], None)
    
    def arr_for_each_indexed(arr: List[Any], callback: Callable) -> None:
        """Execute callback with index for each item."""
        for i, item in enumerate(arr):
            interpreter._call(callback, [item, i], None)
    
    def arr_enumerate(arr: List[Any], start: int = 0) -> List[List[Any]]:
        """Return array of [index, item] pairs."""
        return [[i, item] for i, item in enumerate(arr, start)]
    
    def arr_window(arr: List[Any], size: int) -> List[List[Any]]:
        """Sliding window over array."""
        return [arr[i:i + size] for i in range(len(arr) - size + 1)]
    
    def arr_pairs(arr: List[Any]) -> List[List[Any]]:
        """Return consecutive pairs."""
        return [[arr[i], arr[i + 1]] for i in range(len(arr) - 1)]
    
    def arr_triplets(arr: List[Any]) -> List[List[Any]]:
        """Return consecutive triplets."""
        return [[arr[i], arr[i + 1], arr[i + 2]] for i in range(len(arr) - 2)]
    
    # ========================================================================
    # Sampling
    # ========================================================================
    
    def arr_sample(arr: List[Any]) -> Any:
        """Get random item."""
        import random
        return random.choice(arr) if arr else None
    
    def arr_sample_size(arr: List[Any], n: int) -> List[Any]:
        """Get n random items."""
        import random
        return random.sample(arr, min(n, len(arr)))
    
    # ========================================================================
    # Conversion
    # ========================================================================
    
    def arr_to_dict(arr: List[List[Any]]) -> Dict[Any, Any]:
        """Convert array of [key, value] pairs to dict."""
        return {item[0]: item[1] for item in arr if len(item) >= 2}
    
    def arr_to_set(arr: List[Any]) -> set:
        """Convert array to set."""
        return set(arr)
    
    def arr_to_string(arr: List[Any], separator: str = ',') -> str:
        """Join array items as string."""
        return separator.join(str(item) for item in arr)
    
    def arr_compact(arr: List[Any]) -> List[Any]:
        """Remove falsy values (None, False, 0, '', [], {})."""
        return [item for item in arr if item]
    
    def arr_without_none(arr: List[Any]) -> List[Any]:
        """Remove only None values."""
        return [item for item in arr if item is not None]
    
    return {
        # Creation
        'create': arr_create,
        'range': arr_range,
        'fromIterable': arr_from_iterable,
        'of': arr_of,
        'repeat': arr_repeat,
        'generate': arr_generate,
        
        # Access
        'get': arr_get,
        'first': arr_first,
        'last': arr_last,
        'nth': arr_nth,
        'head': arr_head,
        'tail': arr_tail,
        'initial': arr_initial,
        'rest': arr_rest,
        
        # Modification
        'push': arr_push,
        'unshift': arr_unshift,
        'insert': arr_insert,
        'removeAt': arr_remove_at,
        'removeItem': arr_remove_item,
        'removeAll': arr_remove_all,
        'replace': arr_replace,
        'swap': arr_swap,
        'move': arr_move,
        'rotate': arr_rotate,
        'shuffle': arr_shuffle,
        
        # Slicing
        'slice': arr_slice,
        'splice': arr_splice,
        'chunk': arr_chunk,
        'partition': arr_partition,
        'splitAt': arr_split_at,
        'takeWhile': arr_take_while,
        'dropWhile': arr_drop_while,
        
        # Searching
        'indexOf': arr_index_of,
        'lastIndexOf': arr_last_index_of,
        'find': arr_find,
        'findLast': arr_find_last,
        'findIndex': arr_find_index,
        'findLastIndex': arr_find_last_index,
        'findAll': arr_find_all,
        'findIndices': arr_find_indices,
        'binarySearch': arr_binary_search,
        
        # Testing
        'includes': arr_includes,
        'includesAll': arr_includes_all,
        'includesAny': arr_includes_any,
        'every': arr_every,
        'some': arr_some,
        'none': arr_none,
        'isEmpty': arr_is_empty,
        'isSorted': arr_is_sorted,
        'isUnique': arr_is_unique,
        
        # Transformation
        'map': arr_map,
        'mapIndexed': arr_map_indexed,
        'filter': arr_filter,
        'reject': arr_reject,
        'reduce': arr_reduce,
        'reduceRight': arr_reduce_right,
        'flat': arr_flat,
        'flatMap': arr_flat_map,
        'reverse': arr_reverse,
        'sort': arr_sort,
        'sortBy': arr_sort_by,
        'groupBy': arr_group_by,
        'countBy': arr_count_by,
        'keyBy': arr_key_by,
        
        # Aggregation
        'sum': arr_sum,
        'product': arr_product,
        'min': arr_min,
        'max': arr_max,
        'mean': arr_mean,
        'count': arr_count,
        
        # Set Operations
        'unique': arr_unique,
        'uniqueBy': arr_unique_by,
        'union': arr_union,
        'intersection': arr_intersection,
        'difference': arr_difference,
        'symmetricDifference': arr_symmetric_difference,
        
        # Combination
        'concat': arr_concat,
        'zip': arr_zip,
        'zipLongest': arr_zip_longest,
        'unzip': arr_unzip,
        'cartesian': arr_cartesian,
        'interleave': arr_interleave,
        
        # Iteration
        'forEach': arr_for_each,
        'forEachIndexed': arr_for_each_indexed,
        'enumerate': arr_enumerate,
        'window': arr_window,
        'pairs': arr_pairs,
        'triplets': arr_triplets,
        
        # Sampling
        'sample': arr_sample,
        'sampleSize': arr_sample_size,
        
        # Conversion
        'toDict': arr_to_dict,
        'toSet': arr_to_set,
        'toString': arr_to_string,
        'compact': arr_compact,
        'withoutNone': arr_without_none,
    }
