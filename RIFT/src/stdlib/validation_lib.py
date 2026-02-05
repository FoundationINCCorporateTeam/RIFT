"""
RIFT Standard Library - Validation Module

Input validation and sanitization utilities.
"""

import re
import html
from typing import Any, Dict, List, Optional, Union, Callable


def create_validation_module(interpreter) -> Dict[str, Any]:
    """Create the validation module for RIFT."""
    
    # ========================================================================
    # Type Validators
    # ========================================================================
    
    def val_is_string(value: Any) -> bool:
        """Check if value is a string."""
        return isinstance(value, str)
    
    def val_is_number(value: Any) -> bool:
        """Check if value is a number."""
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    
    def val_is_integer(value: Any) -> bool:
        """Check if value is an integer."""
        if isinstance(value, bool):
            return False
        if isinstance(value, int):
            return True
        if isinstance(value, float):
            return value.is_integer()
        return False
    
    def val_is_float(value: Any) -> bool:
        """Check if value is a float."""
        return isinstance(value, float) and not isinstance(value, bool)
    
    def val_is_boolean(value: Any) -> bool:
        """Check if value is a boolean."""
        return isinstance(value, bool)
    
    def val_is_array(value: Any) -> bool:
        """Check if value is an array/list."""
        return isinstance(value, list)
    
    def val_is_object(value: Any) -> bool:
        """Check if value is an object/dict."""
        return isinstance(value, dict)
    
    def val_is_null(value: Any) -> bool:
        """Check if value is null/None."""
        return value is None
    
    def val_is_defined(value: Any) -> bool:
        """Check if value is not null/None."""
        return value is not None
    
    def val_is_empty(value: Any) -> bool:
        """Check if value is empty (empty string, list, dict, or None)."""
        if value is None:
            return True
        if isinstance(value, (str, list, dict)):
            return len(value) == 0
        return False
    
    def val_is_callable(value: Any) -> bool:
        """Check if value is callable."""
        return callable(value)
    
    # ========================================================================
    # String Validators
    # ========================================================================
    
    def val_is_email(value: str) -> bool:
        """Validate email address."""
        if not isinstance(value, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, value))
    
    def val_is_url(value: str) -> bool:
        """Validate URL."""
        if not isinstance(value, str):
            return False
        pattern = r'^https?://[^\s<>"{}|\\^`\[\]]+$'
        return bool(re.match(pattern, value))
    
    def val_is_uuid(value: str) -> bool:
        """Validate UUID."""
        if not isinstance(value, str):
            return False
        pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return bool(re.match(pattern, value))
    
    def val_is_ip(value: str) -> bool:
        """Validate IPv4 or IPv6 address."""
        return val_is_ipv4(value) or val_is_ipv6(value)
    
    def val_is_ipv4(value: str) -> bool:
        """Validate IPv4 address."""
        if not isinstance(value, str):
            return False
        pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(pattern, value))
    
    def val_is_ipv6(value: str) -> bool:
        """Validate IPv6 address."""
        if not isinstance(value, str):
            return False
        pattern = r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
        return bool(re.match(pattern, value))
    
    def val_is_domain(value: str) -> bool:
        """Validate domain name."""
        if not isinstance(value, str):
            return False
        pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return bool(re.match(pattern, value))
    
    def val_is_hex_color(value: str) -> bool:
        """Validate hex color code."""
        if not isinstance(value, str):
            return False
        pattern = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
        return bool(re.match(pattern, value))
    
    def val_is_credit_card(value: str) -> bool:
        """Validate credit card number (basic Luhn check)."""
        if not isinstance(value, str):
            return False
        
        # Remove spaces and dashes
        digits = value.replace(' ', '').replace('-', '')
        
        if not digits.isdigit() or len(digits) < 13 or len(digits) > 19:
            return False
        
        # Luhn algorithm
        total = 0
        for i, digit in enumerate(reversed(digits)):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        
        return total % 10 == 0
    
    def val_is_phone(value: str) -> bool:
        """Validate phone number (international format)."""
        if not isinstance(value, str):
            return False
        # Remove common separators
        cleaned = re.sub(r'[\s\-\.\(\)]+', '', value)
        pattern = r'^\+?[1-9]\d{6,14}$'
        return bool(re.match(pattern, cleaned))
    
    def val_is_slug(value: str) -> bool:
        """Validate URL slug."""
        if not isinstance(value, str):
            return False
        pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
        return bool(re.match(pattern, value))
    
    def val_is_alpha(value: str) -> bool:
        """Check if string contains only letters."""
        if not isinstance(value, str):
            return False
        return value.isalpha() if value else False
    
    def val_is_alphanumeric(value: str) -> bool:
        """Check if string contains only letters and numbers."""
        if not isinstance(value, str):
            return False
        return value.isalnum() if value else False
    
    def val_is_numeric_string(value: str) -> bool:
        """Check if string contains only digits."""
        if not isinstance(value, str):
            return False
        return value.isdigit() if value else False
    
    def val_is_ascii(value: str) -> bool:
        """Check if string contains only ASCII characters."""
        if not isinstance(value, str):
            return False
        return value.isascii()
    
    def val_is_base64(value: str) -> bool:
        """Check if string is valid base64."""
        if not isinstance(value, str):
            return False
        pattern = r'^[A-Za-z0-9+/]*={0,2}$'
        return bool(re.match(pattern, value)) and len(value) % 4 == 0
    
    def val_is_json(value: str) -> bool:
        """Check if string is valid JSON."""
        if not isinstance(value, str):
            return False
        try:
            import json
            json.loads(value)
            return True
        except (json.JSONDecodeError, ValueError):
            return False
    
    def val_is_date_string(value: str) -> bool:
        """Check if string is a valid ISO date."""
        if not isinstance(value, str):
            return False
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, value):
            return False
        try:
            from datetime import datetime
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def val_is_datetime_string(value: str) -> bool:
        """Check if string is a valid ISO datetime."""
        if not isinstance(value, str):
            return False
        try:
            from datetime import datetime
            datetime.fromisoformat(value.replace('Z', '+00:00'))
            return True
        except ValueError:
            return False
    
    # ========================================================================
    # Number Validators
    # ========================================================================
    
    def val_is_positive(value: Union[int, float]) -> bool:
        """Check if number is positive."""
        return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0
    
    def val_is_negative(value: Union[int, float]) -> bool:
        """Check if number is negative."""
        return isinstance(value, (int, float)) and not isinstance(value, bool) and value < 0
    
    def val_is_zero(value: Union[int, float]) -> bool:
        """Check if number is zero."""
        return isinstance(value, (int, float)) and not isinstance(value, bool) and value == 0
    
    def val_is_between(value: Union[int, float], min_val: Union[int, float], 
                       max_val: Union[int, float], inclusive: bool = True) -> bool:
        """Check if number is between min and max."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return False
        if inclusive:
            return min_val <= value <= max_val
        return min_val < value < max_val
    
    def val_is_even(value: int) -> bool:
        """Check if integer is even."""
        return isinstance(value, int) and not isinstance(value, bool) and value % 2 == 0
    
    def val_is_odd(value: int) -> bool:
        """Check if integer is odd."""
        return isinstance(value, int) and not isinstance(value, bool) and value % 2 != 0
    
    def val_is_finite(value: Union[int, float]) -> bool:
        """Check if number is finite."""
        import math
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return False
        return math.isfinite(value)
    
    def val_is_port(value: int) -> bool:
        """Check if value is a valid port number."""
        return isinstance(value, int) and not isinstance(value, bool) and 0 < value <= 65535
    
    # ========================================================================
    # String Length/Content Validators
    # ========================================================================
    
    def val_min_length(value: str, length: int) -> bool:
        """Check if string has minimum length."""
        return isinstance(value, str) and len(value) >= length
    
    def val_max_length(value: str, length: int) -> bool:
        """Check if string has maximum length."""
        return isinstance(value, str) and len(value) <= length
    
    def val_length_between(value: str, min_len: int, max_len: int) -> bool:
        """Check if string length is between min and max."""
        return isinstance(value, str) and min_len <= len(value) <= max_len
    
    def val_length_exact(value: str, length: int) -> bool:
        """Check if string has exact length."""
        return isinstance(value, str) and len(value) == length
    
    def val_matches(value: str, pattern: str) -> bool:
        """Check if string matches regex pattern."""
        if not isinstance(value, str):
            return False
        try:
            return bool(re.match(pattern, value))
        except re.error:
            return False
    
    def val_contains(value: str, substring: str) -> bool:
        """Check if string contains substring."""
        return isinstance(value, str) and substring in value
    
    def val_starts_with(value: str, prefix: str) -> bool:
        """Check if string starts with prefix."""
        return isinstance(value, str) and value.startswith(prefix)
    
    def val_ends_with(value: str, suffix: str) -> bool:
        """Check if string ends with suffix."""
        return isinstance(value, str) and value.endswith(suffix)
    
    def val_equals(value: str, expected: str, case_sensitive: bool = True) -> bool:
        """Check if string equals expected value."""
        if not isinstance(value, str):
            return False
        if case_sensitive:
            return value == expected
        return value.lower() == expected.lower()
    
    def val_in_list(value: Any, allowed: List[Any]) -> bool:
        """Check if value is in list of allowed values."""
        return value in allowed
    
    def val_not_in_list(value: Any, forbidden: List[Any]) -> bool:
        """Check if value is not in list of forbidden values."""
        return value not in forbidden
    
    # ========================================================================
    # Array Validators
    # ========================================================================
    
    def val_array_min_length(arr: List[Any], length: int) -> bool:
        """Check if array has minimum length."""
        return isinstance(arr, list) and len(arr) >= length
    
    def val_array_max_length(arr: List[Any], length: int) -> bool:
        """Check if array has maximum length."""
        return isinstance(arr, list) and len(arr) <= length
    
    def val_array_length_between(arr: List[Any], min_len: int, max_len: int) -> bool:
        """Check if array length is between min and max."""
        return isinstance(arr, list) and min_len <= len(arr) <= max_len
    
    def val_array_unique(arr: List[Any]) -> bool:
        """Check if all array items are unique."""
        if not isinstance(arr, list):
            return False
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
    
    def val_array_all(arr: List[Any], validator: Callable) -> bool:
        """Check if all array items pass validator."""
        if not isinstance(arr, list):
            return False
        return all(interpreter._call(validator, [item], None) for item in arr)
    
    def val_array_any(arr: List[Any], validator: Callable) -> bool:
        """Check if any array item passes validator."""
        if not isinstance(arr, list):
            return False
        return any(interpreter._call(validator, [item], None) for item in arr)
    
    # ========================================================================
    # Object Validators
    # ========================================================================
    
    def val_has_keys(obj: Dict[str, Any], keys: List[str]) -> bool:
        """Check if object has all required keys."""
        if not isinstance(obj, dict):
            return False
        return all(key in obj for key in keys)
    
    def val_has_only_keys(obj: Dict[str, Any], allowed_keys: List[str]) -> bool:
        """Check if object has only allowed keys."""
        if not isinstance(obj, dict):
            return False
        return all(key in allowed_keys for key in obj.keys())
    
    def val_schema(obj: Dict[str, Any], schema: Dict[str, Callable]) -> Dict[str, Any]:
        """Validate object against schema."""
        if not isinstance(obj, dict):
            return {'valid': False, 'errors': ['Value is not an object']}
        
        errors = []
        for key, validator in schema.items():
            if key not in obj:
                errors.append(f"Missing required key: {key}")
            elif not interpreter._call(validator, [obj[key]], None):
                errors.append(f"Invalid value for key: {key}")
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    # ========================================================================
    # Password Validators
    # ========================================================================
    
    def val_password_strength(password: str) -> Dict[str, Any]:
        """Check password strength."""
        if not isinstance(password, str):
            return {'valid': False, 'score': 0, 'errors': ['Password must be a string']}
        
        errors = []
        score = 0
        
        if len(password) >= 8:
            score += 1
        else:
            errors.append('Password must be at least 8 characters')
        
        if len(password) >= 12:
            score += 1
        
        if re.search(r'[a-z]', password):
            score += 1
        else:
            errors.append('Password must contain a lowercase letter')
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            errors.append('Password must contain an uppercase letter')
        
        if re.search(r'\d', password):
            score += 1
        else:
            errors.append('Password must contain a digit')
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            errors.append('Password must contain a special character')
        
        if len(password) >= 16:
            score += 1
        
        strength = 'weak'
        if score >= 5:
            strength = 'strong'
        elif score >= 3:
            strength = 'medium'
        
        return {
            'valid': len(errors) == 0,
            'score': score,
            'strength': strength,
            'errors': errors,
        }
    
    # ========================================================================
    # Sanitization
    # ========================================================================
    
    def val_sanitize_string(value: Any, options: Dict[str, Any] = None) -> str:
        """Sanitize and convert value to string."""
        options = options or {}
        result = str(value) if value is not None else ''
        
        if options.get('trim', True):
            result = result.strip()
        
        if options.get('lowercase', False):
            result = result.lower()
        
        if options.get('uppercase', False):
            result = result.upper()
        
        if options.get('escape_html', False):
            result = html.escape(result)
        
        max_length = options.get('max_length')
        if max_length and len(result) > max_length:
            result = result[:max_length]
        
        return result
    
    def val_sanitize_number(value: Any, options: Dict[str, Any] = None) -> Optional[float]:
        """Sanitize and convert value to number."""
        options = options or {}
        
        if isinstance(value, bool):
            return None
        
        if isinstance(value, (int, float)):
            result = float(value)
        elif isinstance(value, str):
            try:
                result = float(value.strip())
            except ValueError:
                return options.get('default')
        else:
            return options.get('default')
        
        min_val = options.get('min')
        max_val = options.get('max')
        
        if min_val is not None and result < min_val:
            result = min_val
        if max_val is not None and result > max_val:
            result = max_val
        
        if options.get('integer', False):
            result = int(result)
        
        return result
    
    def val_sanitize_email(value: str) -> Optional[str]:
        """Sanitize email address."""
        if not isinstance(value, str):
            return None
        
        result = value.strip().lower()
        
        if not val_is_email(result):
            return None
        
        return result
    
    def val_sanitize_url(value: str) -> Optional[str]:
        """Sanitize URL."""
        if not isinstance(value, str):
            return None
        
        result = value.strip()
        
        # Add protocol if missing
        if result and not result.startswith(('http://', 'https://')):
            result = 'https://' + result
        
        if not val_is_url(result):
            return None
        
        return result
    
    def val_escape_html(value: str) -> str:
        """Escape HTML special characters."""
        return html.escape(str(value))
    
    def val_strip_html(value: str) -> str:
        """Remove HTML tags from string."""
        return re.sub(r'<[^>]+>', '', str(value))
    
    def val_strip_scripts(value: str) -> str:
        """Remove script tags from HTML using safe HTML parsing."""
        # Use HTML parser for safe script tag removal instead of regex
        # This avoids regex-based XSS vulnerabilities
        from html.parser import HTMLParser
        from io import StringIO
        
        class ScriptStripper(HTMLParser):
            def __init__(self):
                super().__init__()
                self.result = StringIO()
                self.in_script = False
                
            def handle_starttag(self, tag, attrs):
                if tag.lower() == 'script':
                    self.in_script = True
                elif not self.in_script:
                    self.result.write(self.get_starttag_text())
                    
            def handle_endtag(self, tag):
                if tag.lower() == 'script':
                    self.in_script = False
                elif not self.in_script:
                    self.result.write(f'</{tag}>')
                    
            def handle_data(self, data):
                if not self.in_script:
                    self.result.write(data)
                    
            def handle_entityref(self, name):
                if not self.in_script:
                    self.result.write(f'&{name};')
                    
            def handle_charref(self, name):
                if not self.in_script:
                    self.result.write(f'&#{name};')
                    
            def get_result(self):
                return self.result.getvalue()
        
        try:
            stripper = ScriptStripper()
            stripper.feed(str(value))
            return stripper.get_result()
        except Exception:
            # If parsing fails, return the original value
            return str(value)
    
    # ========================================================================
    # Validation Builder
    # ========================================================================
    
    class Validator:
        """Chainable validator builder."""
        
        def __init__(self):
            self._rules = []
            self._messages = {}
        
        def string(self):
            self._rules.append(('string', val_is_string))
            return self
        
        def number(self):
            self._rules.append(('number', val_is_number))
            return self
        
        def email(self):
            self._rules.append(('email', val_is_email))
            return self
        
        def url(self):
            self._rules.append(('url', val_is_url))
            return self
        
        def min(self, length: int):
            self._rules.append(('min', lambda v: val_min_length(v, length)))
            return self
        
        def max(self, length: int):
            self._rules.append(('max', lambda v: val_max_length(v, length)))
            return self
        
        def required(self):
            self._rules.append(('required', lambda v: v is not None and v != ''))
            return self
        
        def matches(self, pattern: str):
            self._rules.append(('matches', lambda v: val_matches(v, pattern)))
            return self
        
        def custom(self, name: str, fn: Callable):
            self._rules.append((name, fn))
            return self
        
        def message(self, rule: str, msg: str):
            self._messages[rule] = msg
            return self
        
        def validate(self, value: Any) -> Dict[str, Any]:
            errors = []
            for rule_name, rule_fn in self._rules:
                if not rule_fn(value):
                    msg = self._messages.get(rule_name, f'Failed {rule_name} validation')
                    errors.append(msg)
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'value': value,
            }
    
    def val_create() -> Validator:
        """Create a new validator builder."""
        return Validator()
    
    return {
        # Type Validators
        'isString': val_is_string,
        'isNumber': val_is_number,
        'isInteger': val_is_integer,
        'isFloat': val_is_float,
        'isBoolean': val_is_boolean,
        'isArray': val_is_array,
        'isObject': val_is_object,
        'isNull': val_is_null,
        'isDefined': val_is_defined,
        'isEmpty': val_is_empty,
        'isCallable': val_is_callable,
        
        # String Validators
        'isEmail': val_is_email,
        'isUrl': val_is_url,
        'isUuid': val_is_uuid,
        'isIp': val_is_ip,
        'isIpv4': val_is_ipv4,
        'isIpv6': val_is_ipv6,
        'isDomain': val_is_domain,
        'isHexColor': val_is_hex_color,
        'isCreditCard': val_is_credit_card,
        'isPhone': val_is_phone,
        'isSlug': val_is_slug,
        'isAlpha': val_is_alpha,
        'isAlphanumeric': val_is_alphanumeric,
        'isNumericString': val_is_numeric_string,
        'isAscii': val_is_ascii,
        'isBase64': val_is_base64,
        'isJson': val_is_json,
        'isDateString': val_is_date_string,
        'isDatetimeString': val_is_datetime_string,
        
        # Number Validators
        'isPositive': val_is_positive,
        'isNegative': val_is_negative,
        'isZero': val_is_zero,
        'isBetween': val_is_between,
        'isEven': val_is_even,
        'isOdd': val_is_odd,
        'isFinite': val_is_finite,
        'isPort': val_is_port,
        
        # String Content Validators
        'minLength': val_min_length,
        'maxLength': val_max_length,
        'lengthBetween': val_length_between,
        'lengthExact': val_length_exact,
        'matches': val_matches,
        'contains': val_contains,
        'startsWith': val_starts_with,
        'endsWith': val_ends_with,
        'equals': val_equals,
        'inList': val_in_list,
        'notInList': val_not_in_list,
        
        # Array Validators
        'arrayMinLength': val_array_min_length,
        'arrayMaxLength': val_array_max_length,
        'arrayLengthBetween': val_array_length_between,
        'arrayUnique': val_array_unique,
        'arrayAll': val_array_all,
        'arrayAny': val_array_any,
        
        # Object Validators
        'hasKeys': val_has_keys,
        'hasOnlyKeys': val_has_only_keys,
        'schema': val_schema,
        
        # Password
        'passwordStrength': val_password_strength,
        
        # Sanitization
        'sanitizeString': val_sanitize_string,
        'sanitizeNumber': val_sanitize_number,
        'sanitizeEmail': val_sanitize_email,
        'sanitizeUrl': val_sanitize_url,
        'escapeHtml': val_escape_html,
        'stripHtml': val_strip_html,
        'stripScripts': val_strip_scripts,
        
        # Builder
        'create': val_create,
    }
