"""
Reservation class.

This module demonstrates:
- Composition
- Encapsulation
- Exception handling
- Special methods
- Class methods
"""

from datetime import datetime

from .exceptions import InvalidReservationStatusError, RoomUnavailableError
from .people import Guest
from .rooms import Room
from .services import HotelService


class Reservation:
    """
    Represents a reservation made by a guest for a room.

    Demonstrates composition because a Reservation contains:
    - Guest object
    - Room object
    - HotelService objects
    """

    _next_reservation_id = 1000

    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

    def __init__(self, guest, room, nights, check_in_date=None):
        if not isinstance(guest, Guest):
            raise TypeError("guest must be an instance of Guest.")

        if not isinstance(room, Room):
            raise TypeError("room must be an instance of Room.")

        Room.validate_nights(nights)

        if not room.is_available():
            raise RoomUnavailableError(
                f"Room {room.room_number} is not available for reservation."
            )

        self._reservation_id = Reservation._generate_reservation_id()
        self._guest = guest
        self._room = room
        self.nights = nights
        self._check_in_date = check_in_date if check_in_date else datetime.now().date()
        self._status = Reservation.PENDING
        self._services = []
        self._created_on = datetime.now()

        self._room.make_reserved()

    @classmethod
    def _generate_reservation_id(cls):
        cls._next_reservation_id += 1
        return f"RES-{cls._next_reservation_id}"

    @property
    def reservation_id(self):
        return self._reservation_id

    @property
    def guest(self):
        return self._guest

    @property
    def room(self):
        return self._room

    @property
    def check_in_date(self):
        return self._check_in_date

    @property
    def status(self):
        return self._status

    @property
    def created_on(self):
        return self._created_on

    @property
    def services(self):
        """Return a tuple of services to prevent external modification."""
        return tuple(self._services)

    @property
    def nights(self):
        return self._nights

    @nights.setter
    def nights(self, value):
        Room.validate_nights(value)
        self._nights = value

    def add_service(self, service):
        """Add an additional hotel service to the reservation."""
        if not isinstance(service, HotelService):
            raise TypeError("service must be an instance of HotelService.")

        if self._status in [Reservation.CANCELLED, Reservation.COMPLETED]:
            raise InvalidReservationStatusError(
                "Services cannot be added to a cancelled or completed reservation."
            )

        if service in self._services:
            raise ValueError(
                f"Service {service.name} has already been added to this reservation."
            )

        self._services.append(service)

    def calculate_room_charge(self):
        """Calculate accommodation charge only."""
        return self._room.calculate_cost(self.nights)

    def calculate_service_charge(self):
        """Calculate total service charge."""
        total_service_charge = sum(service.price for service in self._services)
        return round(total_service_charge, 2)

    def calculate_total_charge(self):
        """Calculate total bill amount."""
        total = self.calculate_room_charge() + self.calculate_service_charge()
        return round(total, 2)

    def cancel(self):
        """Cancel the reservation."""
        if self._status == Reservation.CANCELLED:
            raise InvalidReservationStatusError(
                f"Reservation {self.reservation_id} is already cancelled."
            )

        if self._status == Reservation.COMPLETED:
            raise InvalidReservationStatusError(
                f"Reservation {self.reservation_id} is completed and cannot be cancelled."
            )

        self._status = Reservation.CANCELLED
        self._room.make_available()

    def check_in(self):
        """Check the guest into the reservation."""
        if self._status == Reservation.CANCELLED:
            raise InvalidReservationStatusError(
                f"Reservation {self.reservation_id} is cancelled and cannot check in."
            )

        if self._status == Reservation.COMPLETED:
            raise InvalidReservationStatusError(
                f"Reservation {self.reservation_id} is already completed."
            )

        self._room.make_occupied()
        self._status = Reservation.ACTIVE

    def check_out(self):
        """Check the guest out of the reservation."""
        if self._status != Reservation.ACTIVE:
            raise InvalidReservationStatusError(
                f"Reservation {self.reservation_id} must be active before check-out."
            )

        self._room.make_available()
        self._status = Reservation.COMPLETED

    def get_bill_summary(self):
        """Generate a formatted final bill summary."""
        lines = []

        lines.append("=" * 45)
        lines.append(f"FINAL BILL - {self.reservation_id}")
        lines.append("=" * 45)
        lines.append(f"Guest: {self.guest.name}")
        lines.append(f"Guest ID: {self.guest.id_number}")
        lines.append(f"Room: {self.room.room_number}")
        lines.append(f"Room Type: {self.room.get_description()}")
        lines.append(f"Nights: {self.nights}")
        lines.append(f"Room Charge: {self.calculate_room_charge():.2f}")

        if self._services:
            lines.append("Services:")
            for service in self._services:
                lines.append(f"  - {service.name}: {service.price:.2f}")
        else:
            lines.append("Services: None")

        lines.append(f"Service Charge: {self.calculate_service_charge():.2f}")
        lines.append("-" * 45)
        lines.append(f"Total Charge: {self.calculate_total_charge():.2f}")
        lines.append("=" * 45)

        return "\n".join(lines)

    def __len__(self):
        """Return the number of nights in the reservation."""
        return self.nights

    def __str__(self):
        return (
            f"{self.reservation_id} | {self.guest.name} | "
            f"Room {self.room.room_number} | {self.nights} nights | "
            f"{self.status} | Total: {self.calculate_total_charge():.2f}"
        )

    def __repr__(self):
        return (
            f"<Reservation(reservation_id='{self.reservation_id}', "
            f"guest='{self.guest.name}', room='{self.room.room_number}')>"
        )