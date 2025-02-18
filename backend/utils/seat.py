"""
This module contains the Seat class, which represents a seat in an open space.
Each seat has a unique seat_id and can be occupied by one person.
"""

from typing import Optional, Tuple


class Seat:
    """
    Class to represent a seat in an open space.

    Attributes:
    - seat_id (Tuple[int, int]):
        a tuple representing the seat's id in the format (table_id, seat_number).
    - occupied_by (str): the name of the person occupying the seat, or None if the seat is empty.

    Methods:
    - set_occupant(person_name: str):
        sets the seat's occupant to person_name.
        Raises a ValueError if the seat is already occupied.
    - remove_occupant():
        removes the seat's occupant and returns their name, or None if the seat is empty.
    - __repr__():
        returns a string representation of the seat.
    - __str__():
        returns a human-readable string representation of the seat.

    Example usage:
    >>> seat = Seat(seat_id=(1, 1))
    >>> seat.set_occupant("Alice")
    >>> seat.occupied_by
    "Alice"
    >>> seat.set_occupant("Bob")
    Traceback (most recent call last):
        ...
    ValueError: Seat (1, 1) is already occupied by Alice.
    >>> print(seat)
    Seat(seat_id=(1, 1), occupied_by='Alice')
    >>> seat.remove_occupant()
    "Alice"
    >>> seat.occupied_by
    None
    >>> print(seat)
    Seat(seat_id=(1, 1), occupied_by=None)
    """

    def __init__(self, seat_id: Tuple[int, int], occupied_by: Optional[str] = None):
        if not (isinstance(seat_id, tuple) and
                len(seat_id) == 2 and all(isinstance(i, int) for i in seat_id)):
            raise TypeError(
                "seat_id must be a tuple of two integers (table_id, seat_number)")
        self.seat_id = seat_id
        self.occupied_by = occupied_by

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Seat):
            return self.seat_id == other.seat_id and self.occupied_by == other.occupied_by
        return False

    def set_occupant(self, person_name: str):
        """
        Sets the seat's occupant to person_name.

        Raises:
        - ValueError: if the seat is already occupied.

        Parameters:
        -----------
        person_name : str
            The name of the person to occupy the seat.
        
        Returns:
        --------
        None
        """
        if self.occupied_by is not None:
            raise ValueError(
                f"Seat {self.seat_id} is already occupied by {self.occupied_by}.")
        else:
            self.occupied_by = person_name

    def remove_occupant(self) -> Optional[str]:
        """
        Removes the seat's occupant and returns their name.

        Returns:
        --------
        str or None
            The name of the person who was occupying the seat, or None if the seat was empty.
        """
        if self.occupied_by is not None:
            person_name = self.occupied_by
            self.occupied_by = None
            return person_name
        else:
            return None

    def __repr__(self):
        """
        Returns a string representation of the seat.
        """
        return f"Seat(seat_id={self.seat_id}, occupied_by={self.occupied_by})"

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the seat.
        """
        status = f"occupied by {self.occupied_by}" if self.occupied_by else "unoccupied"
        return f"Seat {self.seat_id} is {status}."
