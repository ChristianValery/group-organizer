"""
Description:
    This module contains the Table class, which represents a table in an open space.
    Each table has a unique table_id and can have multiple seats, each represented by a Seat object.
"""


from typing import List

from backend.utils.seat import Seat


class Table:
    """
    Class to represent a table in an open space.

    Attributes:
    - table_id (int): the table's id.
    - capacity (int): the number of seats at the table.
    - seats (List[Seat]): a list of Seat objects representing the table's seats.
    - occupants (List[str]): a list of the names of the people occupying the table's seats.

    Methods:
    - left_capacity():
        returns the number of free seats at the table.
    - has_free_seats():
        returns True if there are free seats at the table, False otherwise.
    - set_occupant(person_name: str):
        sets the table's next free seat's occupant to person_name.
        Raises a ValueError if all seats are already occupied.
    - set_occupants(person_names: List[str]):
        sets the table's next free seats' occupants to person_names.
    - __repr__():
        returns a string representation of the table.
    
    Example usage:
    >>> table = Table(table_id=1, capacity=4)
    >>> table.set_occupant("Alice")
    >>> table.set_occupant("Bob")
    >>> table.set_occupant("Charlie")
    >>> table.set_occupant("David")
    Traceback (most recent call last):
        ...
    ValueError: Table 1 is already full!
    >>> table.left_capacity()
    0
    >>> table.has_free_seats()
    False
    >>> table.seats
    [
        Seat(seat_id=(1, 1), occupied_by='Alice'),
        Seat(seat_id=(1, 2), occupied_by='Bob'),
        Seat(seat_id=(1, 3), occupied_by='Charlie'),
        Seat(seat_id=(1, 4), occupied_by='David')
    ]
    >>> print(table)
    Table(
        table_id=1,
        capacity=4, 
        seats=[
            Seat(seat_id=(1, 1), occupied_by='Alice'),
            Seat(seat_id=(1, 2), occupied_by='Bob'),
            Seat(seat_id=(1, 3), occupied_by='Charlie'),
            Seat(seat_id=(1, 4), occupied_by='David')
            ]
        )
    >>> another_table = Table(table_id=2, capacity=4)
    >>> print(another_table)
    Table(
        table_id=2,
        capacity=4,
        seats=[
            Seat(seat_id=(2, 1), occupied_by=None),
            Seat(seat_id=(2, 2), occupied_by=None),
            Seat(seat_id=(2, 3), occupied_by=None),
            Seat(seat_id=(2, 4), occupied_by=None)
            ]
        )
    >>> another_table.set_occupants(["Eve", "Frank", "Grace"])
    >>> print(another_table)
    Table(
        table_id=2,
        capacity=4,
        seats=[
            Seat(seat_id=(2, 1), occupied_by='Eve'),
            Seat(seat_id=(2, 2), occupied_by='Frank'),
            Seat(seat_id=(2, 3), occupied_by='Grace'),
            Seat(seat_id=(2, 4), occupied_by=None)
            ]
        )
    >>> another_table.set_occupants(["Hank", "Ivy", "Jack"])
    Traceback (most recent call last):
        ...
    ValueError: Not enough free seats at table 2!
    """

    def __init__(self, table_id: int, capacity: int):
        self.table_id = table_id
        self.capacity = capacity
        self.seats = [Seat(seat_id=(table_id, i))
                      for i in range(1, capacity + 1)]
        self.occupants = []

    def left_capacity(self) -> int:
        """
        Returns the number of free seats at the table.

        Returns:
        --------
        int
            The number of free seats at the table.
        """
        return sum(seat.occupied_by is None for seat in self.seats)

    def has_free_seats(self) -> bool:
        """
        Returns True if there are free seats at the table, False otherwise.

        Returns:
        --------
        bool
            True if there are free seats at the table, False otherwise.
        """
        return any(seat.occupied_by is None for seat in self.seats)

    def set_occupant(self, person_name: str):
        """
        Sets the table's next free seat's occupant to person_name.

        Raises:
        - ValueError: if all seats are already occupied.

        Parameters:
        -----------
        person_name : str
            The name of the person to occupy the seat.
        
        Returns:
        --------
        None
        """
        free_seats = [seat for seat in self.seats if seat.occupied_by is None]
        if free_seats:
            free_seats[0].set_occupant(person_name)
            self.occupants.append(person_name)
        else:
            raise ValueError(f"Table {self.table_id} is already full!")

    def set_occupants(self, person_names: List[str]):
        """
        Sets the table's next free seats' occupants to person_names.
        
        Raises:
        - ValueError: if there are not enough free seats at the table.

        Parameters:
        -----------
        person_names : List[str]
            The names of the people to occupy the seats.
        
        Returns:
        --------
        None
        """
        if len(person_names) <= self.left_capacity():
            for person_name in person_names:
                self.set_occupant(person_name)
        else:
            raise ValueError(
                f"Not enough free seats at table {self.table_id}!")

    def __repr__(self):
        return (f"Table(table_id={self.table_id}, capacity={self.capacity}, "
                f"seats={self.seats}, occupants={self.occupants})")

    def __str__(self) -> str:
        seat_str = ",\n    ".join(str(seat) for seat in self.seats)
        return (f"Table(\n"
                f"  table_id={self.table_id},\n"
                f"  capacity={self.capacity},\n"
                f"  seats=[\n    {seat_str}\n  ],\n"
                f"  occupants={self.occupants}\n)")
