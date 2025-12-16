"""
File-based Repository Implementation - JSON Persistence Strategy

SOLID Principles:
- DIP: Implements IReservationRepository abstraction
- SRP: Single responsibility - handle file-based storage only
- OCP: New storage types (database, cloud) can be added without modifying this

Storage Strategy: JSON File Format
- Human-readable (can inspect with text editor)
- Portable across platforms
- Simple serialization/deserialization
- No external dependencies (uses Python's json module)

Persistence Flow:
1. Load entire file into memory (read all reservations)
2. Modify data structure in memory
3. Write entire structure back to file (atomic write)

Trade-offs:
Pros:
- Simple implementation
- No database setup required
- Data persists between program runs
- Easy backup (just copy file)

Cons:
- Not suitable for concurrent access (no locking)
- Performance degrades with large datasets (loads all into memory)
- No query optimization (loads everything every time)
- Risk of data loss if write fails mid-operation

Production Considerations:
- Real system would use database with transactions
- Would implement file locking for concurrent access
- Would add backup/recovery mechanisms
- Would use append-only logging for safety
"""
import json
import os
from typing import List, Optional
from datetime import datetime
from models.reservation import Reservation
from models.room import Room
from models.room_types import Classroom, ConferenceRoom, Laboratory, ComputerLab
from repositories.repository_interface import IReservationRepository


class FileRepository(IReservationRepository):
    """
    Stores reservations persistently in JSON file.
    
    File Format Example:
    [
      {
        "reservation_id": "RES-ABC123",
        "room": {"type": "Classroom", "room_id": "CL-101", ...},
        "user_name": "John Doe",
        "start_time": "2025-12-20T09:00:00",
        "end_time": "2025-12-20T11:00:00",
        "purpose": "Python Workshop",
        "status": "CONFIRMED"
      }
    ]
    
    Implementation Strategy:
    - Read-modify-write pattern for all operations
    - Full file reload on each operation (simple but not scalable)
    - JSON for human readability and portability
    """
    
    def __init__(self, filepath: str = "reservations.json"):
        """
        Initialize file-based storage.
        
        Args:
            filepath: Path to JSON file (default: reservations.json)
            
        Design Decision: Default filename in current directory
        Makes it easy to use without configuration
        
        Initialization Steps:
        1. Store filepath
        2. Ensure file exists (create if not)
        """
        self._filepath = filepath
        self._ensure_file_exists()  # Idempotent - safe to call multiple times
    
    def _ensure_file_exists(self):
        """
        Create empty JSON file if it doesn't exist.
        
        Why needed? Prevents FileNotFoundError on first run
        Idempotent: Safe to call multiple times
        
        Creates file with empty array [] ready for reservations
        """
        # os.path.exists() checks if file is present
        if not os.path.exists(self._filepath):
            # Create new file with empty JSON array
            # 'w' mode creates file if doesn't exist
            with open(self._filepath, 'w') as f:
                json.dump([], f)  # Write empty list
    
    def _load_reservations(self) -> List[Reservation]:
        """Load reservations from file"""
        try:
            with open(self._filepath, 'r') as f:
                data = json.load(f)
                reservations = []
                for item in data:
                    room = self._deserialize_room(item['room'])
                    reservation = Reservation(
                        reservation_id=item['reservation_id'],
                        room=room,
                        user_name=item['user_name'],
                        start_time=datetime.fromisoformat(item['start_time']),
                        end_time=datetime.fromisoformat(item['end_time']),
                        purpose=item.get('purpose', '')
                    )
                    reservation._status = item.get('status', 'CONFIRMED')
                    reservations.append(reservation)
                return reservations
        except Exception as e:
            print(f"Error loading reservations: {e}")
            return []
    
    def _save_reservations(self, reservations: List[Reservation]) -> bool:
        """Save all reservations to file"""
        try:
            data = []
            for reservation in reservations:
                data.append({
                    'reservation_id': reservation.reservation_id,
                    'room': self._serialize_room(reservation.room),
                    'user_name': reservation.user_name,
                    'start_time': reservation.start_time.isoformat(),
                    'end_time': reservation.end_time.isoformat(),
                    'purpose': reservation.purpose,
                    'status': reservation.status
                })
            with open(self._filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving reservations: {e}")
            return False
    
    def _serialize_room(self, room: Room) -> dict:
        """Convert room to dictionary"""
        return {
            'type': room.get_room_type(),
            'room_id': room.room_id,
            'name': room.name,
            'capacity': room.capacity,
            'equipment': room.get_equipment()
        }
    
    def _deserialize_room(self, data: dict) -> Room:
        """Convert dictionary to room object"""
        room_type = data['type']
        if 'Classroom' in room_type:
            return Classroom(data['room_id'], data['name'], data['capacity'])
        elif 'Conference' in room_type:
            return ConferenceRoom(data['room_id'], data['name'], data['capacity'])
        elif 'Computer' in room_type:
            return ComputerLab(data['room_id'], data['name'], data['capacity'])
        else:  # Laboratory
            return Laboratory(data['room_id'], data['name'], data['capacity'])
    
    def save(self, reservation: Reservation) -> bool:
        """Save a reservation"""
        reservations = self._load_reservations()
        # Update if exists, add if new
        updated = False
        for i, res in enumerate(reservations):
            if res.reservation_id == reservation.reservation_id:
                reservations[i] = reservation
                updated = True
                break
        if not updated:
            reservations.append(reservation)
        return self._save_reservations(reservations)
    
    def find_by_id(self, reservation_id: str) -> Optional[Reservation]:
        """Find a reservation by ID"""
        reservations = self._load_reservations()
        for reservation in reservations:
            if reservation.reservation_id == reservation_id:
                return reservation
        return None
    
    def find_by_room_and_time(self, room: Room, start_time: datetime, 
                              end_time: datetime) -> List[Reservation]:
        """Find overlapping reservations for a room"""
        reservations = self._load_reservations()
        overlapping = []
        for reservation in reservations:
            if (reservation.room.room_id == room.room_id and 
                reservation.overlaps_with(start_time, end_time) and
                reservation.status != "CANCELLED"):
                overlapping.append(reservation)
        return overlapping
    
    def find_all(self) -> List[Reservation]:
        """Get all reservations"""
        return self._load_reservations()
    
    def delete(self, reservation_id: str) -> bool:
        """Delete a reservation"""
        reservations = self._load_reservations()
        reservations = [r for r in reservations if r.reservation_id != reservation_id]
        return self._save_reservations(reservations)