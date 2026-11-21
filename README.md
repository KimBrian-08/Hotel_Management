# Hotel Reservation & Management System

**OOP with Python Capstone Project — Project 6**
DATS 212: Object-Oriented Programming with Python · Kabarak University

A complete hotel management application built with Python and Object-Oriented Programming principles, featuring a Tkinter desktop GUI and JSON data persistence.
The system manages guests, staff, rooms, reservations, hotel services, payments,and billing — from booking to check-out.

---

## Student Information

| Name | Registration Number | GitHub Username |
| ---- | ------------------- | --------------- |
| Brian Kimtai| ****               |   KimBrian-08   |
| Stephen Kiprop | ****               |   kikes2026     |
| William Thotho | ****             | thothowilliam71-pixel           |

**Course:** OOP with Python
**Repository:** <https://github.com/KimBrian-08/Hotel_Management>

---

## Problem Statement

Hotels need a structured way to manage guests, rooms, reservations, payments, and additional services. Manual processes lead to double booking, poor room tracking,billing errors, and inefficient guest management. This project solves that problem with an object-oriented system where each hotel entity is modelled as a class with its own data, validation, and behaviour.

## Features

- **Guest & staff registration** with duplicate-ID protection and input validation
- **Room management** — three room types (Standard, Deluxe, Suite) with polymorphic pricing
- **Room search** by number, type, and availability
- **Reservations** with a full lifecycle: `PENDING → ACTIVE → COMPLETED` (or `CANCELLED`)
- **Double-booking prevention** — a room is locked the moment a reservation is created
- **Hotel services** (laundry, breakfast, etc.) added to reservations
- **Payments** — Cash, Card (Luhn + expiry + CVV validation), and Mobile Money (M-Pesa, etc.)
- **Partial payments** with dynamic balance tracking (`UNPAID → PARTIALLY_PAID → PAID`)
- **Final bills and payment receipts** (formatted, monospaced documents)
- **Guest history, payment history, and hotel summary reports** (revenue, outstanding balances)
- **JSON persistence** — save and reload the entire hotel state, including from the GUI
- **Tkinter desktop GUI** 

---

## OOP Concepts Applied

| Concept | Where it is demonstrated |
| ------- | ------------------------ |
| Classes & objects | `Guest`, `Staff`, `Room`, `Reservation`, `HotelService`, `Payment`, `Hotel` |
| Encapsulation | Private attributes (`_status`, `_payments`, …), `@property` getters/setters, read-only properties, collections exposed as tuples |
| Inheritance | `Person → Guest/Staff`, `Room → StandardRoom/DeluxeRoom/Suite`, `Payment → Cash/Card/Mobile` |
| Polymorphism | `calculate_cost(nights)` and `process_payment()` behave differently per subclass |
| Method overriding | `get_role()`, `get_description()`, `calculate_cost()`, `get_payment_method()`, `__str__()` |
| Abstraction | `Person`, `Room`, and `Payment` are ABCs with `@abstractmethod`s — they cannot be instantiated |
| Composition | A `Reservation` **has a** `Guest`, a `Room`, `HotelService` objects, and `Payment` objects; `Hotel` owns all collections |
| Class attributes & methods | ID counters (`RES-1001`, `SRV-101`, `PAY-5001`), `Guest.number_of_guests()` |
| Static methods | `Guest.validate_phone()`, `Room.validate_nights()`, card validators (Luhn, expiry, CVV) |
| Special methods | `__str__`, `__repr__`, `__len__` (nights), `__eq__`/`__hash__` (service de-duplication) |
| Custom exceptions | `HotelError` base + 11 specific subclasses (see below) |
| Template Method pattern | `Payment.get_receipt()` builds a shared skeleton; subclasses override `_additional_receipt_lines()` |

### Room pricing (polymorphism)

| Room type | Rule | Example: 2 nights @ base |
| --------- | ---- | ------------------------ |
| StandardRoom | `base × nights` | 5,000 → **10,000** |
| DeluxeRoom | `base × nights × 1.15` | 8,000 → **18,400** |
| Suite | `base × nights × 1.25` (+500/night with lounge access) | 15,000 → **38,500** |

---

## Class Structure

```text
Person (ABC)
├── Guest
└── Staff

Room (ABC)
├── StandardRoom
├── DeluxeRoom
└── Suite

Payment (ABC)
├── CashPayment
├── CardPayment
└── MobilePayment

HotelService

Reservation ── has a ── Guest, Room, [HotelService], [Payment]

Hotel (controller) ── owns ── Guests, Staff, Rooms, Services, Reservations

HotelGUI (Tkinter view) ── delegates everything to ── Hotel
```

