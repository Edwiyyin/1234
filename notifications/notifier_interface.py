"""
Notifier Interface
Applies: Interface Segregation Principle (ISP) - Clients depend only on notification methods they need
         Dependency Inversion Principle (DIP) - Services depend on abstraction, not concrete implementations
"""
from abc import ABC, abstractmethod
from models.reservation import Reservation


class INotifier(ABC):
    """Abstract interface for notification systems"""
    
    @abstractmethod
    def notify_reservation_confirmed(self, reservation: Reservation) -> bool:
        """Send notification when reservation is confirmed"""
        pass
    
    @abstractmethod
    def notify_reservation_cancelled(self, reservation: Reservation) -> bool:
        """Send notification when reservation is cancelled"""
        pass