"""Customer management module for the reservation system."""
import json
import os


class Customer:
    """Customer entity with CRUD capabilities."""

    DATA_FILE = "customers.json"

    def __init__(self, customer_id, name, email):
        """Initialize a Customer instance.

        Args:
            customer_id: Unique identifier for the customer.
            name: Name of the customer.
            email: Email address of the customer.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """Convert customer instance to dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Customer from dictionary.

        Args:
            data: Dictionary with customer attributes.

        Returns:
            Customer instance or None if data is invalid.
        """
        try:
            return cls(
                data["customer_id"],
                data["name"],
                data["email"],
            )
        except (KeyError, TypeError) as err:
            print(
                f"Error creating customer from data: {err}"
            )
            return None

    @staticmethod
    def load_data(file_path=None):
        """Load customers from JSON file.

        Args:
            file_path: Optional custom file path.

        Returns:
            Dictionary of customer_id to Customer instances.
        """
        path = file_path or Customer.DATA_FILE
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as fhandle:
                raw = json.load(fhandle)
            customers = {}
            for key, val in raw.items():
                cust = Customer.from_dict(val)
                if cust:
                    customers[key] = cust
            return customers
        except (json.JSONDecodeError, ValueError) as err:
            print(f"Error loading customers file: {err}")
            return {}

    @staticmethod
    def save_data(customers, file_path=None):
        """Save customers to JSON file.

        Args:
            customers: Dict of customer_id to instances.
            file_path: Optional custom file path.
        """
        path = file_path or Customer.DATA_FILE
        data = {k: c.to_dict() for k, c in customers.items()}
        with open(path, "w", encoding="utf-8") as fhandle:
            json.dump(data, fhandle, indent=2)

    @classmethod
    def create_customer(
        cls, customer_id, name, email, file_path=None
    ):
        """Create and persist a new customer.

        Args:
            customer_id: Unique identifier.
            name: Customer name.
            email: Customer email.
            file_path: Optional custom file path.

        Returns:
            Customer instance or None on failure.
        """
        if (
            not isinstance(customer_id, str)
            or not customer_id.strip()
        ):
            print(
                "Error: customer_id must be "
                "a non-empty string"
            )
            return None
        if not isinstance(name, str) or not name.strip():
            print("Error: name must be a non-empty string")
            return None
        if not isinstance(email, str) or not email.strip():
            print(
                "Error: email must be a non-empty string"
            )
            return None
        customers = cls.load_data(file_path)
        if customer_id in customers:
            print(
                f"Error: Customer '{customer_id}' "
                "already exists"
            )
            return None
        customer = cls(customer_id, name, email)
        customers[customer_id] = customer
        cls.save_data(customers, file_path)
        return customer

    @classmethod
    def delete_customer(cls, customer_id, file_path=None):
        """Delete a customer by ID.

        Args:
            customer_id: Customer identifier to delete.
            file_path: Optional custom file path.

        Returns:
            True if deleted, False otherwise.
        """
        customers = cls.load_data(file_path)
        if customer_id not in customers:
            print(
                f"Error: Customer '{customer_id}' not found"
            )
            return False
        del customers[customer_id]
        cls.save_data(customers, file_path)
        return True

    @classmethod
    def display_customer_info(
        cls, customer_id, file_path=None
    ):
        """Display information about a customer.

        Args:
            customer_id: Customer identifier.
            file_path: Optional custom file path.

        Returns:
            Customer instance or None if not found.
        """
        customers = cls.load_data(file_path)
        if customer_id not in customers:
            print(
                f"Error: Customer '{customer_id}' not found"
            )
            return None
        cust = customers[customer_id]
        print(f"Customer ID: {cust.customer_id}")
        print(f"Name: {cust.name}")
        print(f"Email: {cust.email}")
        return cust

    @classmethod
    def modify_customer_info(
        cls, customer_id, file_path=None, **kwargs
    ):
        """Modify customer attributes.

        Args:
            customer_id: Customer identifier.
            file_path: Optional custom file path.
            **kwargs: Attributes to modify (name, email).

        Returns:
            Updated Customer or None if not found.
        """
        customers = cls.load_data(file_path)
        if customer_id not in customers:
            print(
                f"Error: Customer '{customer_id}' not found"
            )
            return None
        cust = customers[customer_id]
        valid_attrs = {"name", "email"}
        for key, value in kwargs.items():
            if key in valid_attrs:
                setattr(cust, key, value)
            else:
                print(
                    f"Warning: '{key}' is not modifiable"
                )
        cls.save_data(customers, file_path)
        return cust
