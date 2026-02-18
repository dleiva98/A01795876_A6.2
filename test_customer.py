"""Unit tests for the Customer class."""
import json
import os
import tempfile
import unittest

from customer import Customer


class TestCustomer(unittest.TestCase):
    """Test cases for Customer class."""

    def setUp(self):
        """Set up test fixtures with temporary files."""
        self.test_dir = tempfile.mkdtemp()
        self.file_path = os.path.join(
            self.test_dir, "test_customers.json"
        )

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    # --- Positive test cases ---

    def test_create_customer_success(self):
        """Test creating a valid customer."""
        cust = Customer.create_customer(
            "C1", "Juan Perez", "juan@email.com",
            file_path=self.file_path
        )
        self.assertIsNotNone(cust)
        self.assertEqual(cust.customer_id, "C1")
        self.assertEqual(cust.name, "Juan Perez")
        self.assertEqual(cust.email, "juan@email.com")

    def test_delete_customer_success(self):
        """Test deleting an existing customer."""
        Customer.create_customer(
            "C1", "Juan Perez", "juan@email.com",
            file_path=self.file_path
        )
        result = Customer.delete_customer(
            "C1", self.file_path
        )
        self.assertTrue(result)
        customers = Customer.load_data(self.file_path)
        self.assertNotIn("C1", customers)

    def test_display_customer_info_success(self):
        """Test displaying customer information."""
        Customer.create_customer(
            "C1", "Juan Perez", "juan@email.com",
            file_path=self.file_path
        )
        cust = Customer.display_customer_info(
            "C1", self.file_path
        )
        self.assertIsNotNone(cust)
        self.assertEqual(cust.name, "Juan Perez")

    def test_modify_customer_name(self):
        """Test modifying customer name."""
        Customer.create_customer(
            "C1", "Juan Perez", "juan@email.com",
            file_path=self.file_path
        )
        cust = Customer.modify_customer_info(
            "C1", file_path=self.file_path,
            name="Carlos Lopez"
        )
        self.assertIsNotNone(cust)
        self.assertEqual(cust.name, "Carlos Lopez")

    def test_modify_customer_email(self):
        """Test modifying customer email."""
        Customer.create_customer(
            "C1", "Juan Perez", "juan@email.com",
            file_path=self.file_path
        )
        cust = Customer.modify_customer_info(
            "C1", file_path=self.file_path,
            email="carlos@email.com"
        )
        self.assertEqual(cust.email, "carlos@email.com")

    def test_to_dict(self):
        """Test customer serialization to dict."""
        cust = Customer("C1", "Juan", "juan@email.com")
        data = cust.to_dict()
        self.assertEqual(data["customer_id"], "C1")
        self.assertEqual(data["name"], "Juan")
        self.assertEqual(data["email"], "juan@email.com")

    def test_from_dict_success(self):
        """Test customer deserialization from dict."""
        data = {
            "customer_id": "C1",
            "name": "Juan",
            "email": "juan@email.com",
        }
        cust = Customer.from_dict(data)
        self.assertIsNotNone(cust)
        self.assertEqual(cust.customer_id, "C1")

    def test_create_multiple_customers(self):
        """Test creating multiple customers."""
        Customer.create_customer(
            "C1", "Juan", "juan@email.com",
            file_path=self.file_path
        )
        Customer.create_customer(
            "C2", "Maria", "maria@email.com",
            file_path=self.file_path
        )
        customers = Customer.load_data(self.file_path)
        self.assertEqual(len(customers), 2)

    def test_persistence_after_modify(self):
        """Test data persists after modification."""
        Customer.create_customer(
            "C1", "Juan", "juan@email.com",
            file_path=self.file_path
        )
        Customer.modify_customer_info(
            "C1", file_path=self.file_path,
            name="Carlos"
        )
        customers = Customer.load_data(self.file_path)
        self.assertEqual(
            customers["C1"].name, "Carlos"
        )

    def test_modify_multiple_attrs(self):
        """Test modifying multiple attributes."""
        Customer.create_customer(
            "C1", "Juan", "juan@email.com",
            file_path=self.file_path
        )
        cust = Customer.modify_customer_info(
            "C1", file_path=self.file_path,
            name="Carlos", email="carlos@email.com"
        )
        self.assertEqual(cust.name, "Carlos")
        self.assertEqual(cust.email, "carlos@email.com")

    # --- Negative test cases ---

    def test_create_customer_empty_id(self):
        """Negative: create with empty ID."""
        cust = Customer.create_customer(
            "", "Juan", "juan@email.com",
            file_path=self.file_path
        )
        self.assertIsNone(cust)

    def test_create_customer_non_string_id(self):
        """Negative: create with non-string ID."""
        cust = Customer.create_customer(
            123, "Juan", "juan@email.com",
            file_path=self.file_path
        )
        self.assertIsNone(cust)

    def test_create_customer_empty_name(self):
        """Negative: create with empty name."""
        cust = Customer.create_customer(
            "C1", "", "juan@email.com",
            file_path=self.file_path
        )
        self.assertIsNone(cust)

    def test_create_customer_non_string_name(self):
        """Negative: create with non-string name."""
        cust = Customer.create_customer(
            "C1", 123, "juan@email.com",
            file_path=self.file_path
        )
        self.assertIsNone(cust)

    def test_create_customer_empty_email(self):
        """Negative: create with empty email."""
        cust = Customer.create_customer(
            "C1", "Juan", "",
            file_path=self.file_path
        )
        self.assertIsNone(cust)

    def test_create_customer_non_string_email(self):
        """Negative: create with non-string email."""
        cust = Customer.create_customer(
            "C1", "Juan", 123,
            file_path=self.file_path
        )
        self.assertIsNone(cust)

    def test_create_duplicate_customer(self):
        """Negative: create customer with existing ID."""
        Customer.create_customer(
            "C1", "Juan", "juan@email.com",
            file_path=self.file_path
        )
        duplicate = Customer.create_customer(
            "C1", "Maria", "maria@email.com",
            file_path=self.file_path
        )
        self.assertIsNone(duplicate)

    def test_delete_nonexistent_customer(self):
        """Negative: delete non-existent customer."""
        result = Customer.delete_customer(
            "C99", self.file_path
        )
        self.assertFalse(result)

    def test_display_nonexistent_customer(self):
        """Negative: display non-existent customer."""
        result = Customer.display_customer_info(
            "C99", self.file_path
        )
        self.assertIsNone(result)

    def test_modify_nonexistent_customer(self):
        """Negative: modify non-existent customer."""
        result = Customer.modify_customer_info(
            "C99", file_path=self.file_path,
            name="New Name"
        )
        self.assertIsNone(result)

    def test_modify_invalid_attribute(self):
        """Negative: modify invalid attribute."""
        Customer.create_customer(
            "C1", "Juan", "juan@email.com",
            file_path=self.file_path
        )
        cust = Customer.modify_customer_info(
            "C1", file_path=self.file_path,
            invalid_attr="value"
        )
        self.assertIsNotNone(cust)

    def test_load_corrupted_json(self):
        """Negative: load corrupted JSON file."""
        with open(
            self.file_path, "w", encoding="utf-8"
        ) as fhandle:
            fhandle.write("{invalid json content")
        customers = Customer.load_data(self.file_path)
        self.assertEqual(customers, {})

    def test_load_nonexistent_file(self):
        """Negative: load non-existent file."""
        customers = Customer.load_data(
            "/tmp/nonexistent_customers.json"
        )
        self.assertEqual(customers, {})

    def test_from_dict_missing_keys(self):
        """Negative: from_dict with missing keys."""
        data = {"name": "Juan"}
        cust = Customer.from_dict(data)
        self.assertIsNone(cust)

    def test_from_dict_none_input(self):
        """Negative: from_dict with None input."""
        cust = Customer.from_dict(None)
        self.assertIsNone(cust)

    def test_load_file_with_invalid_entries(self):
        """Negative: load file with invalid entries."""
        data = {"C1": {"name": "incomplete"}}
        with open(
            self.file_path, "w", encoding="utf-8"
        ) as fhandle:
            json.dump(data, fhandle)
        customers = Customer.load_data(self.file_path)
        self.assertEqual(len(customers), 0)

    def test_create_customer_whitespace_id(self):
        """Negative: create with whitespace-only ID."""
        cust = Customer.create_customer(
            "   ", "Juan", "juan@email.com",
            file_path=self.file_path
        )
        self.assertIsNone(cust)

    def test_create_customer_whitespace_name(self):
        """Negative: create with whitespace-only name."""
        cust = Customer.create_customer(
            "C1", "   ", "juan@email.com",
            file_path=self.file_path
        )
        self.assertIsNone(cust)

    def test_create_customer_whitespace_email(self):
        """Negative: create with whitespace-only email."""
        cust = Customer.create_customer(
            "C1", "Juan", "   ",
            file_path=self.file_path
        )
        self.assertIsNone(cust)


if __name__ == "__main__":
    unittest.main()
