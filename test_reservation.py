"""Unit tests for the Reservation class."""
import json
import os
import tempfile
import unittest

from customer import Customer
from hotel import Hotel
from reservation import Reservation


class TestReservation(unittest.TestCase):
    """Test cases for Reservation class."""

    def setUp(self):
        """Set up test fixtures with temporary files."""
        self.test_dir = tempfile.mkdtemp()
        self.res_file = os.path.join(
            self.test_dir, "test_reservations.json"
        )
        self.hotel_file = os.path.join(
            self.test_dir, "test_hotels.json"
        )
        self.cust_file = os.path.join(
            self.test_dir, "test_customers.json"
        )
        Hotel.create_hotel(
            "H1", "Grand Hotel", "Mexico City", 10,
            file_path=self.hotel_file
        )
        Customer.create_customer(
            "C1", "Juan Perez", "juan@email.com",
            file_path=self.cust_file
        )

    def tearDown(self):
        """Clean up test files."""
        for fpath in [
            self.res_file, self.hotel_file,
            self.cust_file
        ]:
            if os.path.exists(fpath):
                os.remove(fpath)

    # --- Positive test cases ---

    def test_create_reservation_success(self):
        """Test creating a valid reservation."""
        res = Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNotNone(res)
        self.assertEqual(res.reservation_id, "R1")
        self.assertEqual(res.customer_id, "C1")
        self.assertEqual(res.hotel_id, "H1")

    def test_reservation_decrements_rooms(self):
        """Test that reservation decrements rooms."""
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        hotel = Hotel.display_hotel_info(
            "H1", self.hotel_file
        )
        self.assertEqual(hotel.rooms_available, 9)

    def test_cancel_reservation_success(self):
        """Test cancelling an existing reservation."""
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        result = Reservation.cancel_reservation(
            "R1",
            file_path=self.res_file,
            hotel_file=self.hotel_file
        )
        self.assertTrue(result)

    def test_cancel_restores_room(self):
        """Test that cancellation restores room."""
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        Reservation.cancel_reservation(
            "R1",
            file_path=self.res_file,
            hotel_file=self.hotel_file
        )
        hotel = Hotel.display_hotel_info(
            "H1", self.hotel_file
        )
        self.assertEqual(hotel.rooms_available, 10)

    def test_to_dict(self):
        """Test reservation serialization."""
        res = Reservation("R1", "C1", "H1")
        data = res.to_dict()
        self.assertEqual(data["reservation_id"], "R1")
        self.assertEqual(data["customer_id"], "C1")
        self.assertEqual(data["hotel_id"], "H1")

    def test_from_dict_success(self):
        """Test reservation deserialization."""
        data = {
            "reservation_id": "R1",
            "customer_id": "C1",
            "hotel_id": "H1",
        }
        res = Reservation.from_dict(data)
        self.assertIsNotNone(res)
        self.assertEqual(res.reservation_id, "R1")

    def test_multiple_reservations(self):
        """Test creating multiple reservations."""
        Customer.create_customer(
            "C2", "Maria", "maria@email.com",
            file_path=self.cust_file
        )
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        Reservation.create_reservation(
            "R2", "C2", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        reservations = Reservation._load_data(
            self.res_file
        )
        self.assertEqual(len(reservations), 2)

    def test_persistence_after_create(self):
        """Test reservation persists to file."""
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        reservations = Reservation._load_data(
            self.res_file
        )
        self.assertIn("R1", reservations)
        self.assertEqual(
            reservations["R1"].customer_id, "C1"
        )

    def test_cancel_removes_from_file(self):
        """Test cancellation removes from file."""
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        Reservation.cancel_reservation(
            "R1",
            file_path=self.res_file,
            hotel_file=self.hotel_file
        )
        reservations = Reservation._load_data(
            self.res_file
        )
        self.assertNotIn("R1", reservations)

    # --- Negative test cases ---

    def test_create_empty_reservation_id(self):
        """Negative: create with empty reservation ID."""
        res = Reservation.create_reservation(
            "", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(res)

    def test_create_non_string_reservation_id(self):
        """Negative: create with non-string ID."""
        res = Reservation.create_reservation(
            123, "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(res)

    def test_create_empty_customer_id(self):
        """Negative: create with empty customer ID."""
        res = Reservation.create_reservation(
            "R1", "", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(res)

    def test_create_empty_hotel_id(self):
        """Negative: create with empty hotel ID."""
        res = Reservation.create_reservation(
            "R1", "C1", "",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(res)

    def test_create_nonexistent_customer(self):
        """Negative: create with non-existent customer."""
        res = Reservation.create_reservation(
            "R1", "C99", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(res)

    def test_create_nonexistent_hotel(self):
        """Negative: create with non-existent hotel."""
        res = Reservation.create_reservation(
            "R1", "C1", "H99",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(res)

    def test_create_duplicate_reservation(self):
        """Negative: create duplicate reservation."""
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        duplicate = Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(duplicate)

    def test_create_no_rooms_available(self):
        """Negative: create when no rooms available."""
        Hotel.create_hotel(
            "H2", "Small Hotel", "City", 1,
            file_path=self.hotel_file
        )
        Reservation.create_reservation(
            "R1", "C1", "H2",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        res = Reservation.create_reservation(
            "R2", "C1", "H2",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(res)

    def test_cancel_nonexistent_reservation(self):
        """Negative: cancel non-existent reservation."""
        result = Reservation.cancel_reservation(
            "R99",
            file_path=self.res_file,
            hotel_file=self.hotel_file
        )
        self.assertFalse(result)

    def test_load_corrupted_json(self):
        """Negative: load corrupted JSON file."""
        with open(
            self.res_file, "w", encoding="utf-8"
        ) as fhandle:
            fhandle.write("corrupted{{{json")
        reservations = Reservation._load_data(
            self.res_file
        )
        self.assertEqual(reservations, {})

    def test_load_nonexistent_file(self):
        """Negative: load non-existent file."""
        reservations = Reservation._load_data(
            "/tmp/nonexistent_res.json"
        )
        self.assertEqual(reservations, {})

    def test_from_dict_missing_keys(self):
        """Negative: from_dict with missing keys."""
        data = {"customer_id": "C1"}
        res = Reservation.from_dict(data)
        self.assertIsNone(res)

    def test_from_dict_none_input(self):
        """Negative: from_dict with None input."""
        res = Reservation.from_dict(None)
        self.assertIsNone(res)

    def test_load_file_with_invalid_entries(self):
        """Negative: load file with invalid entries."""
        data = {"R1": {"customer_id": "C1"}}
        with open(
            self.res_file, "w", encoding="utf-8"
        ) as fhandle:
            json.dump(data, fhandle)
        reservations = Reservation._load_data(
            self.res_file
        )
        self.assertEqual(len(reservations), 0)

    def test_create_whitespace_reservation_id(self):
        """Negative: create with whitespace ID."""
        res = Reservation.create_reservation(
            "   ", "C1", "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(res)

    def test_create_non_string_customer_id(self):
        """Negative: non-string customer ID."""
        res = Reservation.create_reservation(
            "R1", 123, "H1",
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(res)

    def test_create_non_string_hotel_id(self):
        """Negative: non-string hotel ID."""
        res = Reservation.create_reservation(
            "R1", "C1", 456,
            file_path=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(res)


if __name__ == "__main__":
    unittest.main()
