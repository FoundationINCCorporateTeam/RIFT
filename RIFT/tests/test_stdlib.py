"""
RIFT Standard Library Test Suite

Comprehensive tests for all RIFT standard library modules.
"""

import unittest
import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.interpreter import Interpreter, interpret


class TestMathModule(unittest.TestCase):
    """Test the math module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.math = self.interp._load_math_module()
    
    def test_constants(self):
        """Test math constants."""
        self.assertAlmostEqual(self.math['PI'], 3.14159, places=4)
        self.assertAlmostEqual(self.math['E'], 2.71828, places=4)
        self.assertAlmostEqual(self.math['PHI'], 1.61803, places=4)
    
    def test_basic_operations(self):
        """Test basic math operations."""
        self.assertEqual(self.math['abs'](-5), 5)
        self.assertEqual(self.math['sign'](-10), -1)
        self.assertEqual(self.math['sign'](10), 1)
        self.assertEqual(self.math['sign'](0), 0)
        self.assertEqual(self.math['floor'](3.7), 3)
        self.assertEqual(self.math['ceil'](3.2), 4)
        self.assertEqual(self.math['round'](3.5), 4)
        self.assertEqual(self.math['trunc'](3.9), 3)
    
    def test_power_and_roots(self):
        """Test power and root functions."""
        self.assertEqual(self.math['pow'](2, 3), 8)
        self.assertEqual(self.math['sqrt'](16), 4)
        self.assertAlmostEqual(self.math['cbrt'](27), 3, places=5)
    
    def test_trigonometry(self):
        """Test trigonometric functions."""
        import math
        self.assertAlmostEqual(self.math['sin'](0), 0, places=10)
        self.assertAlmostEqual(self.math['cos'](0), 1, places=10)
        self.assertAlmostEqual(self.math['tan'](0), 0, places=10)
        self.assertAlmostEqual(self.math['sin'](math.pi / 2), 1, places=10)
    
    def test_number_theory(self):
        """Test number theory functions."""
        self.assertEqual(self.math['gcd'](12, 18), 6)
        self.assertEqual(self.math['lcm'](4, 6), 12)
        self.assertEqual(self.math['factorial'](5), 120)
        self.assertTrue(self.math['isPrime'](17))
        self.assertFalse(self.math['isPrime'](15))
        self.assertEqual(self.math['primes'](20), [2, 3, 5, 7, 11, 13, 17, 19])
        self.assertEqual(self.math['factors'](12), [2, 2, 3])
        self.assertEqual(self.math['fibonacci'](10), 55)
    
    def test_statistics(self):
        """Test statistical functions."""
        data = [1, 2, 3, 4, 5]
        self.assertEqual(self.math['sum'](data), 15)
        self.assertEqual(self.math['mean'](data), 3)
        self.assertEqual(self.math['median'](data), 3)
        self.assertEqual(self.math['min'](data), 1)
        self.assertEqual(self.math['max'](data), 5)
    
    def test_random(self):
        """Test random functions."""
        self.math['seed'](42)
        r = self.math['random']()
        self.assertTrue(0 <= r <= 1)
        
        ri = self.math['randomInt'](1, 10)
        self.assertTrue(1 <= ri <= 10)
        
        items = [1, 2, 3, 4, 5]
        choice = self.math['randomChoice'](items)
        self.assertIn(choice, items)
    
    def test_vector_operations(self):
        """Test vector operations."""
        v1 = [1, 2]
        v2 = [3, 4]
        self.assertEqual(self.math['dot2d'](v1, v2), 11)
        self.assertAlmostEqual(self.math['magnitude2d'](v1), 2.236, places=3)
        
        v3 = [1, 0, 0]
        v4 = [0, 1, 0]
        self.assertEqual(self.math['cross3d'](v3, v4), [0, 0, 1])
    
    def test_utility_functions(self):
        """Test utility functions."""
        self.assertEqual(self.math['clamp'](5, 0, 10), 5)
        self.assertEqual(self.math['clamp'](-5, 0, 10), 0)
        self.assertEqual(self.math['clamp'](15, 0, 10), 10)
        self.assertEqual(self.math['lerp'](0, 10, 0.5), 5)
        self.assertTrue(self.math['isEven'](4))
        self.assertTrue(self.math['isOdd'](3))


class TestStringModule(unittest.TestCase):
    """Test the string module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.string = self.interp._load_string_module()
    
    def test_case_conversion(self):
        """Test case conversion functions."""
        self.assertEqual(self.string['upper']('hello'), 'HELLO')
        self.assertEqual(self.string['lower']('HELLO'), 'hello')
        self.assertEqual(self.string['capitalize']('hello'), 'Hello')
        self.assertEqual(self.string['title']('hello world'), 'Hello World')
        self.assertEqual(self.string['camelCase']('hello_world'), 'helloWorld')
        self.assertEqual(self.string['pascalCase']('hello_world'), 'HelloWorld')
        self.assertEqual(self.string['snakeCase']('helloWorld'), 'hello_world')
        self.assertEqual(self.string['kebabCase']('helloWorld'), 'hello-world')
    
    def test_trimming_and_padding(self):
        """Test trimming and padding functions."""
        self.assertEqual(self.string['trim']('  hello  '), 'hello')
        self.assertEqual(self.string['trimStart']('  hello'), 'hello')
        self.assertEqual(self.string['trimEnd']('hello  '), 'hello')
        self.assertEqual(self.string['padStart']('5', 3, '0'), '005')
        self.assertEqual(self.string['padEnd']('5', 3, '0'), '500')
        self.assertEqual(self.string['truncate']('hello world', 8), 'hello...')
    
    def test_search_and_replace(self):
        """Test search and replace functions."""
        self.assertTrue(self.string['contains']('hello world', 'world'))
        self.assertTrue(self.string['startsWith']('hello', 'hel'))
        self.assertTrue(self.string['endsWith']('hello', 'lo'))
        self.assertEqual(self.string['indexOf']('hello', 'l'), 2)
        self.assertEqual(self.string['lastIndexOf']('hello', 'l'), 3)
        self.assertEqual(self.string['count']('hello', 'l'), 2)
        self.assertEqual(self.string['replace']('hello', 'l', 'L', 1), 'heLlo')  # Replace only first
        self.assertEqual(self.string['replace']('hello', 'l', 'L'), 'heLLo')  # Replace all by default
        self.assertEqual(self.string['remove']('hello', 'l'), 'heo')
    
    def test_splitting_and_joining(self):
        """Test splitting and joining functions."""
        self.assertEqual(self.string['split']('a,b,c', ','), ['a', 'b', 'c'])
        self.assertEqual(self.string['join'](['a', 'b', 'c'], '-'), 'a-b-c')
        self.assertEqual(self.string['chunk']('abcdef', 2), ['ab', 'cd', 'ef'])
        self.assertEqual(self.string['splitLines']('a\nb\nc'), ['a', 'b', 'c'])
    
    def test_validation(self):
        """Test validation functions."""
        self.assertTrue(self.string['isEmpty'](''))
        self.assertTrue(self.string['isBlank']('   '))
        self.assertTrue(self.string['isAlpha']('hello'))
        self.assertTrue(self.string['isNumeric']('12345'))
        self.assertTrue(self.string['isAlphanumeric']('hello123'))
    
    def test_comparison(self):
        """Test comparison functions."""
        self.assertTrue(self.string['equals']('hello', 'hello'))
        self.assertTrue(self.string['equalsIgnoreCase']('Hello', 'hello'))
        self.assertEqual(self.string['levenshtein']('kitten', 'sitting'), 3)
        self.assertAlmostEqual(self.string['similarity']('hello', 'hallo'), 0.8, places=1)
    
    def test_extraction(self):
        """Test extraction functions."""
        self.assertEqual(self.string['extractNumbers']('a1b2c3'), [1.0, 2.0, 3.0])
        self.assertEqual(self.string['extractHashtags']('#hello #world'), ['#hello', '#world'])
        self.assertEqual(self.string['extractEmails']('test@example.com'), ['test@example.com'])
    
    def test_slugify(self):
        """Test slugify function."""
        self.assertEqual(self.string['slugify']('Hello World!'), 'hello-world')
        self.assertEqual(self.string['humanize']('hello_world'), 'Hello world')


