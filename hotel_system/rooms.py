"""
Room classes.

This module demonstrates:
- Abstraction
- Inheritance
- Polymorphism
- Method overriding
- Encapsulation
- Static methods
- Special methods
"""

from abc import ABC, abstractmethod
from .exceptions import RoomUnavailableError, InvalidNightsError


class Room(ABC):
    """
    Abstract base class for all hotel rooms.

    Child classes must implement:
    - get_description()
    - calculate_cost(nights)
    """

    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    OCCUPIED = "OCCUPIED"
    CLEANING = "CLEANING"
    MAINTENANCE = "MAINTENANCE"

    def __init__(self, room_number, base_price):
        self.room_number = room_number
        self.base_price = base_price
        self._status = Room.AVAILABLE

    @property
    def room_number(self):
        return self._room_number

    @room_number.setter
    def room_number(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Room number must be a non-empty string.")
        self._room_number = value.strip()

    @property
    def base_price(self):
        return self._base_price

    @base_price.setter
    def base_price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Base price must be greater than zero.")
        self._base_price = float(value)

    @property
    def status(self):
        return self._status

    def is_available(self):
        """Check whether the room is available for booking."""
        return self._status == Room.AVAILABLE

    def make_reserved(self):
        """Reserve the room."""
        if not self.is_available():
            raise RoomUnavailableError(
                f"Room {self.room_number} is not available for reservation."
            )
        self._status = Room.RESERVED

    def make_occupied(self):
        """Mark the room as occupied."""
        if self._status != Room.RESERVED:
            raise RoomUnavailableError(
                f"Room {self.room_number} must be reserved before check-in."
            )
        self._status = Room.OCCUPIED

    def make_cleaning(self):
        """Mark the room as cleaning."""
        self._status = Room.CLEANING

    def make_available(self):
        """Mark the room as available."""
        self._status = Room.AVAILABLE

    @staticmethod
    def validate_nights(nights):
        """Validate number of nights."""
        if isinstance(nights, bool) or not isinstance(nights, int):
            raise InvalidNightsError("Number of nights must be an integer.")

        if nights <= 0 or nights > 365:
            raise InvalidNightsError(
                "Number of nights must be a positive integer not greater than 365."
            )

        return nights

    @abstractmethod
    def get_description(self):
        """Return a description of the room."""
        pass

    @abstractmethod
    def calculate_cost(self, nights):
        """Calculate the accommodation cost for the room."""
        pass

    def __str__(self):
        return (
            f"Room {self.room_number} | Status: {self.status} | "
            f"Base Price: {self.base_price:.2f}"
        )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(room_number='{self.room_number}', "
            f"status='{self.status}')>"
        )


class StandardRoom(Room):
    """
    Represents a standard hotel room.
    """

    def __init__(self, room_number, base_price, has_tv=True):
        super().__init__(room_number, base_price)
        self.has_tv = has_tv

    def get_description(self):
        tv_info = "with TV" if self.has_tv else "without TV"
        return f"Standard Room {self.room_number} {tv_info}"

    def calculate_cost(self, nights):
        Room.validate_nights(nights)
        return round(self.base_price * nights, 2)


class DeluxeRoom(Room):
    """
    Represents a deluxe hotel room.
    """

    def __init__(self, room_number, base_price, includes_breakfast=True):
        super().__init__(room_number, base_price)
        self.includes_breakfast = includes_breakfast

    def get_description(self):
        breakfast_info = "with breakfast" if self.includes_breakfast else "without breakfast"
        return f"Deluxe Room {self.room_number} {breakfast_info}"

    def calculate_cost(self, nights):
        Room.validate_nights(nights)
        return round(self.base_price * nights * 1.15, 2)


class Suite(Room):
    """
    Represents a luxury hotel suite.
    """

    def __init__(self, room_number, base_price, lounge_access=True):
        super().__init__(room_number, base_price)
        self.lounge_access = lounge_access

    def get_description(self):
        lounge_info = "with lounge access" if self.lounge_access else "without lounge access"
        return f"Executive Suite {self.room_number} {lounge_info}"

    def calculate_cost(self, nights):
        Room.validate_nights(nights)

        cost = self.base_price * nights * 1.25

        if self.lounge_access:
            cost += 500 * nights

        return round(cost, 2)