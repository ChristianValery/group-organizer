"""
This is a test suite for the 'excel_handler' module.
It contains unit tests for the functions in the module.

To run the test suite, execute the following command:
```
$ python -m unittest tests.test_excel_handler
```
"""

import os
import tempfile
import unittest
import pandas as pd

from backend.utils.excel_handler import (
    is_excel_file,
    has_valid_structure,
    read_file,
    process_file,
    write_file
)


class TestExcelModule(unittest.TestCase):
    """Unit tests for the 'excel_handler' module."""

    def setUp(self):
        """This method is called before each test."""
        # Create a temporary directory to store our test Excel files.
        self.test_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.test_dir.cleanup)

    def create_excel_file(self, df: pd.DataFrame, filename: str = "temp.xlsx") -> str:
        """
        Helper function to write a DataFrame to an Excel file in the temporary directory.
        Returns the file path.
        """
        file_path = os.path.join(self.test_dir.name, filename)
        df.to_excel(file_path, index=False)
        return file_path

    def test_is_excel_file(self):
        """Test the 'is_excel_file' function."""
        self.assertTrue(is_excel_file("example.xlsx"))
        self.assertFalse(is_excel_file("example.txt"))

    def test_has_valid_structure_valid(self):
        """
        Test the 'has_valid_structure' function with a valid Excel file.
        """
        # Create a DataFrame with the valid structure.
        data = {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "compatible": ["Bob:Charlie", None, None, None, None],
            "incompatible": [None, "David/Eve", None, None, None],
        }
        df = pd.DataFrame(data)
        file_path = self.create_excel_file(df, "valid.xlsx")
        self.assertTrue(has_valid_structure(file_path))

    def test_has_valid_structure_invalid_wrong_columns(self):
        """
        Test the 'has_valid_structure' function with an Excel file with invalid columns.
        """
        # Create a DataFrame with only 2 columns.
        data = {
            "name": ["Alice", "Bob"],
            "compatible": ["Bob:Charlie", None],
        }
        df = pd.DataFrame(data)
        file_path = self.create_excel_file(df, "invalid_columns.xlsx")
        self.assertFalse(has_valid_structure(file_path))

    def test_has_valid_structure_invalid_wrong_format(self):
        """
        Test the 'has_valid_structure' function with an Excel file with invalid format.
        """
        # Create a DataFrame where the 'compatible' column does not use a colon.
        data = {
            "name": ["Alice", "Bob", "Charlie"],
            "compatible": ["Bob-Charlie", None, None],  # Wrong delimiter here.
            "incompatible": [None, None, None],
        }
        df = pd.DataFrame(data)
        file_path = self.create_excel_file(df, "invalid_format.xlsx")
        self.assertFalse(has_valid_structure(file_path))

    def test_read_file(self):
        """Test the 'read_file' function."""
        data = {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "compatible": ["Bob:Charlie", None, None, None, None],
            "incompatible": [None, "David/Eve", None, None, None],
        }
        df = pd.DataFrame(data)
        file_path = self.create_excel_file(df, "read.xlsx")
        person_names, compatible_pairs, incompatible_pairs = read_file(
            file_path)

        expected_names = {"Alice", "Bob", "Charlie", "David", "Eve"}
        self.assertEqual(person_names, expected_names)
        self.assertEqual(len(compatible_pairs), 1)
        self.assertEqual(compatible_pairs[0], {"Bob", "Charlie"})
        self.assertEqual(len(incompatible_pairs), 1)
        self.assertEqual(incompatible_pairs[0], {"David", "Eve"})

    def test_process_file_valid(self):
        """Test the 'process_file' function with a valid Excel file."""
        data = {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "compatible": ["Bob:Charlie", None, None, None, None],
            "incompatible": [None, "David/Eve", None, None, None],
        }
        df = pd.DataFrame(data)
        file_path = self.create_excel_file(df, "process_valid.xlsx")
        success, result = process_file(file_path)

        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["person_names"], {
                         "Alice", "Bob", "Charlie", "David", "Eve"})
        self.assertEqual(len(result["compatible_pairs"]), 1)
        self.assertEqual(result["compatible_pairs"][0], {"Bob", "Charlie"})
        self.assertEqual(len(result["incompatible_pairs"]), 1)
        self.assertEqual(result["incompatible_pairs"][0], {"David", "Eve"})

    def test_process_file_invalid(self):
        """
        Test the 'process_file' function with an invalid Excel file.
        """
        # Create a dummy file with an invalid extension.
        file_path = os.path.join(self.test_dir.name, "invalid.txt")
        with open(file_path, "w", encoding="utf8") as f:
            f.write("This is not an Excel file.")
        success, result = process_file(file_path)
        self.assertFalse(success)
        self.assertIsInstance(result, str)

    def test_write_file(self):
        """Test the 'write_file' function."""
        # Create a sample display dictionary.
        display_dict = {
            "Table1": {"Seat1": "Alice", "Seat2": "Bob"},
            "Table2": {"Seat1": "Charlie", "Seat2": "David"},
        }
        file_path = os.path.join(self.test_dir.name, "write.xlsx")
        write_file(file_path, display_dict)

        # Read back the written Excel file.
        df = pd.read_excel(file_path)
        # The DataFrame should have columns corresponding to the dictionary keys.
        self.assertListEqual(list(df.columns), ["Table1", "Table2"])
        # Check that the data matches.
        self.assertEqual(df["Table1"].tolist(), ["Alice", "Bob"])
        self.assertEqual(df["Table2"].tolist(), ["Charlie", "David"])


if __name__ == "__main__":
    unittest.main()
