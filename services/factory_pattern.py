"""
Factory Pattern Implementation
Demonstrates creational design pattern for object creation
"""
from typing import Optional
from models.room import Room
from models.room_types import Classroom, ConferenceRoom, Laboratory, ComputerLab
from repositories.repository_interface import IReservationRepository
from repositories.in_memory_repository import InMemoryRepository
from repositories.file_repository import FileRepository
from notifications.notifier_interface import INotifier
from notifications.notifiers import EmailNotifier, SMSNotifier, ConsoleNotifier, MultiNotifier


class RoomFactory:
    """
    Factory for creating different room types
    Demonstrates: Factory Pattern, Open/Closed Principle
    """
    
    @staticmethod
    def create_room(room_type: str, room_id: str, name: str, capacity: int, **kwargs) -> Optional[Room]:
        """
        Create a room based on type
        
        Args:
            room_type: Type of room (classroom, conference, laboratory, computer_lab)
            room_id: Unique room identifier
            name: Room name
            capacity: Room capacity
            **kwargs: Additional room-specific parameters
        
        Returns:
            Room instance or None if type is invalid
        """
        room_type = room_type.lower().replace(' ', '_')
        
        if room_type == 'classroom':
            return Classroom(
                room_id, name, capacity,
                has_projector=kwargs.get('has_projector', True),
                whiteboard=kwargs.get('whiteboard', True)
            )
        
        elif room_type == 'conference' or room_type == 'conference_room':
            return ConferenceRoom(
                room_id, name, capacity,
                video_conference=kwargs.get('video_conference', True),
                sound_system=kwargs.get('sound_system', True)
            )
        
        elif room_type == 'laboratory' or room_type == 'lab':
            return Laboratory(
                room_id, name, capacity,
                lab_type=kwargs.get('lab_type', 'General'),
                safety_equipment=kwargs.get('safety_equipment', True)
            )
        
        elif room_type == 'computer_lab':
            return ComputerLab(
                room_id, name, capacity,
                num_computers=kwargs.get('num_computers', capacity),
                has_printer=kwargs.get('has_printer', True)
            )
        
        else:
            print(f"❌ Unknown room type: {room_type}")
            return None
    
    @staticmethod
    def get_available_types() -> list:
        """Get list of available room types"""
        return ['classroom', 'conference', 'laboratory', 'computer_lab']


class RepositoryFactory:
    """
    Factory for creating repository instances
    Demonstrates: Factory Pattern, Dependency Inversion Principle
    """
    
    @staticmethod
    def create_repository(repo_type: str, **kwargs) -> Optional[IReservationRepository]:
        """
        Create a repository based on type
        
        Args:
            repo_type: Type of repository (memory, file, database)
            **kwargs: Repository-specific parameters
        
        Returns:
            Repository instance or None if type is invalid
        """
        repo_type = repo_type.lower()
        
        if repo_type == 'memory' or repo_type == 'in_memory':
            return InMemoryRepository()
        
        elif repo_type == 'file':
            filepath = kwargs.get('filepath', 'reservations.json')
            return FileRepository(filepath)
        
        # Future: database repository
        # elif repo_type == 'database':
        #     return DatabaseRepository(kwargs.get('connection_string'))
        
        else:
            print(f"❌ Unknown repository type: {repo_type}")
            return None
    
    @staticmethod
    def get_available_types() -> list:
        """Get list of available repository types"""
        return ['memory', 'file']


class NotifierFactory:
    """
    Factory for creating notifier instances
    Demonstrates: Factory Pattern
    """
    
    @staticmethod
    def create_notifier(notifier_type: str, **kwargs) -> Optional[INotifier]:
        """
        Create a notifier based on type
        
        Args:
            notifier_type: Type of notifier (email, sms, console, multi)
            **kwargs: Notifier-specific parameters
        
        Returns:
            Notifier instance or None if type is invalid
        """
        notifier_type = notifier_type.lower()
        
        if notifier_type == 'email':
            smtp_server = kwargs.get('smtp_server', 'localhost')
            return EmailNotifier(smtp_server)
        
        elif notifier_type == 'sms':
            api_key = kwargs.get('api_key', 'demo_key')
            return SMSNotifier(api_key)
        
        elif notifier_type == 'console':
            return ConsoleNotifier()
        
        elif notifier_type == 'multi':
            multi = MultiNotifier()
            # Add default notifiers
            multi.add_notifier(ConsoleNotifier())
            multi.add_notifier(EmailNotifier())
            return multi
        
        else:
            print(f"❌ Unknown notifier type: {notifier_type}")
            return None
    
    @staticmethod
    def get_available_types() -> list:
        """Get list of available notifier types"""
        return ['email', 'sms', 'console', 'multi']


class ServiceFactory:
    """
    Factory for creating fully configured services
    Demonstrates: Abstract Factory Pattern, Dependency Injection
    """
    
    @staticmethod
    def create_reservation_service(
        repository_type: str = 'memory',
        notifier_type: str = 'console',
        **kwargs
    ):
        """
        Create a fully configured reservation service
        
        Args:
            repository_type: Type of repository to use
            notifier_type: Type of notifier to use
            **kwargs: Additional configuration
        
        Returns:
            Configured ReservationService instance
        """
        from services.reservation_service import ReservationService
        
        # Create repository
        repository = RepositoryFactory.create_repository(repository_type, **kwargs)
        if not repository:
            raise ValueError(f"Invalid repository type: {repository_type}")
        
        # Create notifier
        notifier = NotifierFactory.create_notifier(notifier_type, **kwargs)
        if not notifier:
            raise ValueError(f"Invalid notifier type: {notifier_type}")
        
        # Create and return service
        return ReservationService(repository, notifier)