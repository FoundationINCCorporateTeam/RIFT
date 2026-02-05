"""
RIFT Standard Library - Math Module

Comprehensive mathematical functions and operations.
"""

import math
import statistics
import random
from typing import Any, Dict, List, Optional, Union


def create_math_module(interpreter) -> Dict[str, Any]:
    """Create the math module for RIFT."""
    
    # ========================================================================
    # Constants
    # ========================================================================
    
    MATH_PI = math.pi
    MATH_E = math.e
    MATH_TAU = math.tau
    MATH_INF = math.inf
    MATH_NAN = math.nan
    MATH_PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
    MATH_SQRT2 = math.sqrt(2)
    MATH_SQRT3 = math.sqrt(3)
    MATH_LN2 = math.log(2)
    MATH_LN10 = math.log(10)
    MATH_LOG2E = math.log2(math.e)
    MATH_LOG10E = math.log10(math.e)
    
    # ========================================================================
    # Basic Operations
    # ========================================================================
    
    def math_abs(x: Union[int, float]) -> Union[int, float]:
        """Return the absolute value of x."""
        return abs(x)
    
    def math_sign(x: Union[int, float]) -> int:
        """Return the sign of x (-1, 0, or 1)."""
        if x > 0:
            return 1
        elif x < 0:
            return -1
        return 0
    
    def math_floor(x: Union[int, float]) -> int:
        """Return the floor of x (largest integer <= x)."""
        return math.floor(x)
    
    def math_ceil(x: Union[int, float]) -> int:
        """Return the ceiling of x (smallest integer >= x)."""
        return math.ceil(x)
    
    def math_round(x: Union[int, float], digits: int = 0) -> Union[int, float]:
        """Round x to the specified number of digits."""
        return round(x, digits)
    
    def math_trunc(x: Union[int, float]) -> int:
        """Truncate x towards zero."""
        return math.trunc(x)
    
    def math_frac(x: Union[int, float]) -> float:
        """Return the fractional part of x."""
        return x - math.floor(x)
    
    # ========================================================================
    # Power and Root Functions
    # ========================================================================
    
    def math_pow(base: Union[int, float], exp: Union[int, float]) -> float:
        """Return base raised to the power of exp."""
        return math.pow(base, exp)
    
    def math_sqrt(x: Union[int, float]) -> float:
        """Return the square root of x."""
        if x < 0:
            raise ValueError("Cannot compute square root of negative number")
        return math.sqrt(x)
    
    def math_cbrt(x: Union[int, float]) -> float:
        """Return the cube root of x."""
        if x >= 0:
            return x ** (1/3)
        return -(-x) ** (1/3)
    
    def math_nthroot(x: Union[int, float], n: int) -> float:
        """Return the nth root of x."""
        if n == 0:
            raise ValueError("Cannot compute 0th root")
        if x < 0 and n % 2 == 0:
            raise ValueError("Cannot compute even root of negative number")
        if x >= 0:
            return x ** (1/n)
        return -(-x) ** (1/n)
    
    def math_hypot(*args) -> float:
        """Return the Euclidean distance (hypotenuse)."""
        return math.hypot(*args)
    
    # ========================================================================
    # Exponential and Logarithmic Functions
    # ========================================================================
    
    def math_exp(x: Union[int, float]) -> float:
        """Return e raised to the power of x."""
        return math.exp(x)
    
    def math_expm1(x: Union[int, float]) -> float:
        """Return e^x - 1, accurate for small x."""
        return math.expm1(x)
    
    def math_log(x: Union[int, float], base: Union[int, float] = math.e) -> float:
        """Return the logarithm of x with the given base."""
        if x <= 0:
            raise ValueError("Cannot compute logarithm of non-positive number")
        return math.log(x, base)
    
    def math_log2(x: Union[int, float]) -> float:
        """Return the base-2 logarithm of x."""
        if x <= 0:
            raise ValueError("Cannot compute logarithm of non-positive number")
        return math.log2(x)
    
    def math_log10(x: Union[int, float]) -> float:
        """Return the base-10 logarithm of x."""
        if x <= 0:
            raise ValueError("Cannot compute logarithm of non-positive number")
        return math.log10(x)
    
    def math_log1p(x: Union[int, float]) -> float:
        """Return log(1 + x), accurate for small x."""
        return math.log1p(x)
    
    # ========================================================================
    # Trigonometric Functions
    # ========================================================================
    
    def math_sin(x: Union[int, float]) -> float:
        """Return the sine of x (in radians)."""
        return math.sin(x)
    
    def math_cos(x: Union[int, float]) -> float:
        """Return the cosine of x (in radians)."""
        return math.cos(x)
    
    def math_tan(x: Union[int, float]) -> float:
        """Return the tangent of x (in radians)."""
        return math.tan(x)
    
    def math_asin(x: Union[int, float]) -> float:
        """Return the arcsine of x."""
        return math.asin(x)
    
    def math_acos(x: Union[int, float]) -> float:
        """Return the arccosine of x."""
        return math.acos(x)
    
    def math_atan(x: Union[int, float]) -> float:
        """Return the arctangent of x."""
        return math.atan(x)
    
    def math_atan2(y: Union[int, float], x: Union[int, float]) -> float:
        """Return the arctangent of y/x, accounting for quadrant."""
        return math.atan2(y, x)
    
    def math_sinh(x: Union[int, float]) -> float:
        """Return the hyperbolic sine of x."""
        return math.sinh(x)
    
    def math_cosh(x: Union[int, float]) -> float:
        """Return the hyperbolic cosine of x."""
        return math.cosh(x)
    
    def math_tanh(x: Union[int, float]) -> float:
        """Return the hyperbolic tangent of x."""
        return math.tanh(x)
    
    def math_asinh(x: Union[int, float]) -> float:
        """Return the inverse hyperbolic sine of x."""
        return math.asinh(x)
    
    def math_acosh(x: Union[int, float]) -> float:
        """Return the inverse hyperbolic cosine of x."""
        return math.acosh(x)
    
    def math_atanh(x: Union[int, float]) -> float:
        """Return the inverse hyperbolic tangent of x."""
        return math.atanh(x)
    
    # ========================================================================
    # Angle Conversion
    # ========================================================================
    
    def math_degrees(radians: Union[int, float]) -> float:
        """Convert radians to degrees."""
        return math.degrees(radians)
    
    def math_radians(degrees: Union[int, float]) -> float:
        """Convert degrees to radians."""
        return math.radians(degrees)
    
    # ========================================================================
    # Number Theory
    # ========================================================================
    
    def math_gcd(a: int, b: int) -> int:
        """Return the greatest common divisor of a and b."""
        return math.gcd(int(a), int(b))
    
    def math_lcm(a: int, b: int) -> int:
        """Return the least common multiple of a and b."""
        return abs(a * b) // math.gcd(int(a), int(b))
    
    def math_factorial(n: int) -> int:
        """Return n! (n factorial)."""
        if n < 0:
            raise ValueError("Cannot compute factorial of negative number")
        return math.factorial(int(n))
    
    def math_comb(n: int, k: int) -> int:
        """Return n choose k (binomial coefficient)."""
        return math.comb(int(n), int(k))
    
    def math_perm(n: int, k: int = None) -> int:
        """Return permutations of n things taken k at a time."""
        if k is None:
            k = n
        return math.perm(int(n), int(k))
    
    def math_is_prime(n: int) -> bool:
        """Check if n is a prime number."""
        n = int(n)
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def math_primes(limit: int) -> List[int]:
        """Return list of prime numbers up to limit (Sieve of Eratosthenes)."""
        limit = int(limit)
        if limit < 2:
            return []
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(limit ** 0.5) + 1):
            if sieve[i]:
                for j in range(i * i, limit + 1, i):
                    sieve[j] = False
        return [i for i, is_prime in enumerate(sieve) if is_prime]
    
    def math_factors(n: int) -> List[int]:
        """Return prime factors of n."""
        n = int(abs(n))
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    def math_divisors(n: int) -> List[int]:
        """Return all divisors of n."""
        n = int(abs(n))
        divisors = []
        for i in range(1, int(n ** 0.5) + 1):
            if n % i == 0:
                divisors.append(i)
                if i != n // i:
                    divisors.append(n // i)
        return sorted(divisors)
    
    def math_fibonacci(n: int) -> int:
        """Return the nth Fibonacci number."""
        n = int(n)
        if n <= 0:
            return 0
        if n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    def math_fib_sequence(n: int) -> List[int]:
        """Return the first n Fibonacci numbers."""
        n = int(n)
        if n <= 0:
            return []
        if n == 1:
            return [0]
        sequence = [0, 1]
        while len(sequence) < n:
            sequence.append(sequence[-1] + sequence[-2])
        return sequence[:n]
    
    # ========================================================================
    # Statistical Functions
    # ========================================================================
    
    def math_sum(numbers: List[Union[int, float]]) -> Union[int, float]:
        """Return the sum of numbers."""
        return sum(numbers)
    
    def math_product(numbers: List[Union[int, float]]) -> Union[int, float]:
        """Return the product of numbers."""
        result = 1
        for n in numbers:
            result *= n
        return result
    
    def math_mean(numbers: List[Union[int, float]]) -> float:
        """Return the arithmetic mean of numbers."""
        if not numbers:
            raise ValueError("Cannot compute mean of empty list")
        return statistics.mean(numbers)
    
    def math_median(numbers: List[Union[int, float]]) -> float:
        """Return the median of numbers."""
        if not numbers:
            raise ValueError("Cannot compute median of empty list")
        return statistics.median(numbers)
    
    def math_mode(numbers: List[Union[int, float]]) -> Union[int, float]:
        """Return the mode (most common value) of numbers."""
        if not numbers:
            raise ValueError("Cannot compute mode of empty list")
        return statistics.mode(numbers)
    
    def math_variance(numbers: List[Union[int, float]]) -> float:
        """Return the variance of numbers."""
        if len(numbers) < 2:
            raise ValueError("Need at least 2 numbers for variance")
        return statistics.variance(numbers)
    
    def math_stdev(numbers: List[Union[int, float]]) -> float:
        """Return the standard deviation of numbers."""
        if len(numbers) < 2:
            raise ValueError("Need at least 2 numbers for standard deviation")
        return statistics.stdev(numbers)
    
    def math_min(numbers: List[Union[int, float]]) -> Union[int, float]:
        """Return the minimum value."""
        if not numbers:
            raise ValueError("Cannot compute min of empty list")
        return min(numbers)
    
    def math_max(numbers: List[Union[int, float]]) -> Union[int, float]:
        """Return the maximum value."""
        if not numbers:
            raise ValueError("Cannot compute max of empty list")
        return max(numbers)
    
    def math_range_stat(numbers: List[Union[int, float]]) -> Union[int, float]:
        """Return the range (max - min) of numbers."""
        if not numbers:
            raise ValueError("Cannot compute range of empty list")
        return max(numbers) - min(numbers)
    
    def math_percentile(numbers: List[Union[int, float]], p: float) -> float:
        """Return the pth percentile of numbers."""
        if not numbers:
            raise ValueError("Cannot compute percentile of empty list")
        if p < 0 or p > 100:
            raise ValueError("Percentile must be between 0 and 100")
        sorted_nums = sorted(numbers)
        k = (len(sorted_nums) - 1) * (p / 100)
        f = int(k)
        c = f + 1 if f < len(sorted_nums) - 1 else f
        return sorted_nums[f] + (k - f) * (sorted_nums[c] - sorted_nums[f])
    
    def math_quantile(numbers: List[Union[int, float]], q: float) -> float:
        """Return the qth quantile (0-1) of numbers."""
        return math_percentile(numbers, q * 100)
    
    # ========================================================================
    # Random Number Generation
    # ========================================================================
    
    def math_random() -> float:
        """Return a random float between 0 and 1."""
        return random.random()
    
    def math_random_int(min_val: int, max_val: int) -> int:
        """Return a random integer between min and max (inclusive)."""
        return random.randint(int(min_val), int(max_val))
    
    def math_random_float(min_val: float, max_val: float) -> float:
        """Return a random float between min and max."""
        return random.uniform(min_val, max_val)
    
    def math_random_choice(items: List[Any]) -> Any:
        """Return a random item from the list."""
        if not items:
            raise ValueError("Cannot choose from empty list")
        return random.choice(items)
    
    def math_random_sample(items: List[Any], k: int) -> List[Any]:
        """Return k random items from the list without replacement."""
        return random.sample(items, int(k))
    
    def math_shuffle(items: List[Any]) -> List[Any]:
        """Return a shuffled copy of the list."""
        result = items.copy()
        random.shuffle(result)
        return result
    
    def math_seed(seed: int) -> None:
        """Seed the random number generator."""
        random.seed(int(seed))
    
    # ========================================================================
    # Comparison and Clamping
    # ========================================================================
    
    def math_clamp(value: Union[int, float], 
                   min_val: Union[int, float], 
                   max_val: Union[int, float]) -> Union[int, float]:
        """Clamp value between min and max."""
        return max(min_val, min(max_val, value))
    
    def math_lerp(a: float, b: float, t: float) -> float:
        """Linear interpolation between a and b by t (0-1)."""
        return a + (b - a) * t
    
    def math_inverse_lerp(a: float, b: float, value: float) -> float:
        """Inverse linear interpolation: find t where lerp(a, b, t) = value."""
        if a == b:
            return 0.0
        return (value - a) / (b - a)
    
    def math_remap(value: float, in_min: float, in_max: float, 
                   out_min: float, out_max: float) -> float:
        """Remap value from input range to output range."""
        t = math_inverse_lerp(in_min, in_max, value)
        return math_lerp(out_min, out_max, t)
    
    def math_smooth_step(edge0: float, edge1: float, x: float) -> float:
        """Smooth Hermite interpolation between 0 and 1."""
        t = math_clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return t * t * (3 - 2 * t)
    
    # ========================================================================
    # Vector and Matrix Operations (2D/3D basics)
    # ========================================================================
    
    def math_dot2d(v1: List[float], v2: List[float]) -> float:
        """2D dot product."""
        return v1[0] * v2[0] + v1[1] * v2[1]
    
    def math_dot3d(v1: List[float], v2: List[float]) -> float:
        """3D dot product."""
        return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    
    def math_cross3d(v1: List[float], v2: List[float]) -> List[float]:
        """3D cross product."""
        return [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]
    
    def math_magnitude2d(v: List[float]) -> float:
        """2D vector magnitude."""
        return math.sqrt(v[0] ** 2 + v[1] ** 2)
    
    def math_magnitude3d(v: List[float]) -> float:
        """3D vector magnitude."""
        return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    
    def math_normalize2d(v: List[float]) -> List[float]:
        """Normalize 2D vector."""
        mag = math_magnitude2d(v)
        if mag == 0:
            return [0, 0]
        return [v[0] / mag, v[1] / mag]
    
    def math_normalize3d(v: List[float]) -> List[float]:
        """Normalize 3D vector."""
        mag = math_magnitude3d(v)
        if mag == 0:
            return [0, 0, 0]
        return [v[0] / mag, v[1] / mag, v[2] / mag]
    
    def math_distance2d(p1: List[float], p2: List[float]) -> float:
        """Distance between two 2D points."""
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    
    def math_distance3d(p1: List[float], p2: List[float]) -> float:
        """Distance between two 3D points."""
        return math.sqrt(
            (p2[0] - p1[0]) ** 2 + 
            (p2[1] - p1[1]) ** 2 + 
            (p2[2] - p1[2]) ** 2
        )
    
    def math_angle2d(v1: List[float], v2: List[float]) -> float:
        """Angle between two 2D vectors (in radians)."""
        dot = math_dot2d(v1, v2)
        mag1 = math_magnitude2d(v1)
        mag2 = math_magnitude2d(v2)
        if mag1 == 0 or mag2 == 0:
            return 0
        cos_angle = math_clamp(dot / (mag1 * mag2), -1, 1)
        return math.acos(cos_angle)
    
    # ========================================================================
    # Utility Functions
    # ========================================================================
    
    def math_is_nan(x: Union[int, float]) -> bool:
        """Check if x is NaN."""
        return math.isnan(x)
    
    def math_is_inf(x: Union[int, float]) -> bool:
        """Check if x is infinite."""
        return math.isinf(x)
    
    def math_is_finite(x: Union[int, float]) -> bool:
        """Check if x is finite."""
        return math.isfinite(x)
    
    def math_is_integer(x: Union[int, float]) -> bool:
        """Check if x is an integer value."""
        return float(x).is_integer()
    
    def math_is_even(x: int) -> bool:
        """Check if x is even."""
        return int(x) % 2 == 0
    
    def math_is_odd(x: int) -> bool:
        """Check if x is odd."""
        return int(x) % 2 != 0
    
    def math_copysign(x: Union[int, float], y: Union[int, float]) -> float:
        """Return x with the sign of y."""
        return math.copysign(x, y)
    
    def math_fmod(x: Union[int, float], y: Union[int, float]) -> float:
        """Return floating-point remainder of x/y."""
        return math.fmod(x, y)
    
    def math_modf(x: Union[int, float]) -> Dict[str, float]:
        """Return fractional and integer parts of x."""
        frac, integer = math.modf(x)
        return {'frac': frac, 'integer': integer}
    
    return {
        # Constants
        'PI': MATH_PI,
        'E': MATH_E,
        'TAU': MATH_TAU,
        'INF': MATH_INF,
        'NAN': MATH_NAN,
        'PHI': MATH_PHI,
        'SQRT2': MATH_SQRT2,
        'SQRT3': MATH_SQRT3,
        'LN2': MATH_LN2,
        'LN10': MATH_LN10,
        'LOG2E': MATH_LOG2E,
        'LOG10E': MATH_LOG10E,
        
        # Basic Operations
        'abs': math_abs,
        'sign': math_sign,
        'floor': math_floor,
        'ceil': math_ceil,
        'round': math_round,
        'trunc': math_trunc,
        'frac': math_frac,
        
        # Power and Root
        'pow': math_pow,
        'sqrt': math_sqrt,
        'cbrt': math_cbrt,
        'nthroot': math_nthroot,
        'hypot': math_hypot,
        
        # Exponential and Logarithmic
        'exp': math_exp,
        'expm1': math_expm1,
        'log': math_log,
        'log2': math_log2,
        'log10': math_log10,
        'log1p': math_log1p,
        
        # Trigonometric
        'sin': math_sin,
        'cos': math_cos,
        'tan': math_tan,
        'asin': math_asin,
        'acos': math_acos,
        'atan': math_atan,
        'atan2': math_atan2,
        'sinh': math_sinh,
        'cosh': math_cosh,
        'tanh': math_tanh,
        'asinh': math_asinh,
        'acosh': math_acosh,
        'atanh': math_atanh,
        
        # Angle Conversion
        'degrees': math_degrees,
        'radians': math_radians,
        
        # Number Theory
        'gcd': math_gcd,
        'lcm': math_lcm,
        'factorial': math_factorial,
        'comb': math_comb,
        'perm': math_perm,
        'isPrime': math_is_prime,
        'primes': math_primes,
        'factors': math_factors,
        'divisors': math_divisors,
        'fibonacci': math_fibonacci,
        'fibSequence': math_fib_sequence,
        
        # Statistical
        'sum': math_sum,
        'product': math_product,
        'mean': math_mean,
        'median': math_median,
        'mode': math_mode,
        'variance': math_variance,
        'stdev': math_stdev,
        'min': math_min,
        'max': math_max,
        'range': math_range_stat,
        'percentile': math_percentile,
        'quantile': math_quantile,
        
        # Random
        'random': math_random,
        'randomInt': math_random_int,
        'randomFloat': math_random_float,
        'randomChoice': math_random_choice,
        'randomSample': math_random_sample,
        'shuffle': math_shuffle,
        'seed': math_seed,
        
        # Comparison and Clamping
        'clamp': math_clamp,
        'lerp': math_lerp,
        'inverseLerp': math_inverse_lerp,
        'remap': math_remap,
        'smoothStep': math_smooth_step,
        
        # Vector Operations
        'dot2d': math_dot2d,
        'dot3d': math_dot3d,
        'cross3d': math_cross3d,
        'magnitude2d': math_magnitude2d,
        'magnitude3d': math_magnitude3d,
        'normalize2d': math_normalize2d,
        'normalize3d': math_normalize3d,
        'distance2d': math_distance2d,
        'distance3d': math_distance3d,
        'angle2d': math_angle2d,
        
        # Utility
        'isNaN': math_is_nan,
        'isInf': math_is_inf,
        'isFinite': math_is_finite,
        'isInteger': math_is_integer,
        'isEven': math_is_even,
        'isOdd': math_is_odd,
        'copysign': math_copysign,
        'fmod': math_fmod,
        'modf': math_modf,
    }
