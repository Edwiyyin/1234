"""
Repository Interface - Data Access Abstraction

SOLID Principles Applied:
- ISP (Interface Segregation): Small, focused interface with only storage operations
  Clients only depend on methods they need - no bloated interface
- DIP (Dependency Inversion): High-level modules (Service) depend on this abstraction
  Low-level modules (InMemory, File) implement this abstraction
  
Design Pattern: Repository Pattern
- Abstracts data access logic from business logic
- Allows swapping storage implementations without changing service code
- Encapsulates query logic in one place

Why Interfaces Matter:
- Enables testing with mock repositories
- Allows multiple storage strategies (memory, file, database)
- Decouples business logic from persistence details
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from models.reservation import Reservation
from models.room import Room


class IReservationRepository(ABC):
    """
    Abstract interface defining contract for reservation storage.
    
    Contract Pattern: Any class implementing this interface MUST provide
    all these methods with the exact same signatures.
    
    Benefits:
    - Service layer doesn't care HOW data is stored
    - Can swap implementations at runtime
    - Testing becomes easy with mock implementations
    """
    
    @abstractmethod
    def save(self, reservation: Reservation) -> bool:
        """
        Persist a reservation to storage.
        
        Implementation Strategy:
        - InMemoryRepository: Store in dictionary
        - FileRepository: Serialize to JSON file
        - DatabaseRepository: INSERT or UPDATE in database
        
        Args:
            reservation: Reservation object to persist
            
        Returns:
            True if successful, False otherwise
            
        Design Note: Returns bool for error handling, not exceptions
        Allows graceful degradation in service layer
        """
        pass
    
    @abstractmethod
    def find_by_id(self, reservation_id: str) -> Optional[Reservation]:
        """
        Retrieve a single reservation by its unique identifier.
        
        Query Strategy:
        - Fast lookup by primary key
        - Returns None if not found (not exception)
        
        Args:
            reservation_id: Unique identifier (e.g., "RES-ABC123")
            
        Returns:
            Reservation object if found, None otherwise
            
        Why Optional? Pythonic way to indicate "might not exist"
        Caller must check for None before using result
        """
        pass
    
    @abstractmethod
    def find_by_room_and_time(self, room: Room, start_time: datetime, 
                              end_time: datetime) -> List[Reservation]:
        """
        Find all reservations for a room that overlap with a time range.
        
        Business Logic: Critical for conflict detection
        - Cannot book same room at overlapping times
        - Must check against all existing reservations
        
        Implementation Notes:
        - Should exclude CANCELLED reservations
        - Uses Reservation.overlaps_with() method
        - Returns empty list if no conflicts
        
        Args:
            room: Room to check availability for
            start_time: Start of requested time range
            end_time: End of requested time range
            
        Returns:
            List of conflicting reservations (empty if available)
            
        Performance: This is a frequent query - implementations should optimize
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Reservation]:
        """
        Retrieve all reservations from storage.
        
        Use Cases:
        - Display all bookings in admin panel
        - Generate reports
        - Export data
        
        Returns:
            List of all reservations (may be empty)
            
        Warning: Could be slow with large datasets
        Production systems should add pagination
        """
        pass
    
    @abstractmethod
    def delete(self, reservation_id: str) -> bool:
        """
        Permanently remove a reservation from storage.
        
        Design Decision: Separate from cancel()
        - cancel() marks status as CANCELLED (soft delete)
        - delete() removes from storage (hard delete)
        
        Business Rule: Usually prefer cancel() for audit trail
        delete() only for admin/cleanup operations
        
        Args:
            reservation_id: ID of reservation to remove
            
        Returns:
            True if deleted, False if not found or error
        """
        pass