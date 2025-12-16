"""
Reservation Service - Core business logic
Applies ALL SOLID Principles:
  - SRP: Single responsibility of managing reservations
  - OCP: Open for extension (new validation rules, notification types)
  - LSP: Works with any Room and Repository implementations
  - ISP: Depends only on required interfaces
  - DIP: Depends on abstractions (IReservationRepository, INotifier)
"""
from datetime import datetime
from typing import List, Optional
import uuid
from models.reservation import Reservation
from models.room import Room
from repositories.repository_interface import IReservationRepository
from notifications.notifier_interface import INotifier


class ReservationService:
    """
    Service for managing room reservations
    Dependencies are injected (DIP), making it testable and flexible
    """
    
    def __init__(self, repository: IReservationRepository, notifier: INotifier):
        """
        Initialize with repository and notifier (Dependency Injection)
        
        Args:
            repository: Implementation of IReservationRepository
            notifier: Implementation of INotifier
        """
        self._repository = repository
        self._notifier = notifier
    
    def create_reservation(self, room: Room, user_name: str, 
                          start_time: datetime, end_time: datetime,
                          purpose: str = "") -> Optional[Reservation]:
        """
        Create a new reservation
        
        Returns:
            Reservation object if successful, None if validation fails
        """
        # Validate time range
        if not self._validate_time_range(start_time, end_time):
            print("❌ Error: Invalid time range. End time must be after start time.")
            return None
        
        # Check for conflicts
        if not self._check_availability(room, start_time, end_time):
            print(f"❌ Error: Room {room.name} is not available for the requested time slot.")
            return None
        
        # Create reservation
        reservation_id = self._generate_reservation_id()
        reservation = Reservation(
            reservation_id=reservation_id,
            room=room,
            user_name=user_name,
            start_time=start_time,
            end_time=end_time,
            purpose=purpose
        )
        
        # Save reservation
        if self._repository.save(reservation):
            # Send notification
            self._notifier.notify_reservation_confirmed(reservation)
            return reservation
        else:
            print("❌ Error: Failed to save reservation.")
            return None
    
    def cancel_reservation(self, reservation_id: str) -> bool:
        """
        Cancel an existing reservation
        
        Returns:
            True if successful, False otherwise
        """
        reservation = self._repository.find_by_id(reservation_id)
        
        if not reservation:
            print(f"❌ Error: Reservation {reservation_id} not found.")
            return False
        
        if reservation.status == "CANCELLED":
            print(f"⚠ Warning: Reservation {reservation_id} is already cancelled.")
            return False
        
        # Cancel the reservation
        reservation.cancel()
        
        # Update in repository
        if self._repository.save(reservation):
            # Send notification
            self._notifier.notify_reservation_cancelled(reservation)
            return True
        else:
            print("❌ Error: Failed to update reservation.")
            return False
    
    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        """Get a reservation by ID"""
        return self._repository.find_by_id(reservation_id)
    
    def get_all_reservations(self) -> List[Reservation]:
        """Get all reservations"""
        return self._repository.find_all()
    
    def get_room_availability(self, room: Room, start_time: datetime, 
                             end_time: datetime) -> List[Reservation]:
        """
        Get all reservations for a room in a time range
        
        Returns:
            List of conflicting reservations (empty if available)
        """
        return self._repository.find_by_room_and_time(room, start_time, end_time)
    
    def _validate_time_range(self, start_time: datetime, end_time: datetime) -> bool:
        """Validate that the time range is valid"""
        return start_time < end_time
    
    def _check_availability(self, room: Room, start_time: datetime, 
                           end_time: datetime) -> bool:
        """Check if the room is available for the requested time"""
        conflicts = self._repository.find_by_room_and_time(room, start_time, end_time)
        return len(conflicts) == 0
    
    def _generate_reservation_id(self) -> str:
        """Generate a unique reservation ID"""
        return f"RES-{uuid.uuid4().hex[:8].upper()}"