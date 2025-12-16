"""
Concrete Notifier Implementations
Applies: Open/Closed Principle - New notifiers can be added without modifying existing code
         Single Responsibility Principle - Each notifier has one notification method
"""
from models.reservation import Reservation
from notifications.notifier_interface import INotifier


class EmailNotifier(INotifier):
    """Send notifications via email (simulated)"""
    
    def __init__(self, smtp_server: str = "localhost"):
        self._smtp_server = smtp_server
    
    def notify_reservation_confirmed(self, reservation: Reservation) -> bool:
        """Simulate sending email confirmation"""
        print(f"[EMAIL] Sending confirmation to {reservation.user_name}")
        print(f"[EMAIL] Subject: Reservation Confirmed - {reservation.room.name}")
        print(f"[EMAIL] Your reservation #{reservation.reservation_id} has been confirmed")
        print(f"[EMAIL] Room: {reservation.room.name}")
        print(f"[EMAIL] Time: {reservation.start_time.strftime('%Y-%m-%d %H:%M')} - {reservation.end_time.strftime('%H:%M')}")
        print(f"[EMAIL] ✓ Email sent successfully via {self._smtp_server}")
        print()
        return True
    
    def notify_reservation_cancelled(self, reservation: Reservation) -> bool:
        """Simulate sending cancellation email"""
        print(f"[EMAIL] Sending cancellation notice to {reservation.user_name}")
        print(f"[EMAIL] Subject: Reservation Cancelled - {reservation.room.name}")
        print(f"[EMAIL] Your reservation #{reservation.reservation_id} has been cancelled")
        print(f"[EMAIL] ✓ Email sent successfully")
        print()
        return True


class SMSNotifier(INotifier):
    """Send notifications via SMS (simulated)"""
    
    def __init__(self, api_key: str = "demo_key"):
        self._api_key = api_key
    
    def notify_reservation_confirmed(self, reservation: Reservation) -> bool:
        """Simulate sending SMS confirmation"""
        message = (f"Reservation confirmed! {reservation.room.name} "
                  f"on {reservation.start_time.strftime('%Y-%m-%d %H:%M')} "
                  f"Ref: {reservation.reservation_id}")
        print(f"[SMS] Sending to {reservation.user_name}: {message}")
        print(f"[SMS] ✓ SMS sent successfully")
        print()
        return True
    
    def notify_reservation_cancelled(self, reservation: Reservation) -> bool:
        """Simulate sending SMS cancellation"""
        message = f"Reservation {reservation.reservation_id} cancelled for {reservation.room.name}"
        print(f"[SMS] Sending to {reservation.user_name}: {message}")
        print(f"[SMS] ✓ SMS sent successfully")
        print()
        return True


class ConsoleNotifier(INotifier):
    """Display notifications in console"""
    
    def notify_reservation_confirmed(self, reservation: Reservation) -> bool:
        """Display confirmation in console"""
        print("=" * 60)
        print("✓ RESERVATION CONFIRMED")
        print("=" * 60)
        print(f"Reservation ID: {reservation.reservation_id}")
        print(f"User: {reservation.user_name}")
        print(f"Room: {reservation.room}")
        print(f"Start: {reservation.start_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"End: {reservation.end_time.strftime('%Y-%m-%d %H:%M')}")
        if reservation.purpose:
            print(f"Purpose: {reservation.purpose}")
        print("=" * 60)
        print()
        return True
    
    def notify_reservation_cancelled(self, reservation: Reservation) -> bool:
        """Display cancellation in console"""
        print("=" * 60)
        print("✗ RESERVATION CANCELLED")
        print("=" * 60)
        print(f"Reservation ID: {reservation.reservation_id}")
        print(f"User: {reservation.user_name}")
        print(f"Room: {reservation.room.name}")
        print("=" * 60)
        print()
        return True


class MultiNotifier(INotifier):
    """
    Composite notifier that can send via multiple channels
    Applies: Composite Pattern - treats multiple notifiers as a single one
    """
    
    def __init__(self):
        self._notifiers = []
    
    def add_notifier(self, notifier: INotifier):
        """Add a notifier to the list"""
        self._notifiers.append(notifier)
    
    def notify_reservation_confirmed(self, reservation: Reservation) -> bool:
        """Send confirmation via all notifiers"""
        results = [notifier.notify_reservation_confirmed(reservation) 
                  for notifier in self._notifiers]
        return all(results)
    
    def notify_reservation_cancelled(self, reservation: Reservation) -> bool:
        """Send cancellation via all notifiers"""
        results = [notifier.notify_reservation_cancelled(reservation) 
                  for notifier in self._notifiers]
        return all(results)