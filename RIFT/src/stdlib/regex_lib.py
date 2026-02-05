"""
RIFT Standard Library - Regex Module

Regular expression utilities for pattern matching.
"""

import re
from typing import Any, Dict, List, Optional, Union


def create_regex_module(interpreter) -> Dict[str, Any]:
    """Create the regex module for RIFT."""
    
    # ========================================================================
    # Pattern Matching
    # ========================================================================
    
    def regex_match(pattern: str, text: str, flags: str = '') -> Optional[Dict[str, Any]]:
        """Match pattern at the beginning of text."""
        re_flags = _parse_flags(flags)
        m = re.match(pattern, text, re_flags)
        return _match_to_dict(m) if m else None
    
    def regex_search(pattern: str, text: str, flags: str = '') -> Optional[Dict[str, Any]]:
        """Search for pattern anywhere in text."""
        re_flags = _parse_flags(flags)
        m = re.search(pattern, text, re_flags)
        return _match_to_dict(m) if m else None
    
    def regex_find_all(pattern: str, text: str, flags: str = '') -> List[str]:
        """Find all matches in text."""
        re_flags = _parse_flags(flags)
        return re.findall(pattern, text, re_flags)
    
    def regex_find_iter(pattern: str, text: str, flags: str = '') -> List[Dict[str, Any]]:
        """Find all matches as match objects."""
        re_flags = _parse_flags(flags)
        return [_match_to_dict(m) for m in re.finditer(pattern, text, re_flags)]
    
    def regex_full_match(pattern: str, text: str, flags: str = '') -> Optional[Dict[str, Any]]:
        """Match pattern against entire text."""
        re_flags = _parse_flags(flags)
        m = re.fullmatch(pattern, text, re_flags)
        return _match_to_dict(m) if m else None
    
    # ========================================================================
    # Testing
    # ========================================================================
    
    def regex_test(pattern: str, text: str, flags: str = '') -> bool:
        """Test if pattern matches anywhere in text."""
        re_flags = _parse_flags(flags)
        return bool(re.search(pattern, text, re_flags))
    
    def regex_is_valid(pattern: str) -> bool:
        """Check if pattern is valid regex."""
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False
    
    # ========================================================================
    # Replacement
    # ========================================================================
    
    def regex_replace(pattern: str, replacement: str, text: str, 
                      count: int = 0, flags: str = '') -> str:
        """Replace matches with replacement string."""
        re_flags = _parse_flags(flags)
        return re.sub(pattern, replacement, text, count=count, flags=re_flags)
    
    def regex_replace_all(pattern: str, replacement: str, text: str, 
                          flags: str = '') -> str:
        """Replace all matches."""
        return regex_replace(pattern, replacement, text, count=0, flags=flags)
    
    def regex_replace_first(pattern: str, replacement: str, text: str, 
                            flags: str = '') -> str:
        """Replace first match only."""
        return regex_replace(pattern, replacement, text, count=1, flags=flags)
    
    def regex_replace_fn(pattern: str, replacer, text: str, 
                         flags: str = '') -> str:
        """Replace matches using a function."""
        re_flags = _parse_flags(flags)
        
        def repl(m):
            match_dict = _match_to_dict(m)
            result = interpreter._call(replacer, [match_dict], None)
            return str(result) if result is not None else ''
        
        return re.sub(pattern, repl, text, flags=re_flags)
    
    # ========================================================================
    # Splitting
    # ========================================================================
    
    def regex_split(pattern: str, text: str, max_split: int = 0, 
                    flags: str = '') -> List[str]:
        """Split text by pattern."""
        re_flags = _parse_flags(flags)
        return re.split(pattern, text, maxsplit=max_split, flags=re_flags)
    
    def regex_split_with_matches(pattern: str, text: str, 
                                 flags: str = '') -> List[str]:
        """Split text but keep matching separators."""
        re_flags = _parse_flags(flags)
        return re.split(f'({pattern})', text, flags=re_flags)
    
    # ========================================================================
    # Extraction
    # ========================================================================
    
    def regex_groups(pattern: str, text: str, flags: str = '') -> Optional[List[str]]:
        """Extract captured groups from first match."""
        re_flags = _parse_flags(flags)
        m = re.search(pattern, text, re_flags)
        return list(m.groups()) if m else None
    
    def regex_named_groups(pattern: str, text: str, 
                           flags: str = '') -> Optional[Dict[str, str]]:
        """Extract named groups from first match."""
        re_flags = _parse_flags(flags)
        m = re.search(pattern, text, re_flags)
        return dict(m.groupdict()) if m else None
    
    def regex_capture_all(pattern: str, text: str, 
                          flags: str = '') -> List[List[str]]:
        """Extract all captured groups from all matches."""
        re_flags = _parse_flags(flags)
        return [list(m.groups()) for m in re.finditer(pattern, text, re_flags)]
    
    # ========================================================================
    # Pattern Information
    # ========================================================================
    
    def regex_count(pattern: str, text: str, flags: str = '') -> int:
        """Count number of matches."""
        re_flags = _parse_flags(flags)
        return len(re.findall(pattern, text, re_flags))
    
    def regex_spans(pattern: str, text: str, 
                    flags: str = '') -> List[Dict[str, int]]:
        """Get start/end positions of all matches."""
        re_flags = _parse_flags(flags)
        return [{'start': m.start(), 'end': m.end()} 
                for m in re.finditer(pattern, text, re_flags)]
    
    # ========================================================================
    # Utility
    # ========================================================================
    
    def regex_escape(text: str) -> str:
        """Escape special regex characters."""
        return re.escape(text)
    
    def regex_compile(pattern: str, flags: str = '') -> Dict[str, Any]:
        """Compile pattern for reuse."""
        re_flags = _parse_flags(flags)
        compiled = re.compile(pattern, re_flags)
        return {
            'pattern': pattern,
            'flags': flags,
            '_compiled': compiled,
        }
    
    # ========================================================================
    # Common Patterns
    # ========================================================================
    
    PATTERNS = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'url': r'https?://[^\s<>"{}|\\^`\[\]]+',
        'ipv4': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
        'ipv6': r'(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}',
        'phone_us': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'phone_intl': r'\+?[1-9]\d{1,14}',
        'zipcode_us': r'\b\d{5}(?:-\d{4})?\b',
        'date_iso': r'\d{4}-\d{2}-\d{2}',
        'time_24h': r'(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?',
        'datetime_iso': r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?',
        'hex_color': r'#(?:[0-9a-fA-F]{3}){1,2}\b',
        'rgb_color': r'rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)',
        'uuid': r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
        'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'hashtag': r'#\w+',
        'mention': r'@\w+',
        'word': r'\b\w+\b',
        'number': r'-?\d+(?:\.\d+)?',
        'integer': r'-?\d+',
        'float': r'-?\d+\.\d+',
        'alpha': r'[a-zA-Z]+',
        'alphanumeric': r'[a-zA-Z0-9]+',
        'whitespace': r'\s+',
        'newline': r'\r?\n',
        'slug': r'^[a-z0-9]+(?:-[a-z0-9]+)*$',
        'username': r'^[a-zA-Z0-9_]{3,20}$',
        'password_strong': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        'html_tag': r'<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>.*?</\1>',
        'html_comment': r'<!--.*?-->',
        'json_string': r'"(?:[^"\\]|\\.)*"',
        'mac_address': r'([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}',
        'domain': r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}',
    }
    
    def regex_pattern(name: str) -> Optional[str]:
        """Get common pattern by name."""
        return PATTERNS.get(name)
    
    def regex_list_patterns() -> List[str]:
        """List all available common patterns."""
        return list(PATTERNS.keys())
    
    def regex_validate_email(text: str) -> bool:
        """Validate email address."""
        return bool(re.fullmatch(PATTERNS['email'], text))
    
    def regex_validate_url(text: str) -> bool:
        """Validate URL."""
        return bool(re.match(PATTERNS['url'], text))
    
    def regex_validate_ipv4(text: str) -> bool:
        """Validate IPv4 address."""
        return bool(re.fullmatch(PATTERNS['ipv4'], text))
    
    def regex_validate_uuid(text: str) -> bool:
        """Validate UUID."""
        return bool(re.fullmatch(PATTERNS['uuid'], text, re.IGNORECASE))
    
    # ========================================================================
    # Helpers
    # ========================================================================
    
    def _parse_flags(flags_str: str) -> int:
        """Parse flags string to re flags."""
        flag_map = {
            'i': re.IGNORECASE,
            'm': re.MULTILINE,
            's': re.DOTALL,
            'x': re.VERBOSE,
            'a': re.ASCII,
        }
        
        result = 0
        for char in flags_str:
            if char in flag_map:
                result |= flag_map[char]
        return result
    
    def _match_to_dict(m) -> Dict[str, Any]:
        """Convert match object to dictionary."""
        return {
            'match': m.group(0),
            'start': m.start(),
            'end': m.end(),
            'groups': list(m.groups()),
            'namedGroups': dict(m.groupdict()),
            'span': [m.start(), m.end()],
        }
    
    return {
        # Matching
        'match': regex_match,
        'search': regex_search,
        'findAll': regex_find_all,
        'findIter': regex_find_iter,
        'fullMatch': regex_full_match,
        
        # Testing
        'test': regex_test,
        'isValid': regex_is_valid,
        
        # Replacement
        'replace': regex_replace,
        'replaceAll': regex_replace_all,
        'replaceFirst': regex_replace_first,
        'replaceFn': regex_replace_fn,
        
        # Splitting
        'split': regex_split,
        'splitWithMatches': regex_split_with_matches,
        
        # Extraction
        'groups': regex_groups,
        'namedGroups': regex_named_groups,
        'captureAll': regex_capture_all,
        
        # Pattern Info
        'count': regex_count,
        'spans': regex_spans,
        
        # Utility
        'escape': regex_escape,
        'compile': regex_compile,
        
        # Common Patterns
        'pattern': regex_pattern,
        'listPatterns': regex_list_patterns,
        'validateEmail': regex_validate_email,
        'validateUrl': regex_validate_url,
        'validateIpv4': regex_validate_ipv4,
        'validateUuid': regex_validate_uuid,
        
        # Pattern Constants
        'PATTERNS': PATTERNS,
    }
