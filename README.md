# 🏢 Room Reservation System

A Python room booking system demonstrating SOLID principles with a beautiful CLI interface.

---

## ⚡ Quick Start

### 1. Install Python
Make sure you have Python 3.7 or higher installed:
```bash
python3 --version
```

If not installed, download from: https://www.python.org/downloads/

### 2. Install Dependencies
```bash
pip install rich pytest
```

### 3. Run the Program
```bash
python3 beautiful_cli.py
```

That's it! The interactive menu will guide you through everything.

---

## 🎯 What Can You Do?

Once you run `beautiful_cli.py`, you can:

1. **📅 Make a Reservation** - Book a room with date/time
2. **🔍 View All Reservations** - See what's booked
3. **🏢 View Available Rooms** - Browse all rooms (8 types!)
4. **❌ Cancel a Reservation** - Cancel any booking
5. **📊 View Statistics** - See system stats
6. **ℹ️ About SOLID** - Learn about design principles

---

## ✨ Project Highlights

### Core Features
- ✅ **4 Room Types**: Classroom, Conference, Laboratory, Computer Lab
- ✅ **Smart Conflict Detection**: Can't double-book the same room
- ✅ **Persistent Storage**: Saves to `reservations.json` file
- ✅ **Beautiful Interface**: Colorful tables and menus (using Rich library)
- ✅ **Input Validation**: Won't let you book in the past or outside business hours

### Advanced Features
- 🎨 **Beautiful CLI**: Professional interface with colors and tables
- 🏭 **Factory Pattern**: Easy object creation
- 👁️ **Observer Pattern**: Real-time statistics tracking
- ✅ **Business Rules**: 7AM-10PM hours, 1-8 hour duration limits
- 🧪 **20+ Tests**: Run `pytest tests.py` to verify everything works

---

## 📂 Project Structure

```
room_reservation_system/
├── beautiful_cli.py          ⭐ RUN THIS - Interactive menu
├── main_advanced.py          📊 Demo with all patterns
├── tests.py                  🧪 Unit tests
│
├── models/                   📦 Room & Reservation classes
├── repositories/             💾 Storage (memory & file)
├── notifications/            📧 Email, SMS, Console alerts
└── services/                 ⚙️ Business logic & validation
```

---

## 🚀 Usage Examples

### Interactive Mode (Recommended)
```bash
python3 beautiful_cli.py
```
Follow the menu to make reservations!

### Run All Demos
```bash
python3 main_advanced.py
```
Shows off all features with example data.

### Run Tests
```bash
pytest tests.py -v
```
Verifies all 20+ tests pass.

---

## 🐛 Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'rich'`
**Solution:**
```bash
pip install rich
```

### Problem: `python3: command not found`
**Solution:** 
- **Windows**: Use `python` instead of `python3`
- **Mac/Linux**: Make sure Python 3 is installed

### Problem: Can't make reservation in the past
**Solution:** This is intentional! The system validates dates. Use today or future dates.

### Problem: Business hours error (before 7AM or after 10PM)
**Solution:** This is a business rule. Reservations must be between 7:00 AM - 10:00 PM.

### Problem: `reservations.json` file not found
**Solution:** The file is created automatically on first reservation. If missing, just make a new booking!

### Problem: Room not available / conflict detected
**Solution:** Someone already booked that room at that time. Try a different time or room.

---

## 💡 Quick Tips

- **Default file**: Reservations save to `reservations.json` automatically
- **Business hours**: 7:00 AM - 10:00 PM only
- **Max duration**: 8 hours per reservation
- **Room IDs**: CL-101, CF-201, LAB-301, etc. (shown in room list)
- **Cancellation**: Use the reservation ID (e.g., RES-ABC12345)

---

## 🎓 SOLID Principles Demo

This project demonstrates all 5 SOLID principles:

| Principle | Example in Code |
|-----------|----------------|
| **SRP** | Each class has ONE job (Room manages rooms, Service manages reservations) |
| **OCP** | Add new room types without changing existing code |
| **LSP** | Any Room type works with ReservationService |
| **ISP** | Small interfaces (INotifier has only 2 methods) |
| **DIP** | Service depends on interfaces, not concrete classes |

See `TP1_SOLID_Principles_Documentation.pdf` for detailed explanations.

---

## 📄 Documentation

- **README.md** (this file) - Quick start guide
- **UML_DIAGRAMS.md** - Architecture diagrams
- **TP1_SOLID_Principles_Documentation.pdf** - Full SOLID explanations (17 pages)
- Inline code comments - Every class documented

---

## 📊 Sample Session

```bash
$ python3 beautiful_cli.py

🏢 ROOM RESERVATION SYSTEM
Advanced OOP Design with SOLID Principles

[Main Menu appears]
Select an option: 1

📅 Make a Reservation
[Shows 8 available rooms in a table]

Enter Room ID: CL-101
Enter your name: Alice
Date (YYYY-MM-DD): 2025-12-20
Start time (HH:MM): 14:00
Duration (hours): 2
Purpose (optional): Python Workshop

✓ Reservation created successfully!
Reservation ID: RES-A1B2C3D4
Time: 2025-12-20 14:00 - 16:00
```

---

## 🏆 Features Count

- **25 classes** organized across 4 layers
- **6+ design patterns** (Repository, Factory, Observer, Strategy, DI, Composite)
- **20+ unit tests** with pytest
- **4 room types** with unique equipment
- **2 storage options** (memory & file)
- **4 notification channels** (Console, Email, SMS, Multi)

