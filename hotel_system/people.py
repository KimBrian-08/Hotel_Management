"""
Person, Guest, and Staff classes.

This module demonstrates:
- Abstraction
- Inheritance
- Encapsulation
- Class attributes
- Class methods
- Static methods
- Special methods
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Person(ABC):
    """
    Abstract base class for all people in the hotel system.

    Demonstrates abstraction through the abstract method get_role().
    """

    def __init__(self, name, id_number):
        self.name = name
        self.id_number = id_number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = value.strip()

    @property
    def id_number(self):
        return self._id_number

    @id_number.setter
    def id_number(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("ID number must be a non-empty string.")
        self._id_number = value.strip()

    @abstractmethod
    def get_role(self):
        """Return the role of the person in the hotel system."""
        pass

    def get_details(self):
        """Return basic person details."""
        return f"{self.get_role()}: {self.name} (ID: {self.id_number})"

    def __str__(self):
        return self.get_details()

    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', id_number='{self.id_number}')>"


class Guest(Person):
    """
    Represents a hotel guest.

    Inherits from Person.
    """

    guest_count = 0

    def __init__(self, name, id_number, phone, guest_type="Regular"):
        super().__init__(name, id_number)
        self.phone = Guest.validate_phone(phone)
        self.guest_type = guest_type
        self.registered_on = datetime.now().date()
        self._loyalty_points = 0
        Guest.guest_count += 1

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = Guest.validate_phone(value)

    @property
    def guest_type(self):
        return self._guest_type

    @guest_type.setter
    def guest_type(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Guest type must be a non-empty string.")
        self._guest_type = value.strip()

    @property
    def loyalty_points(self):
        return self._loyalty_points

    def add_loyalty_points(self, points):
        """Add loyalty points to the guest account."""
        if not isinstance(points, int) or points < 0:
            raise ValueError("Loyalty points must be zero or a positive integer.")
        self._loyalty_points += points

    def get_role(self):
        return "Guest"

    @classmethod
    def number_of_guests(cls):
        """Return the total number of registered guests."""
        return cls.guest_count

    @staticmethod
    def validate_phone(phone):
        """Validate phone number format."""
        if not isinstance(phone, str):
            raise ValueError("Phone number must be a string.")

        phone = phone.strip()

        if len(phone) < 7:
            raise ValueError("Phone number is too short.")

        return phone

    def __str__(self):
        return (
            f"Guest: {self.name} | ID: {self.id_number} | "
            f"Phone: {self.phone} | Type: {self.guest_type}"
        )


class Staff(Person):
    """
    Represents hotel staff.

    Inherits from Person.
    """

    def __init__(self, name, id_number, role):
        super().__init__(name, id_number)
        self.role = role

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Staff role must be a non-empty string.")
        self._role = value.strip()

    def get_role(self):
        return f"Staff - {self.role}"

    def __str__(self):
        return f"Staff: {self.name} | ID: {self.id_number} | Role: {self.role}"