"""
RIFT Standard Library - String Module

Comprehensive string manipulation utilities.
"""

import re
import unicodedata
from typing import Any, Dict, List, Optional, Union


def create_string_module(interpreter) -> Dict[str, Any]:
    """Create the string module for RIFT."""
    
    # ========================================================================
    # Case Conversion
    # ========================================================================
    
    def str_upper(s: str) -> str:
        """Convert string to uppercase."""
        return s.upper()
    
    def str_lower(s: str) -> str:
        """Convert string to lowercase."""
        return s.lower()
    
    def str_capitalize(s: str) -> str:
        """Capitalize first letter."""
        return s.capitalize()
    
    def str_title(s: str) -> str:
        """Convert to title case."""
        return s.title()
    
    def str_swapcase(s: str) -> str:
        """Swap case of all characters."""
        return s.swapcase()
    
    def str_camel_case(s: str) -> str:
        """Convert to camelCase."""
        words = re.split(r'[\s_\-]+', s)
        return words[0].lower() + ''.join(w.capitalize() for w in words[1:])
    
    def str_pascal_case(s: str) -> str:
        """Convert to PascalCase."""
        words = re.split(r'[\s_\-]+', s)
        return ''.join(w.capitalize() for w in words)
    
    def str_snake_case(s: str) -> str:
        """Convert to snake_case."""
        # Insert underscore before capitals
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        # Replace spaces and hyphens
        s3 = re.sub(r'[\s\-]+', '_', s2)
        return s3.lower()
    
    def str_kebab_case(s: str) -> str:
        """Convert to kebab-case."""
        return str_snake_case(s).replace('_', '-')
    
    def str_constant_case(s: str) -> str:
        """Convert to CONSTANT_CASE."""
        return str_snake_case(s).upper()
    
    # ========================================================================
    # Trimming and Padding
    # ========================================================================
    
    def str_trim(s: str) -> str:
        """Remove whitespace from both ends."""
        return s.strip()
    
    def str_trim_start(s: str) -> str:
        """Remove whitespace from start."""
        return s.lstrip()
    
    def str_trim_end(s: str) -> str:
        """Remove whitespace from end."""
        return s.rstrip()
    
    def str_pad_start(s: str, length: int, char: str = ' ') -> str:
        """Pad string at start to specified length."""
        return s.rjust(length, char[:1])
    
    def str_pad_end(s: str, length: int, char: str = ' ') -> str:
        """Pad string at end to specified length."""
        return s.ljust(length, char[:1])
    
    def str_pad_center(s: str, length: int, char: str = ' ') -> str:
        """Center string with padding."""
        return s.center(length, char[:1])
    
    def str_truncate(s: str, max_length: int, suffix: str = '...') -> str:
        """Truncate string to max length with suffix."""
        if len(s) <= max_length:
            return s
        return s[:max_length - len(suffix)] + suffix
    
    # ========================================================================
    # Search and Replace
    # ========================================================================
    
    def str_contains(s: str, substring: str) -> bool:
        """Check if string contains substring."""
        return substring in s
    
    def str_starts_with(s: str, prefix: str) -> bool:
        """Check if string starts with prefix."""
        return s.startswith(prefix)
    
    def str_ends_with(s: str, suffix: str) -> bool:
        """Check if string ends with suffix."""
        return s.endswith(suffix)
    
    def str_index_of(s: str, substring: str, start: int = 0) -> int:
        """Find first index of substring, or -1 if not found."""
        return s.find(substring, start)
    
    def str_last_index_of(s: str, substring: str) -> int:
        """Find last index of substring, or -1 if not found."""
        return s.rfind(substring)
    
    def str_count(s: str, substring: str) -> int:
        """Count occurrences of substring."""
        return s.count(substring)
    
    def str_replace(s: str, old: str, new: str, count: int = -1) -> str:
        """Replace occurrences of old with new."""
        if count == -1:
            return s.replace(old, new)
        return s.replace(old, new, count)
    
    def str_replace_all(s: str, replacements: Dict[str, str]) -> str:
        """Replace multiple patterns at once."""
        for old, new in replacements.items():
            s = s.replace(old, new)
        return s
    
    def str_remove(s: str, substring: str) -> str:
        """Remove all occurrences of substring."""
        return s.replace(substring, '')
    
    # ========================================================================
    # Splitting and Joining
    # ========================================================================
    
    def str_split(s: str, separator: str = None, max_split: int = -1) -> List[str]:
        """Split string by separator."""
        return s.split(separator, max_split) if max_split >= 0 else s.split(separator)
    
    def str_split_lines(s: str) -> List[str]:
        """Split string into lines."""
        return s.splitlines()
    
    def str_split_words(s: str) -> List[str]:
        """Split string into words."""
        return s.split()
    
    def str_join(items: List[str], separator: str = '') -> str:
        """Join list of strings with separator."""
        return separator.join(str(item) for item in items)
    
    def str_chunk(s: str, size: int) -> List[str]:
        """Split string into chunks of specified size."""
        return [s[i:i+size] for i in range(0, len(s), size)]
    
    # ========================================================================
    # Character Access
    # ========================================================================
    
    def str_char_at(s: str, index: int) -> str:
        """Get character at index."""
        if 0 <= index < len(s):
            return s[index]
        return ''
    
    def str_char_code_at(s: str, index: int) -> int:
        """Get character code at index."""
        if 0 <= index < len(s):
            return ord(s[index])
        return -1
    
    def str_from_char_code(*codes: int) -> str:
        """Create string from character codes."""
        return ''.join(chr(code) for code in codes)
    
    def str_chars(s: str) -> List[str]:
        """Split string into individual characters."""
        return list(s)
    
    def str_codes(s: str) -> List[int]:
        """Get character codes of all characters."""
        return [ord(c) for c in s]
    
    # ========================================================================
    # Substring Operations
    # ========================================================================
    
    def str_substring(s: str, start: int, end: int = None) -> str:
        """Get substring from start to end."""
        if end is None:
            return s[start:]
        return s[start:end]
    
    def str_slice(s: str, start: int, end: int = None) -> str:
        """Slice string (supports negative indices)."""
        if end is None:
            return s[start:]
        return s[start:end]
    
    def str_left(s: str, count: int) -> str:
        """Get leftmost characters."""
        return s[:count]
    
    def str_right(s: str, count: int) -> str:
        """Get rightmost characters."""
        return s[-count:] if count > 0 else ''
    
    def str_mid(s: str, start: int, length: int) -> str:
        """Get substring starting at index with specified length."""
        return s[start:start + length]
    
    # ========================================================================
    # Formatting
    # ========================================================================
    
    def str_format(template: str, *args, **kwargs) -> str:
        """Format string with placeholders."""
        try:
            return template.format(*args, **kwargs)
        except (IndexError, KeyError):
            return template
    
    def str_repeat(s: str, count: int) -> str:
        """Repeat string n times."""
        return s * count
    
    def str_reverse(s: str) -> str:
        """Reverse string."""
        return s[::-1]
    
    def str_wrap(text: str, width: int) -> str:
        """Word wrap text to specified width."""
        import textwrap
        return textwrap.fill(text, width)
    
    def str_dedent(text: str) -> str:
        """Remove leading whitespace from each line."""
        import textwrap
        return textwrap.dedent(text)
    
    def str_indent(text: str, prefix: str = '  ') -> str:
        """Add prefix to each line."""
        return '\n'.join(prefix + line for line in text.splitlines())
    
    # ========================================================================
    # Validation
    # ========================================================================
    
    def str_is_empty(s: str) -> bool:
        """Check if string is empty."""
        return len(s) == 0
    
    def str_is_blank(s: str) -> bool:
        """Check if string is empty or whitespace only."""
        return len(s.strip()) == 0
    
    def str_is_alpha(s: str) -> bool:
        """Check if string contains only letters."""
        return s.isalpha() if s else False
    
    def str_is_numeric(s: str) -> bool:
        """Check if string contains only digits."""
        return s.isdigit() if s else False
    
    def str_is_alphanumeric(s: str) -> bool:
        """Check if string contains only letters and digits."""
        return s.isalnum() if s else False
    
    def str_is_upper(s: str) -> bool:
        """Check if string is uppercase."""
        return s.isupper()
    
    def str_is_lower(s: str) -> bool:
        """Check if string is lowercase."""
        return s.islower()
    
    def str_is_whitespace(s: str) -> bool:
        """Check if string contains only whitespace."""
        return s.isspace() if s else False
    
    def str_is_ascii(s: str) -> bool:
        """Check if string contains only ASCII characters."""
        return s.isascii()
    
    def str_is_printable(s: str) -> bool:
        """Check if string contains only printable characters."""
        return s.isprintable()
    
    def str_is_identifier(s: str) -> bool:
        """Check if string is a valid identifier."""
        return s.isidentifier() if s else False
    
    def str_matches(s: str, pattern: str) -> bool:
        """Check if string matches regex pattern."""
        return bool(re.match(pattern, s))
    
    # ========================================================================
    # Unicode and Encoding
    # ========================================================================
    
    def str_normalize(s: str, form: str = 'NFC') -> str:
        """Normalize unicode string."""
        return unicodedata.normalize(form.upper(), s)
    
    def str_encode(s: str, encoding: str = 'utf-8') -> bytes:
        """Encode string to bytes."""
        return s.encode(encoding)
    
    def str_decode(data: bytes, encoding: str = 'utf-8') -> str:
        """Decode bytes to string."""
        if isinstance(data, str):
            return data
        return data.decode(encoding)
    
    def str_escape_html(s: str) -> str:
        """Escape HTML special characters."""
        import html
        return html.escape(s)
    
    def str_unescape_html(s: str) -> str:
        """Unescape HTML entities."""
        import html
        return html.unescape(s)
    
    def str_escape_regex(s: str) -> str:
        """Escape regex special characters."""
        return re.escape(s)
    
    def str_strip_accents(s: str) -> str:
        """Remove accents from characters."""
        return ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
        )
    
    # ========================================================================
    # Comparison
    # ========================================================================
    
    def str_equals(s1: str, s2: str) -> bool:
        """Check if two strings are equal."""
        return s1 == s2
    
    def str_equals_ignore_case(s1: str, s2: str) -> bool:
        """Check if two strings are equal (case-insensitive)."""
        return s1.lower() == s2.lower()
    
    def str_compare(s1: str, s2: str) -> int:
        """Compare two strings (-1, 0, 1)."""
        if s1 < s2:
            return -1
        elif s1 > s2:
            return 1
        return 0
    
    def str_natural_compare(s1: str, s2: str) -> int:
        """Natural string comparison (for sorting)."""
        def convert(text):
            return int(text) if text.isdigit() else text.lower()
        
        def alphanum_key(s):
            return [convert(c) for c in re.split('([0-9]+)', s)]
        
        k1, k2 = alphanum_key(s1), alphanum_key(s2)
        if k1 < k2:
            return -1
        elif k1 > k2:
            return 1
        return 0
    
    def str_levenshtein(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def str_similarity(s1: str, s2: str) -> float:
        """Calculate similarity ratio (0-1) between two strings."""
        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0
        distance = str_levenshtein(s1, s2)
        max_len = max(len(s1), len(s2))
        return 1 - (distance / max_len)
    
    # ========================================================================
    # Extraction
    # ========================================================================
    
    def str_extract_numbers(s: str) -> List[float]:
        """Extract all numbers from string."""
        numbers = re.findall(r'-?\d+\.?\d*', s)
        return [float(n) for n in numbers]
    
    def str_extract_words(s: str) -> List[str]:
        """Extract all words from string."""
        return re.findall(r'\b\w+\b', s)
    
    def str_extract_emails(s: str) -> List[str]:
        """Extract email addresses from string."""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(pattern, s)
    
    def str_extract_urls(s: str) -> List[str]:
        """Extract URLs from string."""
        pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(pattern, s)
    
    def str_extract_hashtags(s: str) -> List[str]:
        """Extract hashtags from string."""
        return re.findall(r'#\w+', s)
    
    def str_extract_mentions(s: str) -> List[str]:
        """Extract @mentions from string."""
        return re.findall(r'@\w+', s)
    
    # ========================================================================
    # Generation
    # ========================================================================
    
    def str_random(length: int, charset: str = 'alphanumeric') -> str:
        """Generate random string."""
        import random
        chars = {
            'alpha': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'numeric': '0123456789',
            'alphanumeric': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
            'hex': '0123456789abcdef',
            'special': '!@#$%^&*()_+-=[]{}|;:,.<>?',
        }
        pool = chars.get(charset, charset)
        return ''.join(random.choice(pool) for _ in range(length))
    
    def str_uuid() -> str:
        """Generate UUID string."""
        import uuid
        return str(uuid.uuid4())
    
    # ========================================================================
    # Template and Slugify
    # ========================================================================
    
    def str_slugify(s: str) -> str:
        """Convert string to URL-friendly slug."""
        s = s.lower()
        s = str_strip_accents(s)
        s = re.sub(r'[^\w\s-]', '', s)
        s = re.sub(r'[\s_-]+', '-', s)
        s = s.strip('-')
        return s
    
    def str_humanize(s: str) -> str:
        """Convert identifier to human-readable form."""
        s = str_snake_case(s)
        s = s.replace('_', ' ')
        return s.capitalize()
    
    def str_pluralize(s: str, count: int = 2) -> str:
        """Simple English pluralization."""
        if count == 1:
            return s
        
        # Common irregular plurals
        irregulars = {
            'child': 'children', 'person': 'people', 'man': 'men',
            'woman': 'women', 'foot': 'feet', 'tooth': 'teeth',
            'goose': 'geese', 'mouse': 'mice', 'ox': 'oxen',
        }
        
        lower_s = s.lower()
        if lower_s in irregulars:
            return irregulars[lower_s]
        
        # Basic rules
        if s.endswith(('s', 'sh', 'ch', 'x', 'z')):
            return s + 'es'
        if s.endswith('y') and len(s) > 1 and s[-2] not in 'aeiou':
            return s[:-1] + 'ies'
        if s.endswith('f'):
            return s[:-1] + 'ves'
        if s.endswith('fe'):
            return s[:-2] + 'ves'
        
        return s + 's'
    
    def str_singularize(s: str) -> str:
        """Simple English singularization."""
        if not s:
            return s
        
        # Common irregular plurals
        irregulars = {
            'children': 'child', 'people': 'person', 'men': 'man',
            'women': 'woman', 'feet': 'foot', 'teeth': 'tooth',
            'geese': 'goose', 'mice': 'mouse', 'oxen': 'ox',
        }
        
        lower_s = s.lower()
        if lower_s in irregulars:
            return irregulars[lower_s]
        
        # Basic rules
        if s.endswith('ies') and len(s) > 4:
            return s[:-3] + 'y'
        if s.endswith('ves'):
            return s[:-3] + 'f'
        if s.endswith('es') and len(s) > 3:
            if s[:-2].endswith(('s', 'sh', 'ch', 'x', 'z')):
                return s[:-2]
        if s.endswith('s') and not s.endswith('ss'):
            return s[:-1]
        
        return s
    
    return {
        # Case Conversion
        'upper': str_upper,
        'lower': str_lower,
        'capitalize': str_capitalize,
        'title': str_title,
        'swapcase': str_swapcase,
        'camelCase': str_camel_case,
        'pascalCase': str_pascal_case,
        'snakeCase': str_snake_case,
        'kebabCase': str_kebab_case,
        'constantCase': str_constant_case,
        
        # Trimming and Padding
        'trim': str_trim,
        'trimStart': str_trim_start,
        'trimEnd': str_trim_end,
        'padStart': str_pad_start,
        'padEnd': str_pad_end,
        'padCenter': str_pad_center,
        'truncate': str_truncate,
        
        # Search and Replace
        'contains': str_contains,
        'startsWith': str_starts_with,
        'endsWith': str_ends_with,
        'indexOf': str_index_of,
        'lastIndexOf': str_last_index_of,
        'count': str_count,
        'replace': str_replace,
        'replaceAll': str_replace_all,
        'remove': str_remove,
        
        # Splitting and Joining
        'split': str_split,
        'splitLines': str_split_lines,
        'splitWords': str_split_words,
        'join': str_join,
        'chunk': str_chunk,
        
        # Character Access
        'charAt': str_char_at,
        'charCodeAt': str_char_code_at,
        'fromCharCode': str_from_char_code,
        'chars': str_chars,
        'codes': str_codes,
        
        # Substring Operations
        'substring': str_substring,
        'slice': str_slice,
        'left': str_left,
        'right': str_right,
        'mid': str_mid,
        
        # Formatting
        'format': str_format,
        'repeat': str_repeat,
        'reverse': str_reverse,
        'wrap': str_wrap,
        'dedent': str_dedent,
        'indent': str_indent,
        
        # Validation
        'isEmpty': str_is_empty,
        'isBlank': str_is_blank,
        'isAlpha': str_is_alpha,
        'isNumeric': str_is_numeric,
        'isAlphanumeric': str_is_alphanumeric,
        'isUpper': str_is_upper,
        'isLower': str_is_lower,
        'isWhitespace': str_is_whitespace,
        'isAscii': str_is_ascii,
        'isPrintable': str_is_printable,
        'isIdentifier': str_is_identifier,
        'matches': str_matches,
        
        # Unicode and Encoding
        'normalize': str_normalize,
        'encode': str_encode,
        'decode': str_decode,
        'escapeHtml': str_escape_html,
        'unescapeHtml': str_unescape_html,
        'escapeRegex': str_escape_regex,
        'stripAccents': str_strip_accents,
        
        # Comparison
        'equals': str_equals,
        'equalsIgnoreCase': str_equals_ignore_case,
        'compare': str_compare,
        'naturalCompare': str_natural_compare,
        'levenshtein': str_levenshtein,
        'similarity': str_similarity,
        
        # Extraction
        'extractNumbers': str_extract_numbers,
        'extractWords': str_extract_words,
        'extractEmails': str_extract_emails,
        'extractUrls': str_extract_urls,
        'extractHashtags': str_extract_hashtags,
        'extractMentions': str_extract_mentions,
        
        # Generation
        'random': str_random,
        'uuid': str_uuid,
        
        # Template and Slugify
        'slugify': str_slugify,
        'humanize': str_humanize,
        'pluralize': str_pluralize,
        'singularize': str_singularize,
    }
