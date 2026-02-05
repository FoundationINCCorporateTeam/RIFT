"""
RIFT Standard Library - Events Module

Event emitter pattern for pub/sub communication.
"""

from typing import Any, Dict, List, Optional, Callable, Set
from collections import defaultdict
import threading


def create_events_module(interpreter) -> Dict[str, Any]:
    """Create the events module for RIFT."""
    
    # ========================================================================
    # EventEmitter
    # ========================================================================
    
    class EventEmitter:
        """Event emitter for pub/sub pattern."""
        
        def __init__(self):
            self._listeners: Dict[str, List[Dict]] = defaultdict(list)
            self._max_listeners = 10
            self._lock = threading.Lock()
        
        def on(self, event: str, callback: Callable, priority: int = 0) -> 'EventEmitter':
            """Add event listener."""
            with self._lock:
                listener = {
                    'callback': callback,
                    'once': False,
                    'priority': priority,
                }
                self._listeners[event].append(listener)
                self._listeners[event].sort(key=lambda x: -x['priority'])
                
                if len(self._listeners[event]) > self._max_listeners:
                    print(f"Warning: EventEmitter has more than {self._max_listeners} listeners for '{event}'")
            
            return self
        
        def once(self, event: str, callback: Callable, priority: int = 0) -> 'EventEmitter':
            """Add one-time event listener."""
            with self._lock:
                listener = {
                    'callback': callback,
                    'once': True,
                    'priority': priority,
                }
                self._listeners[event].append(listener)
                self._listeners[event].sort(key=lambda x: -x['priority'])
            
            return self
        
        def off(self, event: str, callback: Callable = None) -> 'EventEmitter':
            """Remove event listener(s)."""
            with self._lock:
                if callback is None:
                    # Remove all listeners for event
                    self._listeners[event] = []
                else:
                    # Remove specific callback
                    self._listeners[event] = [
                        l for l in self._listeners[event] 
                        if l['callback'] != callback
                    ]
            return self
        
        def emit(self, event: str, *args) -> bool:
            """Emit event with arguments."""
            listeners = self._listeners.get(event, [])
            if not listeners:
                return False
            
            # Copy list to allow modification during iteration
            listeners_copy = list(listeners)
            
            for listener in listeners_copy:
                try:
                    interpreter._call(listener['callback'], list(args), None)
                except Exception as e:
                    self.emit('error', e, event)
                
                if listener['once']:
                    self.off(event, listener['callback'])
            
            return True
        
        def emitAsync(self, event: str, *args) -> None:
            """Emit event asynchronously."""
            import threading
            thread = threading.Thread(target=self.emit, args=(event, *args))
            thread.start()
        
        def listeners(self, event: str) -> List[Callable]:
            """Get all listeners for event."""
            return [l['callback'] for l in self._listeners.get(event, [])]
        
        def listenerCount(self, event: str) -> int:
            """Get number of listeners for event."""
            return len(self._listeners.get(event, []))
        
        def eventNames(self) -> List[str]:
            """Get all event names with listeners."""
            return [k for k, v in self._listeners.items() if v]
        
        def removeAllListeners(self, event: str = None) -> 'EventEmitter':
            """Remove all listeners."""
            with self._lock:
                if event:
                    self._listeners[event] = []
                else:
                    self._listeners = defaultdict(list)
            return self
        
        def setMaxListeners(self, n: int) -> 'EventEmitter':
            """Set max listeners per event."""
            self._max_listeners = n
            return self
        
        def getMaxListeners(self) -> int:
            """Get max listeners per event."""
            return self._max_listeners
        
        def prependListener(self, event: str, callback: Callable) -> 'EventEmitter':
            """Add listener to beginning."""
            with self._lock:
                listener = {
                    'callback': callback,
                    'once': False,
                    'priority': float('inf'),  # Highest priority
                }
                self._listeners[event].insert(0, listener)
            return self
        
        def __repr__(self):
            event_count = len(self.eventNames())
            return f"EventEmitter(events={event_count})"
    
    # ========================================================================
    # TypedEventEmitter
    # ========================================================================
    
    class TypedEventEmitter(EventEmitter):
        """Event emitter with typed events."""
        
        def __init__(self, event_types: Dict[str, List[str]] = None):
            super().__init__()
            self._event_types = event_types or {}
        
        def defineEvent(self, event: str, arg_names: List[str]) -> 'TypedEventEmitter':
            """Define event with argument names."""
            self._event_types[event] = arg_names
            return self
        
        def emit(self, event: str, *args, **kwargs) -> bool:
            """Emit with optional named arguments."""
            if event in self._event_types and kwargs:
                # Convert kwargs to positional args
                arg_names = self._event_types[event]
                args = tuple(kwargs.get(name) for name in arg_names)
            
            return super().emit(event, *args)
        
        def getEventTypes(self) -> Dict[str, List[str]]:
            """Get all defined event types."""
            return dict(self._event_types)
    
    # ========================================================================
    # EventBus (Global Event System)
    # ========================================================================
    
    class EventBus:
        """Global event bus for application-wide events."""
        
        _instance = None
        
        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._emitter = EventEmitter()
                cls._instance._namespaces: Dict[str, EventEmitter] = {}
            return cls._instance
        
        def on(self, event: str, callback: Callable) -> 'EventBus':
            """Subscribe to event."""
            self._emitter.on(event, callback)
            return self
        
        def once(self, event: str, callback: Callable) -> 'EventBus':
            """Subscribe to event once."""
            self._emitter.once(event, callback)
            return self
        
        def off(self, event: str, callback: Callable = None) -> 'EventBus':
            """Unsubscribe from event."""
            self._emitter.off(event, callback)
            return self
        
        def emit(self, event: str, *args) -> bool:
            """Emit event."""
            return self._emitter.emit(event, *args)
        
        def namespace(self, name: str) -> EventEmitter:
            """Get or create namespaced emitter."""
            if name not in self._namespaces:
                self._namespaces[name] = EventEmitter()
            return self._namespaces[name]
        
        def clear(self) -> 'EventBus':
            """Clear all events."""
            self._emitter.removeAllListeners()
            self._namespaces = {}
            return self
    
    _global_bus = EventBus()
    
    # ========================================================================
    # Event Utilities
    # ========================================================================
    
    def event_debounce(callback: Callable, wait: int) -> Callable:
        """Create debounced version of callback."""
        timer = [None]  # Use list to allow mutation in closure
        
        def debounced(*args):
            if timer[0]:
                timer[0].cancel()
            
            def call():
                interpreter._call(callback, list(args), None)
            
            timer[0] = threading.Timer(wait / 1000, call)
            timer[0].start()
        
        return debounced
    
    def event_throttle(callback: Callable, wait: int) -> Callable:
        """Create throttled version of callback."""
        last_call = [0]
        
        def throttled(*args):
            import time
            now = time.time() * 1000
            if now - last_call[0] >= wait:
                last_call[0] = now
                interpreter._call(callback, list(args), None)
        
        return throttled
    
    def event_once_any(emitter: EventEmitter, events: List[str], 
                       callback: Callable) -> None:
        """Listen to multiple events, trigger callback once."""
        triggered = [False]
        
        def handler(*args):
            if not triggered[0]:
                triggered[0] = True
                interpreter._call(callback, list(args), None)
                # Remove all listeners
                for event in events:
                    emitter.off(event, handler)
        
        for event in events:
            emitter.once(event, handler)
    
    def event_wait_for(emitter: EventEmitter, event: str, 
                       timeout: int = None) -> Dict[str, Any]:
        """Wait for event (blocking, returns event data)."""
        import time
        result = {'received': False, 'data': None}
        
        def handler(*args):
            result['received'] = True
            result['data'] = list(args)
        
        emitter.once(event, handler)
        
        start = time.time()
        while not result['received']:
            if timeout and (time.time() - start) * 1000 > timeout:
                break
            time.sleep(0.01)
        
        return result
    
    def event_pipe(source: EventEmitter, target: EventEmitter, 
                   events: List[str] = None) -> Callable:
        """Pipe events from source to target."""
        if events is None:
            events = source.eventNames()
        
        handlers = {}
        
        def forwarder(event):
            def forward(*args):
                target.emit(event, *args)
            return forward
        
        for event in events:
            handler = forwarder(event)
            handlers[event] = handler
            source.on(event, handler)
        
        def unpipe():
            for event, handler in handlers.items():
                source.off(event, handler)
        
        return unpipe
    
    # ========================================================================
    # Observable (Reactive Pattern)
    # ========================================================================
    
    class Observable:
        """Observable value that notifies subscribers on change."""
        
        def __init__(self, initial_value: Any = None):
            self._value = initial_value
            self._emitter = EventEmitter()
            self._computed: List['Observable'] = []
        
        def get(self) -> Any:
            """Get current value."""
            return self._value
        
        def set(self, value: Any) -> None:
            """Set value and notify subscribers."""
            old_value = self._value
            self._value = value
            
            if old_value != value:
                self._emitter.emit('change', value, old_value)
                self._update_computed()
        
        def subscribe(self, callback: Callable) -> Callable:
            """Subscribe to value changes."""
            self._emitter.on('change', callback)
            
            def unsubscribe():
                self._emitter.off('change', callback)
            
            return unsubscribe
        
        def _update_computed(self):
            """Update computed observables."""
            for computed in self._computed:
                computed._recompute()
        
        def map(self, mapper: Callable) -> 'Observable':
            """Create computed observable."""
            def compute():
                return interpreter._call(mapper, [self._value], None)
            
            computed = ComputedObservable(compute)
            self._computed.append(computed)
            return computed
        
        def __repr__(self):
            return f"Observable({self._value})"
    
    class ComputedObservable(Observable):
        """Computed observable that depends on other observables."""
        
        def __init__(self, compute: Callable):
            super().__init__()
            self._compute = compute
            self._recompute()
        
        def _recompute(self):
            """Recompute value."""
            old_value = self._value
            self._value = self._compute()
            
            if old_value != self._value:
                self._emitter.emit('change', self._value, old_value)
        
        def set(self, value: Any):
            """Cannot set computed observable."""
            raise ValueError("Cannot set computed observable")
    
    # ========================================================================
    # Module Exports
    # ========================================================================
    
    def create_emitter() -> EventEmitter:
        return EventEmitter()
    
    def create_typed_emitter(event_types: Dict[str, List[str]] = None) -> TypedEventEmitter:
        return TypedEventEmitter(event_types)
    
    def create_observable(initial: Any = None) -> Observable:
        return Observable(initial)
    
    return {
        # EventEmitter
        'EventEmitter': create_emitter,
        'TypedEventEmitter': create_typed_emitter,
        
        # Global Bus
        'bus': _global_bus,
        'on': _global_bus.on,
        'once': _global_bus.once,
        'off': _global_bus.off,
        'emit': _global_bus.emit,
        
        # Utilities
        'debounce': event_debounce,
        'throttle': event_throttle,
        'onceAny': event_once_any,
        'waitFor': event_wait_for,
        'pipe': event_pipe,
        
        # Observable
        'Observable': create_observable,
    }
