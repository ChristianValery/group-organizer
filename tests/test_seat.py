"""
This is a test suite for the Seat class.

To run this script, run `python -m unittest tests/test_seat.py` from the project root directory.
"""

import unittest

from backend.utils.seat import Seat


class TestSeat(unittest.TestCase):
    """Tests for the Seat class."""

    def setUp(self):
        self.valid_seat_id = (1, 1)
        self.seat = Seat(self.valid_seat_id)

    def test_initial_state(self):
        """Test that a new seat is created with the correct initial state."""
        self.assertEqual(self.seat.seat_id, self.valid_seat_id)
        self.assertIsNone(self.seat.occupied_by)

    def test_invalid_seat_id(self):
        """Test that invalid seat_id values raise a TypeError."""
        with self.assertRaises(TypeError):
            Seat("invalid")  # Not a tuple

        with self.assertRaises(TypeError):
            Seat((1, "a"))  # Second element is not an int

        with self.assertRaises(TypeError):
            Seat((1,))  # Tuple does not have two elements

        with self.assertRaises(TypeError):
            Seat((1, 2, 3))  # Tuple has too many elements

    def test_set_occupant_success(self):
        """Test that setting an occupant on an unoccupied seat works correctly."""
        self.seat.set_occupant("Alice")
        self.assertEqual(self.seat.occupied_by, "Alice")

    def test_set_occupant_already_occupied(self):
        """
        Test that attempting to set an occupant on an already occupied seat raises a ValueError.
        """
        self.seat.set_occupant("Alice")
        with self.assertRaises(ValueError) as context:
            self.seat.set_occupant("Bob")
        self.assertIn("already occupied", str(context.exception))

    def test_remove_occupant(self):
        """
        Test that remove_occupant returns None when the seat is empty, 
        and the occupant's name when occupied.
        """
        # Removing occupant from an empty seat should return None.
        self.assertIsNone(self.seat.remove_occupant())

        # Set an occupant and then remove.
        self.seat.set_occupant("Alice")
        removed = self.seat.remove_occupant()
        self.assertEqual(removed, "Alice")
        self.assertIsNone(self.seat.occupied_by)

    def test_repr(self):
        """Test that __repr__ returns the expected string representation."""
        self.assertEqual(
            repr(self.seat), "Seat(seat_id=(1, 1), occupied_by=None)")
        self.seat.set_occupant("Alice")
        # Note: __repr__ does not add extra quotes around string attributes.
        self.assertEqual(
            repr(self.seat), "Seat(seat_id=(1, 1), occupied_by=Alice)")

    def test_str(self):
        """Test that __str__ returns a human-readable string representation."""
        self.assertEqual(str(self.seat), "Seat (1, 1) is unoccupied.")
        self.seat.set_occupant("Alice")
        self.assertEqual(str(self.seat), "Seat (1, 1) is occupied by Alice.")

    def test_equality(self):
        """Test the __eq__ method for Seat objects."""
        seat1 = Seat((1, 1), "Alice")
        seat2 = Seat((1, 1), "Alice")
        seat3 = Seat((1, 1))
        seat4 = Seat((2, 1), "Alice")

        self.assertEqual(seat1, seat2)
        self.assertNotEqual(seat1, seat3)
        self.assertNotEqual(seat1, seat4)


if __name__ == '__main__':
    unittest.main()
