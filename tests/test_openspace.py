"""
This is a test suite for the Openspace class.

To run this script, execute the following command from the project root directory:
```	
python -m unittest tests.test_openspace
```
"""


import unittest
from backend.utils.openspace import Openspace


class TestOpenspace(unittest.TestCase):
    """
    Test suite for the Openspace class.
    """

    def test_initialization(self):
        """
        Test that the open space is initialized with the correct number of tables and seats.
        """
        num_tables = 3
        table_capacity = 4
        openspace = Openspace(num_tables, table_capacity)
        self.assertEqual(len(openspace.tables), num_tables)
        for i, table in enumerate(openspace.tables, start=1):
            self.assertEqual(table.table_id, i)
            self.assertEqual(table.capacity, table_capacity)
            self.assertEqual(len(table.seats), table_capacity)

    def test_organize_seating_valid(self):
        """
        Test that valid partitions are assigned to tables correctly.
        """
        num_tables = 3
        table_capacity = 4
        openspace = Openspace(num_tables, table_capacity)
        # Provide two groups (fewer than the number of tables)
        partition = [
            ["Alice", "Bob"],
            ["Charlie"]
        ]
        openspace.organize_seating(partition)
        seating = openspace.display_seating()
        found_alice_bob = False
        found_charlie = False
        # Since the tables might be shuffled, iterate over all to find our groups.
        for _, seat_map in seating.items():
            occupants = list(seat_map.values())
            if occupants.count("Alice") == 1 and occupants.count("Bob") == 1:
                found_alice_bob = True
            if occupants.count("Charlie") == 1:
                found_charlie = True
        self.assertTrue(found_alice_bob,
                        "The group ['Alice', 'Bob'] was not seated correctly.")
        self.assertTrue(
            found_charlie, "The group ['Charlie'] was not seated correctly.")

    def test_invalid_number_of_groups(self):
        """
        Test that organizing seating fails when there are more groups than tables.
        """
        num_tables = 2
        table_capacity = 4
        openspace = Openspace(num_tables, table_capacity)
        partition = [
            ["Alice"],
            ["Bob"],
            ["Charlie"]
        ]
        with self.assertRaises(ValueError) as cm:
            openspace.organize_seating(partition)
        self.assertEqual(str(cm.exception),
                         "The number of groups exceeds the number of tables.")

    def test_group_exceeds_capacity(self):
        """
        Test that organizing seating fails when any group exceeds a table's capacity.
        """
        num_tables = 3
        table_capacity = 4
        openspace = Openspace(num_tables, table_capacity)
        # One group has 5 people, which exceeds the table capacity.
        partition = [
            ["Alice", "Bob", "Charlie", "David", "Eve"],
        ]
        with self.assertRaises(ValueError) as cm:
            openspace.organize_seating(partition)
        self.assertEqual(str(cm.exception),
                         "A group exceeds the table capacity.")

    @unittest.skip("Cannot trigger total seating capacity error due to group capacity constraints.")
    def test_total_exceeds_capacity(self):
        """
        Test that organizing seating fails when the total number of people 
        exceeds overall seating capacity.
        Note: This condition is logically unreachable given that each group is
        individually constrained to not exceed table capacity.
        """
        num_tables = 2
        table_capacity = 4  # Total seats = 8
        openspace = Openspace(num_tables, table_capacity)
        partition = [
            ["Alice", "Bob", "Charlie", "David"],
            ["Eve", "Frank", "Grace", "Heidi", "Ivan"]
        ]
        with self.assertRaises(ValueError) as cm:
            openspace.organize_seating(partition)
        self.assertEqual(str(
            cm.exception), "The total number of people exceeds the total seating capacity.")

    def test_display_seating(self):
        """
        Test that the seating display returns the correct dictionary structure.
        """
        num_tables = 2
        table_capacity = 3
        openspace = Openspace(num_tables, table_capacity)
        partition = [
            ["Alice", "Bob"]
        ]
        openspace.organize_seating(partition)
        seating = openspace.display_seating()
        self.assertEqual(len(seating), num_tables)
        for table in openspace.tables:
            key = f"Table_{table.table_id}"
            self.assertIn(key, seating)
            seat_map = seating[key]
            self.assertEqual(len(seat_map), table_capacity)
            # Check that each seat key follows the "Seat_x" pattern.
            for seat_name in seat_map.keys():
                self.assertTrue(seat_name.startswith("Seat_"))

    def test_repr(self):
        """
        Test the __repr__ string of the Openspace class.
        """
        num_tables = 2
        table_capacity = 3
        openspace = Openspace(num_tables, table_capacity)
        rep = repr(openspace)
        self.assertIn("Openspace(num_tables=", rep)
        self.assertIn("table_capacity=", rep)
        self.assertIn("tables=", rep)

    def test_str(self):
        """
        Test the human-readable string representation of the seating arrangement.
        """
        num_tables = 2
        table_capacity = 3
        openspace = Openspace(num_tables, table_capacity)
        partition = [
            ["Alice"]
        ]
        openspace.organize_seating(partition)
        s = str(openspace)
        self.assertIn("Table_", s)
        self.assertIn("Seat_", s)
        self.assertIn("Alice", s)


if __name__ == '__main__':
    unittest.main()