The `Hotel` class is the central controller (Facade). The GUI contains no business logic — every button calls one controller method, which looks up entities and delegates to the domain objects, where all business rules are enforced.

---

## Project Structure

```text
Hotel_Management/
├── README.md
├── hotel_management.ipynb      # Full report + implementation + demonstration
└── data/
    └── hotel_data.json         # Sample persisted hotel state
```

## Requirements

- **Python 3.10+** (developed and tested on Python 3.13)
- **tkinter** — included with standard Python installers
- **Jupyter Notebook or JupyterLab** — `pip install notebook`

No third-party libraries are needed for the core system, GUI, or persistence.

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/KimBrian-08/Hotel_Management.git
cd Hotel_Management

# 2. (Optional) create a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate  

# 3. Install Jupyter and launch the notebook
pip install notebook
jupyter notebook hotel_management.ipynb
```

1. Run the notebook top to bottom (**Run All**) — this defines all classes, runs the
   demonstration workflow, the test suites, and saves/loads the JSON data.
2. To open the desktop GUI, set `LAUNCH_GUI = True` in the final cell and run it.
   While the GUI window is open the kernel is paused; close the window to continue.

> On startup the GUI offers to load `data/hotel_data.json` if it exists, so you can
> resume exactly where you left off.

## Using the GUI

| Tab | What you can do |
| --- | --------------- |
| **Dashboard** | Live KPI cards (rooms, availability, guests, revenue, outstanding) + full summary |
| **Rooms** | Add rooms, search/filter by number/type/availability; status colour-coding |
| **Guests & Staff** | Register guests and staff; view a guest's reservation history |
| **Services** | Create hotel services (laundry, breakfast, …) |
| **Reservations & Payments** | Book, add services, check in/out, cancel, pay (cash/card/mobile), view bills, receipts, and payment history |

**Typical workflow:** Register guest → Add room → Make reservation → Add services → Process payment(s) → Check in → Check out → Final bill → **Save Data**.

## Data Persistence

All state is stored in `data/hotel_data.json`:

- **Saving:** converter functions (`hotel_to_dict`, `room_to_dict`, …) serialize the
  object graph. Shared entities (guests, rooms, services) are referenced **by ID**;
  payments are **embedded** inside their reservation. Polymorphic types are preserved
  with a `"class"` tag, and dates use ISO format.
- **Loading:** objects are rebuilt in dependency order and re-linked through lookup
  maps. `Class.__new__()` restores objects **without re-running constructors**, so no
  new IDs are generated and rooms are not re-reserved. ID counters are then resynchronised
  so new objects never collide with loaded ones.
- **Security:** full card numbers and CVVs are **never written to disk** — only the
  last four digits and expiry date are stored.

## Testing

The notebook contains **17 executed checks** with visible outputs:

- **7 core tests** — guest registration, duplicate rejection, room search, valid
  reservation, unavailable room, invalid nights, duplicate reservation
- **5 payment tests** — insufficient cash, invalid card, unsupported method,
  overpayment, payment on a cancelled reservation
- **5 persistence tests** — guest, room, reservation totals, amount paid, and payment
  status survive a save/load round trip

Run the testing cells (or Run All) to reproduce every result.

## Exception Handling

All domain errors inherit from a single base, `HotelError`, so callers can catch one
umbrella type or handle specific cases:

```python
try:
    hotel.make_reservation("CU2026001", "301", 2)
except RoomUnavailableError as e:
    print("Room already booked:", e)
except HotelError as e:
    print("Hotel operation failed:", e)
```

Custom exceptions include `GuestNotFoundError`, `DuplicateGuestError`,
`RoomNotFoundError`, `RoomUnavailableError`, `InvalidNightsError`,
`DuplicateReservationError`, `ReservationNotFoundError`, `ServiceNotFoundError`,
`InvalidReservationStatusError`, `PaymentError`, and `ValidationError`.

## Known Limitations & Future Work

- JSON storage is single-file: no concurrent access or atomic writes yet
  (planned: temp-file + `os.replace`, or migration to SQLite).
- Availability is per-room, not per-date-range; a reserved room is blocked for the
  whole reservation regardless of dates.
- The `CLEANING` / `MAINTENANCE` room states and payment refunds are defined but not
  yet wired into workflows (housekeeping step after check-out is planned).
- No user authentication — intended as a single-operator front-desk tool.

## Acknowledgements

Course material: DATS 212 *Object-Oriented Programming with Python*, Kabarak
University (Week 6 capstone brief, Project 6). All guest/staff data in the demo is
fictional.

## License

This project is released under the MIT License for educational use.