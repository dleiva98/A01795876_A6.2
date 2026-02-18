"""Reservation management module for the reservation system."""
import json
import os

from customer import Customer
from hotel import Hotel


class Reservation:
    """Reservation linking a customer to a hotel."""

    DATA_FILE = "reservations.json"

    def __init__(
        self, reservation_id, customer_id, hotel_id
    ):
        """Initialize a Reservation instance.

        Args:
            reservation_id: Unique reservation identifier.
            customer_id: Associated customer identifier.
            hotel_id: Associated hotel identifier.
        """
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Convert reservation instance to dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Reservation from dictionary.

        Args:
            data: Dictionary with reservation attributes.

        Returns:
            Reservation instance or None if invalid.
        """
        try:
            return cls(
                data["reservation_id"],
                data["customer_id"],
                data["hotel_id"],
            )
        except (KeyError, TypeError) as err:
            print(
                "Error creating reservation "
                f"from data: {err}"
            )
            return None

    @staticmethod
    def _load_data(file_path=None):
        """Load reservations from JSON file.

        Args:
            file_path: Optional custom file path.

        Returns:
            Dict of reservation_id to Reservation.
        """
        path = file_path or Reservation.DATA_FILE
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
            reservations = {}
            for key, val in raw.items():
                res = Reservation.from_dict(val)
                if res:
                    reservations[key] = res
            return reservations
        except (json.JSONDecodeError, ValueError) as err:
            print(
                f"Error loading reservations file: {err}"
            )
            return {}

    @staticmethod
    def _save_data(reservations, file_path=None):
        """Save reservations to JSON file.

        Args:
            reservations: Dict of id to Reservation.
            file_path: Optional custom file path.
        """
        path = file_path or Reservation.DATA_FILE
        data = {k: r.to_dict() for k, r in reservations.items()}
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

    @classmethod
    def create_reservation(
        cls, reservation_id, customer_id, hotel_id,
        file_path=None, hotel_file=None,
        customer_file=None
    ):
        """Create a new reservation.

        Verifies that customer and hotel exist,
        and that the hotel has available rooms.

        Args:
            reservation_id: Unique identifier.
            customer_id: Customer making the reservation.
            hotel_id: Hotel being reserved.
            file_path: Reservations data file path.
            hotel_file: Hotels data file path.
            customer_file: Customers data file path.

        Returns:
            Reservation instance or None on failure.
        """
        if (
            not isinstance(reservation_id, str)
            or not reservation_id.strip()
        ):
            print(
                "Error: reservation_id must be "
                "a non-empty string"
            )
            return None
        if (
            not isinstance(customer_id, str)
            or not customer_id.strip()
        ):
            print(
                "Error: customer_id must be "
                "a non-empty string"
            )
            return None
        if (
            not isinstance(hotel_id, str)
            or not hotel_id.strip()
        ):
            print(
                "Error: hotel_id must be "
                "a non-empty string"
            )
            return None

        customers = Customer._load_data(customer_file)
        if customer_id not in customers:
            print(
                f"Error: Customer '{customer_id}' "
                "not found"
            )
            return None

        hotels = Hotel._load_data(hotel_file)
        if hotel_id not in hotels:
            print(
                f"Error: Hotel '{hotel_id}' not found"
            )
            return None

        reservations = cls._load_data(file_path)
        if reservation_id in reservations:
            print(
                f"Error: Reservation "
                f"'{reservation_id}' already exists"
            )
            return None

        if not Hotel.reserve_room(hotel_id, hotel_file):
            return None

        reservation = cls(
            reservation_id, customer_id, hotel_id
        )
        reservations[reservation_id] = reservation
        cls._save_data(reservations, file_path)
        return reservation

    @classmethod
    def cancel_reservation(
        cls, reservation_id,
        file_path=None, hotel_file=None
    ):
        """Cancel an existing reservation.

        Frees the room in the associated hotel.

        Args:
            reservation_id: Reservation to cancel.
            file_path: Reservations data file path.
            hotel_file: Hotels data file path.

        Returns:
            True if cancelled, False otherwise.
        """
        reservations = cls._load_data(file_path)
        if reservation_id not in reservations:
            print(
                f"Error: Reservation "
                f"'{reservation_id}' not found"
            )
            return False
        reservation = reservations[reservation_id]
        Hotel.cancel_room_reservation(
            reservation.hotel_id, hotel_file
        )
        del reservations[reservation_id]
        cls._save_data(reservations, file_path)
        return True
