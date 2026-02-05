"""
RIFT Standard Library - Async Module

Async/await utilities and promise-like patterns.
"""

import asyncio
import threading
import concurrent.futures
from typing import Any, Dict, List, Optional, Callable, Union
from functools import partial
import time


def create_async_module(interpreter) -> Dict[str, Any]:
    """Create the async module for RIFT."""
    
    # ========================================================================
    # Promise-like Future
    # ========================================================================
    
    class RiftPromise:
        """Promise-like async wrapper."""
        
        def __init__(self, executor: Callable = None):
            self._state = 'pending'
            self._value = None
            self._error = None
            self._then_callbacks: List[Callable] = []
            self._catch_callbacks: List[Callable] = []
            self._finally_callbacks: List[Callable] = []
            self._lock = threading.Lock()
            
            if executor:
                try:
                    executor(self._resolve, self._reject)
                except Exception as e:
                    self._reject(e)
        
        def _resolve(self, value: Any) -> None:
            """Resolve the promise."""
            with self._lock:
                if self._state != 'pending':
                    return
                
                # Handle promise chaining
                if isinstance(value, RiftPromise):
                    value.then(self._resolve).catch(self._reject)
                    return
                
                self._state = 'fulfilled'
                self._value = value
                
                for callback in self._then_callbacks:
                    self._execute_callback(callback, value)
                
                for callback in self._finally_callbacks:
                    self._execute_callback(callback)
        
        def _reject(self, error: Any) -> None:
            """Reject the promise."""
            with self._lock:
                if self._state != 'pending':
                    return
                
                self._state = 'rejected'
                self._error = error
                
                for callback in self._catch_callbacks:
                    self._execute_callback(callback, error)
                
                for callback in self._finally_callbacks:
                    self._execute_callback(callback)
        
        def _execute_callback(self, callback: Callable, *args) -> None:
            """Execute callback in thread pool."""
            threading.Thread(target=lambda: interpreter._call(callback, list(args), None)).start()
        
        def then(self, callback: Callable) -> 'RiftPromise':
            """Add success callback."""
            with self._lock:
                if self._state == 'pending':
                    self._then_callbacks.append(callback)
                elif self._state == 'fulfilled':
                    self._execute_callback(callback, self._value)
            return self
        
        def catch(self, callback: Callable) -> 'RiftPromise':
            """Add error callback."""
            with self._lock:
                if self._state == 'pending':
                    self._catch_callbacks.append(callback)
                elif self._state == 'rejected':
                    self._execute_callback(callback, self._error)
            return self
        
        def finally_(self, callback: Callable) -> 'RiftPromise':
            """Add finally callback."""
            with self._lock:
                if self._state == 'pending':
                    self._finally_callbacks.append(callback)
                else:
                    self._execute_callback(callback)
            return self
        
        def await_(self, timeout: float = None) -> Any:
            """Block until resolved (for sync contexts)."""
            start = time.time()
            while self._state == 'pending':
                if timeout and (time.time() - start) > timeout:
                    raise TimeoutError("Promise await timeout")
                time.sleep(0.001)
            
            if self._state == 'rejected':
                raise Exception(self._error)
            
            return self._value
        
        @property
        def state(self) -> str:
            return self._state
        
        @property
        def value(self) -> Any:
            return self._value
        
        def __repr__(self):
            return f"Promise({self._state})"
    
    # ========================================================================
    # Promise Static Methods
    # ========================================================================
    
    def promise_resolve(value: Any) -> RiftPromise:
        """Create resolved promise."""
        promise = RiftPromise()
        promise._resolve(value)
        return promise
    
    def promise_reject(error: Any) -> RiftPromise:
        """Create rejected promise."""
        promise = RiftPromise()
        promise._reject(error)
        return promise
    
    def promise_all(promises: List[RiftPromise]) -> RiftPromise:
        """Wait for all promises to resolve."""
        def executor(resolve, reject):
            results = [None] * len(promises)
            completed = [0]
            rejected = [False]
            
            def on_resolve(index, value):
                if rejected[0]:
                    return
                results[index] = value
                completed[0] += 1
                if completed[0] == len(promises):
                    resolve(results)
            
            def on_reject(error):
                if not rejected[0]:
                    rejected[0] = True
                    reject(error)
            
            if not promises:
                resolve([])
                return
            
            for i, promise in enumerate(promises):
                if isinstance(promise, RiftPromise):
                    promise.then(partial(on_resolve, i)).catch(on_reject)
                else:
                    on_resolve(i, promise)
        
        return RiftPromise(executor)
    
    def promise_race(promises: List[RiftPromise]) -> RiftPromise:
        """Return first promise to settle."""
        def executor(resolve, reject):
            settled = [False]
            
            def on_settle(value, is_error=False):
                if not settled[0]:
                    settled[0] = True
                    if is_error:
                        reject(value)
                    else:
                        resolve(value)
            
            for promise in promises:
                if isinstance(promise, RiftPromise):
                    promise.then(on_settle).catch(lambda e: on_settle(e, True))
                else:
                    on_settle(promise)
        
        return RiftPromise(executor)
    
    def promise_all_settled(promises: List[RiftPromise]) -> RiftPromise:
        """Wait for all promises to settle (resolve or reject)."""
        def executor(resolve, reject):
            results = [None] * len(promises)
            completed = [0]
            
            def on_settle(index, value, status):
                results[index] = {'status': status, 'value': value}
                completed[0] += 1
                if completed[0] == len(promises):
                    resolve(results)
            
            if not promises:
                resolve([])
                return
            
            for i, promise in enumerate(promises):
                if isinstance(promise, RiftPromise):
                    promise.then(
                        lambda v, idx=i: on_settle(idx, v, 'fulfilled')
                    ).catch(
                        lambda e, idx=i: on_settle(idx, e, 'rejected')
                    )
                else:
                    on_settle(i, promise, 'fulfilled')
        
        return RiftPromise(executor)
    
    def promise_any(promises: List[RiftPromise]) -> RiftPromise:
        """Return first promise to resolve."""
        def executor(resolve, reject):
            errors = []
            rejected_count = [0]
            resolved = [False]
            
            def on_resolve(value):
                if not resolved[0]:
                    resolved[0] = True
                    resolve(value)
            
            def on_reject(error):
                errors.append(error)
                rejected_count[0] += 1
                if rejected_count[0] == len(promises):
                    reject(errors)
            
            if not promises:
                reject([])
                return
            
            for promise in promises:
                if isinstance(promise, RiftPromise):
                    promise.then(on_resolve).catch(on_reject)
                else:
                    on_resolve(promise)
        
        return RiftPromise(executor)
    
    # ========================================================================
    # Async Utilities
    # ========================================================================
    
    def async_delay(ms: int) -> RiftPromise:
        """Create promise that resolves after delay."""
        def executor(resolve, reject):
            def delayed():
                time.sleep(ms / 1000)
                resolve(None)
            threading.Thread(target=delayed).start()
        
        return RiftPromise(executor)
    
    def async_timeout(promise: RiftPromise, ms: int) -> RiftPromise:
        """Add timeout to promise."""
        def executor(resolve, reject):
            timer_done = [False]
            promise_done = [False]
            
            def on_timeout():
                time.sleep(ms / 1000)
                if not promise_done[0]:
                    timer_done[0] = True
                    reject(TimeoutError(f"Promise timeout after {ms}ms"))
            
            def on_resolve(value):
                if not timer_done[0]:
                    promise_done[0] = True
                    resolve(value)
            
            def on_reject(error):
                if not timer_done[0]:
                    promise_done[0] = True
                    reject(error)
            
            threading.Thread(target=on_timeout).start()
            promise.then(on_resolve).catch(on_reject)
        
        return RiftPromise(executor)
    
    def async_retry(fn: Callable, retries: int = 3, delay: int = 1000,
                    backoff: float = 1.0) -> RiftPromise:
        """Retry async operation."""
        def executor(resolve, reject):
            attempts = [0]
            
            def attempt():
                attempts[0] += 1
                try:
                    result = interpreter._call(fn, [], None)
                    if isinstance(result, RiftPromise):
                        result.then(resolve).catch(on_error)
                    else:
                        resolve(result)
                except Exception as e:
                    on_error(e)
            
            def on_error(error):
                if attempts[0] < retries:
                    wait_time = delay * (backoff ** (attempts[0] - 1))
                    time.sleep(wait_time / 1000)
                    attempt()
                else:
                    reject(error)
            
            threading.Thread(target=attempt).start()
        
        return RiftPromise(executor)
    
    def async_parallel(tasks: List[Callable], concurrency: int = None) -> RiftPromise:
        """Run tasks in parallel with optional concurrency limit."""
        def executor(resolve, reject):
            results = [None] * len(tasks)
            completed = [0]
            errors = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
                def run_task(index, task):
                    try:
                        result = interpreter._call(task, [], None)
                        results[index] = result
                    except Exception as e:
                        errors.append(e)
                    finally:
                        completed[0] += 1
                        if completed[0] == len(tasks):
                            if errors:
                                reject(errors)
                            else:
                                resolve(results)
                
                for i, task in enumerate(tasks):
                    pool.submit(run_task, i, task)
        
        return RiftPromise(executor)
    
    def async_sequence(tasks: List[Callable]) -> RiftPromise:
        """Run tasks sequentially."""
        def executor(resolve, reject):
            results = []
            
            def run_next(index):
                if index >= len(tasks):
                    resolve(results)
                    return
                
                try:
                    result = interpreter._call(tasks[index], [], None)
                    if isinstance(result, RiftPromise):
                        result.then(lambda v: on_success(index, v)).catch(reject)
                    else:
                        on_success(index, result)
                except Exception as e:
                    reject(e)
            
            def on_success(index, value):
                results.append(value)
                run_next(index + 1)
            
            threading.Thread(target=lambda: run_next(0)).start()
        
        return RiftPromise(executor)
    
    def async_map(items: List[Any], mapper: Callable, 
                  concurrency: int = None) -> RiftPromise:
        """Map items with async mapper."""
        tasks = [lambda item=item: interpreter._call(mapper, [item], None) for item in items]
        return async_parallel(tasks, concurrency)
    
    def async_filter(items: List[Any], predicate: Callable) -> RiftPromise:
        """Filter items with async predicate."""
        def executor(resolve, reject):
            results = []
            completed = [0]
            
            def check_item(index, item):
                try:
                    result = interpreter._call(predicate, [item], None)
                    if isinstance(result, RiftPromise):
                        result.then(lambda v: on_result(index, item, v)).catch(reject)
                    else:
                        on_result(index, item, result)
                except Exception as e:
                    reject(e)
            
            def on_result(index, item, passed):
                if passed:
                    results.append((index, item))
                completed[0] += 1
                if completed[0] == len(items):
                    # Sort by original index to preserve order
                    sorted_results = sorted(results, key=lambda x: x[0])
                    resolve([item for _, item in sorted_results])
            
            if not items:
                resolve([])
                return
            
            for i, item in enumerate(items):
                threading.Thread(target=lambda idx=i, it=item: check_item(idx, it)).start()
        
        return RiftPromise(executor)
    
    def async_reduce(items: List[Any], reducer: Callable, 
                     initial: Any = None) -> RiftPromise:
        """Reduce items with async reducer."""
        def executor(resolve, reject):
            if not items:
                resolve(initial)
                return
            
            accumulator = [initial if initial is not None else items[0]]
            start_index = 0 if initial is not None else 1
            current_index = [start_index]
            
            def process_next():
                if current_index[0] >= len(items):
                    resolve(accumulator[0])
                    return
                
                try:
                    result = interpreter._call(
                        reducer, 
                        [accumulator[0], items[current_index[0]]], 
                        None
                    )
                    
                    if isinstance(result, RiftPromise):
                        result.then(on_result).catch(reject)
                    else:
                        on_result(result)
                except Exception as e:
                    reject(e)
            
            def on_result(value):
                accumulator[0] = value
                current_index[0] += 1
                process_next()
            
            threading.Thread(target=process_next).start()
        
        return RiftPromise(executor)
    
    # ========================================================================
    # Debounce and Throttle (Async versions)
    # ========================================================================
    
    def async_debounce(fn: Callable, wait: int) -> Callable:
        """Create debounced async function."""
        timer = [None]
        
        def debounced(*args) -> RiftPromise:
            def executor(resolve, reject):
                if timer[0]:
                    timer[0].cancel()
                
                def call():
                    try:
                        result = interpreter._call(fn, list(args), None)
                        resolve(result)
                    except Exception as e:
                        reject(e)
                
                timer[0] = threading.Timer(wait / 1000, call)
                timer[0].start()
            
            return RiftPromise(executor)
        
        return debounced
    
    def async_throttle(fn: Callable, wait: int) -> Callable:
        """Create throttled async function."""
        last_call = [0]
        pending = [None]
        
        def throttled(*args) -> RiftPromise:
            def executor(resolve, reject):
                now = time.time() * 1000
                
                if now - last_call[0] >= wait:
                    last_call[0] = now
                    try:
                        result = interpreter._call(fn, list(args), None)
                        resolve(result)
                    except Exception as e:
                        reject(e)
                else:
                    # Queue for later
                    pending[0] = (args, resolve, reject)
                    
                    def delayed():
                        time.sleep((wait - (now - last_call[0])) / 1000)
                        if pending[0]:
                            a, res, rej = pending[0]
                            pending[0] = None
                            last_call[0] = time.time() * 1000
                            try:
                                result = interpreter._call(fn, list(a), None)
                                res(result)
                            except Exception as e:
                                rej(e)
                    
                    threading.Thread(target=delayed).start()
            
            return RiftPromise(executor)
        
        return throttled
    
    # ========================================================================
    # Semaphore (Concurrency Limiting)
    # ========================================================================
    
    class Semaphore:
        """Semaphore for limiting concurrency."""
        
        def __init__(self, count: int):
            self._count = count
            self._max = count
            self._waiting: List[Callable] = []
            self._lock = threading.Lock()
        
        def acquire(self) -> RiftPromise:
            """Acquire semaphore."""
            def executor(resolve, reject):
                with self._lock:
                    if self._count > 0:
                        self._count -= 1
                        resolve(True)
                    else:
                        self._waiting.append(resolve)
            
            return RiftPromise(executor)
        
        def release(self) -> None:
            """Release semaphore."""
            with self._lock:
                if self._waiting:
                    resolve = self._waiting.pop(0)
                    resolve(True)
                else:
                    self._count = min(self._count + 1, self._max)
        
        @property
        def available(self) -> int:
            return self._count
        
        def __repr__(self):
            return f"Semaphore({self._count}/{self._max})"
    
    # ========================================================================
    # Mutex
    # ========================================================================
    
    class Mutex:
        """Mutual exclusion lock."""
        
        def __init__(self):
            self._locked = False
            self._waiting: List[Callable] = []
            self._lock = threading.Lock()
        
        def lock(self) -> RiftPromise:
            """Acquire lock."""
            def executor(resolve, reject):
                with self._lock:
                    if not self._locked:
                        self._locked = True
                        resolve(True)
                    else:
                        self._waiting.append(resolve)
            
            return RiftPromise(executor)
        
        def unlock(self) -> None:
            """Release lock."""
            with self._lock:
                if self._waiting:
                    resolve = self._waiting.pop(0)
                    resolve(True)
                else:
                    self._locked = False
        
        @property
        def isLocked(self) -> bool:
            return self._locked
        
        def __repr__(self):
            return f"Mutex(locked={self._locked})"
    
    # ========================================================================
    # Module Exports
    # ========================================================================
    
    def create_promise(executor: Callable = None) -> RiftPromise:
        return RiftPromise(executor)
    
    def create_semaphore(count: int) -> Semaphore:
        return Semaphore(count)
    
    def create_mutex() -> Mutex:
        return Mutex()
    
    return {
        # Promise
        'Promise': create_promise,
        'resolve': promise_resolve,
        'reject': promise_reject,
        'all': promise_all,
        'race': promise_race,
        'allSettled': promise_all_settled,
        'any': promise_any,
        
        # Async Utilities
        'delay': async_delay,
        'timeout': async_timeout,
        'retry': async_retry,
        'parallel': async_parallel,
        'sequence': async_sequence,
        'map': async_map,
        'filter': async_filter,
        'reduce': async_reduce,
        
        # Function Modifiers
        'debounce': async_debounce,
        'throttle': async_throttle,
        
        # Concurrency
        'Semaphore': create_semaphore,
        'Mutex': create_mutex,
    }
