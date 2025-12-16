"""
Validation Service - Advanced Business Rules
Demonstrates additional SOLID principles and validation patterns
"""
from datetime import datetime, time
from typing import Optional, List, Tuple
from models.room import Room
from models.reservation import Reservation


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class ReservationValidator:
    """
    Validates reservations against business rules
    Applies: Single Responsibility Principle - only validation logic
    """
    
    def __init__(self, 
                 min_duration_hours: int = 1,
                 max_duration_hours: int = 8,
                 business_start: time = time(7, 0),
                 business_end: time = time(22, 0),
                 max_advance_days: int = 90):
        self.min_duration_hours = min_duration_hours
        self.max_duration_hours = max_duration_hours
        self.business_start = business_start
        self.business_end = business_end
        self.max_advance_days = max_advance_days
    
    def validate_all(self, room: Room, start_time: datetime, 
                     end_time: datetime, user_name: str) -> Tuple[bool, List[str]]:
        """
        Validate all rules and return (is_valid, list_of_errors)
        """
        errors = []
        
        # Time range validation
        if not self._validate_time_order(start_time, end_time):
            errors.append("End time must be after start time")
        
        # Duration validation
        duration_error = self._validate_duration(start_time, end_time)
        if duration_error:
            errors.append(duration_error)
        
        # Business hours validation
        hours_error = self._validate_business_hours(start_time, end_time)
        if hours_error:
            errors.append(hours_error)
        
        # Future booking validation
        advance_error = self._validate_advance_booking(start_time)
        if advance_error:
            errors.append(advance_error)
        
        # Past booking validation
        if not self._validate_not_in_past(start_time):
            errors.append("Cannot book reservations in the past")
        
        # User name validation
        if not self._validate_user_name(user_name):
            errors.append("User name must be at least 2 characters")
        
        # Room capacity notification (warning, not error)
        if room.capacity < 5:
            errors.append(f"⚠️ Warning: Small room capacity ({room.capacity} people)")
        
        return len(errors) == 0, errors
    
    def _validate_time_order(self, start: datetime, end: datetime) -> bool:
        return start < end
    
    def _validate_duration(self, start: datetime, end: datetime) -> Optional[str]:
        duration_hours = (end - start).total_seconds() / 3600
        
        if duration_hours < self.min_duration_hours:
            return f"Minimum reservation duration is {self.min_duration_hours} hour(s)"
        
        if duration_hours > self.max_duration_hours:
            return f"Maximum reservation duration is {self.max_duration_hours} hours"
        
        return None
    
    def _validate_business_hours(self, start: datetime, end: datetime) -> Optional[str]:
        """Validate reservation is within business hours"""
        start_time = start.time()
        end_time = end.time()
        
        if start_time < self.business_start or end_time > self.business_end:
            return (f"Reservations must be between {self.business_start.strftime('%H:%M')} "
                   f"and {self.business_end.strftime('%H:%M')}")
        
        return None
    
    def _validate_advance_booking(self, start: datetime) -> Optional[str]:
        """Validate not booking too far in advance"""
        days_ahead = (start.date() - datetime.now().date()).days
        
        if days_ahead > self.max_advance_days:
            return f"Cannot book more than {self.max_advance_days} days in advance"
        
        return None
    
    def _validate_not_in_past(self, start: datetime) -> bool:
        """Validate reservation is not in the past"""
        return start > datetime.now()
    
    def _validate_user_name(self, user_name: str) -> bool:
        """Validate user name is not empty"""
        return len(user_name.strip()) >= 2


class CapacityValidator:
    """
    Validates room capacity against number of attendees
    Demonstrates Strategy Pattern for different validation strategies
    """
    
    def validate(self, room: Room, num_attendees: int) -> Tuple[bool, Optional[str]]:
        if num_attendees <= 0:
            return False, "Number of attendees must be positive"
        
        if num_attendees > room.capacity:
            return False, f"Room capacity ({room.capacity}) exceeded by {num_attendees - room.capacity} people"
        
        # Warning for near-capacity
        if num_attendees > room.capacity * 0.9:
            return True, f"⚠️ Warning: Room will be at {(num_attendees/room.capacity)*100:.0f}% capacity"
        
        return True, None