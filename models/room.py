"""
Room Module - Defines the abstract base class for all room types

SOLID Principles Applied:
- SRP: Room class has single responsibility - managing room attributes
- OCP: Open for extension (new room types) via inheritance, closed for modification
- LSP: All subclasses can substitute Room without breaking functionality

Design Pattern: Template Method Pattern
- Base class defines structure, subclasses fill in specifics
"""
from abc import ABC, abstractmethod
from typing import Dict


class Room(ABC):
    """
    Abstract base class for all room types using Template Method pattern.
    
    Each room has core attributes (id, name, capacity) and must define:
    - Equipment available (specific to room type)
    - Room type identifier (for display/filtering)
    
    Why abstract? Forces all room types to implement required methods,
    ensuring consistent interface across different room implementations.
    """
    
    def __init__(self, room_id: str, name: str, capacity: int):
        """
        Initialize room with core attributes shared by all types.
        
        Protected attributes (_prefix) follow encapsulation principle:
        - Data hiding prevents direct external modification
        - Access controlled through @property decorators
        """
        self._room_id = room_id      # Unique identifier for reservation tracking
        self._name = name            # Human-readable name for display
        self._capacity = capacity    # Maximum occupancy for validation
    
    # Properties provide controlled read-only access (encapsulation)
    @property
    def room_id(self) -> str:
        """Unique identifier - immutable after creation"""
        return self._room_id
    
    @property
    def name(self) -> str:
        """Display name - immutable after creation"""
        return self._name
    
    @property
    def capacity(self) -> int:
        """Maximum number of people - used for validation"""
        return self._capacity
    
    @abstractmethod
    def get_equipment(self) -> Dict[str, any]:
        """
        Abstract method: Each room type defines its own equipment.
        
        Why abstract? Equipment varies by room type (projector vs lab equipment).
        Forces subclasses to specify what's available.
        
        Returns:
            Dictionary of equipment_name: availability/details
        """
        pass
    
    @abstractmethod
    def get_room_type(self) -> str:
        """
        Abstract method: Each room type identifies itself.
        
        Used for:
        - Display in UI (user sees "Classroom" vs "Laboratory")
        - Filtering/searching by type
        - Polymorphic behavior (same interface, different types)
        
        Returns:
            Human-readable room type string
        """
        pass
    
    def __str__(self) -> str:
        """
        String representation for logging and display.
        Uses polymorphism - get_room_type() calls subclass implementation.
        """
        return f"{self.get_room_type()} - {self.name} (ID: {self.room_id}, Capacity: {self.capacity})"