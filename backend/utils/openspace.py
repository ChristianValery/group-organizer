"""
Description:
    This module contains the Openspace class, which represents an open space with multiple tables.
    The open space can be used to organize the seating of people according to certain constraints.
"""

from typing import List, Dict, Set
from random import sample

from utils.table import Table


class Openspace:
    """
    Class to represent an open space with multiple tables.

    Attributes:
    -----------
      - num_tables (int): number of tables in the open space.
      - table_capacity (int): number of seats at each table.
      - tables (List[Table]): list of Table objects in the open space.
    
    Methods:
    --------
      - organize_seating(person_names, compatible_pairs, incompatible_pairs):
          Organizes seating according to the given constraints.
      - display_seating():
          Returns a dictionary representing the seating arrangement.
      - __repr__():
          Returns a string representation of the open space.
    """

    def __init__(self, num_tables: int, table_capacity: int):
        self.num_tables = num_tables
        self.table_capacity = table_capacity
        self.tables = [Table(table_id=i, capacity=self.table_capacity)
                       for i in range(1, self.num_tables + 1)]

    def organize_seating(
            self,
            person_names: Set[str],
            compatible_pairs: List[Set[str]],
            incompatible_pairs: List[Set[str]]):
        """
        Organizes seating of people in the open space according to the given constraints.

        Parameters:
        -----------
          - person_names: Set[str] -- names of people to be seated.
          - compatible_pairs: List[Set[str]] -- pairs who should be seated together.
          - incompatible_pairs: List[Set[str]] -- pairs who should not be seated together.
        
        Returns:
        --------
            None
        
        Raises:
        -------
            ValueError: if constraints cannot be satisfied due to insufficient seats.
        """
        # Check overall capacity.
        total_seats = sum(table.capacity for table in self.tables)
        if len(person_names) > total_seats:
            raise ValueError("Not enough seats available in the open space!")

        names_to_assign = person_names.copy()

        # Assign incompatible pairs to different tables.
        for pair in incompatible_pairs:
            # Unpack without modifying the original set.
            name_1, name_2 = tuple(pair)
            available_tables = [
                table for table in self.tables if table.left_capacity() >= 1]
            if len(available_tables) < 2:
                raise ValueError(
                    "Not enough tables available for incompatible pair assignment!")
            table_1, table_2 = sample(available_tables, 2)
            table_1.set_occupant(name_1)
            table_2.set_occupant(name_2)
            names_to_assign.remove(name_1)
            names_to_assign.remove(name_2)

        # Assign compatible pairs to the same table.
        for pair in compatible_pairs:
            name_1, name_2 = tuple(pair)
            available_tables = [
                table for table in self.tables if table.left_capacity() >= 2]
            if not available_tables:
                raise ValueError(
                    "Not enough seats available for compatible pair assignment!")
            table = sample(available_tables, 1)[0]
            table.set_occupants([name_1, name_2])
            names_to_assign.remove(name_1)
            names_to_assign.remove(name_2)

        # Assign remaining names.
        for name in names_to_assign:
            available_tables = [
                table for table in self.tables if table.left_capacity() >= 1]
            if not available_tables:
                raise ValueError(
                    "Not enough seats available for remaining assignments!")
            table = sample(available_tables, 1)[0]
            table.set_occupant(name)

    def display_seating(self) -> Dict[str, Dict[str, str]]:
        """
        Returns a dictionary representing the seating arrangement.

        Returns:
          Dict[str, Dict[str, str]]: Keys are table identifiers and values are
          dictionaries mapping seat numbers to occupant names.
        """
        display_dictionary = {}
        for table in self.tables:
            seat_names = [f"Seat_{seat.seat_id[1]}" for seat in table.seats]
            occupants = [
                '' if seat.occupied_by is None else seat.occupied_by for seat in table.seats
            ]
            display_dictionary[f"Table_{table.table_id}"] = dict(
                zip(seat_names, occupants))
        return display_dictionary

    def __repr__(self):
        return (f"Openspace(num_tables={self.num_tables}, table_capacity={self.table_capacity}, "
                f"tables={self.tables})")

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the seating arrangement.
        """
        seating = self.display_seating()
        lines = []
        for table, seats in seating.items():
            # For each seat, display its name and occupant (or 'Empty' if unoccupied).
            seat_details = ", ".join(f"{seat}: {occupant if occupant else 'Empty'}"
                                     for seat, occupant in seats.items())
            lines.append(f"{table}: {seat_details}")
        return "\n".join(lines)
