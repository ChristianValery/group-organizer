"""
This is a test suite for the Openspace class.

To run this script, run `python -m unittest tests/test_openspace.py` from the project root directory.
"""

import unittest
from random import seed
from backend.utils.openspace import Openspace


class TestOpenspace(unittest.TestCase):
    """Test case for the Openspace class."""

    def setUp(self):
        # Set a seed for reproducibility in tests that use randomness.
        seed(0)
        # Create an Openspace with 3 tables, each with a capacity of 3 seats.
        self.openspace = Openspace(num_tables=3, table_capacity=3)

    def test_initial_state(self):
        """Test that the Openspace initializes with the correct attributes."""
        self.assertEqual(self.openspace.num_tables, 3)
        self.assertEqual(self.openspace.table_capacity, 3)
        self.assertEqual(len(self.openspace.tables), 3)
        for table in self.openspace.tables:
            self.assertEqual(table.capacity, 3)
            self.assertEqual(table.left_capacity(), 3)

    def test_display_seating_empty(self):
        """Test that display_seating shows all seats empty when no one is assigned."""
        seating = self.openspace.display_seating()
        self.assertEqual(len(seating), 3)  # Three tables
        for _, seats in seating.items():
            self.assertEqual(len(seats), 3)  # Each table has 3 seats
            for occupant in seats.values():
                self.assertEqual(occupant, '')

    def test_organize_seating_success(self):
        """
        Test that organize_seating assigns all persons and meets
        the compatible and incompatible constraints.
        """
        # Prepare a set of 8 persons (total seats available = 9).
        persons = {'Alice', 'Bob', 'Charlie',
                   'David', 'Eve', 'Frank', 'Grace', 'Hank'}
        # Incompatible pair: Alice and Bob must be on different tables.
        incompatible_pairs = [{'Alice', 'Bob'}]
        # Compatible pair: Charlie and David must be on the same table.
        compatible_pairs = [{'Charlie', 'David'}]

        self.openspace.organize_seating(
            person_names=persons,
            compatible_pairs=compatible_pairs,
            incompatible_pairs=incompatible_pairs
        )

        # Build a mapping from person to table id using display_seating.
        assignment = {}
        seating = self.openspace.display_seating()
        for table_key, seats in seating.items():
            for occupant in seats.values():
                if occupant:
                    assignment[occupant] = table_key

        # Verify that all persons have been assigned.
        self.assertEqual(len(assignment), len(persons))

        # Check incompatible pair: Alice and Bob must be in different tables.
        self.assertIn('Alice', assignment)
        self.assertIn('Bob', assignment)
        self.assertNotEqual(assignment['Alice'], assignment['Bob'])

        # Check compatible pair: Charlie and David must be in the same table.
        self.assertIn('Charlie', assignment)
        self.assertIn('David', assignment)
        self.assertEqual(assignment['Charlie'], assignment['David'])

    def test_organize_seating_insufficient_seats(self):
        """Test that a ValueError is raised when there are not enough seats available."""
        # Create an Openspace with only 1 table of capacity 2 (total 2 seats).
        small_space = Openspace(num_tables=1, table_capacity=2)
        persons = {'Alice', 'Bob', 'Charlie'}  # 3 persons, but only 2 seats.
        incompatible_pairs = []
        compatible_pairs = []

        with self.assertRaises(ValueError):
            small_space.organize_seating(
                person_names=persons,
                compatible_pairs=compatible_pairs,
                incompatible_pairs=incompatible_pairs
            )

    def test_repr(self):
        """Test that __repr__ returns a string containing key details."""
        repr_str = repr(self.openspace)
        self.assertIn("Openspace(num_tables=3", repr_str)
        self.assertIn("table_capacity=3", repr_str)
        self.assertIn("tables=", repr_str)

    def test_str_method(self):
        """
        Test that the __str__ method returns a properly formatted string
        representation of the seating arrangement.
        """
        seating_str = str(self.openspace)
        # Since no one is assigned yet, each table should display all seats as "Empty".
        for i in range(1, self.openspace.num_tables + 1):
            self.assertIn(f"Table_{i}:", seating_str)
        for i in range(1, self.openspace.table_capacity + 1):
            self.assertIn(f"Seat_{i}: Empty", seating_str)


if __name__ == '__main__':
    unittest.main()