class TestArrayModule(unittest.TestCase):
    """Test the array module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.array = self.interp._load_array_module()
    
    def test_creation(self):
        """Test array creation functions."""
        self.assertEqual(self.array['create'](3, 0), [0, 0, 0])
        self.assertEqual(self.array['range'](5), [0, 1, 2, 3, 4])
        self.assertEqual(self.array['range'](1, 5), [1, 2, 3, 4])
        self.assertEqual(self.array['of'](1, 2, 3), [1, 2, 3])
        self.assertEqual(self.array['repeat']('x', 3), ['x', 'x', 'x'])
    
    def test_access(self):
        """Test array access functions."""
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(self.array['first'](arr), 1)
        self.assertEqual(self.array['last'](arr), 5)
        self.assertEqual(self.array['get'](arr, 2), 3)
        self.assertEqual(self.array['head'](arr, 3), [1, 2, 3])
        self.assertEqual(self.array['tail'](arr, 2), [4, 5])
        self.assertEqual(self.array['rest'](arr), [2, 3, 4, 5])
        self.assertEqual(self.array['initial'](arr), [1, 2, 3, 4])
    
    def test_modification(self):
        """Test array modification functions."""
        arr = [1, 2, 3]
        self.assertEqual(self.array['push'](arr, 4), [1, 2, 3, 4])
        self.assertEqual(self.array['unshift'](arr, 0), [0, 1, 2, 3])
        self.assertEqual(self.array['removeAt'](arr, 1), [1, 3])
        self.assertEqual(self.array['reverse'](arr), [3, 2, 1])
        self.assertEqual(self.array['rotate']([1, 2, 3, 4], 1), [4, 1, 2, 3])
    
    def test_slicing(self):
        """Test array slicing functions."""
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(self.array['slice'](arr, 1, 4), [2, 3, 4])
        self.assertEqual(self.array['chunk']([1, 2, 3, 4, 5, 6], 2), [[1, 2], [3, 4], [5, 6]])
    
    def test_searching(self):
        """Test array searching functions."""
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(self.array['indexOf'](arr, 3), 2)
        self.assertEqual(self.array['indexOf'](arr, 10), -1)
        self.assertTrue(self.array['includes'](arr, 3))
        self.assertFalse(self.array['includes'](arr, 10))
    
    def test_testing(self):
        """Test array testing functions."""
        arr = [1, 2, 3, 4, 5]
        self.assertTrue(self.array['isEmpty']([]))
        self.assertFalse(self.array['isEmpty'](arr))
        self.assertTrue(self.array['isSorted']([1, 2, 3, 4, 5]))
        self.assertFalse(self.array['isSorted']([1, 3, 2]))
        self.assertTrue(self.array['isUnique']([1, 2, 3]))
        self.assertFalse(self.array['isUnique']([1, 2, 1]))
    
    def test_aggregation(self):
        """Test array aggregation functions."""
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(self.array['sum'](arr), 15)
        self.assertEqual(self.array['product'](arr), 120)
        self.assertEqual(self.array['min'](arr), 1)
        self.assertEqual(self.array['max'](arr), 5)
        self.assertEqual(self.array['mean'](arr), 3)
    
    def test_set_operations(self):
        """Test set operations."""
        arr1 = [1, 2, 3]
        arr2 = [2, 3, 4]
        self.assertEqual(self.array['unique']([1, 2, 2, 3, 3, 3]), [1, 2, 3])
        self.assertEqual(self.array['union'](arr1, arr2), [1, 2, 3, 4])
        self.assertEqual(self.array['intersection'](arr1, arr2), [2, 3])
        self.assertEqual(self.array['difference'](arr1, arr2), [1])
    
    def test_combination(self):
        """Test combination functions."""
        self.assertEqual(self.array['concat']([1, 2], [3, 4]), [1, 2, 3, 4])
        self.assertEqual(self.array['zip']([1, 2], ['a', 'b']), [[1, 'a'], [2, 'b']])
        self.assertEqual(self.array['flat']([[1, 2], [3, 4]]), [1, 2, 3, 4])
        self.assertEqual(self.array['interleave']([1, 3], [2, 4]), [1, 2, 3, 4])


class TestDateTimeModule(unittest.TestCase):
    """Test the datetime module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.datetime = self.interp._load_datetime_module()
    
    def test_now(self):
        """Test now functions."""
        now = self.datetime['now']()
        self.assertIn('year', now)
        self.assertIn('month', now)
        self.assertIn('day', now)
        
        ts = self.datetime['timestamp']()
        self.assertIsInstance(ts, float)
        self.assertGreater(ts, 0)
    
    def test_create(self):
        """Test date creation."""
        dt = self.datetime['create'](2024, 6, 15, 12, 30, 0)
        self.assertEqual(dt['year'], 2024)
        self.assertEqual(dt['month'], 6)
        self.assertEqual(dt['day'], 15)
        self.assertEqual(dt['hour'], 12)
        self.assertEqual(dt['minute'], 30)
    
    def test_formatting(self):
        """Test date formatting."""
        dt = self.datetime['create'](2024, 6, 15, 12, 30, 0)
        formatted = self.datetime['format'](dt, '%Y-%m-%d')
        self.assertEqual(formatted, '2024-06-15')
        
        iso = self.datetime['toIso'](dt)
        self.assertIn('2024-06-15', iso)
    
    def test_manipulation(self):
        """Test date manipulation."""
        dt = self.datetime['create'](2024, 6, 15)
        
        added = self.datetime['add'](dt, days=5)
        self.assertEqual(added['day'], 20)
        
        subtracted = self.datetime['subtract'](dt, days=5)
        self.assertEqual(subtracted['day'], 10)
        
        start_of_month = self.datetime['startOf'](dt, 'month')
        self.assertEqual(start_of_month['day'], 1)
        
        end_of_month = self.datetime['endOf'](dt, 'month')
        self.assertEqual(end_of_month['day'], 30)  # June has 30 days
    
    def test_comparison(self):
        """Test date comparison."""
        dt1 = self.datetime['create'](2024, 6, 15)
        dt2 = self.datetime['create'](2024, 6, 20)
        
        self.assertTrue(self.datetime['isBefore'](dt1, dt2))
        self.assertTrue(self.datetime['isAfter'](dt2, dt1))
        self.assertTrue(self.datetime['isSame'](dt1, dt1))
        
        diff = self.datetime['diff'](dt1, dt2, 'days')
        self.assertEqual(diff, 5)
    
    def test_properties(self):
        """Test date properties."""
        self.assertTrue(self.datetime['isLeapYear'](2024))
        self.assertFalse(self.datetime['isLeapYear'](2023))
        self.assertEqual(self.datetime['daysInMonth'](2024, 2), 29)  # Leap year
        self.assertEqual(self.datetime['daysInMonth'](2023, 2), 28)
        
        saturday = self.datetime['create'](2024, 6, 15)  # Saturday
        self.assertTrue(self.datetime['isWeekend'](saturday))


