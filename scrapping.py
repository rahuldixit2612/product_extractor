import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re

def get_beautiful_soup_obj(url):
    """
    Get a BeautifulSoup object from a given URL.
    
    Parameters:
    - url (str): The URL to fetch and parse.
    
    Returns:
    - soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML content.
    """
    response = requests.get(url)
    soup = None
    if response.status_code == 200:
        response_data = response.content
        soup = BeautifulSoup(response_data, 'html.parser')
    return soup

def get_div_only_classes_with_count_range(soup, min_count, max_count):
    """
    Extract div elements with specific class count range and their associated data.
    
    Parameters:
    - soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML content.
    - min_count (int): Minimum count of occurrences for a class.
    - max_count (int): Maximum count of occurrences for a class.
    
    Returns:
    - div_only_classes_with_count_range (dict): A dictionary containing class names as keys,
      and their count and associated data as values.
    """
    class_count_dict = defaultdict(lambda: {'count': 0, 'data': []})
    div_elements_with_classes = soup.find_all('div', class_=True)

    for element in div_elements_with_classes:
        classes = element.get('class')
        text = element.get_text()
        for class_name in classes:
            class_info = class_count_dict[class_name]
            class_info['count'] += 1
            if class_info['count'] >= min_count and class_info['count'] <= max_count:
                class_info['data'].append(text)

    div_only_classes_with_count_range = {
        class_name: {
            'count': class_info['count'],
            'data': class_info['data']
        } for class_name, class_info in class_count_dict.items()
        if min_count <= class_info['count'] <= max_count
    }
    return div_only_classes_with_count_range

def is_valid_data(data):
    """
    Validate extracted data.
    
    Parameters:
    - data (str): The data to be validated.
    
    Returns:
    - valid (bool): True if the data is valid, False otherwise.
    """
    if len(data) < 20:
        return False

    # Check if data is vertical
    if all(line.strip() == "" for line in data.split('\n')):
        return False

    # Check if data contains only numbers and names
    data_words = re.findall(r'\b(?:\d+|[A-Za-z]+)\b', data)
    if len(data_words) == 0 or len(data_words) == len(data.split()):
        return False

    return True

def extract_data(url, min_count, max_count):
    """
    Extract and filter data from a given URL within a specific class count range.
    
    Parameters:
    - url (str): The URL to fetch and parse.
    - min_count (int): Minimum count of occurrences for a class.
    - max_count (int): Maximum count of occurrences for a class.
    
    Returns:
    - extracted_data (list): A list of extracted and filtered data.
    - title (str): The title of the web page.
    """
    soup = get_beautiful_soup_obj(url)
    title = soup.title.string.strip() if soup.title else "No Title Found"
    div_only_classes_with_count_range = get_div_only_classes_with_count_range(soup, min_count, max_count)

    extracted_data = []
    for class_name, class_info in div_only_classes_with_count_range.items():
        filtered_data_list = [data for data in class_info['data'] if is_valid_data(data)]
        filtered_count = len(filtered_data_list)
        if filtered_count > 1:
            for data in filtered_data_list:
                extracted_data.append(data)
    return extracted_data, title

def store_data(output_filename, url, min_count, max_count):
    """
    Extract and store data from a given URL within a specific class count range in a file.
    
    Parameters:
    - output_filename (str): The name of the output file to write data into.
    - url (str): The URL to fetch and parse.
    - min_count (int): Minimum count of occurrences for a class.
    - max_count (int): Maximum count of occurrences for a class.
    
    Returns:
    - success (bool): True if data was written successfully, False if an exception occurred.
    """
    extracted_data, title = extract_data(url, min_count, max_count)
    success = False
    try:
        with open(output_filename, "w", encoding="utf-8") as output_file:
            output_file.write("Title - " + title + "\n\n")
            output_file.write("-" * 100 + "\n") 
            for data in extracted_data:
                output_file.write("*  " + data + "\n")
                output_file.write("-" * 100 + "\n")
        success = True
        print("Data written successfully!")
    except Exception as e:
        print(f"Exception occurred: {e}")
    return success


            