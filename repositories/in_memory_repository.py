"""
In-Memory Repository Implementation

SOLID Principles:
- DIP: Implements IReservationRepository abstraction
- SRP: Single responsibility - manage in-memory storage only
- OCP: New storage types can be added without modifying this class

Storage Strategy: Python Dictionary (Hash Table)
- Key: reservation_id (string)
- Value: Reservation object
- O(1) lookup by ID - very fast!
- Data lost when program terminates (volatile storage)

Use Cases:
- Development and testing (no file I/O overhead)
- Temporary data that doesn't need persistence
- Demonstration purposes
- Unit tests with mock data
"""
from typing import List, Optional, Dict
from datetime import datetime
from models.reservation import Reservation
from models.room import Room
from repositories.repository_interface import IReservationRepository


class InMemoryRepository(IReservationRepository):
    """
    Stores reservations in RAM using a Python dictionary.
    
    Pros:
    - Very fast (no disk I/O)
    - Simple implementation
    - Great for testing
    
    Cons:
    - Data lost when program ends
    - Limited by available RAM
    - No sharing between processes
    
    Implementation Detail: Uses dict for O(1) lookup performance
    """
    
    def __init__(self):
        """
        Initialize empty storage.
        
        Data Structure: Dictionary for fast key-based access
        Type hint ensures type safety throughout class
        """
        # Dictionary: reservation_id -> Reservation object
        # Provides O(1) lookup, insert, and delete
        self._reservations: Dict[str, Reservation] = {}
    
    def save(self, reservation: Reservation) -> bool:
        """
        Store reservation in memory dictionary.
        
        Behavior:
        - If ID exists: Updates existing reservation (upsert)
        - If ID new: Adds new reservation
        
        Why upsert? Allows updating reservation status (e.g., cancellation)
        without separate update method (keeps interface small - ISP)
        """
        try:
            # Dictionary assignment: O(1) operation
            # Overwrites if key exists, creates if new
            self._reservations[reservation.reservation_id] = reservation
            return True
        except Exception as e:
            # Defensive programming: Catch unexpected errors
            # In practice, dict assignment rarely fails
            print(f"Error saving reservation: {e}")
            return False
    
    def find_by_id(self, reservation_id: str) -> Optional[Reservation]:
        """
        Retrieve reservation by ID using dictionary lookup.
        
        Performance: O(1) - hash table lookup
        Much faster than searching through a list
        """
        # dict.get() returns None if key doesn't exist
        # Safer than dict[key] which raises KeyError
        return self._reservations.get(reservation_id)
    
    def find_by_room_and_time(self, room: Room, start_time: datetime, 
                              end_time: datetime) -> List[Reservation]:
        """
        Find conflicting reservations for conflict detection.
        
        Algorithm:
        1. Iterate through all reservations
        2. Filter by room_id match
        3. Check for time overlap using overlaps_with()
        4. Exclude cancelled reservations
        
        Performance: O(n) where n = total reservations
        Could be optimized with indexing by room_id
        """
        overlapping = []
        
        # Linear search through all reservations
        # Production system would use indexes for better performance
        for reservation in self._reservations.values():
            # Three conditions must ALL be true:
            # 1. Same room (compare by room_id for accuracy)
            # 2. Time ranges overlap (uses mathematical overlap logic)
            # 3. Not cancelled (cancelled bookings don't block)
            if (reservation.room.room_id == room.room_id and 
                reservation.overlaps_with(start_time, end_time) and
                reservation.status != "CANCELLED"):
                overlapping.append(reservation)
        
        return overlapping
    
    def find_all(self) -> List[Reservation]:
        """
        Return all reservations as a list.
        
        Implementation: Convert dictionary values to list
        Order is not guaranteed (dict iteration order in Python 3.7+)
        """
        # dict.values() returns view of all values
        # list() converts to actual list for caller
        return list(self._reservations.values())
    
    def delete(self, reservation_id: str) -> bool:
        """
        Remove reservation from memory.
        
        Hard delete: Reservation is completely removed
        Compare to soft delete (setting status=CANCELLED)
        """
        # Check if key exists before attempting delete
        if reservation_id in self._reservations:
            # Remove from dictionary - O(1) operation
            del self._reservations[reservation_id]
            return True
        
        # Key didn't exist - nothing to delete
        return False