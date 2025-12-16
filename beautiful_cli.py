"""
Beautiful Command-Line Interface using Rich library
Demonstrates professional CLI design with colors, tables, and formatting
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich import box
from rich.layout import Layout
from rich.live import Live
from datetime import datetime, timedelta
from typing import List
from models.reservation import Reservation
from models.room import Room
from services.reservation_service import ReservationService
from services.factory_pattern import RoomFactory, ServiceFactory


class BeautifulCLI:
    """
    Beautiful command-line interface for room reservation system
    Demonstrates: Professional user interface design
    """
    
    def __init__(self):
        self.console = Console()
        self.service = ServiceFactory.create_reservation_service(
            repository_type='file',
            notifier_type='multi',
            filepath='reservations.json'
        )
        self.rooms = self._create_sample_rooms()
    
    def _create_sample_rooms(self) -> List[Room]:
        """Create sample rooms for the system"""
        return [
            RoomFactory.create_room('classroom', 'CL-101', 'Python Programming Lab', 30),
            RoomFactory.create_room('classroom', 'CL-102', 'Java Development Lab', 28),
            RoomFactory.create_room('conference', 'CF-201', 'Executive Board Room', 15),
            RoomFactory.create_room('conference', 'CF-202', 'Meeting Room A', 10),
            RoomFactory.create_room('laboratory', 'LAB-301', 'Chemistry Lab', 25, lab_type='Chemistry'),
            RoomFactory.create_room('laboratory', 'LAB-302', 'Physics Lab', 20, lab_type='Physics'),
            RoomFactory.create_room('computer_lab', 'CL-401', 'AI Research Lab', 35, num_computers=35),
            RoomFactory.create_room('computer_lab', 'CL-402', 'Software Engineering Lab', 32, num_computers=32),
        ]
    
    def show_welcome(self):
        """Display welcome screen"""
        self.console.clear()
        
        welcome_text = """
[bold cyan]🏢 ROOM RESERVATION SYSTEM[/bold cyan]
[yellow]Advanced OOP Design with SOLID Principles[/yellow]

