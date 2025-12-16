"""
Comprehensive Unit Tests
Demonstrates professional testing practices with pytest
"""
import pytest
from datetime import datetime, timedelta
from models.room_types import Classroom, ConferenceRoom, Laboratory
from models.reservation import Reservation
from repositories.in_memory_repository import InMemoryRepository
from repositories.file_repository import FileRepository
from notifications.notifiers import ConsoleNotifier, EmailNotifier
from services.reservation_service import ReservationService
from services.validation_service import ReservationValidator, CapacityValidator
from services.factory_pattern import RoomFactory, RepositoryFactory, NotifierFactory
import os


class TestRoomModels:
    """Test room models"""
    
    def test_classroom_creation(self):
        """Test creating a classroom"""
        room = Classroom("CL-101", "Test Room", 30)
        assert room.room_id == "CL-101"
        assert room.name == "Test Room"
        assert room.capacity == 30
        assert room.get_room_type() == "Classroom"
    
    def test_room_equipment(self):
        """Test room equipment retrieval"""
        room = Classroom("CL-101", "Test Room", 30, has_projector=True)
        equipment = room.get_equipment()
        assert equipment['projector'] == True
        assert 'desks' in equipment
    
    def test_conference_room(self):
        """Test conference room creation"""
        room = ConferenceRoom("CF-201", "Board Room", 15, video_conference=True)
        assert room.get_room_type() == "Conference Room"
        assert room.get_equipment()['video_conference'] == True
    
    def test_laboratory(self):
        """Test laboratory creation"""
        room = Laboratory("LAB-301", "Chem Lab", 25, lab_type="Chemistry")
        assert "Chemistry" in room.get_room_type()


class TestReservation:
    """Test reservation model"""
    
    def test_reservation_creation(self):
        """Test creating a reservation"""
        room = Classroom("CL-101", "Test Room", 30)
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(hours=2)
        
        reservation = Reservation("RES-001", room, "John Doe", start, end, "Test")
        
        assert reservation.reservation_id == "RES-001"
        assert reservation.user_name == "John Doe"
        assert reservation.status == "CONFIRMED"
    
    def test_reservation_cancellation(self):
        """Test cancelling a reservation"""
        room = Classroom("CL-101", "Test Room", 30)
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(hours=2)
        
        reservation = Reservation("RES-001", room, "John Doe", start, end)
        reservation.cancel()
        
        assert reservation.status == "CANCELLED"
    
    def test_reservation_overlap(self):
        """Test reservation overlap detection"""
        room = Classroom("CL-101", "Test Room", 30)
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(hours=2)
        
        reservation = Reservation("RES-001", room, "John Doe", start, end)
        
        # Overlapping time
        overlap_start = start + timedelta(hours=1)
        overlap_end = end + timedelta(hours=1)
        assert reservation.overlaps_with(overlap_start, overlap_end) == True
        
        # Non-overlapping time
        future_start = end + timedelta(hours=1)
        future_end = future_start + timedelta(hours=1)
        assert reservation.overlaps_with(future_start, future_end) == False


class TestInMemoryRepository:
    """Test in-memory repository"""
    
    def test_save_and_find(self):
        """Test saving and finding reservations"""
        repo = InMemoryRepository()
        room = Classroom("CL-101", "Test Room", 30)
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(hours=2)
        
        reservation = Reservation("RES-001", room, "John Doe", start, end)
        
        assert repo.save(reservation) == True
        found = repo.find_by_id("RES-001")
        assert found is not None
        assert found.reservation_id == "RES-001"
    
    def test_find_by_room_and_time(self):
        """Test finding reservations by room and time"""
        repo = InMemoryRepository()
        room = Classroom("CL-101", "Test Room", 30)
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(hours=2)
        
        reservation = Reservation("RES-001", room, "John Doe", start, end)
        repo.save(reservation)
        
        # Find overlapping
        conflicts = repo.find_by_room_and_time(room, start, end)
        assert len(conflicts) == 1
        
        # Find non-overlapping
        future_start = end + timedelta(hours=1)
        future_end = future_start + timedelta(hours=1)
        conflicts = repo.find_by_room_and_time(room, future_start, future_end)
        assert len(conflicts) == 0
    
    def test_delete(self):
        """Test deleting reservations"""
        repo = InMemoryRepository()
        room = Classroom("CL-101", "Test Room", 30)
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(hours=2)
        
        reservation = Reservation("RES-001", room, "John Doe", start, end)
        repo.save(reservation)
        
        assert repo.delete("RES-001") == True
        assert repo.find_by_id("RES-001") is None


