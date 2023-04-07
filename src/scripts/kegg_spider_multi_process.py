import os
import warnings
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_txt_files(root_dir):
    """
    Get a list of all txt files in the root directory and its subdirectories.

    Args:
        root_dir: A string representing the root directory to start searching.

    Returns:
        A list of strings representing the paths of all txt files found.
    """
    txt_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files


def save_data(data: List[Tuple], file_path: str) -> None:
    """
    Save data to file.

    Args:
        data: A list of tuples representing the data to be saved.
        file_path: A string representing the file path to save the data.

    Returns:
        None.
    """
    file_type = file_path.split('.')[-1]
    if file_type == 'csv':
        df = pd.DataFrame(data, columns=['id', 'link', 'text', 'state', 'title', 'big_title'])
        df.to_csv(file_path, index=False)
    elif file_type == 'txt':
        with open(file_path, 'w') as f:
            for row in data:
                f.write('\t'.join([str(i) for i in row]) + '\n')
    else:
        print(f'Unsupported file type: {file_type}')


def run_mapper(driver_path: str, base_url: str, input_file: str, output_file: str) -> None:
    warnings.filterwarnings('ignore', category=DeprecationWarning)

    # Set up Chrome driver options and service.
    service = Service(driver_path)

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')

    # Create Chrome browser instance.
    driver = webdriver.Chrome(service=service, options=options)

    # Open the mapper website.
    driver.get(url=base_url)
    driver.implicitly_wait(10)

    # Upload the input text file.
    upload_element = driver.find_element("xpath", '//input[@type="file"]')
    file_path = os.path.abspath(input_file)
    upload_element.send_keys(file_path)
    driver.implicitly_wait(10)

    # Submit the upload.
    submit_button = driver.find_element("xpath", '//input[@type="submit"]')
    submit_button.click()
    driver.implicitly_wait(10)

    # Click the target button.
    target_link = driver.find_element("xpath", "/html/body/div[1]/ul/form/li[4]/a")
    target_link.click()
    driver.implicitly_wait(10)

    view_link = driver.find_element("xpath", "/html/body/div[2]/form/label[3]/input")
    view_link.click()
    driver.implicitly_wait(10)

    view_link = driver.find_element("xpath", "/html/body/div[2]/form/input[1]")
    view_link.click()
    driver.implicitly_wait(10)

    div = driver.find_element("id", 'list')
    html = div.get_attribute('innerHTML')

    soup = BeautifulSoup(html, 'html.parser')
    li_tags = soup.find_all('li')

    res = []
    for li_tag in li_tags:
        li_parent = li_tag.parent
        par_parent = li_parent.parent
        title = par_parent.contents[0].text.strip()
        big_title = par_parent.parent.contents[1].text.strip()

        children = li_tag.contents
        id = children[0].text.strip()
        link = f"https://www.genome.jp{children[0]['href']}"
        text = children[1].text.strip()[:-1]
        state = children[3].text.strip()[1:]
        res.append((id, link, text, state, title, big_title))

    save_data(data=res, file_path=output_file)

    driver.quit()


if __name__ == "__main__":
    max_workers = 8
    driver_path = '/usr/local/bin/chromedriver'
    base_url = "https://www.genome.jp/kegg/mapper/reconstruct.html"
    input_file = "/Users/jessytsui/PycharmProjects/PKU_EMBL_tools/data/genelist.txt"

    input_file_list = get_txt_files("/Users/jessytsui/PycharmProjects/PKU_EMBL_tools/data")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(len(input_file_list)):
            out_file_name = os.path.basename(input_file_list[i]).split('.')[0]
            executor.submit(run_mapper, driver_path, base_url, input_file_list[i], f"./{out_file_name}_out.csv")