[green]✓[/green] Multiple Room Types
[green]✓[/green] Smart Conflict Detection
[green]✓[/green] Real-time Notifications
[green]✓[/green] Persistent Storage
[green]✓[/green] Advanced Validation
[green]✓[/green] Beautiful Interface
        """
        
        panel = Panel(
            welcome_text,
            title="[bold magenta]Welcome![/bold magenta]",
            border_style="cyan",
            box=box.DOUBLE
        )
        
        self.console.print(panel)
        self.console.print()
    
    def show_main_menu(self):
        """Display main menu"""
        table = Table(title="[bold cyan]Main Menu[/bold cyan]", box=box.ROUNDED)
        table.add_column("Option", style="cyan", justify="center")
        table.add_column("Action", style="white")
        
        table.add_row("1", "📅 Make a Reservation")
        table.add_row("2", "🔍 View All Reservations")
        table.add_row("3", "🏢 View Available Rooms")
        table.add_row("4", "❌ Cancel a Reservation")
        table.add_row("5", "📊 View Statistics")
        table.add_row("6", "ℹ️  About SOLID Principles")
        table.add_row("0", "🚪 Exit")
        
        self.console.print(table)
        self.console.print()
    
    def show_rooms(self):
        """Display all available rooms in a beautiful table"""
        table = Table(title="[bold cyan]Available Rooms[/bold cyan]", box=box.ROUNDED)
        
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Name", style="yellow")
        table.add_column("Type", style="magenta")
        table.add_column("Capacity", style="green", justify="center")
        table.add_column("Equipment", style="white")
        
        for room in self.rooms:
            equipment = ", ".join([f"{k}: {v}" for k, v in room.get_equipment().items()][:3])
            table.add_row(
                room.room_id,
                room.name,
                room.get_room_type(),
                str(room.capacity),
                equipment
            )
        
        self.console.print(table)
        self.console.print()
    
    def show_reservations(self):
        """Display all reservations"""
        reservations = self.service.get_all_reservations()
        
        if not reservations:
            self.console.print("[yellow]No reservations found.[/yellow]")
            return
        
        table = Table(title=f"[bold cyan]All Reservations ({len(reservations)})[/bold cyan]", box=box.ROUNDED)
        
        table.add_column("ID", style="cyan")
        table.add_column("User", style="yellow")
        table.add_column("Room", style="magenta")
        table.add_column("Date", style="green")
        table.add_column("Time", style="white")
        table.add_column("Status", style="bold")
        
        for res in reservations:
            status_color = "green" if res.status == "CONFIRMED" else "red"
            table.add_row(
                res.reservation_id,
                res.user_name,
                res.room.name,
                res.start_time.strftime("%Y-%m-%d"),
                f"{res.start_time.strftime('%H:%M')}-{res.end_time.strftime('%H:%M')}",
                f"[{status_color}]{res.status}[/{status_color}]"
            )
        
        self.console.print(table)
        self.console.print()
    
    def make_reservation(self):
        """Interactive reservation creation with full error handling"""
        self.console.print("[bold cyan]📅 Make a Reservation[/bold cyan]\n")
        
        try:
            # Show rooms
            self.show_rooms()
            
            # Get room selection with validation
            while True:
                room_id = Prompt.ask("Enter Room ID").strip().upper()
                room = next((r for r in self.rooms if r.room_id == room_id), None)
                
                if room:
                    break
                else:
                    self.console.print("[red]❌ Invalid room ID. Please try again.[/red]")
            
            # Get user name with validation
            while True:
                user_name = Prompt.ask("Enter your name").strip()
                if len(user_name) >= 2:
                    break
                else:
                    self.console.print("[red]❌ Name must be at least 2 characters[/red]")
            
            # Get date with validation
            self.console.print("\n[yellow]Enter reservation date and time:[/yellow]")
            while True:
                date_str = Prompt.ask("Date (YYYY-MM-DD)", default=datetime.now().strftime("%Y-%m-%d"))
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    if date_obj.date() < datetime.now().date():
                        self.console.print("[red]❌ Cannot book in the past. Please enter a future date.[/red]")
                        continue
                    break
                except ValueError:
                    self.console.print("[red]❌ Invalid date format. Use YYYY-MM-DD (e.g., 2025-12-25)[/red]")
            
            # Get start time with validation
            while True:
                start_time_str = Prompt.ask("Start time (HH:MM)", default="09:00")
                try:
                    start_time_obj = datetime.strptime(start_time_str, "%H:%M").time()
                    # Check business hours (7:00 - 22:00)
                    if start_time_obj < datetime.strptime("07:00", "%H:%M").time():
                        self.console.print("[red]❌ Too early. Business hours start at 07:00[/red]")
                        continue
                    if start_time_obj > datetime.strptime("22:00", "%H:%M").time():
                        self.console.print("[red]❌ Too late. Business hours end at 22:00[/red]")
                        continue
                    break
                except ValueError:
                    self.console.print("[red]❌ Invalid time format. Use HH:MM (e.g., 09:00)[/red]")
            
            # Get duration with validation
            while True:
                duration_str = Prompt.ask("Duration (hours)", default="2")
                try:
                    duration = int(duration_str)
                    if duration < 1:
                        self.console.print("[red]❌ Duration must be at least 1 hour[/red]")
                        continue
                    if duration > 8:
                        self.console.print("[red]❌ Duration cannot exceed 8 hours[/red]")
                        continue
                    break
                except ValueError:
                    self.console.print("[red]❌ Duration must be a number (e.g., 2)[/red]")
            
            # Calculate end time and validate business hours
            start_datetime = datetime.combine(date_obj.date(), start_time_obj)
            end_datetime = start_datetime + timedelta(hours=duration)
            
            if end_datetime.time() > datetime.strptime("22:00", "%H:%M").time():
                self.console.print(f"[red]❌ Reservation would end at {end_datetime.strftime('%H:%M')}, past business hours (22:00)[/red]")
                return
            
            # Get purpose
            purpose = Prompt.ask("Purpose (optional)", default="").strip()
            
            # Create reservation with progress indicator
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("[cyan]Creating reservation...", total=None)
                
                reservation = self.service.create_reservation(
                    room=room,
                    user_name=user_name,
                    start_time=start_datetime,
                    end_time=end_datetime,
                    purpose=purpose
                )
                
                progress.update(task, completed=True)
            
            if reservation:
                self.console.print(f"\n[green]✓ Reservation created successfully![/green]")
                self.console.print(f"[cyan]Reservation ID: {reservation.reservation_id}[/cyan]")
                self.console.print(f"[cyan]Time: {start_datetime.strftime('%Y-%m-%d %H:%M')} - {end_datetime.strftime('%H:%M')}[/cyan]")
            else:
                self.console.print("\n[red]❌ Failed to create reservation (room may be unavailable)[/red]")
                
        except KeyboardInterrupt:
            self.console.print("\n[yellow]⚠️  Reservation cancelled by user[/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]❌ Unexpected error: {str(e)}[/red]")
            self.console.print("[yellow]Please try again or contact support[/yellow]")
    
    def cancel_reservation(self):
        """Cancel a reservation with full error handling"""
        self.console.print("[bold cyan]❌ Cancel a Reservation[/bold cyan]\n")
        
        try:
            # Show current reservations
            reservations = self.service.get_all_reservations()
            
            if not reservations:
                self.console.print("[yellow]No reservations found to cancel.[/yellow]")
                return
            
            self.show_reservations()
            
            # Get reservation ID with validation
            while True:
                reservation_id = Prompt.ask("Enter Reservation ID to cancel").strip().upper()
                
                # Check if reservation exists
                reservation = self.service.get_reservation(reservation_id)
                if reservation:
                    if reservation.status == "CANCELLED":
                        self.console.print(f"[yellow]⚠️  Reservation {reservation_id} is already cancelled[/yellow]")
                        if not Confirm.ask("Choose a different reservation?"):
                            return
                        continue
                    break
                else:
                    self.console.print(f"[red]❌ Reservation {reservation_id} not found[/red]")
                    if not Confirm.ask("Try again?"):
                        return
            
            # Confirm cancellation
            self.console.print(f"\n[yellow]About to cancel:[/yellow]")
            self.console.print(f"  ID: {reservation.reservation_id}")
            self.console.print(f"  User: {reservation.user_name}")
            self.console.print(f"  Room: {reservation.room.name}")
            self.console.print(f"  Time: {reservation.start_time.strftime('%Y-%m-%d %H:%M')}\n")
            
            if Confirm.ask(f"[bold red]Are you sure you want to cancel this reservation?[/bold red]"):
                success = self.service.cancel_reservation(reservation_id)
                
                if success:
                    self.console.print(f"\n[green]✓ Reservation {reservation_id} cancelled successfully[/green]")
                else:
                    self.console.print(f"\n[red]❌ Failed to cancel reservation[/red]")
            else:
                self.console.print("[yellow]Cancellation aborted[/yellow]")
                
        except KeyboardInterrupt:
            self.console.print("\n[yellow]⚠️  Operation cancelled by user[/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]❌ Unexpected error: {str(e)}[/red]")
    
    def show_statistics(self):
        """Show system statistics"""
        reservations = self.service.get_all_reservations()
        confirmed = sum(1 for r in reservations if r.status == "CONFIRMED")
        cancelled = sum(1 for r in reservations if r.status == "CANCELLED")
        
        stats_table = Table(title="[bold cyan]System Statistics[/bold cyan]", box=box.ROUNDED)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green", justify="right")
        
        stats_table.add_row("Total Reservations", str(len(reservations)))
        stats_table.add_row("Confirmed", str(confirmed))
        stats_table.add_row("Cancelled", str(cancelled))
        stats_table.add_row("Available Rooms", str(len(self.rooms)))
        stats_table.add_row("Total Capacity", str(sum(r.capacity for r in self.rooms)))
        
        self.console.print(stats_table)
        self.console.print()
    
    def show_solid_principles(self):
        """Show SOLID principles information"""
        principles = [
            ("SRP", "Single Responsibility", "Each class has one reason to change"),
            ("OCP", "Open/Closed", "Open for extension, closed for modification"),
            ("LSP", "Liskov Substitution", "Subtypes must be substitutable for base types"),
            ("ISP", "Interface Segregation", "Many specific interfaces over one general"),
            ("DIP", "Dependency Inversion", "Depend on abstractions, not concretions")
        ]
        
        table = Table(title="[bold cyan]SOLID Principles Applied[/bold cyan]", box=box.DOUBLE)
        table.add_column("Acronym", style="cyan bold", justify="center")
        table.add_column("Principle", style="yellow")
        table.add_column("Description", style="white")
        
        for acronym, name, desc in principles:
            table.add_row(acronym, name, desc)
        
        self.console.print(table)
        self.console.print()
    
    def run(self):
        """Run the main application loop with complete error handling"""
        try:
            self.show_welcome()
            
            while True:
                try:
                    self.show_main_menu()
                    choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4", "5", "6"])
                    
                    self.console.print()
                    
                    if choice == "0":
                        self.console.print("[cyan]Thank you for using the Room Reservation System![/cyan]")
                        break
                    elif choice == "1":
                        self.make_reservation()
                    elif choice == "2":
                        self.show_reservations()
                    elif choice == "3":
                        self.show_rooms()
                    elif choice == "4":
                        self.cancel_reservation()
                    elif choice == "5":
                        self.show_statistics()
                    elif choice == "6":
                        self.show_solid_principles()
                    
                    self.console.print()
                    Prompt.ask("Press Enter to continue")
                    self.console.clear()
                    
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]⚠️  Returning to main menu...[/yellow]")
                    self.console.print()
                    Prompt.ask("Press Enter to continue")
                    self.console.clear()
                    continue
                    
        except KeyboardInterrupt:
            self.console.print("\n\n[cyan]Thank you for using the Room Reservation System![/cyan]")
        except Exception as e:
            self.console.print(f"\n[red]❌ Critical error: {str(e)}[/red]")
            self.console.print("[yellow]Please restart the application[/yellow]")


if __name__ == "__main__":
    cli = BeautifulCLI()
    cli.run()