class TestRegexModule(unittest.TestCase):
    """Test the regex module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.regex = self.interp._load_regex_module()
    
    def test_matching(self):
        """Test regex matching."""
        match = self.regex['match'](r'\d+', '123abc')
        self.assertIsNotNone(match)
        self.assertEqual(match['match'], '123')
        
        search = self.regex['search'](r'\d+', 'abc123def')
        self.assertIsNotNone(search)
        self.assertEqual(search['match'], '123')
    
    def test_find_all(self):
        """Test find all."""
        matches = self.regex['findAll'](r'\d+', 'a1b2c3')
        self.assertEqual(matches, ['1', '2', '3'])
    
    def test_testing(self):
        """Test regex testing."""
        self.assertTrue(self.regex['test'](r'\d+', 'abc123'))
        self.assertFalse(self.regex['test'](r'\d+', 'abc'))
        self.assertTrue(self.regex['isValid'](r'\d+'))
        self.assertFalse(self.regex['isValid'](r'['))
    
    def test_replacement(self):
        """Test regex replacement."""
        result = self.regex['replace'](r'\d+', 'X', 'a1b2c3')
        self.assertEqual(result, 'aXbXcX')
        
        result = self.regex['replaceFirst'](r'\d+', 'X', 'a1b2c3')
        self.assertEqual(result, 'aXb2c3')
    
    def test_splitting(self):
        """Test regex splitting."""
        result = self.regex['split'](r'\s+', 'a b  c')
        self.assertEqual(result, ['a', 'b', 'c'])
    
    def test_groups(self):
        """Test group extraction."""
        groups = self.regex['groups'](r'(\w+)@(\w+)', 'test@example')
        self.assertEqual(groups, ['test', 'example'])
        
        named = self.regex['namedGroups'](r'(?P<user>\w+)@(?P<domain>\w+)', 'test@example')
        self.assertEqual(named['user'], 'test')
        self.assertEqual(named['domain'], 'example')
    
    def test_common_patterns(self):
        """Test common pattern validation."""
        self.assertTrue(self.regex['validateEmail']('test@example.com'))
        self.assertFalse(self.regex['validateEmail']('invalid'))
        self.assertTrue(self.regex['validateUrl']('https://example.com'))
        self.assertTrue(self.regex['validateIpv4']('192.168.1.1'))
        self.assertTrue(self.regex['validateUuid']('550e8400-e29b-41d4-a716-446655440000'))


class TestValidationModule(unittest.TestCase):
    """Test the validation module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.validation = self.interp._load_validation_module()
    
    def test_type_validators(self):
        """Test type validators."""
        self.assertTrue(self.validation['isString']('hello'))
        self.assertFalse(self.validation['isString'](123))
        self.assertTrue(self.validation['isNumber'](123))
        self.assertTrue(self.validation['isNumber'](3.14))
        self.assertTrue(self.validation['isBoolean'](True))
        self.assertTrue(self.validation['isArray']([1, 2, 3]))
        self.assertTrue(self.validation['isObject']({'a': 1}))
        self.assertTrue(self.validation['isNull'](None))
    
    def test_string_validators(self):
        """Test string validators."""
        self.assertTrue(self.validation['isEmail']('test@example.com'))
        self.assertFalse(self.validation['isEmail']('invalid'))
        self.assertTrue(self.validation['isUrl']('https://example.com'))
        self.assertTrue(self.validation['isUuid']('550e8400-e29b-41d4-a716-446655440000'))
        self.assertTrue(self.validation['isIpv4']('192.168.1.1'))
        self.assertTrue(self.validation['isAlpha']('hello'))
        self.assertTrue(self.validation['isNumericString']('12345'))
        self.assertTrue(self.validation['isJson']('{"a": 1}'))
    
    def test_number_validators(self):
        """Test number validators."""
        self.assertTrue(self.validation['isPositive'](5))
        self.assertTrue(self.validation['isNegative'](-5))
        self.assertTrue(self.validation['isZero'](0))
        self.assertTrue(self.validation['isBetween'](5, 1, 10))
        self.assertTrue(self.validation['isEven'](4))
        self.assertTrue(self.validation['isOdd'](3))
        self.assertTrue(self.validation['isPort'](8080))
    
    def test_string_content(self):
        """Test string content validators."""
        self.assertTrue(self.validation['minLength']('hello', 3))
        self.assertTrue(self.validation['maxLength']('hello', 10))
        self.assertTrue(self.validation['lengthBetween']('hello', 3, 10))
        self.assertTrue(self.validation['contains']('hello world', 'world'))
        self.assertTrue(self.validation['startsWith']('hello', 'hel'))
        self.assertTrue(self.validation['endsWith']('hello', 'lo'))
        self.assertTrue(self.validation['inList']('a', ['a', 'b', 'c']))
    
    def test_password_strength(self):
        """Test password strength."""
        weak = self.validation['passwordStrength']('abc')
        self.assertFalse(weak['valid'])
        self.assertEqual(weak['strength'], 'weak')
        
        strong = self.validation['passwordStrength']('MyP@ssw0rd123')
        self.assertTrue(strong['valid'])
        self.assertEqual(strong['strength'], 'strong')
    
    def test_sanitization(self):
        """Test sanitization functions."""
        self.assertEqual(self.validation['sanitizeString']('  hello  '), 'hello')
        self.assertEqual(self.validation['sanitizeNumber']('123'), 123.0)
        self.assertEqual(self.validation['escapeHtml']('<script>'), '&lt;script&gt;')
        self.assertEqual(self.validation['stripHtml']('<p>hello</p>'), 'hello')


