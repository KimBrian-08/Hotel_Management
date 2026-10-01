"""
Hotel controller class.

This module demonstrates:
- Composition
- Encapsulation
- Exception handling
- Controller class design
"""

from .exceptions import (
    DuplicateGuestError,
    DuplicateReservationError,
    GuestNotFoundError,
    ReservationNotFoundError,
    RoomNotFoundError,
    ServiceNotFoundError,
)

from .people import Guest, Staff
from .rooms import Room, StandardRoom, DeluxeRoom, Suite
from .services import HotelService
from .reservation import Reservation


class Hotel:
    """
    Central controller class for the hotel system.

    Manages:
    - Guests
    - Staff
    - Rooms
    - Reservations
    - Hotel services
    """

    def __init__(self, name):
        self.name = name
        self._guests = []
        self._staff = []
        self._rooms = []
        self._reservations = []
        self._services = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Hotel name must be a non-empty string.")
        self._name = value.strip()

    @property
    def guests(self):
        return tuple(self._guests)

    @property
    def staff(self):
        return tuple(self._staff)

    @property
    def rooms(self):
        return tuple(self._rooms)

    @property
    def reservations(self):
        return tuple(self._reservations)

    @property
    def services(self):
        return tuple(self._services)

    def register_guest(self, name, id_number, phone, guest_type="Regular"):
        """Register a new guest."""
        for guest in self._guests:
            if guest.id_number == id_number:
                raise DuplicateGuestError(
                    f"Guest with ID {id_number} already exists."
                )

        guest = Guest(name, id_number, phone, guest_type)
        self._guests.append(guest)
        return guest

    def register_staff(self, name, id_number, role):
        """Register a new staff member."""
        for staff in self._staff:
            if staff.id_number == id_number:
                raise ValueError(f"Staff with ID {id_number} already exists.")

        staff = Staff(name, id_number, role)
        self._staff.append(staff)
        return staff

    def add_room(self, room_type, room_number, base_price):
        """Add a room to the hotel."""
        for room in self._rooms:
            if room.room_number == room_number:
                raise ValueError(f"Room {room_number} already exists.")

        if not isinstance(room_type, str) or not room_type.strip():
            raise ValueError("Room type must be a non-empty string.")

        room_type = room_type.strip().lower()

        if room_type == "standard":
            room = StandardRoom(room_number, base_price)
        elif room_type == "deluxe":
            room = DeluxeRoom(room_number, base_price)
        elif room_type == "suite":
            room = Suite(room_number, base_price)
        else:
            raise ValueError(
                "Invalid room type. Use 'standard', 'deluxe', or 'suite'."
            )

        self._rooms.append(room)
        return room

    def add_service(self, name, price):
        """Add a hotel service."""
        service = HotelService(name, price)
        self._services.append(service)
        return service

    def get_guest_by_id(self, id_number):
        """Retrieve a guest by ID."""
        id_number = str(id_number).strip()

        for guest in self._guests:
            if guest.id_number == id_number:
                return guest

        raise GuestNotFoundError(f"Guest with ID {id_number} was not found.")

    def get_room_by_number(self, room_number):
        """Retrieve a room by room number."""
        room_number = str(room_number).strip()

        for room in self._rooms:
            if room.room_number == room_number:
                return room

        raise RoomNotFoundError(f"Room {room_number} was not found.")

    def get_reservation_by_id(self, reservation_id):
        """Retrieve a reservation by reservation ID."""
        reservation_id = str(reservation_id).strip()

        for reservation in self._reservations:
            if reservation.reservation_id == reservation_id:
                return reservation

        raise ReservationNotFoundError(
            f"Reservation {reservation_id} was not found."
        )

    def get_service_by_id(self, service_id):
        """Retrieve a service by service ID."""
        service_id = str(service_id).strip()

        for service in self._services:
            if service.service_id == service_id:
                return service

        raise ServiceNotFoundError(f"Service {service_id} was not found.")

    def search_rooms(self, room_number=None, room_type=None, available_only=True):
        """
        Search rooms by room number, room type, and availability.

        This satisfies the requirement:
        - Search for rooms
        """
        results = self._rooms.copy()

        if room_number:
            room_number = str(room_number).strip()
            results = [
                room for room in results
                if room.room_number == room_number
            ]

        if room_type:
            if not isinstance(room_type, str) or not room_type.strip():
                raise ValueError("Room type must be a non-empty string.")

            room_type = room_type.strip().lower()

            if room_type == "standard":
                results = [
                    room for room in results
                    if isinstance(room, StandardRoom)
                ]
            elif room_type == "deluxe":
                results = [
                    room for room in results
                    if isinstance(room, DeluxeRoom)
                ]
            elif room_type == "suite":
                results = [
                    room for room in results
                    if isinstance(room, Suite)
                ]
            else:
                raise ValueError(
                    "Invalid room type. Use 'standard', 'deluxe', or 'suite'."
                )

        if available_only:
            results = [room for room in results if room.is_available()]

        return results

    def make_reservation(self, guest_id, room_number, nights):
        """Create a reservation."""
        guest = self.get_guest_by_id(guest_id)
        room = self.get_room_by_number(room_number)

        for reservation in self._reservations:
            if (
                reservation.guest.id_number == guest.id_number
                and reservation.room.room_number == room.room_number
                and reservation.status in [Reservation.PENDING, Reservation.ACTIVE]
            ):
                raise DuplicateReservationError(
                    f"Guest {guest.id_number} already has an active reservation "
                    f"for room {room.room_number}."
                )

        reservation = Reservation(guest, room, nights)
        self._reservations.append(reservation)

        return reservation

    def cancel_reservation(self, reservation_id):
        """Cancel a reservation."""
        reservation = self.get_reservation_by_id(reservation_id)
        reservation.cancel()
        return reservation

    def check_in(self, reservation_id):
        """Check a guest in."""
        reservation = self.get_reservation_by_id(reservation_id)
        reservation.check_in()
        return reservation

    def check_out(self, reservation_id):
        """Check a guest out."""
        reservation = self.get_reservation_by_id(reservation_id)
        reservation.check_out()
        return reservation

    def add_service_to_reservation(self, reservation_id, service_id):
        """Add a service to a reservation."""
        reservation = self.get_reservation_by_id(reservation_id)
        service = self.get_service_by_id(service_id)

        reservation.add_service(service)
        return reservation

    def calculate_accommodation_cost(self, reservation_id):
        """Calculate accommodation cost only."""
        reservation = self.get_reservation_by_id(reservation_id)
        return reservation.calculate_room_charge()

    def calculate_total_charge(self, reservation_id):
        """Calculate total bill including services."""
        reservation = self.get_reservation_by_id(reservation_id)
        return reservation.calculate_total_charge()

    def generate_final_bill(self, reservation_id):
        """Generate final bill summary."""
        reservation = self.get_reservation_by_id(reservation_id)
        return reservation.get_bill_summary()

    def display_available_rooms(self):
        """Display all available rooms."""
        available_rooms = [
            str(room) for room in self._rooms
            if room.is_available()
        ]

        if not available_rooms:
            return "No available rooms."

        return "\n".join(available_rooms)

    def display_hotel_summary(self):
        """Display hotel summary."""
        total_rooms = len(self._rooms)
        available_rooms = len([
            room for room in self._rooms
            if room.is_available()
        ])

        total_guests = len(self._guests)
        total_staff = len(self._staff)
        total_reservations = len(self._reservations)

        active_reservations = len([
            reservation for reservation in self._reservations
            if reservation.status in [Reservation.PENDING, Reservation.ACTIVE]
        ])

        completed_reservations = len([
            reservation for reservation in self._reservations
            if reservation.status == Reservation.COMPLETED
        ])

        cancelled_reservations = len([
            reservation for reservation in self._reservations
            if reservation.status == Reservation.CANCELLED
        ])

        lines = []
        lines.append("=" * 45)
        lines.append(f"HOTEL SUMMARY - {self.name}")
        lines.append("=" * 45)
        lines.append(f"Total Rooms: {total_rooms}")
        lines.append(f"Available Rooms: {available_rooms}")
        lines.append(f"Total Guests: {total_guests}")
        lines.append(f"Total Staff: {total_staff}")
        lines.append(f"Total Reservations: {total_reservations}")
        lines.append(f"Active/Pending Reservations: {active_reservations}")
        lines.append(f"Completed Reservations: {completed_reservations}")
        lines.append(f"Cancelled Reservations: {cancelled_reservations}")
        lines.append("=" * 45)

        return "\n".join(lines)

    def __str__(self):
        return (
            f"Hotel: {self.name} | Rooms: {len(self._rooms)} | "
            f"Guests: {len(self._guests)}"
        )