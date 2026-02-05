"""
RIFT Standard Library - Date/Time Module

Comprehensive date and time handling utilities.
"""

import time as time_module
from datetime import datetime, date, timedelta, timezone
from typing import Any, Dict, List, Optional, Union
import calendar


def create_datetime_module(interpreter) -> Dict[str, Any]:
    """Create the datetime module for RIFT."""
    
    # ========================================================================
    # Current Date/Time
    # ========================================================================
    
    def dt_now() -> Dict[str, Any]:
        """Get current datetime."""
        now = datetime.now()
        return _datetime_to_dict(now)
    
    def dt_utc_now() -> Dict[str, Any]:
        """Get current UTC datetime."""
        now = datetime.now(timezone.utc)
        return _datetime_to_dict(now)
    
    def dt_today() -> Dict[str, Any]:
        """Get today's date."""
        today = date.today()
        return _date_to_dict(today)
    
    def dt_timestamp() -> float:
        """Get current Unix timestamp."""
        return time_module.time()
    
    def dt_timestamp_ms() -> int:
        """Get current Unix timestamp in milliseconds."""
        return int(time_module.time() * 1000)
    
    # ========================================================================
    # Date/Time Creation
    # ========================================================================
    
    def dt_create(year: int, month: int = 1, day: int = 1,
                  hour: int = 0, minute: int = 0, second: int = 0,
                  microsecond: int = 0) -> Dict[str, Any]:
        """Create datetime from components."""
        dt = datetime(year, month, day, hour, minute, second, microsecond)
        return _datetime_to_dict(dt)
    
    def dt_from_timestamp(timestamp: Union[int, float]) -> Dict[str, Any]:
        """Create datetime from Unix timestamp."""
        dt = datetime.fromtimestamp(timestamp)
        return _datetime_to_dict(dt)
    
    def dt_from_timestamp_utc(timestamp: Union[int, float]) -> Dict[str, Any]:
        """Create UTC datetime from Unix timestamp."""
        dt = datetime.fromtimestamp(timestamp, timezone.utc)
        return _datetime_to_dict(dt)
    
    def dt_from_iso(iso_string: str) -> Dict[str, Any]:
        """Parse ISO 8601 datetime string."""
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return _datetime_to_dict(dt)
    
    def dt_parse(date_string: str, format: str) -> Dict[str, Any]:
        """Parse datetime string with format."""
        dt = datetime.strptime(date_string, format)
        return _datetime_to_dict(dt)
    
    # ========================================================================
    # Formatting
    # ========================================================================
    
    def dt_format(dt_dict: Dict[str, Any], format: str) -> str:
        """Format datetime with format string."""
        dt = _dict_to_datetime(dt_dict)
        return dt.strftime(format)
    
    def dt_to_iso(dt_dict: Dict[str, Any]) -> str:
        """Convert to ISO 8601 string."""
        dt = _dict_to_datetime(dt_dict)
        return dt.isoformat()
    
    def dt_to_timestamp(dt_dict: Dict[str, Any]) -> float:
        """Convert to Unix timestamp."""
        dt = _dict_to_datetime(dt_dict)
        return dt.timestamp()
    
    def dt_to_string(dt_dict: Dict[str, Any]) -> str:
        """Convert to human-readable string."""
        dt = _dict_to_datetime(dt_dict)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    def dt_format_relative(dt_dict: Dict[str, Any]) -> str:
        """Format as relative time (e.g., '2 hours ago')."""
        dt = _dict_to_datetime(dt_dict)
        now = datetime.now()
        diff = now - dt
        
        seconds = diff.total_seconds()
        
        if seconds < 0:
            # Future date
            seconds = abs(seconds)
            suffix = 'from now'
        else:
            suffix = 'ago'
        
        if seconds < 60:
            return 'just now' if suffix == 'ago' else 'in a moment'
        elif seconds < 3600:
            minutes = int(seconds / 60)
            unit = 'minute' if minutes == 1 else 'minutes'
            return f'{minutes} {unit} {suffix}'
        elif seconds < 86400:
            hours = int(seconds / 3600)
            unit = 'hour' if hours == 1 else 'hours'
            return f'{hours} {unit} {suffix}'
        elif seconds < 604800:
            days = int(seconds / 86400)
            unit = 'day' if days == 1 else 'days'
            return f'{days} {unit} {suffix}'
        elif seconds < 2592000:
            weeks = int(seconds / 604800)
            unit = 'week' if weeks == 1 else 'weeks'
            return f'{weeks} {unit} {suffix}'
        elif seconds < 31536000:
            months = int(seconds / 2592000)
            unit = 'month' if months == 1 else 'months'
            return f'{months} {unit} {suffix}'
        else:
            years = int(seconds / 31536000)
            unit = 'year' if years == 1 else 'years'
            return f'{years} {unit} {suffix}'
    
    # ========================================================================
    # Date/Time Manipulation
    # ========================================================================
    
    def dt_add(dt_dict: Dict[str, Any], 
               years: int = 0, months: int = 0, days: int = 0,
               hours: int = 0, minutes: int = 0, seconds: int = 0) -> Dict[str, Any]:
        """Add time to datetime."""
        dt = _dict_to_datetime(dt_dict)
        
        # Handle years and months separately
        new_year = dt.year + years
        new_month = dt.month + months
        
        while new_month > 12:
            new_year += 1
            new_month -= 12
        while new_month < 1:
            new_year -= 1
            new_month += 12
        
        # Handle day overflow
        max_day = calendar.monthrange(new_year, new_month)[1]
        new_day = min(dt.day, max_day)
        
        dt = dt.replace(year=new_year, month=new_month, day=new_day)
        
        # Add remaining time
        dt = dt + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        
        return _datetime_to_dict(dt)
    
    def dt_subtract(dt_dict: Dict[str, Any], 
                    years: int = 0, months: int = 0, days: int = 0,
                    hours: int = 0, minutes: int = 0, seconds: int = 0) -> Dict[str, Any]:
        """Subtract time from datetime."""
        return dt_add(dt_dict, -years, -months, -days, -hours, -minutes, -seconds)
    
    def dt_set(dt_dict: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Set specific datetime components."""
        dt = _dict_to_datetime(dt_dict)
        dt = dt.replace(**kwargs)
        return _datetime_to_dict(dt)
    
    def dt_start_of(dt_dict: Dict[str, Any], unit: str) -> Dict[str, Any]:
        """Get start of time unit (year, month, week, day, hour, minute)."""
        dt = _dict_to_datetime(dt_dict)
        
        if unit == 'year':
            dt = dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        elif unit == 'month':
            dt = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif unit == 'week':
            days_since_monday = dt.weekday()
            dt = dt - timedelta(days=days_since_monday)
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif unit == 'day':
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif unit == 'hour':
            dt = dt.replace(minute=0, second=0, microsecond=0)
        elif unit == 'minute':
            dt = dt.replace(second=0, microsecond=0)
        
        return _datetime_to_dict(dt)
    
    def dt_end_of(dt_dict: Dict[str, Any], unit: str) -> Dict[str, Any]:
        """Get end of time unit."""
        dt = _dict_to_datetime(dt_dict)
        
        if unit == 'year':
            dt = dt.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        elif unit == 'month':
            last_day = calendar.monthrange(dt.year, dt.month)[1]
            dt = dt.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
        elif unit == 'week':
            days_until_sunday = 6 - dt.weekday()
            dt = dt + timedelta(days=days_until_sunday)
            dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif unit == 'day':
            dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif unit == 'hour':
            dt = dt.replace(minute=59, second=59, microsecond=999999)
        elif unit == 'minute':
            dt = dt.replace(second=59, microsecond=999999)
        
        return _datetime_to_dict(dt)
    
    # ========================================================================
    # Comparison and Difference
    # ========================================================================
    
    def dt_diff(dt1_dict: Dict[str, Any], dt2_dict: Dict[str, Any], 
                unit: str = 'seconds') -> float:
        """Get difference between two datetimes."""
        dt1 = _dict_to_datetime(dt1_dict)
        dt2 = _dict_to_datetime(dt2_dict)
        
        diff = dt2 - dt1
        total_seconds = diff.total_seconds()
        
        if unit == 'seconds':
            return total_seconds
        elif unit == 'minutes':
            return total_seconds / 60
        elif unit == 'hours':
            return total_seconds / 3600
        elif unit == 'days':
            return total_seconds / 86400
        elif unit == 'weeks':
            return total_seconds / 604800
        elif unit == 'months':
            return total_seconds / 2592000  # Approximate
        elif unit == 'years':
            return total_seconds / 31536000  # Approximate
        
        return total_seconds
    
    def dt_is_before(dt1_dict: Dict[str, Any], dt2_dict: Dict[str, Any]) -> bool:
        """Check if dt1 is before dt2."""
        dt1 = _dict_to_datetime(dt1_dict)
        dt2 = _dict_to_datetime(dt2_dict)
        return dt1 < dt2
    
    def dt_is_after(dt1_dict: Dict[str, Any], dt2_dict: Dict[str, Any]) -> bool:
        """Check if dt1 is after dt2."""
        dt1 = _dict_to_datetime(dt1_dict)
        dt2 = _dict_to_datetime(dt2_dict)
        return dt1 > dt2
    
    def dt_is_same(dt1_dict: Dict[str, Any], dt2_dict: Dict[str, Any], 
                   unit: str = 'second') -> bool:
        """Check if two datetimes are the same (up to specified unit)."""
        dt1 = _dict_to_datetime(dt1_dict)
        dt2 = _dict_to_datetime(dt2_dict)
        
        if unit == 'year':
            return dt1.year == dt2.year
        elif unit == 'month':
            return dt1.year == dt2.year and dt1.month == dt2.month
        elif unit == 'day':
            return dt1.date() == dt2.date()
        elif unit == 'hour':
            return dt1.date() == dt2.date() and dt1.hour == dt2.hour
        elif unit == 'minute':
            return (dt1.date() == dt2.date() and dt1.hour == dt2.hour and 
                    dt1.minute == dt2.minute)
        else:
            return dt1 == dt2
    
    def dt_is_between(dt_dict: Dict[str, Any], start_dict: Dict[str, Any], 
                      end_dict: Dict[str, Any], inclusive: bool = True) -> bool:
        """Check if datetime is between start and end."""
        dt = _dict_to_datetime(dt_dict)
        start = _dict_to_datetime(start_dict)
        end = _dict_to_datetime(end_dict)
        
        if inclusive:
            return start <= dt <= end
        return start < dt < end
    
    # ========================================================================
    # Date Properties
    # ========================================================================
    
    def dt_is_leap_year(year: int) -> bool:
        """Check if year is a leap year."""
        return calendar.isleap(year)
    
    def dt_days_in_month(year: int, month: int) -> int:
        """Get number of days in month."""
        return calendar.monthrange(year, month)[1]
    
    def dt_days_in_year(year: int) -> int:
        """Get number of days in year."""
        return 366 if calendar.isleap(year) else 365
    
    def dt_week_of_year(dt_dict: Dict[str, Any]) -> int:
        """Get ISO week number."""
        dt = _dict_to_datetime(dt_dict)
        return dt.isocalendar()[1]
    
    def dt_day_of_year(dt_dict: Dict[str, Any]) -> int:
        """Get day of year (1-366)."""
        dt = _dict_to_datetime(dt_dict)
        return dt.timetuple().tm_yday
    
    def dt_day_of_week(dt_dict: Dict[str, Any]) -> int:
        """Get day of week (0=Monday, 6=Sunday)."""
        dt = _dict_to_datetime(dt_dict)
        return dt.weekday()
    
    def dt_day_name(dt_dict: Dict[str, Any]) -> str:
        """Get name of day."""
        dt = _dict_to_datetime(dt_dict)
        return dt.strftime('%A')
    
    def dt_month_name(dt_dict: Dict[str, Any]) -> str:
        """Get name of month."""
        dt = _dict_to_datetime(dt_dict)
        return dt.strftime('%B')
    
    def dt_quarter(dt_dict: Dict[str, Any]) -> int:
        """Get quarter (1-4)."""
        dt = _dict_to_datetime(dt_dict)
        return (dt.month - 1) // 3 + 1
    
    def dt_is_weekend(dt_dict: Dict[str, Any]) -> bool:
        """Check if date is weekend."""
        dt = _dict_to_datetime(dt_dict)
        return dt.weekday() >= 5
    
    def dt_is_weekday(dt_dict: Dict[str, Any]) -> bool:
        """Check if date is weekday."""
        dt = _dict_to_datetime(dt_dict)
        return dt.weekday() < 5
    
    def dt_is_today(dt_dict: Dict[str, Any]) -> bool:
        """Check if date is today."""
        dt = _dict_to_datetime(dt_dict)
        return dt.date() == date.today()
    
    def dt_is_future(dt_dict: Dict[str, Any]) -> bool:
        """Check if datetime is in the future."""
        dt = _dict_to_datetime(dt_dict)
        return dt > datetime.now()
    
    def dt_is_past(dt_dict: Dict[str, Any]) -> bool:
        """Check if datetime is in the past."""
        dt = _dict_to_datetime(dt_dict)
        return dt < datetime.now()
    
    # ========================================================================
    # Duration
    # ========================================================================
    
    def dt_duration(days: int = 0, hours: int = 0, minutes: int = 0, 
                    seconds: int = 0, milliseconds: int = 0) -> Dict[str, Any]:
        """Create a duration object."""
        total_seconds = (days * 86400 + hours * 3600 + 
                        minutes * 60 + seconds + milliseconds / 1000)
        return {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'milliseconds': milliseconds,
            'totalSeconds': total_seconds,
            'totalMinutes': total_seconds / 60,
            'totalHours': total_seconds / 3600,
            'totalDays': total_seconds / 86400,
        }
    
    def dt_duration_between(dt1_dict: Dict[str, Any], 
                            dt2_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Get duration between two datetimes."""
        dt1 = _dict_to_datetime(dt1_dict)
        dt2 = _dict_to_datetime(dt2_dict)
        
        diff = abs(dt2 - dt1)
        total_seconds = diff.total_seconds()
        
        days = diff.days
        remaining_seconds = int(diff.seconds)
        hours = remaining_seconds // 3600
        remaining_seconds %= 3600
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        
        return {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'totalSeconds': total_seconds,
            'totalMinutes': total_seconds / 60,
            'totalHours': total_seconds / 3600,
            'totalDays': total_seconds / 86400,
        }
    
    def dt_format_duration(duration_dict: Dict[str, Any]) -> str:
        """Format duration as human-readable string."""
        days = duration_dict.get('days', 0)
        hours = duration_dict.get('hours', 0)
        minutes = duration_dict.get('minutes', 0)
        seconds = duration_dict.get('seconds', 0)
        
        parts = []
        if days:
            parts.append(f'{days} day{"s" if days != 1 else ""}')
        if hours:
            parts.append(f'{hours} hour{"s" if hours != 1 else ""}')
        if minutes:
            parts.append(f'{minutes} minute{"s" if minutes != 1 else ""}')
        if seconds or not parts:
            parts.append(f'{seconds} second{"s" if seconds != 1 else ""}')
        
        return ', '.join(parts)
    
    # ========================================================================
    # Time Zones
    # ========================================================================
    
    def dt_timezone_offset() -> int:
        """Get local timezone offset in minutes."""
        return -time_module.timezone // 60
    
    def dt_timezone_name() -> str:
        """Get local timezone name."""
        return time_module.tzname[0]
    
    # ========================================================================
    # Helpers
    # ========================================================================
    
    def _datetime_to_dict(dt: datetime) -> Dict[str, Any]:
        """Convert datetime to dictionary."""
        return {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'microsecond': dt.microsecond,
            'weekday': dt.weekday(),
            'dayOfYear': dt.timetuple().tm_yday,
            'weekOfYear': dt.isocalendar()[1],
            'timestamp': dt.timestamp(),
            'iso': dt.isoformat(),
        }
    
    def _date_to_dict(d: date) -> Dict[str, Any]:
        """Convert date to dictionary."""
        return {
            'year': d.year,
            'month': d.month,
            'day': d.day,
            'weekday': d.weekday(),
            'dayOfYear': d.timetuple().tm_yday,
            'weekOfYear': d.isocalendar()[1],
            'iso': d.isoformat(),
        }
    
    def _dict_to_datetime(d: Dict[str, Any]) -> datetime:
        """Convert dictionary to datetime."""
        return datetime(
            d.get('year', 1970),
            d.get('month', 1),
            d.get('day', 1),
            d.get('hour', 0),
            d.get('minute', 0),
            d.get('second', 0),
            d.get('microsecond', 0)
        )
    
    return {
        # Current
        'now': dt_now,
        'utcNow': dt_utc_now,
        'today': dt_today,
        'timestamp': dt_timestamp,
        'timestampMs': dt_timestamp_ms,
        
        # Creation
        'create': dt_create,
        'fromTimestamp': dt_from_timestamp,
        'fromTimestampUtc': dt_from_timestamp_utc,
        'fromIso': dt_from_iso,
        'parse': dt_parse,
        
        # Formatting
        'format': dt_format,
        'toIso': dt_to_iso,
        'toTimestamp': dt_to_timestamp,
        'toString': dt_to_string,
        'formatRelative': dt_format_relative,
        
        # Manipulation
        'add': dt_add,
        'subtract': dt_subtract,
        'set': dt_set,
        'startOf': dt_start_of,
        'endOf': dt_end_of,
        
        # Comparison
        'diff': dt_diff,
        'isBefore': dt_is_before,
        'isAfter': dt_is_after,
        'isSame': dt_is_same,
        'isBetween': dt_is_between,
        
        # Properties
        'isLeapYear': dt_is_leap_year,
        'daysInMonth': dt_days_in_month,
        'daysInYear': dt_days_in_year,
        'weekOfYear': dt_week_of_year,
        'dayOfYear': dt_day_of_year,
        'dayOfWeek': dt_day_of_week,
        'dayName': dt_day_name,
        'monthName': dt_month_name,
        'quarter': dt_quarter,
        'isWeekend': dt_is_weekend,
        'isWeekday': dt_is_weekday,
        'isToday': dt_is_today,
        'isFuture': dt_is_future,
        'isPast': dt_is_past,
        
        # Duration
        'duration': dt_duration,
        'durationBetween': dt_duration_between,
        'formatDuration': dt_format_duration,
        
        # Timezone
        'timezoneOffset': dt_timezone_offset,
        'timezoneName': dt_timezone_name,
    }
