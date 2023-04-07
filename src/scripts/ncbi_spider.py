import os
import subprocess
from typing import List, Tuple

import openpyxl
import requests
from bs4 import BeautifulSoup
from requests import Response
from retrying import retry


def read_excel(file_path: str) -> List[str]:
    """
    Read links from an Excel file.

    Args:
        file_path (str): Path of the Excel file.

    Returns:
        List[str]: A list of links extracted from the Excel file.
    """
    workbook = openpyxl.load_workbook(file_path)
    worksheet = workbook.active
    links = []
    for cell in worksheet['A']:
        hyperlink = cell.hyperlink
        if hyperlink is not None:
            link_display = hyperlink.display
            links.append(link_display)
    return links


@retry(stop_max_attempt_number=5, wait_fixed=1000)
def get_version_url(url: str) -> Tuple[Response, str]:
    """
    Get the URL of the latest assembly version.

    Args:
        url (str): The URL of the genome database.

    Returns:
        Tuple[Response, str]: A tuple containing the HTTP response of the latest assembly version URL and the URL itself.
    """
    response = requests.get(url)
    if 'latest_assembly_versions' in response.text:
        post_url = url + 'latest_assembly_versions/'
    else:
        post_url = url + "all_assembly_versions/"

    post_response = requests.get(post_url)
    return post_response, post_url


@retry(stop_max_attempt_number=5, wait_fixed=1000)
def get_extract_url(url: str) -> List[str]:
    """
    Get URLs of the files with genomic.fna.gz extensions.

    Args:
        url (str): The URL of the genome database.

    Returns:
        List[str]: A list of URLs of the files with genomic.fna.gz extensions.
    """
    post_response, post_url = get_version_url(url)
    soup = BeautifulSoup(post_response.text, 'html.parser')

    pre_tag = soup.find('pre')
    links = []
    res = []

    for i, a_tag in enumerate(pre_tag.find_all('a')):
        if i >= 1:
            href = a_tag.get('href')
            if href is not None:
                links.append(post_url + href)
    print("links:", links)

    for link in links:
        post_post_url = link
        post_post_response = requests.get(post_post_url)
        soup = BeautifulSoup(post_post_response.text, 'html.parser')
        import re
        pre_tag = soup.find('pre')
        pre_processed_url = []
        if pre_tag is not None:
            links = pre_tag.find_all('a')[1:]
            for link in links:
                href = link.get('href')
                if href and re.search('genomic\.fna\.gz$', href):
                    pre_processed_url.append(post_post_url + href)
        if pre_processed_url:
            target_url = min(pre_processed_url, key=lambda x: len(x))
            res.append(target_url)
    return res


@retry(stop_max_attempt_number=5, wait_fixed=1000)
def download_file(url: str, output_dir: str):
    """
    Download a file from a URL and save it to the specified directory.

    Args:
        url (str): The URL of the file to download.
        output_dir (str): The directory to save the downloaded file.
    """
    subprocess.run(['wget', '-P', output_dir, url])
    print("downloaded: ", url)

if __name__ == "__main__":
    file_path = '../../data/balabala.xlsx'
    output_dir = "../../data/output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pre_processed_links = read_excel(file_path)
    print(pre_processed_links)

    for url in pre_processed_links:
        try:
            res = get_extract_url(url)
            print("res:", res)
            for extract_url in res:
                download_file(extract_url, output_dir)
        except Exception as e:
            print(e)


