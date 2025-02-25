"""
This module contains a function that partitions people into groups, 
according to compatibility constraints.

The function uses the Google OR-Tools CP-SAT solver to find a solution 
that satisfies the constraints.
"""

from typing import List, Tuple
from ortools.sat.python import cp_model


def partition_people(
        person_names: List[str],
        compatible_pairs: List[Tuple[str, str]],
        incompatible_pairs: List[Tuple[str, str]],
        capacity: int
) -> List[List[str]]:
    """
    Partitions people into groups according to compatibility constraints.
    Parameters:
    -----------
    person_names : List[str]
        The names of people to partition.
    compatible_pairs : List[Tuple[str, str]]
        Pairs of people who should be in the same group.
    incompatible_pairs : List[Tuple[str, str]]
        Pairs of people who should not be in the same group.
    capacity : int
        The maximum number of people in each group.
   
    Returns:
    --------
    List[List[str]]
        A list of groups of people that satisfy the constraints
        or an empty list if no solution is found.
    """
    # Create a CP-SAT model
    model = cp_model.CpModel()
    num_people = len(person_names)
    num_groups = num_people // capacity + (1 if num_people % capacity else 0)

    # Create a variable for each person representing the group they belong to
    people = [model.NewIntVar(
        0, num_groups - 1, f"person_{i}") for i in range(num_people)]

    # Add constraints for compatible pairs
    for person1, person2 in compatible_pairs:
        model.Add(people[person_names.index(person1)] ==
                  people[person_names.index(person2)])

    # Add constraints for incompatible pairs
    for person1, person2 in incompatible_pairs:
        model.Add(people[person_names.index(person1)] !=
                  people[person_names.index(person2)])

    # Indicator variables for group membership and enforce group sizes
    is_in_group = [[model.NewBoolVar(f"is_{person}_in_group_{group}") \
         for group in range(num_groups)] for person in person_names]

    # Each person must be in exactly one group
    for i, person in enumerate(person_names):
        model.Add(sum(is_in_group[i]) == 1)
        # Link the indicator variables to the people variables
        for group in range(num_groups):
            model.Add(people[i] == group).OnlyEnforceIf(is_in_group[i][group])
            model.Add(people[i] != group).OnlyEnforceIf(
                is_in_group[i][group].Not())

    # Each group must have at least one person and not exceed capacity
    for group in range(num_groups):
        group_members = [is_in_group[i][group] for i in range(num_people)]
        model.Add(sum(group_members) >= 1)
        model.Add(sum(group_members) <= capacity)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        groups = [[] for _ in range(num_groups)]
        for i, person in enumerate(person_names):
            assigned_group = solver.Value(people[i])
            groups[assigned_group].append(person)
        # Remove any empty groups
        return [group for group in groups if group]
    else:
        return []
