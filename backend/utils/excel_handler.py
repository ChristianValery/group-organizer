"""
Description: This module contains functions to handle Excel files.

Functions:
- is_excel_file(file_path: str) -> bool:
    checks if the file at the given path is an Excel file.
- has_valid_structure(file_path: str) -> bool:
    checks if the Excel file has a valid structure for seating arrangement.
- read_file(file_path: str) -> Tuple[Set[str], List[Set[str]], List[Set[str]]]:
    reads an Excel file containing the names of people and their compatibility constraints.
- process_file(file_path: str) -> 
        Tuple[bool, Union[Dict[str, Union[Set[str], List[Set[str]]]], str]]:
    processes an Excel file containing the names of people and their compatibility constraints.
- write_file(file_path: str, display_dictionary: Dict[str, Dict[str, str]]) -> None:
    writes the seating arrangement to an Excel file.
"""

from typing import Dict, List, Tuple, Union
import pandas as pd


def is_excel_file(file_path: str) -> bool:
    """
    Checks if the file at the given path is an Excel file.

    Parameters:
    -----------
    file_path : str
        The path to the file to check.

    Returns:
    --------
    bool
        True if the file is an Excel file, False otherwise.
    """
    return file_path.endswith('.xlsx')


def has_valid_structure(file_path: str) -> bool:
    """
    Checks if the Excel file has a valid structure for seating arrangement.

    Parameters:
    -----------
    file_path : str
        The path to the Excel file.

    Returns:
    --------
    bool
        True if the Excel file has a valid structure, False otherwise.
    """
    df = pd.read_excel(file_path)
    # Check if the dataframe has 3 columns
    if df.shape[1] != 3:
        return False
    # Check if the columns have the correct names
    if any(
        (df.columns[0] != 'name',
         df.columns[1] != 'compatible',
         df.columns[2] != 'incompatible')):
        return False
    # Check if the first column has at least one non-null value
    if not any(df.iloc[:, 0].notnull()):
        return False
    # Check if all non-null values in the whole dataframe are strings
    non_null_values = df.iloc[:, :].values.flatten(
    )[df.iloc[:, :].notnull().values.flatten()]
    if not all((isinstance(value, str) for value in non_null_values)):
        return False
    # Remove trailing and leading whitespaces from the strings
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    # Check if the names in the first column are unique
    if len(df.iloc[:, 0].dropna().unique()) != df.iloc[:, 0].dropna().shape[0]:
        return False
    # Check if each non-null value in the second column has the format 'name:name'
    if not all(df.iloc[:, 1][df.iloc[:, 1].notnull()].apply(
            lambda x: len(x.split(':')) == 2).tolist()):
        return False
    # Check if each non-null value in the third column has the format 'name/name'
    if not all(df.iloc[:, 2][df.iloc[:, 2].notnull()].apply(
            lambda x: len(x.split('/')) == 2).tolist()):
        return False
    # Set of all names in the first column
    names = set(df.iloc[:, 0].dropna())
    # List of all pairs of names in the second column
    compatible_pairs = df.iloc[:, 1][df.iloc[:, 1].notnull()].apply(
        lambda x: set(x.split(':'))).tolist()
    compatible_names = [name for pair in compatible_pairs for name in pair]
    # List of all pairs of names in the third column
    incompatible_pairs = df.iloc[:, 2][df.iloc[:, 2].notnull()].apply(
        lambda x: set(x.split('/'))).tolist()
    incompatible_names = [name for pair in incompatible_pairs for name in pair]
    # Check if all names in the second and third columns are in the first column
    if not all(name in names for name in compatible_names + incompatible_names):
        return False
    return True


def read_file(file_path: str) -> Tuple[List[str], List[Tuple[str]], List[Tuple[str]]]:
    """
    Reads an Excel file containing the names of people and their compatibility constraints.
    Returns a tuple containing the list of person names, the list of compatible tuples,
    and the list of incompatible tuples.

    Parameters:
    -----------
    file_path : str
        The path to the Excel file to read.

    Returns:
    --------
    Tuple[List[str], List[Tuple[str]], List[Tuple[str]]]
        A tuple containing the list of person names, the list of compatible tuples,
        and the list of incompatible tuples.
    """
    df = pd.read_excel(file_path)
    # Get the list of person names from the first column of the dataframe
    person_names = df.iloc[:, 0][df.iloc[:, 0].notnull()].tolist()
    # Get list of compatible tuples from the second column of the dataframe
    compatible_tuples = df.iloc[:, 1][df.iloc[:, 1].notnull()].apply(
        lambda x: tuple(x.split(':'))).tolist()
    # Get list of incompatible pairs from the third column of the dataframe
    incompatible_tuples = df.iloc[:, 2][df.iloc[:, 2].notnull()].apply(
        lambda x: tuple(x.split('/'))).tolist()
    return person_names, compatible_tuples, incompatible_tuples


def process_file(file_path: str) -> \
        Tuple[bool, Union[Dict[str, Union[List[str], List[Tuple[str]]]], str]]:
    """
    Processes an Excel file containing the names of people and their compatibility constraints.
    Returns a tuple containing a boolean indicating if the file was processed successfully
    and a dictionary containing the person names, compatible pairs, and incompatible pairs.

    Parameters:
    -----------
    file_path : str
        The path to the Excel file to process.
    
    Returns:
    --------
    Tuple[bool, Union[Dict[str, Union[Set[str], List[Set[str]]]], str]]
        A tuple containing a boolean indicating if the file was processed successfully
        and a dictionary containing the person names, compatible pairs, and incompatible pairs.
    """
    if not is_excel_file(file_path):
        return False, "The file is not an Excel file."
    if not has_valid_structure(file_path):
        return False, "The Excel file does not have a valid structure."
    person_names, compatible_tuples, incompatible_tuples = read_file(file_path)
    return True, {
        "person_names": person_names,
        "compatible_tuples": compatible_tuples,
        "incompatible_tuples": incompatible_tuples
    }


def write_file(file_path: str, display_dictionary: Dict[str, Dict[str, str]]) -> None:
    """
    Writes the seating arrangement to an Excel file.

    Parameters:
    -----------
    file_path : str
        The path to the Excel file to write.
    display_dictionary : Dict[str, Dict[str, str]]
        A dictionary representing the seating arrangement in the open space.

    Returns:
    --------
    None
    """
    df = pd.DataFrame({key: list(value.values())
                      for key, value in display_dictionary.items()})
    df.to_excel(file_path, index=False)