class TestCollectionsModule(unittest.TestCase):
    """Test the collections module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.collections = self.interp._load_collections_module()
    
    def test_stack(self):
        """Test Stack data structure."""
        stack = self.collections['Stack']()
        stack.push(1, 2, 3)
        self.assertEqual(stack.size(), 3)
        self.assertEqual(stack.peek(), 3)
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.size(), 2)
        self.assertEqual(stack.toList(), [2, 1])
    
    def test_queue(self):
        """Test Queue data structure."""
        queue = self.collections['Queue']()
        queue.enqueue(1, 2, 3)
        self.assertEqual(queue.size(), 3)
        self.assertEqual(queue.peek(), 1)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.size(), 2)
    
    def test_deque(self):
        """Test Deque data structure."""
        deque = self.collections['Deque']()
        deque.pushBack(1).pushBack(2)
        deque.pushFront(0)
        self.assertEqual(deque.toList(), [0, 1, 2])
        self.assertEqual(deque.popFront(), 0)
        self.assertEqual(deque.popBack(), 2)
    
    def test_linked_list(self):
        """Test LinkedList data structure."""
        ll = self.collections['LinkedList']([1, 2, 3])
        self.assertEqual(ll.size(), 3)
        self.assertEqual(ll.head(), 1)
        self.assertEqual(ll.tail(), 3)
        ll.append(4)
        self.assertEqual(ll.tail(), 4)
        ll.prepend(0)
        self.assertEqual(ll.head(), 0)
        self.assertEqual(ll.indexOf(2), 2)
    
    def test_set(self):
        """Test Set data structure."""
        s = self.collections['Set']([1, 2, 3])
        s.add(4)
        self.assertEqual(s.size(), 4)
        self.assertTrue(s.has(3))
        s.remove(3)
        self.assertFalse(s.has(3))
        
        s2 = self.collections['Set']([3, 4, 5])
        union = s.union(s2)
        # s has [1, 2, 4] after removing 3, s2 has [3, 4, 5]
        # union should be [1, 2, 3, 4, 5]
        self.assertEqual(sorted(union.toList()), [1, 2, 3, 4, 5])
    
    def test_map(self):
        """Test Map data structure."""
        m = self.collections['Map']({'a': 1, 'b': 2})
        m.set('c', 3)
        self.assertEqual(m.get('c'), 3)
        self.assertTrue(m.has('a'))
        self.assertEqual(m.keys(), ['a', 'b', 'c'])
        self.assertEqual(m.values(), [1, 2, 3])
    
    def test_counter(self):
        """Test Counter data structure."""
        c = self.collections['Counter'](['a', 'b', 'a', 'a', 'b', 'c'])
        self.assertEqual(c.count('a'), 3)
        self.assertEqual(c.count('b'), 2)
        self.assertEqual(c.mostCommon(2), [['a', 3], ['b', 2]])
    
    def test_lru_cache(self):
        """Test LRU Cache."""
        cache = self.collections['LRUCache'](3)
        cache.set('a', 1).set('b', 2).set('c', 3)
        self.assertEqual(cache.get('a'), 1)
        cache.set('d', 4)  # Should evict 'b' (least recently used)
        self.assertIsNone(cache.get('b'))
        self.assertEqual(cache.get('d'), 4)


class TestEventsModule(unittest.TestCase):
    """Test the events module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.events = self.interp._load_events_module()
    
    def test_event_emitter(self):
        """Test EventEmitter."""
        emitter = self.events['EventEmitter']()
        results = []
        
        def handler(data):
            results.append(data)
        
        emitter.on('test', handler)
        emitter.emit('test', 'hello')
        
        # Give time for async callback
        time.sleep(0.1)
        self.assertEqual(results, ['hello'])
    
    def test_once_listener(self):
        """Test once listener."""
        emitter = self.events['EventEmitter']()
        results = []
        
        def handler(data):
            results.append(data)
        
        emitter.once('test', handler)
        emitter.emit('test', 'first')
        emitter.emit('test', 'second')
        
        time.sleep(0.1)
        self.assertEqual(results, ['first'])
    
    def test_off(self):
        """Test removing listeners."""
        emitter = self.events['EventEmitter']()
        results = []
        
        def handler(data):
            results.append(data)
        
        emitter.on('test', handler)
        emitter.off('test', handler)
        emitter.emit('test', 'hello')
        
        time.sleep(0.1)
        self.assertEqual(results, [])


