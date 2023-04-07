import pandas as pd
from typing import List, Any

def read_excel_file(filename: str) -> List[List[str]]:
    """
    Read an Excel file and return its contents as a two-dimensional list.

    Args:
        filename: The name or path of the Excel file.

    Returns:
        A list of lists, where each inner list contains the values of a row in the Excel file.

    Raises:
        ValueError: If the file does not exist or cannot be read.
    """
    try:
        df = pd.read_excel(filename, sheet_name=0, header=None)
        data = df.values.tolist()
        transposed_data = list(map(list, zip(*data)))
        return transposed_data
    except Exception as e:
        raise ValueError(f"Failed to read file {filename}: {e}")

def merge_lists(*lists: List) -> List[List[Any]]:
    """
    Merge multiple lists into a list of lists.

    Args:
        *lists: One or more lists to merge.

    Returns:
        A list of lists, where each inner list contains the elements of the corresponding input lists.

    Raises:
        ValueError: If the input lists are not of equal length.
    """
    # Check if all input lists are of the same length
    length = len(lists[0])
    if not all(len(lst) == length for lst in lists):
        raise ValueError("Input lists are not of equal length")

    # Merge the input lists into a list of lists
    merged_list = [list(x) for x in zip(*lists)]
    return merged_list

def save_list_to_file(data: List[List], filename: str) -> None:
    """
    Save a list of lists to a file using Pandas.

    Args:
        data: A list of lists to be saved.
        filename: The name or path of the file to be saved.

    Returns:
        None.

    Raises:
        ValueError: If the specified filetype is not supported.
    """
    # Create a DataFrame from the input data
    df = pd.DataFrame(data)
    filetype = filename.split(".")[-1]

    # Save the DataFrame to a file
    if filetype == 'xlsx':
        df.to_excel(filename, index=False, header=False)
    elif filetype == 'csv':
        df.to_csv(filename, index=False, header=False)
    else:
        raise ValueError(f"Unsupported filetype: {filetype}")

if __name__ == "__main__":
    # Example usage
    filename = "../../data/microbial_data.xlsx"
    output = "../../data/output.xlsx"
    res = []
    try:
        data = read_excel_file(filename)
        print(f"Contents of {filename}:")
        for row in data[:10]:
            res.append(row)
            # print(row)
    except ValueError as e:
        print(f"Error: {e}")

    print(merge_lists(res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9]))
    print(merge_lists(*res))

    pre_saved_data = merge_lists(*res)
    save_list_to_file(data=pre_saved_data, filename=output)
