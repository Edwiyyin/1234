"""
Concrete Room Implementations - Demonstrates OCP and LSP

SOLID Principles:
- OCP: New room types can be added without modifying existing code
  Simply extend Room class and implement abstract methods
- LSP: All room types are substitutable for base Room class
  Any code working with Room works with Classroom, Laboratory, etc.
- SRP: Each class represents one specific room type with its equipment

Pattern: Strategy Pattern (different room types = different strategies)
"""
from typing import Dict
from models.room import Room


class Classroom(Room):
    """
    Standard classroom for teaching with basic educational equipment.
    
    Business Context: Used for lectures, workshops, training sessions.
    Equipment focuses on presentation and writing surfaces.
    """
    
    def __init__(self, room_id: str, name: str, capacity: int, 
                 has_projector: bool = True, whiteboard: bool = True):
        """
        Initialize classroom with educational equipment.
        
        Default values (has_projector=True) reflect standard classroom setup.
        Makes API easier to use - most classrooms have projectors.
        """
        super().__init__(room_id, name, capacity)  # Call parent constructor
        self._has_projector = has_projector
        self._whiteboard = whiteboard
    
    def get_equipment(self) -> Dict[str, any]:
        """
        Return classroom-specific equipment.
        
        LSP: Returns Dict[str, any] as promised by parent class.
        Implementation differs but interface stays same.
        """
        return {
            "projector": self._has_projector,
            "whiteboard": self._whiteboard,
            "desks": True  # All classrooms have desks
        }
    
    def get_room_type(self) -> str:
        """Identify as Classroom type for filtering/display"""
        return "Classroom"


class ConferenceRoom(Room):
    """
    Conference room with advanced audio/video equipment for meetings.
    
    Business Context: Executive meetings, client presentations, video calls.
    Equipment focuses on professional communication.
    """
    
    def __init__(self, room_id: str, name: str, capacity: int, 
                 video_conference: bool = True, sound_system: bool = True):
        """
        Initialize conference room with A/V equipment.
        
        Defaults reflect modern conference room expectations.
        Video conferencing is standard in 2025.
        """
        super().__init__(room_id, name, capacity)
        self._video_conference = video_conference
        self._sound_system = sound_system
    
    def get_equipment(self) -> Dict[str, any]:
        """
        Return conference-specific equipment.
        
        More equipment than classroom - reflects higher-end usage.
        """
        return {
            "video_conference": self._video_conference,
            "sound_system": self._sound_system,
            "projector": True,          # Standard in conference rooms
            "conference_table": True    # Differentiates from classroom
        }
    
    def get_room_type(self) -> str:
        """Identify as Conference Room for professional context"""
        return "Conference Room"


class Laboratory(Room):
    """
    Laboratory with specialized scientific equipment.
    
    Business Context: Science experiments, research, practical work.
    Equipment varies by lab type (Chemistry, Physics, Biology, etc.)
    """
    
    def __init__(self, room_id: str, name: str, capacity: int, 
                 lab_type: str = "General", safety_equipment: bool = True):
        """
        Initialize laboratory with type-specific equipment.
        
        lab_type: Allows specialization (Chemistry vs Physics)
        safety_equipment: Default True for regulatory compliance
        """
        super().__init__(room_id, name, capacity)
        self._lab_type = lab_type
        self._safety_equipment = safety_equipment
    
    def get_equipment(self) -> Dict[str, any]:
        """
        Return laboratory-specific equipment.
        
        Safety equipment is critical - different from other room types.
        Lab type allows customization without new classes (flexible).
        """
        return {
            "lab_type": self._lab_type,              # Specialization identifier
            "safety_equipment": self._safety_equipment,  # Safety first!
            "workbenches": True,                     # Lab-specific furniture
            "storage": True                          # Chemical/equipment storage
        }
    
    def get_room_type(self) -> str:
        """
        Return lab type with specialization.
        
        Shows polymorphism: Different data but same method signature.
        Output: "Laboratory (Chemistry)" vs "Laboratory (Physics)"
        """
        return f"Laboratory ({self._lab_type})"


class ComputerLab(Room):
    """
    Computer lab with workstations for programming/design work.
    
    Business Context: Software development, design courses, research.
    Equipment focuses on computing infrastructure.
    """
    
    def __init__(self, room_id: str, name: str, capacity: int, 
                 num_computers: int = 0, has_printer: bool = True):
        """
        Initialize computer lab with computing equipment.
        
        num_computers: Defaults to capacity if not specified
        Assumes 1 computer per person for accurate resource planning.
        """
        super().__init__(room_id, name, capacity)
        # Smart default: If not specified, assume 1 computer per seat
        self._num_computers = num_computers if num_computers > 0 else capacity
        self._has_printer = has_printer
    
    def get_equipment(self) -> Dict[str, any]:
        """
        Return computer lab-specific equipment.
        
        Focuses on digital infrastructure rather than physical presentation.
        Number of computers is key metric for availability.
        """
        return {
            "computers": self._num_computers,  # Critical resource count
            "printer": self._has_printer,      # Common peripheral
            "network": True                    # All computer labs need network
        }
    
    def get_room_type(self) -> str:
        """Identify as Computer Lab for technical context"""
        return "Computer Lab"