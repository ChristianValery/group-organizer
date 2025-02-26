"""
Test suite for the partition_people function in the partition module.

To run this test suite, run the following command from the project root:
```
python -m unittest tests.test_partition
```
"""


import unittest
from backend.utils.partition import partition_people


class TestPartitionPeople(unittest.TestCase):
    """
    Test suite for the partition_people function.
    """

    def test_no_constraints(self):
        """
        Test partitioning with no compatibility or incompatibility constraints.
        """
        person_names = ["Alice", "Bob", "Charlie", "David"]
        compatible_pairs = []
        incompatible_pairs = []
        capacity = 2
        groups = partition_people(
            person_names, compatible_pairs, incompatible_pairs, capacity)

        # Check that all persons appear in some group.
        grouped_persons = [person for group in groups for person in group]
        self.assertCountEqual(grouped_persons, person_names)

        # Check that no group exceeds the capacity.
        for group in groups:
            self.assertLessEqual(len(group), capacity)

    def test_compatible_pairs(self):
        """Test that people required to be together end up in the same group."""
        person_names = ["Alice", "Bob", "Charlie", "David"]
        compatible_pairs = [("Alice", "Bob")]
        incompatible_pairs = []
        capacity = 3
        groups = partition_people(
            person_names, compatible_pairs, incompatible_pairs, capacity)

        # Find the groups for Alice and Bob.
        group_alice = group_bob = None
        for group in groups:
            if "Alice" in group:
                group_alice = group
            if "Bob" in group:
                group_bob = group

        self.assertIsNotNone(group_alice)
        self.assertIsNotNone(group_bob)
        self.assertEqual(group_alice, group_bob,
                         "Alice and Bob should be in the same group.")

    def test_incompatible_pairs(self):
        """
        Test that people required to be separate end up in different groups.
        """
        person_names = ["Alice", "Bob", "Charlie", "David"]
        compatible_pairs = []
        incompatible_pairs = [("Alice", "Bob")]
        capacity = 3
        groups = partition_people(
            person_names, compatible_pairs, incompatible_pairs, capacity)

        # Find the groups for Alice and Bob.
        group_alice = group_bob = None
        for group in groups:
            if "Alice" in group:
                group_alice = group
            if "Bob" in group:
                group_bob = group

        self.assertIsNotNone(group_alice)
        self.assertIsNotNone(group_bob)
        self.assertNotEqual(group_alice, group_bob,
                            "Alice and Bob should not be in the same group.")

    def test_unsolvable_constraints(self):
        """
        Test that contradictory constraints (being forced to be together and apart)
        result in no solution.
        """
        person_names = ["Alice", "Bob"]
        compatible_pairs = [("Alice", "Bob")]
        incompatible_pairs = [("Alice", "Bob")]
        capacity = 2
        groups = partition_people(
            person_names, compatible_pairs, incompatible_pairs, capacity)
        self.assertEqual(
            groups, [], "Expected no solution due to contradictory constraints.")

    def test_all_in_one_group(self):
        """
        Test that when the capacity is larger than the number of people,
        all people are grouped together.
        """
        person_names = ["Alice", "Bob", "Charlie"]
        compatible_pairs = []
        incompatible_pairs = []
        capacity = 5  # More than the number of persons.
        groups = partition_people(
            person_names, compatible_pairs, incompatible_pairs, capacity)
        self.assertEqual(
            len(groups), 1, "All people should be in a single group.")
        self.assertCountEqual(groups[0], person_names)


if __name__ == '__main__':
    unittest.main()
