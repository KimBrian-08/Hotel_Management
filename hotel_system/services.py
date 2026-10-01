"""
HotelService class.

This module demonstrates:
- Encapsulation
- Class attributes
- Class methods
- Special methods
"""


class HotelService:
    """
    Represents an additional hotel service such as laundry,
    breakfast, airport pickup, or room service.
    """

    _next_service_id = 100

    def __init__(self, name, price):
        self.service_id = HotelService._generate_service_id()
        self.name = name
        self.price = price

    @classmethod
    def _generate_service_id(cls):
        cls._next_service_id += 1
        return f"SRV-{cls._next_service_id}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Service name must be a non-empty string.")
        self._name = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Service price must be zero or greater.")
        self._price = float(value)

    def __str__(self):
        return f"{self.service_id}: {self.name} - {self.price:.2f}"

    def __repr__(self):
        return f"<HotelService(service_id='{self.service_id}', name='{self.name}')>"

    def __eq__(self, other):
        if not isinstance(other, HotelService):
            return NotImplemented
        return self.service_id == other.service_id

    def __hash__(self):
        return hash(self.service_id)