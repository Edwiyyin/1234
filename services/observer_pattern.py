"""
Observer Pattern Implementation
Demonstrates advanced design pattern for event-driven notifications
"""
from abc import ABC, abstractmethod
from typing import List
from models.reservation import Reservation


class ReservationObserver(ABC):
    """
    Observer interface for reservation events
    Demonstrates: Observer Pattern, Interface Segregation Principle
    """
    
    @abstractmethod
    def on_reservation_created(self, reservation: Reservation):
        """Called when a new reservation is created"""
        pass
    
    @abstractmethod
    def on_reservation_cancelled(self, reservation: Reservation):
        """Called when a reservation is cancelled"""
        pass
    
    @abstractmethod
    def on_reservation_modified(self, reservation: Reservation):
        """Called when a reservation is modified"""
        pass


class ReservationSubject:
    """
    Subject that notifies observers of reservation events
    Demonstrates: Observer Pattern
    """
    
    def __init__(self):
        self._observers: List[ReservationObserver] = []
    
    def attach(self, observer: ReservationObserver):
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: ReservationObserver):
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_created(self, reservation: Reservation):
        """Notify all observers of creation"""
        for observer in self._observers:
            observer.on_reservation_created(reservation)
    
    def notify_cancelled(self, reservation: Reservation):
        """Notify all observers of cancellation"""
        for observer in self._observers:
            observer.on_reservation_cancelled(reservation)
    
    def notify_modified(self, reservation: Reservation):
        """Notify all observers of modification"""
        for observer in self._observers:
            observer.on_reservation_modified(reservation)


class StatisticsObserver(ReservationObserver):
    """
    Observer that tracks reservation statistics
    Demonstrates: Observer Pattern application
    """
    
    def __init__(self):
        self.total_created = 0
        self.total_cancelled = 0
        self.total_modified = 0
        self.active_reservations = 0
    
    def on_reservation_created(self, reservation: Reservation):
        self.total_created += 1
        self.active_reservations += 1
        print(f"📊 Stats: {self.total_created} created, {self.active_reservations} active")
    
    def on_reservation_cancelled(self, reservation: Reservation):
        self.total_cancelled += 1
        self.active_reservations -= 1
        print(f"📊 Stats: {self.total_cancelled} cancelled, {self.active_reservations} active")
    
    def on_reservation_modified(self, reservation: Reservation):
        self.total_modified += 1
        print(f"📊 Stats: {self.total_modified} modified")
    
    def get_statistics(self):
        """Get current statistics"""
        return {
            'total_created': self.total_created,
            'total_cancelled': self.total_cancelled,
            'total_modified': self.total_modified,
            'active_reservations': self.active_reservations
        }


class AuditLogObserver(ReservationObserver):
    """
    Observer that maintains an audit log
    Demonstrates: Observer Pattern for logging/auditing
    """
    
    def __init__(self):
        self.audit_log = []
    
    def on_reservation_created(self, reservation: Reservation):
        self._log_event('CREATED', reservation)
    
    def on_reservation_cancelled(self, reservation: Reservation):
        self._log_event('CANCELLED', reservation)
    
    def on_reservation_modified(self, reservation: Reservation):
        self._log_event('MODIFIED', reservation)
    
    def _log_event(self, event_type: str, reservation: Reservation):
        from datetime import datetime
        log_entry = {
            'timestamp': datetime.now(),
            'event': event_type,
            'reservation_id': reservation.reservation_id,
            'room': reservation.room.name,
            'user': reservation.user_name
        }
        self.audit_log.append(log_entry)
        print(f"📝 Audit: {event_type} - {reservation.reservation_id} by {reservation.user_name}")
    
    def get_audit_log(self):
        """Get complete audit log"""
        return self.audit_log