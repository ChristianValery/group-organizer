"""
This is a test suite for the 'excel_handler' module.
It contains unit tests for the functions in the module.

To run the test suite, execute the following command:
```
python -m unittest tests.test_excel_handler
```
"""


import unittest
import os
import tempfile
import pandas as pd
import numpy as np

from backend.utils.excel_handler import (
    is_excel_file,
    has_valid_structure,
    read_file,
    process_file,
    write_file
)


class TestExcelUtils(unittest.TestCase):
    """
    Test suite for the functions in the excel_handler module.
    """

    def setUp(self):
        # Track temporary files created during tests for cleanup.
        self.temp_files = []

    def tearDown(self):
        # Remove all temporary files created.
        for file_path in self.temp_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        self.temp_files = []

    def _create_temp_excel_file(self, df: pd.DataFrame, suffix=".xlsx") -> str:
        """
        Helper method to write a DataFrame to a temporary Excel file.
        Returns the path to the created file.
        """
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        file_path = tmp.name
        # Close the file so pandas can write to it (especially on Windows).
        tmp.close()
        df.to_excel(file_path, index=False)
        self.temp_files.append(file_path)
        return file_path

    def test_is_excel_file(self):
        """
        Test that is_excel_file returns True only for files ending with '.xlsx'.
        """
        self.assertTrue(is_excel_file("data.xlsx"))
        self.assertFalse(is_excel_file("data.xls"))
        self.assertFalse(is_excel_file("data.txt"))

    def test_has_valid_structure_valid(self):
        """
        Test that a correctly structured Excel file is recognized as valid.
        """
        data = {
            "name": ["Alice", "Bob", "Charlie"],
            "compatible": ["Alice:Bob", pd.NA, pd.NA],
            "incompatible": ["Alice/Charlie", pd.NA, "Alice/Charlie"]
        }
        df = pd.DataFrame(data)
        file_path = self._create_temp_excel_file(df)
        self.assertTrue(has_valid_structure(file_path))

    def test_has_valid_structure_invalid_wrong_columns(self):
        """
        Test that a file with an incorrect number of columns is invalid.
        """
        data = {
            "name": ["Alice", "Bob"],
            "compatible": ["Alice:Bob", pd.NA]
            # Missing the 'incompatible' column.
        }
        df = pd.DataFrame(data)
        file_path = self._create_temp_excel_file(df)
        self.assertFalse(has_valid_structure(file_path))

    def test_has_valid_structure_invalid_wrong_column_names(self):
        """
        Test that a file with wrong column names is invalid.
        """
        data = {
            "Name": ["Alice", "Bob"],
            "Compatible": ["Alice:Bob", pd.NA],
            "Incompatible": ["Alice/Charlie", pd.NA]
        }
        df = pd.DataFrame(data)
        file_path = self._create_temp_excel_file(df)
        self.assertFalse(has_valid_structure(file_path))

    def test_has_valid_structure_invalid_format_in_columns(self):
        """
        Test that a file with improperly formatted compatible/incompatible values is invalid.
        """
        data = {
            "name": ["Alice", "Bob"],
            "compatible": ["Alice", pd.NA],
            "incompatible": ["Alice/Charlie", pd.NA]
        }
        df = pd.DataFrame(data)
        file_path = self._create_temp_excel_file(df)
        self.assertFalse(has_valid_structure(file_path))

    def test_read_file(self):
        """
        Test that read_file returns the expected tuples from a valid Excel file.
        """
        data = {
            "name": ["Alice", "Bob", "Charlie"],
            "compatible": ["Alice:Bob", pd.NA, pd.NA],
            "incompatible": ["Alice/Charlie", pd.NA, "Alice/Charlie"]
        }
        df = pd.DataFrame(data)
        file_path = self._create_temp_excel_file(df)
        person_names, compatible_tuples, incompatible_tuples = read_file(
            file_path)
        self.assertCountEqual(person_names, ["Alice", "Bob", "Charlie"])
        self.assertEqual(compatible_tuples, [("Alice", "Bob")])
        self.assertEqual(incompatible_tuples, [
                         ("Alice", "Charlie"), ("Alice", "Charlie")])

    def test_process_file_invalid_extension(self):
        """
        Test that process_file returns an error for a non-Excel file.
        """
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        file_path = tmp.name
        tmp.close()
        self.temp_files.append(file_path)
        success, result = process_file(file_path)
        self.assertFalse(success)
        self.assertEqual(result, "The file is not an Excel file.")

    def test_process_file_invalid_structure(self):
        """
        Test that process_file returns an error for an Excel file with an invalid structure.
        """
        data = {
            "name": ["Alice", "Bob"],
            "compatible": ["Alice:Bob", pd.NA]
            # Missing the 'incompatible' column.
        }
        df = pd.DataFrame(data)
        file_path = self._create_temp_excel_file(df)
        success, result = process_file(file_path)
        self.assertFalse(success)
        self.assertEqual(
            result, "The Excel file does not have a valid structure.")

    def test_process_file_valid(self):
        """
        Test that process_file successfully processes a correctly structured Excel file.
        """
        data = {
            "name": ["Alice", "Bob", "Charlie"],
            "compatible": ["Alice:Bob", pd.NA, pd.NA],
            "incompatible": ["Alice/Charlie", pd.NA, "Alice/Charlie"]
        }
        df = pd.DataFrame(data)
        file_path = self._create_temp_excel_file(df)
        success, result = process_file(file_path)
        self.assertTrue(success)
        expected = {
            "person_names": ["Alice", "Bob", "Charlie"],
            "compatible_tuples": [("Alice", "Bob")],
            "incompatible_tuples": [("Alice", "Charlie"), ("Alice", "Charlie")]
        }
        self.assertEqual(result, expected)

    def test_write_file(self):
        """
        Test that write_file writes the seating arrangement correctly to an Excel file.
        """
        display_dictionary = {
            "Table_1": {"Seat_1": "Alice", "Seat_2": "Bob"},
            "Table_2": {"Seat_1": "Charlie", "Seat_2": ""}
        }
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        file_path = tmp.name
        tmp.close()
        self.temp_files.append(file_path)
        write_file(file_path, display_dictionary)
        # Read the written file into a DataFrame.
        df = pd.read_excel(file_path)
        # Verify that the expected columns are present.
        self.assertIn("Table_1", df.columns)
        self.assertIn("Table_2", df.columns)
        # The DataFrame was built using lists of the dictionary values.
        # Use fillna('') to convert NaN values to empty strings for comparison.
        table1 = df["Table_1"].fillna('').tolist()
        table2 = df["Table_2"].fillna('').tolist()
        self.assertEqual(table1, ["Alice", "Bob"])
        self.assertEqual(table2, ["Charlie", ""])


if __name__ == '__main__':
    unittest.main()
