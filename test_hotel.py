"""Unit tests for the Hotel class."""
import json
import os
import tempfile
import unittest

from hotel import Hotel


class TestHotel(unittest.TestCase):
    """Test cases for Hotel class."""

    def setUp(self):
        """Set up test fixtures with temporary files."""
        self.test_dir = tempfile.mkdtemp()
        self.file_path = os.path.join(
            self.test_dir, "test_hotels.json"
        )

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    # --- Positive test cases ---

    def test_create_hotel_success(self):
        """Test creating a valid hotel."""
        hotel = Hotel.create_hotel(
            "H1", "Grand Hotel", "Mexico City", 50,
            file_path=self.file_path
        )
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.hotel_id, "H1")
        self.assertEqual(hotel.name, "Grand Hotel")
        self.assertEqual(hotel.location, "Mexico City")
        self.assertEqual(hotel.total_rooms, 50)
        self.assertEqual(hotel.rooms_available, 50)

    def test_delete_hotel_success(self):
        """Test deleting an existing hotel."""
        Hotel.create_hotel(
            "H1", "Grand Hotel", "Mexico City", 50,
            file_path=self.file_path
        )
        result = Hotel.delete_hotel(
            "H1", self.file_path
        )
        self.assertTrue(result)
        hotels = Hotel._load_data(self.file_path)
        self.assertNotIn("H1", hotels)

    def test_display_hotel_info_success(self):
        """Test displaying existing hotel information."""
        Hotel.create_hotel(
            "H1", "Grand Hotel", "Mexico City", 50,
            file_path=self.file_path
        )
        hotel = Hotel.display_hotel_info(
            "H1", self.file_path
        )
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.name, "Grand Hotel")

    def test_modify_hotel_name(self):
        """Test modifying hotel name."""
        Hotel.create_hotel(
            "H1", "Grand Hotel", "Mexico City", 50,
            file_path=self.file_path
        )
        hotel = Hotel.modify_hotel_info(
            "H1", file_path=self.file_path,
            name="Luxury Hotel"
        )
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.name, "Luxury Hotel")

    def test_modify_hotel_location(self):
        """Test modifying hotel location."""
        Hotel.create_hotel(
            "H1", "Grand Hotel", "Mexico City", 50,
            file_path=self.file_path
        )
        hotel = Hotel.modify_hotel_info(
            "H1", file_path=self.file_path,
            location="Guadalajara"
        )
        self.assertEqual(hotel.location, "Guadalajara")

    def test_reserve_room_success(self):
        """Test reserving a room successfully."""
        Hotel.create_hotel(
            "H1", "Grand Hotel", "Mexico City", 5,
            file_path=self.file_path
        )
        result = Hotel.reserve_room(
            "H1", self.file_path
        )
        self.assertTrue(result)
        hotel = Hotel.display_hotel_info(
            "H1", self.file_path
        )
        self.assertEqual(hotel.rooms_available, 4)

    def test_cancel_room_reservation_success(self):
        """Test cancelling a room reservation."""
        Hotel.create_hotel(
            "H1", "Grand Hotel", "Mexico City", 5,
            file_path=self.file_path
        )
        Hotel.reserve_room("H1", self.file_path)
        result = Hotel.cancel_room_reservation(
            "H1", self.file_path
        )
        self.assertTrue(result)
        hotel = Hotel.display_hotel_info(
            "H1", self.file_path
        )
        self.assertEqual(hotel.rooms_available, 5)

    def test_to_dict(self):
        """Test hotel serialization to dict."""
        hotel = Hotel("H1", "Grand Hotel", "City", 10)
        data = hotel.to_dict()
        self.assertEqual(data["hotel_id"], "H1")
        self.assertEqual(data["name"], "Grand Hotel")
        self.assertEqual(data["total_rooms"], 10)
        self.assertEqual(data["rooms_available"], 10)

    def test_from_dict_success(self):
        """Test hotel deserialization from dict."""
        data = {
            "hotel_id": "H1",
            "name": "Grand Hotel",
            "location": "City",
            "total_rooms": 10,
            "rooms_available": 7,
        }
        hotel = Hotel.from_dict(data)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.hotel_id, "H1")
        self.assertEqual(hotel.rooms_available, 7)

    def test_from_dict_default_availability(self):
        """Test from_dict uses total_rooms as default."""
        data = {
            "hotel_id": "H1",
            "name": "Hotel",
            "location": "City",
            "total_rooms": 10,
        }
        hotel = Hotel.from_dict(data)
        self.assertEqual(hotel.rooms_available, 10)

    def test_multiple_reservations(self):
        """Test making multiple room reservations."""
        Hotel.create_hotel(
            "H1", "Grand Hotel", "City", 3,
            file_path=self.file_path
        )
        Hotel.reserve_room("H1", self.file_path)
        Hotel.reserve_room("H1", self.file_path)
        hotel = Hotel.display_hotel_info(
            "H1", self.file_path
        )
        self.assertEqual(hotel.rooms_available, 1)

    def test_create_multiple_hotels(self):
        """Test creating multiple hotels."""
        Hotel.create_hotel(
            "H1", "Hotel A", "City A", 10,
            file_path=self.file_path
        )
        Hotel.create_hotel(
            "H2", "Hotel B", "City B", 20,
            file_path=self.file_path
        )
        hotels = Hotel._load_data(self.file_path)
        self.assertEqual(len(hotels), 2)

    def test_persistence_after_operations(self):
        """Test data persists after create and modify."""
        Hotel.create_hotel(
            "H1", "Hotel A", "City A", 10,
            file_path=self.file_path
        )
        Hotel.modify_hotel_info(
            "H1", file_path=self.file_path,
            name="Hotel B"
        )
        hotels = Hotel._load_data(self.file_path)
        self.assertEqual(hotels["H1"].name, "Hotel B")

    # --- Negative test cases ---

    def test_create_hotel_empty_id(self):
        """Negative: create hotel with empty ID."""
        hotel = Hotel.create_hotel(
            "", "Hotel A", "City A", 10,
            file_path=self.file_path
        )
        self.assertIsNone(hotel)

    def test_create_hotel_non_string_id(self):
        """Negative: create hotel with non-string ID."""
        hotel = Hotel.create_hotel(
            123, "Hotel A", "City A", 10,
            file_path=self.file_path
        )
        self.assertIsNone(hotel)

    def test_create_hotel_empty_name(self):
        """Negative: create hotel with empty name."""
        hotel = Hotel.create_hotel(
            "H1", "", "City A", 10,
            file_path=self.file_path
        )
        self.assertIsNone(hotel)

    def test_create_hotel_non_string_name(self):
        """Negative: create hotel with non-string name."""
        hotel = Hotel.create_hotel(
            "H1", 999, "City A", 10,
            file_path=self.file_path
        )
        self.assertIsNone(hotel)

    def test_create_hotel_negative_rooms(self):
        """Negative: create hotel with negative rooms."""
        hotel = Hotel.create_hotel(
            "H1", "Hotel A", "City A", -5,
            file_path=self.file_path
        )
        self.assertIsNone(hotel)

    def test_create_hotel_zero_rooms(self):
        """Negative: create hotel with zero rooms."""
        hotel = Hotel.create_hotel(
            "H1", "Hotel A", "City A", 0,
            file_path=self.file_path
        )
        self.assertIsNone(hotel)

    def test_create_hotel_float_rooms(self):
        """Negative: create hotel with float rooms."""
        hotel = Hotel.create_hotel(
            "H1", "Hotel A", "City A", 5.5,
            file_path=self.file_path
        )
        self.assertIsNone(hotel)

    def test_create_hotel_string_rooms(self):
        """Negative: create hotel with string rooms."""
        hotel = Hotel.create_hotel(
            "H1", "Hotel A", "City A", "ten",
            file_path=self.file_path
        )
        self.assertIsNone(hotel)

    def test_create_duplicate_hotel(self):
        """Negative: create hotel with existing ID."""
        Hotel.create_hotel(
            "H1", "Hotel A", "City A", 10,
            file_path=self.file_path
        )
        duplicate = Hotel.create_hotel(
            "H1", "Hotel B", "City B", 5,
            file_path=self.file_path
        )
        self.assertIsNone(duplicate)

    def test_delete_nonexistent_hotel(self):
        """Negative: delete a non-existent hotel."""
        result = Hotel.delete_hotel(
            "H99", self.file_path
        )
        self.assertFalse(result)

    def test_display_nonexistent_hotel(self):
        """Negative: display a non-existent hotel."""
        result = Hotel.display_hotel_info(
            "H99", self.file_path
        )
        self.assertIsNone(result)

    def test_modify_nonexistent_hotel(self):
        """Negative: modify a non-existent hotel."""
        result = Hotel.modify_hotel_info(
            "H99", file_path=self.file_path,
            name="New Name"
        )
        self.assertIsNone(result)

    def test_modify_invalid_attribute(self):
        """Negative: modify an invalid attribute."""
        Hotel.create_hotel(
            "H1", "Hotel A", "City A", 10,
            file_path=self.file_path
        )
        hotel = Hotel.modify_hotel_info(
            "H1", file_path=self.file_path,
            invalid_attr="value"
        )
        self.assertIsNotNone(hotel)

    def test_reserve_nonexistent_hotel(self):
        """Negative: reserve at non-existent hotel."""
        result = Hotel.reserve_room(
            "H99", self.file_path
        )
        self.assertFalse(result)

    def test_reserve_no_rooms_available(self):
        """Negative: reserve when all rooms taken."""
        Hotel.create_hotel(
            "H1", "Hotel A", "City A", 1,
            file_path=self.file_path
        )
        Hotel.reserve_room("H1", self.file_path)
        result = Hotel.reserve_room(
            "H1", self.file_path
        )
        self.assertFalse(result)

    def test_cancel_nonexistent_hotel(self):
        """Negative: cancel at non-existent hotel."""
        result = Hotel.cancel_room_reservation(
            "H99", self.file_path
        )
        self.assertFalse(result)

    def test_cancel_no_reservations(self):
        """Negative: cancel when no reservations."""
        Hotel.create_hotel(
            "H1", "Hotel A", "City A", 5,
            file_path=self.file_path
        )
        result = Hotel.cancel_room_reservation(
            "H1", self.file_path
        )
        self.assertFalse(result)

    def test_load_corrupted_json_file(self):
        """Negative: load a corrupted JSON file."""
        with open(
            self.file_path, "w", encoding="utf-8"
        ) as fhandle:
            fhandle.write("not valid json{{{")
        hotels = Hotel._load_data(self.file_path)
        self.assertEqual(hotels, {})

    def test_load_nonexistent_file(self):
        """Negative: load from non-existent file."""
        hotels = Hotel._load_data(
            "/tmp/nonexistent_file.json"
        )
        self.assertEqual(hotels, {})

    def test_from_dict_missing_keys(self):
        """Negative: from_dict with missing keys."""
        data = {"name": "Hotel A"}
        hotel = Hotel.from_dict(data)
        self.assertIsNone(hotel)

    def test_from_dict_none_input(self):
        """Negative: from_dict with None input."""
        hotel = Hotel.from_dict(None)
        self.assertIsNone(hotel)

    def test_load_file_with_invalid_entries(self):
        """Negative: load file with invalid entries."""
        data = {"H1": {"name": "incomplete data"}}
        with open(
            self.file_path, "w", encoding="utf-8"
        ) as fhandle:
            json.dump(data, fhandle)
        hotels = Hotel._load_data(self.file_path)
        self.assertEqual(len(hotels), 0)

    def test_create_hotel_whitespace_id(self):
        """Negative: create hotel with whitespace ID."""
        hotel = Hotel.create_hotel(
            "   ", "Hotel A", "City A", 10,
            file_path=self.file_path
        )
        self.assertIsNone(hotel)

    def test_create_hotel_whitespace_name(self):
        """Negative: create hotel with whitespace name."""
        hotel = Hotel.create_hotel(
            "H1", "   ", "City A", 10,
            file_path=self.file_path
        )
        self.assertIsNone(hotel)


if __name__ == "__main__":
    unittest.main()