class TestLoggingModule(unittest.TestCase):
    """Test the logging module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.logging = self.interp._load_logging_module()
    
    def test_logger_creation(self):
        """Test logger creation."""
        logger = self.logging['Logger']('test')
        self.assertIsNotNone(logger)
    
    def test_log_levels(self):
        """Test log level constants."""
        self.assertEqual(self.logging['TRACE'], 0)
        self.assertEqual(self.logging['DEBUG'], 10)
        self.assertEqual(self.logging['INFO'], 20)
        self.assertEqual(self.logging['WARN'], 30)
        self.assertEqual(self.logging['ERROR'], 40)
        self.assertEqual(self.logging['FATAL'], 50)
    
    def test_memory_handler(self):
        """Test memory handler."""
        handler = self.logging['MemoryHandler']()
        logger = self.logging['Logger']('test')
        logger.handlers = [handler]
        
        logger.info('Test message')
        
        records = handler.get_records()
        self.assertEqual(len(records), 1)
        self.assertIn('Test message', records[0])


class TestAsyncModule(unittest.TestCase):
    """Test the async module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.async_mod = self.interp._load_async_module()
    
    def test_promise_resolve(self):
        """Test Promise.resolve."""
        promise = self.async_mod['resolve'](42)
        result = promise.await_(timeout=1)
        self.assertEqual(result, 42)
    
    def test_promise_reject(self):
        """Test Promise.reject."""
        promise = self.async_mod['reject']('error')
        with self.assertRaises(Exception):
            promise.await_(timeout=1)
    
    def test_delay(self):
        """Test async delay."""
        start = time.time()
        promise = self.async_mod['delay'](100)  # 100ms
        promise.await_(timeout=1)
        elapsed = (time.time() - start) * 1000
        self.assertGreater(elapsed, 90)  # Should take at least 90ms
    
    def test_promise_all(self):
        """Test Promise.all."""
        p1 = self.async_mod['resolve'](1)
        p2 = self.async_mod['resolve'](2)
        p3 = self.async_mod['resolve'](3)
        
        result = self.async_mod['all']([p1, p2, p3]).await_(timeout=1)
        self.assertEqual(result, [1, 2, 3])
    
    def test_promise_race(self):
        """Test Promise.race."""
        p1 = self.async_mod['delay'](100)
        p1.then(lambda _: 1)  # This won't work as expected, but tests structure
        p2 = self.async_mod['resolve'](2)
        
        result = self.async_mod['race']([p1, p2]).await_(timeout=1)
        self.assertEqual(result, 2)  # p2 resolves immediately
    
    def test_semaphore(self):
        """Test Semaphore."""
        sem = self.async_mod['Semaphore'](2)
        self.assertEqual(sem.available, 2)
        
        sem.acquire().await_(timeout=1)
        self.assertEqual(sem.available, 1)
        
        sem.release()
        self.assertEqual(sem.available, 2)
    
    def test_mutex(self):
        """Test Mutex."""
        mutex = self.async_mod['Mutex']()
        self.assertFalse(mutex.isLocked)
        
        mutex.lock().await_(timeout=1)
        self.assertTrue(mutex.isLocked)
        
        mutex.unlock()
        self.assertFalse(mutex.isLocked)


