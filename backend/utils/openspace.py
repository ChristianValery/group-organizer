"""
Description:
    This module contains the Openspace class, which represents an open space with multiple tables.
    The open space can be used to organize the seating of people according to certain constraints.
"""

from typing import List, Dict
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
            partition: List[List[str]]
    ) -> None:
        """
        Organizes seating according to the given partition.
        
        Parameters:
        -----------
        partition : List[List[str]]
            A list of groups of people to seat at the tables.
        
        Returns:
        --------
        None
        """
        if len(partition) > self.num_tables:
            raise ValueError("The number of groups exceeds the number of tables.")
        if any(len(group) > self.table_capacity for group in partition):
            raise ValueError("A group exceeds the table capacity.")
        if sum(len(group) for group in partition) > self.num_tables * self.table_capacity:
            raise ValueError("The total number of people exceeds the total seating capacity.")

        shuffle_tables = sample(self.tables, len(self.tables))
        # Assign each group to a table
        for table, group in zip(shuffle_tables, partition):
            table.set_occupants(group)

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
