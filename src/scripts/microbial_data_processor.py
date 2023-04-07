import pandas as pd
from typing import List, Dict, Tuple
from collections import namedtuple

Contamination = namedtuple("Contamination", ["items"])
Plant = namedtuple("Plant", ["items"])


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from an Excel file and return as a Pandas DataFrame.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        pd.DataFrame: The data read from the Excel file.
    """
    return pd.read_excel(file_path)


def extract_contamination_and_plant(data: pd.DataFrame) -> Tuple[Contamination, Plant]:
    """
    Extract Contamination and Plant lists from a DataFrame.

    Args:
        data (pd.DataFrame): The DataFrame to extract from.

    Returns:
        Tuple[Contamination, Plant]: The Contamination and Plant lists.
    """
    Contamination_items = data.iloc[0, 1:].tolist()
    Plant_items = data.iloc[1, 1:].tolist()
    return Contamination(Contamination_items), Plant(Plant_items)


def extract_filtered_samples_data(data: pd.DataFrame, pre_processed_name: str) -> List[List[float]]:
    """
    Extract filtered samples data from a DataFrame based on a pre-processed name.

    Args:
        data (pd.DataFrame): The DataFrame to extract from.
        pre_processed_name (str): The pre-processed name to filter by.

    Returns:
        List[List[float]]: The filtered samples data.
    """
    list_data = data.values.tolist()
    samples_data = list_data[2:]
    filtered_samples_data = [sample_data[1:] for sample_data in samples_data if
                             sample_data[0].startswith(pre_processed_name)]
    return filtered_samples_data


def calculate_results(Contamination: Contamination, Plant: Plant, filtered_samples_data: List[List[float]]) -> Tuple[
    Dict[str, float], Dict[str, float]]:
    """
    Calculate results based on Contamination and Plant lists and filtered samples data.

    Args:
        Contamination (Contamination): The Contamination list.
        Plant (Plant): The Plant list.
        filtered_samples_data (List[List[float]]): The filtered samples data.

    Returns:
        Tuple[Dict[str, float], Dict[str, float]]: The Contamination and Plant results.
    """
    con_dict = calculate_contamination_results(Contamination.items, filtered_samples_data)
    plant_dict = calculate_plant_results(Plant.items, filtered_samples_data)
    Con_res = {k: v for k, v in sorted(con_dict.items(), key=lambda item: item[1])}
    Plant_res = {k: v for k, v in sorted(plant_dict.items(), key=lambda item: item[1])}
    return Con_res, Plant_res


def calculate_contamination_results(Contamination_items: List[str], filtered_samples_data: List[List[float]]) -> Dict[
    str, float]:
    """
    Calculate Contamination results based on Contamination items and filtered samples data.

    Args:
        Contamination_items (List[str]): The Contamination items.
        filtered_samples_data (List[List[float]]): The filtered samples data.

    Returns:
        Dict[str, float]: The Contamination results.
    """
    post_process_res = [sum(i) for i in zip(*filtered_samples_data)]
    con_dict = {item: 0 for item in Contamination_items}
    for item, res in zip(Contamination_items, post_process_res):
        if item in con_dict:
            con_dict[item] += res
    return con_dict


def calculate_plant_results(Plant_items: List[str], filtered_samples_data: List[List[float]]) -> Dict[str, float]:
    """
    Calculate Plant results based on Plant items and filtered samples data.

    Args:
        Plant_items (List[str]): The Plant items.
        filtered_samples_data (List[List[float]]): The filtered samples data.

    Returns:
        Dict[str, float]: The Plant results.
    """
    post_process_res = [sum(i) for i in zip(*filtered_samples_data)]
    plant_dict = {item: 0 for item in Plant_items}
    for item, res in zip(Plant_items, post_process_res):
        if item in plant_dict:
            plant_dict[item] += res
    return plant_dict


if __name__ == "__main__":
    excel_file_path = "/Users/jessytsui/PycharmProjects/PKU_EMBL_tools/data/microbial_data.xlsx"
    pre_processed_name = "d__Archaea"

    data = load_data(file_path=excel_file_path)
    Contamination, Plant = extract_contamination_and_plant(data)
    filtered_samples_data = extract_filtered_samples_data(data, pre_processed_name=pre_processed_name)


    # Con_res, Plant_res = calculate_results(Contamination, Plant, filtered_samples_data)
    #
    # results = Con_res.copy()
    # results.update(Plant_res)
    # print(f'{pre_processed_name} will be processed, and the results are: {results}')
