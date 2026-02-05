"""
RIFT Standard Library - Functional Module

Functional programming utilities.
"""

from typing import Any, Dict, List, Optional, Callable, Union, TypeVar
from functools import reduce as functools_reduce


def create_functional_module(interpreter) -> Dict[str, Any]:
    """Create the functional module for RIFT."""
    
    # ========================================================================
    # Function Composition
    # ========================================================================
    
    def fn_compose(*fns) -> Callable:
        """Compose functions right-to-left: compose(f, g, h)(x) = f(g(h(x)))."""
        def composed(*args):
            result = interpreter._call(fns[-1], list(args), None)
            for fn in reversed(fns[:-1]):
                result = interpreter._call(fn, [result], None)
            return result
        return composed
    
    def fn_pipe(*fns) -> Callable:
        """Pipe functions left-to-right: pipe(f, g, h)(x) = h(g(f(x)))."""
        def piped(*args):
            result = interpreter._call(fns[0], list(args), None)
            for fn in fns[1:]:
                result = interpreter._call(fn, [result], None)
            return result
        return piped
    
    def fn_flow(*fns) -> Callable:
        """Alias for pipe."""
        return fn_pipe(*fns)
    
    # ========================================================================
    # Currying and Partial Application
    # ========================================================================
    
    def fn_curry(fn: Callable, arity: int = None) -> Callable:
        """Curry a function."""
        # For simplicity, we'll implement basic currying
        def curried(*args):
            collected_args = list(args)
            
            def collect(*more_args):
                all_args = collected_args + list(more_args)
                if arity is None or len(all_args) >= arity:
                    return interpreter._call(fn, all_args, None)
                return fn_curry(lambda *a: interpreter._call(fn, all_args + list(a), None))
            
            if arity is None or len(collected_args) >= arity:
                return interpreter._call(fn, collected_args, None)
            return collect
        
        return curried
    
    def fn_partial(fn: Callable, *args) -> Callable:
        """Partially apply arguments."""
        def partially_applied(*more_args):
            return interpreter._call(fn, list(args) + list(more_args), None)
        return partially_applied
    
    def fn_partial_right(fn: Callable, *args) -> Callable:
        """Partially apply arguments from the right."""
        def partially_applied(*more_args):
            return interpreter._call(fn, list(more_args) + list(args), None)
        return partially_applied
    
    # ========================================================================
    # Function Modifiers
    # ========================================================================
    
    def fn_negate(predicate: Callable) -> Callable:
        """Negate a predicate function."""
        def negated(*args):
            return not interpreter._call(predicate, list(args), None)
        return negated
    
    def fn_once(fn: Callable) -> Callable:
        """Function that only runs once."""
        called = [False]
        result = [None]
        
        def once_fn(*args):
            if not called[0]:
                called[0] = True
                result[0] = interpreter._call(fn, list(args), None)
            return result[0]
        
        return once_fn
    
    def fn_memoize(fn: Callable, key_fn: Callable = None) -> Callable:
        """Memoize function results."""
        cache = {}
        
        def memoized(*args):
            if key_fn:
                key = interpreter._call(key_fn, list(args), None)
            else:
                key = str(args)
            
            if key not in cache:
                cache[key] = interpreter._call(fn, list(args), None)
            return cache[key]
        
        memoized.cache = cache
        memoized.clear = lambda: cache.clear()
        return memoized
    
    def fn_after(count: int, fn: Callable) -> Callable:
        """Create function that only runs after n calls."""
        calls = [0]
        
        def after_fn(*args):
            calls[0] += 1
            if calls[0] >= count:
                return interpreter._call(fn, list(args), None)
            return None
        
        return after_fn
    
    def fn_before(count: int, fn: Callable) -> Callable:
        """Create function that only runs before n calls."""
        calls = [0]
        result = [None]
        
        def before_fn(*args):
            calls[0] += 1
            if calls[0] < count:
                result[0] = interpreter._call(fn, list(args), None)
            return result[0]
        
        return before_fn
    
    def fn_times(count: int, fn: Callable) -> List[Any]:
        """Call function n times, return results."""
        return [interpreter._call(fn, [i], None) for i in range(count)]
    
    def fn_constant(value: Any) -> Callable:
        """Create function that always returns the same value."""
        return lambda *args: value
    
    def fn_identity(value: Any) -> Any:
        """Identity function."""
        return value
    
    def fn_noop(*args) -> None:
        """No-operation function."""
        pass
    
    def fn_flip(fn: Callable) -> Callable:
        """Flip first two arguments of function."""
        def flipped(a, b, *rest):
            return interpreter._call(fn, [b, a] + list(rest), None)
        return flipped
    
    def fn_spread(fn: Callable) -> Callable:
        """Create function that spreads array argument."""
        def spread(arr):
            return interpreter._call(fn, list(arr), None)
        return spread
    
    def fn_unary(fn: Callable) -> Callable:
        """Create function that only takes one argument."""
        def unary(arg):
            return interpreter._call(fn, [arg], None)
        return unary
    
    def fn_binary(fn: Callable) -> Callable:
        """Create function that only takes two arguments."""
        def binary(a, b):
            return interpreter._call(fn, [a, b], None)
        return binary
    
    # ========================================================================
    # Comparison Helpers
    # ========================================================================
    
    def fn_eq(value: Any) -> Callable:
        """Create equality predicate."""
        return lambda x: x == value
    
    def fn_ne(value: Any) -> Callable:
        """Create inequality predicate."""
        return lambda x: x != value
    
    def fn_lt(value: Any) -> Callable:
        """Create less-than predicate."""
        return lambda x: x < value
    
    def fn_le(value: Any) -> Callable:
        """Create less-or-equal predicate."""
        return lambda x: x <= value
    
    def fn_gt(value: Any) -> Callable:
        """Create greater-than predicate."""
        return lambda x: x > value
    
    def fn_ge(value: Any) -> Callable:
        """Create greater-or-equal predicate."""
        return lambda x: x >= value
    
    def fn_between(low: Any, high: Any) -> Callable:
        """Create between predicate."""
        return lambda x: low <= x <= high
    
    # ========================================================================
    # Property Access
    # ========================================================================
    
    def fn_prop(name: str) -> Callable:
        """Create property getter."""
        def get_prop(obj):
            if isinstance(obj, dict):
                return obj.get(name)
            return getattr(obj, name, None)
        return get_prop
    
    def fn_path(path: List[str]) -> Callable:
        """Create nested property getter."""
        def get_path(obj):
            result = obj
            for key in path:
                if result is None:
                    return None
                if isinstance(result, dict):
                    result = result.get(key)
                else:
                    result = getattr(result, key, None)
            return result
        return get_path
    
    def fn_prop_eq(name: str, value: Any) -> Callable:
        """Create property equality predicate."""
        def check_prop(obj):
            if isinstance(obj, dict):
                return obj.get(name) == value
            return getattr(obj, name, None) == value
        return check_prop
    
    def fn_pick(*keys: str) -> Callable:
        """Create function that picks keys from object."""
        def pick_keys(obj):
            if isinstance(obj, dict):
                return {k: obj[k] for k in keys if k in obj}
            return {k: getattr(obj, k) for k in keys if hasattr(obj, k)}
        return pick_keys
    
    def fn_omit(*keys: str) -> Callable:
        """Create function that omits keys from object."""
        def omit_keys(obj):
            if isinstance(obj, dict):
                return {k: v for k, v in obj.items() if k not in keys}
            return obj  # Can't omit from non-dict
        return omit_keys
    
    # ========================================================================
    # Logical Combinators
    # ========================================================================
    
    def fn_all_pass(*predicates) -> Callable:
        """Create predicate that passes when all predicates pass."""
        def all_pass(value):
            return all(
                interpreter._call(p, [value], None) 
                for p in predicates
            )
        return all_pass
    
    def fn_any_pass(*predicates) -> Callable:
        """Create predicate that passes when any predicate passes."""
        def any_pass(value):
            return any(
                interpreter._call(p, [value], None) 
                for p in predicates
            )
        return any_pass
    
    def fn_both(p1: Callable, p2: Callable) -> Callable:
        """Create predicate that passes when both pass."""
        return fn_all_pass(p1, p2)
    
    def fn_either(p1: Callable, p2: Callable) -> Callable:
        """Create predicate that passes when either passes."""
        return fn_any_pass(p1, p2)
    
    def fn_complement(predicate: Callable) -> Callable:
        """Alias for negate."""
        return fn_negate(predicate)
    
    # ========================================================================
    # Control Flow
    # ========================================================================
    
    def fn_if_else(predicate: Callable, on_true: Callable, 
                   on_false: Callable) -> Callable:
        """Conditional function."""
        def conditional(*args):
            if interpreter._call(predicate, list(args), None):
                return interpreter._call(on_true, list(args), None)
            return interpreter._call(on_false, list(args), None)
        return conditional
    
    def fn_when(predicate: Callable, fn: Callable) -> Callable:
        """Apply function when predicate passes, else return input."""
        def when_fn(*args):
            if interpreter._call(predicate, list(args), None):
                return interpreter._call(fn, list(args), None)
            return args[0] if len(args) == 1 else args
        return when_fn
    
    def fn_unless(predicate: Callable, fn: Callable) -> Callable:
        """Apply function when predicate fails, else return input."""
        def unless_fn(*args):
            if not interpreter._call(predicate, list(args), None):
                return interpreter._call(fn, list(args), None)
            return args[0] if len(args) == 1 else args
        return unless_fn
    
    def fn_cond(*pairs) -> Callable:
        """Conditional with multiple branches."""
        def cond_fn(*args):
            for i in range(0, len(pairs), 2):
                predicate = pairs[i]
                action = pairs[i + 1] if i + 1 < len(pairs) else None
                
                if predicate is True or (
                    callable(predicate) and 
                    interpreter._call(predicate, list(args), None)
                ):
                    if action:
                        return interpreter._call(action, list(args), None)
                    return None
            return None
        return cond_fn
    
    def fn_switch(key_fn: Callable, cases: Dict[Any, Callable], 
                  default: Callable = None) -> Callable:
        """Switch/case function."""
        def switch_fn(*args):
            key = interpreter._call(key_fn, list(args), None)
            handler = cases.get(key, default)
            if handler:
                return interpreter._call(handler, list(args), None)
            return None
        return switch_fn
    
    # ========================================================================
    # Tap and Through
    # ========================================================================
    
    def fn_tap(fn: Callable) -> Callable:
        """Create tap function (run fn, return original value)."""
        def tap_fn(value):
            interpreter._call(fn, [value], None)
            return value
        return tap_fn
    
    def fn_through(fn: Callable) -> Callable:
        """Alias for tap."""
        return fn_tap(fn)
    
    # ========================================================================
    # Type Checking Predicates
    # ========================================================================
    
    def fn_is_nil(value: Any) -> bool:
        """Check if value is None."""
        return value is None
    
    def fn_is_not_nil(value: Any) -> bool:
        """Check if value is not None."""
        return value is not None
    
    def fn_is_type(type_name: str) -> Callable:
        """Create type checking predicate."""
        type_map = {
            'string': str,
            'number': (int, float),
            'integer': int,
            'float': float,
            'boolean': bool,
            'list': list,
            'array': list,
            'dict': dict,
            'object': dict,
            'function': callable,
        }
        
        expected = type_map.get(type_name)
        
        def check_type(value):
            if type_name == 'function':
                return callable(value)
            return isinstance(value, expected) if expected else False
        
        return check_type
    
    # ========================================================================
    # Math Helpers
    # ========================================================================
    
    def fn_add(a: Union[int, float]) -> Callable:
        """Create add function."""
        return lambda b: a + b
    
    def fn_subtract(a: Union[int, float]) -> Callable:
        """Create subtract function."""
        return lambda b: b - a
    
    def fn_multiply(a: Union[int, float]) -> Callable:
        """Create multiply function."""
        return lambda b: a * b
    
    def fn_divide(a: Union[int, float]) -> Callable:
        """Create divide function."""
        return lambda b: b / a if a != 0 else float('inf')
    
    def fn_modulo(a: int) -> Callable:
        """Create modulo function."""
        return lambda b: b % a
    
    def fn_inc(value: Union[int, float]) -> Union[int, float]:
        """Increment by 1."""
        return value + 1
    
    def fn_dec(value: Union[int, float]) -> Union[int, float]:
        """Decrement by 1."""
        return value - 1
    
    # ========================================================================
    # Monads (Simple Implementations)
    # ========================================================================
    
    class Maybe:
        """Maybe monad for handling optional values."""
        
        def __init__(self, value: Any = None, is_nothing: bool = False):
            self._value = value
            self._is_nothing = is_nothing or value is None
        
        @staticmethod
        def just(value: Any) -> 'Maybe':
            return Maybe(value, False)
        
        @staticmethod
        def nothing() -> 'Maybe':
            return Maybe(None, True)
        
        def isNothing(self) -> bool:
            return self._is_nothing
        
        def isJust(self) -> bool:
            return not self._is_nothing
        
        def map(self, fn: Callable) -> 'Maybe':
            if self._is_nothing:
                return Maybe.nothing()
            return Maybe.just(interpreter._call(fn, [self._value], None))
        
        def flatMap(self, fn: Callable) -> 'Maybe':
            if self._is_nothing:
                return Maybe.nothing()
            return interpreter._call(fn, [self._value], None)
        
        def getOrElse(self, default: Any) -> Any:
            if self._is_nothing:
                return default
            return self._value
        
        def filter(self, predicate: Callable) -> 'Maybe':
            if self._is_nothing:
                return Maybe.nothing()
            if interpreter._call(predicate, [self._value], None):
                return self
            return Maybe.nothing()
        
        def __repr__(self):
            if self._is_nothing:
                return "Nothing"
            return f"Just({self._value})"
    
    class Either:
        """Either monad for handling errors."""
        
        def __init__(self, value: Any = None, is_left: bool = False):
            self._value = value
            self._is_left = is_left
        
        @staticmethod
        def left(value: Any) -> 'Either':
            return Either(value, True)
        
        @staticmethod
        def right(value: Any) -> 'Either':
            return Either(value, False)
        
        def isLeft(self) -> bool:
            return self._is_left
        
        def isRight(self) -> bool:
            return not self._is_left
        
        def map(self, fn: Callable) -> 'Either':
            if self._is_left:
                return self
            return Either.right(interpreter._call(fn, [self._value], None))
        
        def flatMap(self, fn: Callable) -> 'Either':
            if self._is_left:
                return self
            return interpreter._call(fn, [self._value], None)
        
        def mapLeft(self, fn: Callable) -> 'Either':
            if self._is_left:
                return Either.left(interpreter._call(fn, [self._value], None))
            return self
        
        def getOrElse(self, default: Any) -> Any:
            if self._is_left:
                return default
            return self._value
        
        def fold(self, left_fn: Callable, right_fn: Callable) -> Any:
            if self._is_left:
                return interpreter._call(left_fn, [self._value], None)
            return interpreter._call(right_fn, [self._value], None)
        
        def __repr__(self):
            if self._is_left:
                return f"Left({self._value})"
            return f"Right({self._value})"
    
    def fn_try_catch(fn: Callable) -> Either:
        """Wrap function call in Either."""
        try:
            result = interpreter._call(fn, [], None)
            return Either.right(result)
        except Exception as e:
            return Either.left(e)
    
    # ========================================================================
    # Module Exports
    # ========================================================================
    
    def create_maybe(value: Any = None) -> Maybe:
        if value is None:
            return Maybe.nothing()
        return Maybe.just(value)
    
    def create_either(is_left: bool, value: Any) -> Either:
        if is_left:
            return Either.left(value)
        return Either.right(value)
    
    return {
        # Composition
        'compose': fn_compose,
        'pipe': fn_pipe,
        'flow': fn_flow,
        
        # Currying/Partial
        'curry': fn_curry,
        'partial': fn_partial,
        'partialRight': fn_partial_right,
        
        # Function Modifiers
        'negate': fn_negate,
        'once': fn_once,
        'memoize': fn_memoize,
        'after': fn_after,
        'before': fn_before,
        'times': fn_times,
        'constant': fn_constant,
        'identity': fn_identity,
        'noop': fn_noop,
        'flip': fn_flip,
        'spread': fn_spread,
        'unary': fn_unary,
        'binary': fn_binary,
        
        # Comparison
        'eq': fn_eq,
        'ne': fn_ne,
        'lt': fn_lt,
        'le': fn_le,
        'gt': fn_gt,
        'ge': fn_ge,
        'between': fn_between,
        
        # Property Access
        'prop': fn_prop,
        'path': fn_path,
        'propEq': fn_prop_eq,
        'pick': fn_pick,
        'omit': fn_omit,
        
        # Logical
        'allPass': fn_all_pass,
        'anyPass': fn_any_pass,
        'both': fn_both,
        'either': fn_either,
        'complement': fn_complement,
        
        # Control Flow
        'ifElse': fn_if_else,
        'when': fn_when,
        'unless': fn_unless,
        'cond': fn_cond,
        'switch': fn_switch,
        
        # Tap
        'tap': fn_tap,
        'through': fn_through,
        
        # Type Checking
        'isNil': fn_is_nil,
        'isNotNil': fn_is_not_nil,
        'isType': fn_is_type,
        
        # Math
        'add': fn_add,
        'subtract': fn_subtract,
        'multiply': fn_multiply,
        'divide': fn_divide,
        'modulo': fn_modulo,
        'inc': fn_inc,
        'dec': fn_dec,
        
        # Monads
        'Maybe': create_maybe,
        'Either': create_either,
        'Just': Maybe.just,
        'Nothing': Maybe.nothing,
        'Left': Either.left,
        'Right': Either.right,
        'tryCatch': fn_try_catch,
    }
