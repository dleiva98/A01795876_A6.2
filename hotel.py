"""Hotel management module for the reservation system."""
import json
import os


class Hotel:
    """Hotel entity with room management capabilities."""

    DATA_FILE = "hotels.json"

    def __init__(self, hotel_id, name, location, total_rooms):
        """Initialize a Hotel instance.

        Args:
            hotel_id: Unique identifier for the hotel.
            name: Name of the hotel.
            location: Location of the hotel.
            total_rooms: Total number of rooms.
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.rooms_available = total_rooms

    def to_dict(self):
        """Convert hotel instance to dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "rooms_available": self.rooms_available,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Hotel from dictionary.

        Args:
            data: Dictionary with hotel attributes.

        Returns:
            Hotel instance or None if data is invalid.
        """
        try:
            hotel = cls(
                data["hotel_id"],
                data["name"],
                data["location"],
                data["total_rooms"],
            )
            hotel.rooms_available = data.get(
                "rooms_available", data["total_rooms"]
            )
            return hotel
        except (KeyError, TypeError) as err:
            print(f"Error creating hotel from data: {err}")
            return None

    @staticmethod
    def load_data(file_path=None):
        """Load hotels from JSON file.

        Args:
            file_path: Optional custom file path.

        Returns:
            Dictionary of hotel_id to Hotel instances.
        """
        path = file_path or Hotel.DATA_FILE
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as fhandle:
                raw = json.load(fhandle)
            hotels = {}
            for key, val in raw.items():
                hotel = Hotel.from_dict(val)
                if hotel:
                    hotels[key] = hotel
            return hotels
        except (json.JSONDecodeError, ValueError) as err:
            print(f"Error loading hotels file: {err}")
            return {}

    @staticmethod
    def save_data(hotels, file_path=None):
        """Save hotels to JSON file.

        Args:
            hotels: Dictionary of hotel_id to Hotel instances.
            file_path: Optional custom file path.
        """
        path = file_path or Hotel.DATA_FILE
        data = {k: h.to_dict() for k, h in hotels.items()}
        with open(path, "w", encoding="utf-8") as fhandle:
            json.dump(data, fhandle, indent=2)

    @classmethod
    def create_hotel(
        cls, hotel_id, name, location, total_rooms,
        file_path=None
    ):
        """Create and persist a new hotel.

        Args:
            hotel_id: Unique identifier.
            name: Hotel name.
            location: Hotel location.
            total_rooms: Number of rooms (positive integer).
            file_path: Optional custom file path.

        Returns:
            Hotel instance or None on failure.
        """
        if not isinstance(hotel_id, str) or not hotel_id.strip():
            print("Error: hotel_id must be a non-empty string")
            return None
        if not isinstance(name, str) or not name.strip():
            print("Error: name must be a non-empty string")
            return None
        if not isinstance(total_rooms, int) or total_rooms <= 0:
            print(
                "Error: total_rooms must be a positive integer"
            )
            return None
        hotels = cls.load_data(file_path)
        if hotel_id in hotels:
            print(f"Error: Hotel '{hotel_id}' already exists")
            return None
        hotel = cls(hotel_id, name, location, total_rooms)
        hotels[hotel_id] = hotel
        cls.save_data(hotels, file_path)
        return hotel

    @classmethod
    def delete_hotel(cls, hotel_id, file_path=None):
        """Delete a hotel by its ID.

        Args:
            hotel_id: Hotel identifier to delete.
            file_path: Optional custom file path.

        Returns:
            True if deleted, False otherwise.
        """
        hotels = cls.load_data(file_path)
        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found")
            return False
        del hotels[hotel_id]
        cls.save_data(hotels, file_path)
        return True

    @classmethod
    def display_hotel_info(cls, hotel_id, file_path=None):
        """Display information about a hotel.

        Args:
            hotel_id: Hotel identifier.
            file_path: Optional custom file path.

        Returns:
            Hotel instance or None if not found.
        """
        hotels = cls.load_data(file_path)
        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found")
            return None
        hotel = hotels[hotel_id]
        print(f"Hotel ID: {hotel.hotel_id}")
        print(f"Name: {hotel.name}")
        print(f"Location: {hotel.location}")
        print(f"Total Rooms: {hotel.total_rooms}")
        print(f"Available Rooms: {hotel.rooms_available}")
        return hotel

    @classmethod
    def modify_hotel_info(
        cls, hotel_id, file_path=None, **kwargs
    ):
        """Modify hotel attributes.

        Args:
            hotel_id: Hotel identifier.
            file_path: Optional custom file path.
            **kwargs: Attributes to modify.

        Returns:
            Updated Hotel instance or None if not found.
        """
        hotels = cls.load_data(file_path)
        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found")
            return None
        hotel = hotels[hotel_id]
        valid_attrs = {"name", "location", "total_rooms"}
        for key, value in kwargs.items():
            if key in valid_attrs:
                setattr(hotel, key, value)
            else:
                print(f"Warning: '{key}' is not modifiable")
        cls.save_data(hotels, file_path)
        return hotel

    @classmethod
    def reserve_room(cls, hotel_id, file_path=None):
        """Reserve a room at the specified hotel.

        Args:
            hotel_id: Hotel identifier.
            file_path: Optional custom file path.

        Returns:
            True if reserved, False otherwise.
        """
        hotels = cls.load_data(file_path)
        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found")
            return False
        hotel = hotels[hotel_id]
        if hotel.rooms_available <= 0:
            print("Error: No rooms available")
            return False
        hotel.rooms_available -= 1
        cls.save_data(hotels, file_path)
        return True

    @classmethod
    def cancel_room_reservation(
        cls, hotel_id, file_path=None
    ):
        """Cancel a room reservation, freeing up a room.

        Args:
            hotel_id: Hotel identifier.
            file_path: Optional custom file path.

        Returns:
            True if cancelled, False otherwise.
        """
        hotels = cls.load_data(file_path)
        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found")
            return False
        hotel = hotels[hotel_id]
        if hotel.rooms_available >= hotel.total_rooms:
            print("Error: No reservations to cancel")
            return False
        hotel.rooms_available += 1
        cls.save_data(hotels, file_path)
        return True