class TestFunctionalModule(unittest.TestCase):
    """Test the functional module."""
    
    def setUp(self):
        self.interp = Interpreter()
        self.fn = self.interp._load_functional_module()
    
    def test_identity(self):
        """Test identity function."""
        self.assertEqual(self.fn['identity'](5), 5)
        self.assertEqual(self.fn['identity']('hello'), 'hello')
    
    def test_constant(self):
        """Test constant function."""
        always5 = self.fn['constant'](5)
        self.assertEqual(always5(), 5)
        self.assertEqual(always5(10, 20), 5)
    
    def test_comparison_predicates(self):
        """Test comparison predicates."""
        eq5 = self.fn['eq'](5)
        self.assertTrue(eq5(5))
        self.assertFalse(eq5(6))
        
        gt5 = self.fn['gt'](5)
        self.assertTrue(gt5(10))
        self.assertFalse(gt5(3))
        
        between = self.fn['between'](1, 10)
        self.assertTrue(between(5))
        self.assertFalse(between(15))
    
    def test_type_checking(self):
        """Test type checking predicates."""
        self.assertTrue(self.fn['isNil'](None))
        self.assertFalse(self.fn['isNil'](5))
        self.assertTrue(self.fn['isNotNil'](5))
        
        isString = self.fn['isType']('string')
        self.assertTrue(isString('hello'))
        self.assertFalse(isString(123))
    
    def test_inc_dec(self):
        """Test increment/decrement."""
        self.assertEqual(self.fn['inc'](5), 6)
        self.assertEqual(self.fn['dec'](5), 4)
    
    def test_maybe_monad(self):
        """Test Maybe monad."""
        just = self.fn['Just'](5)
        self.assertTrue(just.isJust())
        self.assertFalse(just.isNothing())
        self.assertEqual(just.getOrElse(0), 5)
        
        nothing = self.fn['Nothing']()
        self.assertTrue(nothing.isNothing())
        self.assertEqual(nothing.getOrElse(0), 0)
    
    def test_either_monad(self):
        """Test Either monad."""
        right = self.fn['Right'](5)
        self.assertTrue(right.isRight())
        self.assertFalse(right.isLeft())
        self.assertEqual(right.getOrElse(0), 5)
        
        left = self.fn['Left']('error')
        self.assertTrue(left.isLeft())
        self.assertEqual(left.getOrElse(0), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for RIFT with new modules."""
    
    def test_math_module_in_rift(self):
        """Test math module through RIFT interpreter."""
        # This tests the basic structure - actual RIFT syntax would require
        # proper syntax with @ and # for blocks
        interp = Interpreter()
        math_mod = interp._load_math_module()
        
        result = math_mod['sum']([1, 2, 3, 4, 5])
        self.assertEqual(result, 15)
        
        result = math_mod['mean']([1, 2, 3, 4, 5])
        self.assertEqual(result, 3)
    
    def test_string_module_in_rift(self):
        """Test string module through RIFT interpreter."""
        interp = Interpreter()
        string_mod = interp._load_string_module()
        
        result = string_mod['camelCase']('hello_world')
        self.assertEqual(result, 'helloWorld')
        
        result = string_mod['slugify']('Hello World!')
        self.assertEqual(result, 'hello-world')
    
    def test_array_module_in_rift(self):
        """Test array module through RIFT interpreter."""
        interp = Interpreter()
        array_mod = interp._load_array_module()
        
        result = array_mod['unique']([1, 2, 2, 3, 3, 3])
        self.assertEqual(result, [1, 2, 3])
        
        result = array_mod['chunk']([1, 2, 3, 4, 5, 6], 2)
        self.assertEqual(result, [[1, 2], [3, 4], [5, 6]])


if __name__ == '__main__':
    unittest.main()
