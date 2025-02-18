"""
This is a test suite for the Table class.

To run this script, run `python -m unittest tests/test_table.py` from the project root directory.
"""

import unittest
from backend.utils.table import Table


class TestTable(unittest.TestCase):
    """Test the Table class."""

    def setUp(self):
        # Create a table with table_id=1 and capacity=4 before each test.
        self.table = Table(table_id=1, capacity=4)

    def test_initial_state(self):
        """Test that a new table is initialized correctly."""
        self.assertEqual(self.table.table_id, 1)
        self.assertEqual(self.table.capacity, 4)
        self.assertEqual(len(self.table.seats), 4)
        # All seats should be unoccupied initially.
        for seat in self.table.seats:
            self.assertIsNone(seat.occupied_by)
        self.assertEqual(self.table.left_capacity(), 4)
        self.assertTrue(self.table.has_free_seats())
        self.assertEqual(self.table.occupants, [])

    def test_set_occupant(self):
        """Test that setting a single occupant works correctly."""
        self.table.set_occupant("Alice")
        # Check that the first free seat is now occupied.
        self.assertEqual(self.table.seats[0].occupied_by, "Alice")
        # left_capacity should decrease.
        self.assertEqual(self.table.left_capacity(), 3)
        # The occupant should appear in the occupants list.
        self.assertIn("Alice", self.table.occupants)

    def test_set_occupant_full(self):
        """Test that setting an occupant on a full table raises an error."""
        # Fill the table.
        for name in ["Alice", "Bob", "Charlie", "David"]:
            self.table.set_occupant(name)
        self.assertEqual(self.table.left_capacity(), 0)
        self.assertFalse(self.table.has_free_seats())
        # Attempting to add another occupant should raise a ValueError.
        with self.assertRaises(ValueError) as context:
            self.table.set_occupant("Eve")
        self.assertIn("Table 1 is already full!", str(context.exception))

    def test_set_occupants_success(self):
        """Test that setting multiple occupants works correctly."""
        # Use a different table for clarity.
        table2 = Table(table_id=2, capacity=4)
        names = ["Eve", "Frank", "Grace"]
        table2.set_occupants(names)
        # The first three seats should be occupied accordingly.
        self.assertEqual(table2.seats[0].occupied_by, "Eve")
        self.assertEqual(table2.seats[1].occupied_by, "Frank")
        self.assertEqual(table2.seats[2].occupied_by, "Grace")
        self.assertIsNone(table2.seats[3].occupied_by)
        self.assertEqual(table2.left_capacity(), 1)
        self.assertTrue(table2.has_free_seats())
        # Check that occupants list is correctly populated (no duplicates).
        self.assertEqual(table2.occupants, names)

    def test_set_occupants_not_enough_free_seats(self):
        """Test that setting too many occupants at once raises an error."""
        # Occupy one seat first.
        self.table.set_occupant("Alice")  # Free seats now = 3.
        # Attempt to set occupants for 4 people when only 3 seats are free.
        with self.assertRaises(ValueError) as context:
            self.table.set_occupants(["Bob", "Charlie", "David", "Eve"])
        self.assertIn("Not enough free seats at table 1!",
                      str(context.exception))

    def test_repr_and_str(self):
        """Test the __repr__ and __str__ methods."""
        # Before adding any occupants.
        repr_str = repr(self.table)
        self.assertIn("Table(table_id=1", repr_str)
        str_str = str(self.table)
        self.assertIn("table_id=1", str_str)
        # After setting an occupant.
        self.table.set_occupant("Alice")
        repr_str = repr(self.table)
        self.assertIn("Alice", repr_str)
        str_str = str(self.table)
        self.assertIn("Alice", str_str)


if __name__ == '__main__':
    unittest.main()