class TestReservationService:
    """Test reservation service"""
    
    def test_create_reservation_success(self):
        """Test successful reservation creation"""
        repo = InMemoryRepository()
        notifier = ConsoleNotifier()
        service = ReservationService(repo, notifier)
        
        room = Classroom("CL-101", "Test Room", 30)
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(hours=2)
        
        reservation = service.create_reservation(room, "John Doe", start, end, "Test")
        
        assert reservation is not None
        assert reservation.user_name == "John Doe"
    
    def test_create_reservation_conflict(self):
        """Test reservation conflict detection"""
        repo = InMemoryRepository()
        notifier = ConsoleNotifier()
        service = ReservationService(repo, notifier)
        
        room = Classroom("CL-101", "Test Room", 30)
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(hours=2)
        
        # First reservation
        res1 = service.create_reservation(room, "John Doe", start, end)
        assert res1 is not None
        
        # Conflicting reservation
        res2 = service.create_reservation(room, "Jane Smith", start, end)
        assert res2 is None  # Should fail due to conflict
    
    def test_cancel_reservation(self):
        """Test reservation cancellation"""
        repo = InMemoryRepository()
        notifier = ConsoleNotifier()
        service = ReservationService(repo, notifier)
        
        room = Classroom("CL-101", "Test Room", 30)
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(hours=2)
        
        reservation = service.create_reservation(room, "John Doe", start, end)
        assert reservation is not None
        
        # Cancel
        success = service.cancel_reservation(reservation.reservation_id)
        assert success == True
        
        # Check status
        res = service.get_reservation(reservation.reservation_id)
        assert res.status == "CANCELLED"


class TestValidation:
    """Test validation service"""
    
    def test_time_order_validation(self):
        """Test time order validation"""
        validator = ReservationValidator()
        room = Classroom("CL-101", "Test Room", 30)
        
        start = datetime.now() + timedelta(hours=2)
        end = start - timedelta(hours=1)  # Invalid: end before start
        
        is_valid, errors = validator.validate_all(room, start, end, "John Doe")
        assert is_valid == False
        assert len(errors) > 0
    
    def test_duration_validation(self):
        """Test duration validation"""
        validator = ReservationValidator(min_duration_hours=1, max_duration_hours=8)
        room = Classroom("CL-101", "Test Room", 30)
        
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(minutes=30)  # Too short
        
        is_valid, errors = validator.validate_all(room, start, end, "John Doe")
        assert is_valid == False
    
    def test_capacity_validation(self):
        """Test capacity validation"""
        validator = CapacityValidator()
        room = Classroom("CL-101", "Test Room", 30)
        
        # Valid capacity
        is_valid, msg = validator.validate(room, 25)
        assert is_valid == True
        
        # Exceeds capacity
        is_valid, msg = validator.validate(room, 35)
        assert is_valid == False


class TestFactoryPattern:
    """Test factory pattern implementations"""
    
    def test_room_factory(self):
        """Test room factory"""
        room = RoomFactory.create_room('classroom', 'CL-101', 'Test Room', 30)
        assert room is not None
        assert isinstance(room, Classroom)
        
        room = RoomFactory.create_room('conference', 'CF-201', 'Board Room', 15)
        assert room is not None
        assert isinstance(room, ConferenceRoom)
    
    def test_repository_factory(self):
        """Test repository factory"""
        repo = RepositoryFactory.create_repository('memory')
        assert repo is not None
        assert isinstance(repo, InMemoryRepository)
    
    def test_notifier_factory(self):
        """Test notifier factory"""
        notifier = NotifierFactory.create_notifier('console')
        assert notifier is not None
        assert isinstance(notifier, ConsoleNotifier)


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )


# Run tests with: pytest tests.py -v
# Run with coverage: pytest tests.py --cov=. --cov-report=html