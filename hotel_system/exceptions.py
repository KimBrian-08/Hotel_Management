"""
Custom exceptions for the Hotel Reservation and Management System.

This module demonstrates exception handling and custom exception design.
"""


class HotelError(Exception):
    """Base exception for all hotel-related errors."""
    pass


class ValidationError(HotelError):
    """Raised when input data is invalid."""
    pass


class GuestNotFoundError(HotelError):
    """Raised when a guest cannot be found."""
    pass


class DuplicateGuestError(HotelError):
    """Raised when a guest already exists in the system."""
    pass


class RoomNotFoundError(HotelError):
    """Raised when a room cannot be found."""
    pass


class RoomUnavailableError(HotelError):
    """Raised when a room cannot be reserved."""
    pass


class InvalidNightsError(HotelError):
    """Raised when the number of nights is invalid."""
    pass


class DuplicateReservationError(HotelError):
    """Raised when a duplicate reservation is attempted."""
    pass


class ReservationNotFoundError(HotelError):
    """Raised when a reservation cannot be found."""
    pass


class ServiceNotFoundError(HotelError):
    """Raised when a hotel service cannot be found."""
    pass


class InvalidReservationStatusError(HotelError):
    """Raised when a reservation operation is not allowed due to its status."""
    pass


class PaymentError(HotelError):
    """Raised when a payment operation fails."""
    pass